from gensim.models import Word2Vec

corpus_path = 'F:\\RetombDroid\\dataset\\train_dataset_4.txt'

with open(corpus_path,"r",encoding="utf-8") as file:
    lines = file.readlines()
sentences = [line.strip().split() for line in lines if line.strip()]

model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)

model.save("APISim2vec_model.model")


