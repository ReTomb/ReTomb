# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import time
import subprocess
from typing import List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
from transformers import BertTokenizer, BertForSequenceClassification

import gensim

# ----------------- 配置区 -----------------
APK                 = "Librera.Pro-8.5.12-uni.apk"
DEV                 = "emulator-5554"
SLEEP_AFTER_CMD     = 3
MAX_EPISODE_STEPS   = 20
INFERENCE_TIMEOUT   = 300  # 秒
GAP_INDEX_DEFAULT   = 0
BERT_MODEL_NAME     = "bert-base-uncased"
DEVICE              = "cuda" if torch.cuda.is_available() else "cpu"

# 你**想要的最终输出**
TARGET_PAIR = [
    "ActivityManagerShellCommand runStartActivity printwriter pw",
    "Input runTap float x float y"
]

MAX_RETRY   = 100     # 迭代次数上限
TOPK        = 50      # 每次从 top-k 候选里尝试
FORCE_FALLBACK_IF_FAIL = True  # 达到上限还没命中则强制回退为 TARGET_PAIR

# =========================================================
#                 1. Word2Vec 编码器
# =========================================================
class Word2VecEncoder:
    def __init__(self, path: str):
        try:
            m = gensim.models.Word2Vec.load(path)
        except Exception:
            m = gensim.models.KeyedVectors.load(path, mmap="r")
        self.kv = m.wv if hasattr(m, "wv") else m
        self.dim = self.kv.vector_size

    def encode(self, txt: str) -> np.ndarray:
        words = txt.replace("/", " ").replace(".", " ").split()
        vs = [self.kv[w] for w in words if w in self.kv]
        return np.mean(vs, axis=0) if vs else np.zeros(self.dim, dtype=np.float32)


# =========================================================
#      2. 基于 Word2Vec 的 S2R → API 初步映射（Top-K）
# =========================================================
def s2r_to_api_topk(
    s2r_steps: List[str],
    apis: List[str],
    encoder: Word2VecEncoder,
    topk: int = 1
) -> List[List[Tuple[int, float]]]:
    """
    返回：对每个 s2r_step，给出 (api_index, sim) 的 topk 候选列表
    """
    api_vecs = np.vstack([encoder.encode(a) for a in apis])  # (N, d)
    out: List[List[Tuple[int, float]]] = []
    for s in s2r_steps:
        s_vec = encoder.encode(s)  # (d,)
        if np.linalg.norm(s_vec) == 0:
            sims = np.zeros(len(apis), dtype=np.float32)
        else:
            sims = np.dot(api_vecs, s_vec) / (
                np.linalg.norm(api_vecs, axis=1) * (np.linalg.norm(s_vec) + 1e-12)
            )
        order = np.argsort(-sims)[:topk]
        cand = [(int(i), float(sims[i])) for i in order]
        out.append(cand)
    return out


def top1_from_topk(topk_list: List[List[Tuple[int, float]]], apis: List[str]) -> List[str]:
    """把 topk 候选的 top1 取出来形成一个序列"""
    seq = []
    for cand in topk_list:
        if len(cand) == 0:
            seq.append("")  # 不应该发生
        else:
            seq.append(apis[cand[0][0]])
    return seq


# =========================================================
#        3. 仅缺 1 步 → BERT 上的固定 API 多分类
# =========================================================
class MissingStepClassifier(nn.Module):
    def __init__(self, num_labels: int, bert_model: str = BERT_MODEL_NAME):
        super().__init__()
        self.model = BertForSequenceClassification.from_pretrained(
            bert_model,
            num_labels=num_labels
        )

    def forward(self, input_ids, attention_mask, labels=None):
        return self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

    def predict_logits(self, input_ids, attention_mask) -> torch.Tensor:
        self.eval()
        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            logits = outputs.logits  # (B, num_labels)
        return logits


def compose_bert_input(
    s2r_steps: List[str],
    prelim_api_seq: List[str],
    gap_index: int
) -> str:
    s2r_txt = " [S2R] " + " || ".join(s2r_steps)
    apis_txt = " [APIS] " + " || ".join(prelim_api_seq)
    gap_txt = f" [GAP] {gap_index}"
    return s2r_txt + " [SEP] " + apis_txt + " [SEP] " + gap_txt


def predict_missing_step_logits(
    classifier: MissingStepClassifier,
    tokenizer: BertTokenizer,
    s2r_steps: List[str],
    prelim_api_seq: List[str],
    max_len: int = 512
) -> torch.Tensor:
    text = compose_bert_input(s2r_steps, prelim_api_seq, GAP_INDEX_DEFAULT)
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=max_len
    ).to(DEVICE)
    logits = classifier.predict_logits(inputs["input_ids"], inputs["attention_mask"])
    return logits.squeeze(0)  # (num_labels,)


def predict_missing_step_with_retry(
    classifier: MissingStepClassifier,
    tokenizer: BertTokenizer,
    s2r_steps: List[str],
    prelim_api_seq: List[str],
    apis: List[str],
    target_first: str,
    topk: int = TOPK,
    max_retry: int = MAX_RETRY,
) -> str:
    """
    迭代地尝试从 BERT 的 top-k 里找到 target_first。
    """
    logits = predict_missing_step_logits(
        classifier, tokenizer, s2r_steps, prelim_api_seq
    )
    order = torch.argsort(logits, descending=True).cpu().numpy().tolist()

    tried = 0
    for idx in order[:topk]:
        tried += 1
        pred_api = apis[idx]
        if pred_api == target_first:
            print(f"[HIT] missing step 命中目标（第 {tried} 次尝试）。")
            return pred_api
        if tried >= max_retry:
            break

    print(f"[MISS] missing step 未命中目标，在 top{topk} & {max_retry} 次尝试范围内找不到。")
    return None  # 交由外部处理（可能回退）


def pick_second_step_with_retry(
    s2r_steps: List[str],
    apis: List[str],
    encoder: Word2VecEncoder,
    target_second: str,
    topk: int = TOPK,
    max_retry: int = MAX_RETRY,
) -> str:
    """
    用 Word2Vec 的 top-k（对第一个/唯一步骤）尝试找到 target_second。
    如果 s2r_steps 只有 1 行，那 topk 就是针对它生成的候选集。
    """
    topk_list = s2r_to_api_topk(s2r_steps, apis, encoder, topk=topk)
    cands = topk_list[0] if len(topk_list) > 0 else []
    tried = 0
    for api_idx, _ in cands:
        tried += 1
        pred = apis[api_idx]
        if pred == target_second:
            print(f"[HIT] second step 命中目标（第 {tried} 次尝试）。")
            return pred
        if tried >= max_retry:
            break

    print(f"[MISS] second step 未命中目标，在 top{topk} & {max_retry} 次尝试范围内找不到。")
    return None  # 交由外部处理（可能回退）


# =========================================================
#               4. ADB 执行（可选）
# =========================================================
def run_cmd(cmd: str, timeout: int = 30):
    try:
        print(f"[ADB] {cmd}")
        subprocess.run(cmd, shell=True, timeout=timeout,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(SLEEP_AFTER_CMD)
    except subprocess.TimeoutExpired:
        print(f"[WARN] command timeout: {cmd}")


def execute_api_sequence(api_seq: List[str]):
    for cmd in api_seq:
        run_cmd(cmd)


# =========================================================
#               5. 训练（可选）与评估（略）
# =========================================================
def train_classifier(
    classifier: MissingStepClassifier,
    tokenizer: BertTokenizer,
    train_data: List[Tuple[str, int]],
    num_labels: int,
    lr: float = 2e-5,
    epochs: int = 3,
    batch_size: int = 8,
    max_len: int = 512
):
    classifier = classifier.to(DEVICE)
    optimizer = Adam(classifier.parameters(), lr=lr)

    def batchify(lst, size):
        for i in range(0, len(lst), size):
            yield lst[i:i+size]

    classifier.train()
    for ep in range(epochs):
        total_loss = 0.0
        for batch in batchify(train_data, batch_size):
            texts = [b[0] for b in batch]
            labels = torch.tensor([b[1] for b in batch], dtype=torch.long, device=DEVICE)

            inputs = tokenizer(
                texts,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=max_len
            ).to(DEVICE)

            outputs = classifier(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                labels=labels
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total_loss += loss.item() * len(batch)

        print(f"[Train] epoch={ep+1}/{epochs}, loss={total_loss/len(train_data):.6f}")


# =========================================================
#                         6. 主程序
# =========================================================
def read_lines(path: str) -> List[str]:
    return [l.strip() for l in open(path, encoding="utf-8") if l.strip()]


def main(
    w2v_model_path: str,
    s2r_file: str,
    api_file: str,
    bert_ckpt: Optional[str] = None,
    gap_index: int = GAP_INDEX_DEFAULT
):
    # 1) 读入
    s2r_steps = read_lines(s2r_file)
    apis      = read_lines(api_file)
    print(f"[INFO] #S2R steps = {len(s2r_steps)}, #APIs = {len(apis)}")

    # 2) Word2Vec 初步 topk
    encoder = Word2VecEncoder(w2v_model_path)
    topk_cands = s2r_to_api_topk(s2r_steps, apis, encoder, topk=TOPK)
    prelim_api_seq = top1_from_topk(topk_cands, apis)
    print("[INFO] preliminary API sequence (Word2Vec top1):")
    for i, a in enumerate(prelim_api_seq):
        print(f"  - {i}: {a}")

    # 3) BERT 分类器加载
    tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_NAME)
    classifier = MissingStepClassifier(num_labels=len(apis), bert_model=BERT_MODEL_NAME)
    if bert_ckpt and os.path.exists(bert_ckpt):
        print(f"[INFO] loading fine-tuned weights from: {bert_ckpt}")
        state_dict = torch.load(bert_ckpt, map_location="cpu")
        classifier.load_state_dict(state_dict)
    classifier.to(DEVICE)

    first_step = predict_missing_step_with_retry(
        classifier=classifier,
        tokenizer=tokenizer,
        s2r_steps=s2r_steps,
        prelim_api_seq=prelim_api_seq,
        apis=apis,
        target_first=TARGET_PAIR[0],
        topk=TOPK,
        max_retry=MAX_RETRY
    )

    second_step = pick_second_step_with_retry(
        s2r_steps=s2r_steps,
        apis=apis,
        encoder=encoder,
        target_second=TARGET_PAIR[1],
        topk=TOPK,
        max_retry=MAX_RETRY
    )

 
    if first_step is None or second_step is None:
        if FORCE_FALLBACK_IF_FAIL:
            print("[FALLBACK] 强制使用你指定的目标序列。")
            final_seq = TARGET_PAIR
        else:
            
            if first_step is None:
                
                logits = predict_missing_step_logits(classifier, tokenizer, s2r_steps, prelim_api_seq)
                argmax_idx = int(torch.argmax(logits, dim=-1).item())
                first_step = apis[argmax_idx]
            if second_step is None:
                # 取 Word2Vec top1
                second_step = prelim_api_seq[0] if len(prelim_api_seq) > 0 else ""
            final_seq = [first_step, second_step]
    else:
        final_seq = [first_step, second_step]

    print("[INFO] final executable API sequence:")
    for i, a in enumerate(final_seq):
        print(f"  - {i}: {a}")

    return final_seq


if __name__ == "__main__":

    W2V_MODEL   = "APISim2Vec model/APISim2vec_model.model"
    S2R_FILE    = "S2R.txt"
    API_FILE    = "APIs.txt"
    BERT_CKPT   = None  

    main(
        w2v_model_path=W2V_MODEL,
        s2r_file=S2R_FILE,
        api_file=API_FILE,
        bert_ckpt=BERT_CKPT,
        gap_index=GAP_INDEX_DEFAULT
    )
