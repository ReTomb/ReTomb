import os
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#get given tombstone file
signal_list = ["SIGABRT","SIGBUS","SIGFPE","SIGILL","SIGSEGV","SIGSTKFLT","SIGSYS","SIGTRAP"]
code_list = ["SI_USER","SI_KERNEL","SI_QUEUE","SI_TIMER","SI_MESGQ","SI_ASYNCIO","SI_SIGIO","SI_TKILL","SI_DETHREAD","SI_ASYNCNL","SI_LWP","SI_MPLAB","SI_CLOCK","SI_MINCORE","SI_SYSCALL","SI_ARCH","SI_RDTSC","SI_LLVM"]

def get_given_tombstone_metrics(issue_name):
    given_tombstone_metric_dict = {}
    frame_list = []
    backtrace_patten = r'#\d+\s+pc\s+[a-f\d]+\s+[^\s]+\s+\([^+]+\+\d+\)'
    with open("../DataSet/34_Native_Crash_Reports/%s/tombstone.txt"%issue_name, "r", encoding="utf-8") as given_tombstone_file:
        lines = given_tombstone_file.readlines()
        # print(lines)
        for line in lines:
            # print(line.strip())
            for signal in signal_list:
                for code in code_list:
                    if signal in line.strip() and code in line.strip():
                        given_tombstone_metric_dict["error_signal"] = signal
                        given_tombstone_metric_dict["error_code"] = code
            if "Abort message" in line.strip():
                abort_content = line.strip().split("Abort message:")[1]
                # print(abort_content)
                given_tombstone_metric_dict["abort_content"] = abort_content
                # print(given_tombstone_metric_dict)
            if "#" in line.strip():
                backtrace_frames = re.findall(backtrace_patten,line.strip())
                for backtrace_frame in backtrace_frames:
                    if backtrace_frame:

                        frame_list.append(backtrace_frame)
                        given_tombstone_metric_dict["backtrace_frame"] = frame_list

    return given_tombstone_metric_dict
    # print(given_tombstone_metric_dict)


def get_generated_tombstone_metrics(issue_name):
    given_tombstone_metric_dict = {}
    frame_list = []
    backtrace_patten = r'#\d+\s+pc\s+[a-f\d]+\s+[^\s]+\s+\([^+]+\+\d+\)'
    with open("./Artifact-Evaluation/%s/tombstone_00"%issue_name, "r", encoding="utf-8") as given_tombstone_file:
        lines = given_tombstone_file.readlines()
        # print(lines)
        for line in lines:
            # print(line.strip())
            for signal in signal_list:
                for code in code_list:
                    if signal in line.strip() and code in line.strip():
                        given_tombstone_metric_dict["error_signal"] = signal
                        given_tombstone_metric_dict["error_code"] = code
            if "Abort message" in line.strip():
                abort_content = line.strip().split("Abort message:")[1]
                # print(abort_content)
                given_tombstone_metric_dict["abort_content"] = abort_content
                # print(given_tombstone_metric_dict)
            if "#" in line.strip():
                backtrace_frames = re.findall(backtrace_patten,line.strip())
                for backtrace_frame in backtrace_frames:
                    if backtrace_frame:

                        frame_list.append(backtrace_frame)
                        given_tombstone_metric_dict["backtrace_frame"] = frame_list

    return given_tombstone_metric_dict
    # print(given_tombstone_metric_dict)

def calculate_cos_similarity(sentence_1, sentence_2):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([sentence_1, sentence_2])

    vector1 = X.toarray()[0]
    vector2 = X.toarray()[1]
    similarity = cosine_similarity([vector1], [vector2])[0, 0]
    return similarity

if __name__ == '__main__':

    error_signal = 1
    error_code = 1

    given_tombstone = get_given_tombstone_metrics("Brave_Issue#20628")
    generated_tombstone = get_generated_tombstone_metrics("Brave_Issue#20628")
    # print(given_tombstone)
    # print(generated_tombstone)
    if given_tombstone["error_signal"] == generated_tombstone["error_signal"] and given_tombstone["error_code"] == generated_tombstone["error_code"]:
        error_signal = 0
        error_code = 0
        abort_message_cos_value = calculate_cos_similarity(given_tombstone["abort_content"],generated_tombstone["abort_content"])
        # print(given_tombstone["abort_content"],"---------------------")
        # print(generated_tombstone["abort_content"],"---------------------")
        if abort_message_cos_value >= 0.6:
            for given_backtrace in given_tombstone["backtrace_frame"]:
                for generated_backtrace in generated_tombstone["backtrace_frame"]:
                    if given_backtrace and generated_backtrace:
                        cos_backtraces = calculate_cos_similarity(given_backtrace,generated_backtrace)
                        if cos_backtraces >= 0.9:
                            print("The given tombstone is reproduced.")
                        else:
                            print("The given tombstone is not reproduced.")

        else:
            print("The given tombstone is not reproduced.")
