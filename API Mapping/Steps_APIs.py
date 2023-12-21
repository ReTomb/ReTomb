from gensim.models import Word2Vec
from itertools import product
import jieba
import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Steps_APIs():

    model = Word2Vec.load("APISim2vec_model.model")
    api_squence_dict = {}

    def read_text_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.readlines()
        return text

    def calculate_similarity(self, vec1, vec2):
        if vec1 is not None and vec2 is not None:
            return cosine_similarity([vec1], [vec2])[0][0]
        return None

    def get_sentence_vector(self,text):
        tokens = jieba.lcut(text)
        vectors = []
        for token in tokens:
            if token in self.model.wv:
                vectors.append(self.model.wv[token])
        if vectors:
            return np.mean(vectors, axis=0)
        return None
    #get n-step API squence and write into json file
    def similarity_between_steps(self, steps_path, apis_list):
        # print(apis_list)
        top_1_apis = []
        top_3_apis = []
        top_5_apis = []
        top_10_apis = []
        issue_name = steps_path.split("/")[2].split(".")[0]
        if not os.path.exists("./midResults/%s/" % (issue_name)):
            os.makedirs("./midResults/%s/" % (issue_name))
        for step in self.read_text_from_file(steps_path):
            apis_squences = {}
            for api in apis_list:
                print(step,"#########################")
                print(api,"----------------------------")
                steps_vector = self.get_sentence_vector(step)
                apis_vector = self.get_sentence_vector(api)
                similarity = self.calculate_similarity(steps_vector, apis_vector)
                print(step,api,similarity)

                if similarity is not None:
                    # print("The similarity between" + step + "and" + api.strip() + "is", similarity)
                    apis_squences[api.strip()] = similarity
                    sorted_apis_squences = dict(sorted(apis_squences.items(), key=lambda x: x[1], reverse=True))
            # print(sorted_apis_squences) top n
                    top_1_apis = list(sorted_apis_squences.items())[0:1]
                    top_3_apis = list(sorted_apis_squences.items())[0:3]
                    top_5_apis = list(sorted_apis_squences.items())[0:5]
                    top_10_apis = list(sorted_apis_squences.items())[0:10]

                    # print(top_10_apis)
                    # steps_api_dict[step.strip()] = top_10_apis
            #  write into top-n txt file
            #get top 1
            if not os.path.exists("./midResults/%s/top_1/" % (issue_name)):
                os.makedirs("./midResults/%s/top_1/" % (issue_name))
            json_path = "%s.json" % step.strip()
            with open(os.path.join("./midResults/%s/top_1/" % issue_name, json_path), 'w', encoding='utf-8') as file:
                top_1_step_api = {}
                for items in top_1_apis:
                    top_1_step_api[items[0]] = str(items[1])
                file.write(json.dumps(top_1_step_api, indent=2))
            #get top 3
            if not os.path.exists("./midResults/%s/top_3/" % (issue_name)):
                os.makedirs("./midResults/%s/top_3/" % (issue_name))
            with open("./midResults/%s/top_3/%s.json" % (issue_name, step.strip()), 'w', encoding='utf-8') as file:
                top_3_step_api = {}
                for items in top_3_apis:
                    top_3_step_api[items[0]] = str(items[1])
                file.write(json.dumps(top_3_step_api, indent=2))
            #get  top 5
            if not os.path.exists("./midResults/%s/top_5/" % (issue_name)):
                os.makedirs("./midResults/%s/top_5/" % (issue_name))
            with open("./midResults/%s/top_5/%s.json" % (issue_name, step.strip()), 'w', encoding='utf-8') as file:
                top_5_step_api = {}
                for items in top_5_apis:
                    top_5_step_api[items[0]] = str(items[1])
                file.write(json.dumps(top_5_step_api, indent=2))
             #get top 10
            if not os.path.exists("./midResults/%s/top_10/" % (issue_name)):
                os.makedirs("./midResults/%s/top_10/" % (issue_name))
            with open("./midResults/%s/top_10/%s.json" % (issue_name, step.strip()), 'w', encoding='utf-8') as file:
                top_10_step_api = {}
                for items in top_10_apis:
                    top_10_step_api[items[0]] = str(items[1])
                file.write(json.dumps(top_10_step_api, indent=2))
        print("The top-n APIs have been generated!")

    #Read the top-n API files corresponding to each step and then arrange and combine these items to get all API combinations for all steps.
    def combine_top_n_apis(self, file_name, n):
        top_n_apis = []
        issue_name = file_name.split(".")[0]
        steps_path = "../Preprocessed S2Rs/%s" % (file_name)
        for step in self.read_text_from_file(steps_path):
            with open("./midResults/%s/top_%s/%s.json" % (issue_name, n, step.strip()), 'r', encoding='utf-8') as file:
                top_n_apis.append(json.load(file))
        generate_api_combination = []
        for step_json_file in os.listdir("./midResults/%s/top_%s/" % (issue_name,n)):
            json_path = "./midResults/%s/top_%s/%s" % (issue_name, n, step_json_file)
            # print(json_path)
            with open(json_path, 'r') as file:
                top_10_api_json = json.load(file)
                generate_api_combination.append(top_10_api_json)
        # get all combinations of dictionary items
        all_combinations = list(product(*[d.keys() for d in generate_api_combination]))
        # print(len(all_combinations))
        # The output is a list of tuples, where each tuple contains one possible combination of dictionary items
        for idx, combination in enumerate(all_combinations):
            if not os.path.exists("./results/%s/top_%s/" % (issue_name, n)):
                os.makedirs("./results/%s/top_%s/" % (issue_name, n))
            with open("./results/%s/top_%s/%s.txt" % (issue_name, n, idx + 1), 'w', encoding='utf-8') as write_file:
                for item in combination:
                    with open("../dataset/mapping.json", 'r', encoding='utf-8') as read_file:
                        result = json.load(read_file)
                        for api in result.keys():
                            if api == item:
                                item_value = result[api]
                                # print(item_value, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                                write_file.write(item_value + "\n")
            print("The %s-th combination has been generated!" % (idx + 1))

    def get_apis(self):
        apis_list = []
        with open("../dataset/mapping.json", 'r', encoding='utf-8') as file:
            result = json.load(file)
            for api in result.keys():
                apis_list.append(api)
        return apis_list

    def categorize_manager(self,s2r):
        pm_list = ["install", "create"]
        am_list = ["open", "start", "launch", "switch", "run", "reopen", "enter", "move", "go", "navigate", "back",
                   "execute", "use", "put", "load"]
        widget_list = ["input", "tap", "click", "scroll", "swipe", "search", "press", "change", "read", "pull up", "play","scoll"]
        shell_managers_list = []

        for pm_item in pm_list:
            if pm_item in s2r:
                for pm_shell in self.get_apis():
                    if "PackageManagerShellCommand" in pm_shell:
                        shell_managers_list.append(pm_shell)
        for am_item in am_list:
            if am_item in s2r:
                for am_shell in self.get_apis():
                    if "ActivityManagerShellCommand" in am_shell:
                        shell_managers_list.append(am_shell)
        for widget_item in widget_list:
            if widget_item in s2r:
                for widget_shell in self.get_apis():
                    if "Input" in widget_shell:
                        shell_managers_list.append(widget_shell)

        return shell_managers_list

# similarity_between_steps(steps_path, APIs_path)
if __name__ == '__main__':

    for file_name in os.listdir("../Preprocessed S2Rs/"):

        steps_path = "../Preprocessed S2Rs/%s" % (file_name)
        with open(steps_path, 'r', encoding='utf-8') as file:
            steps = file.readlines()
            for step in steps:
                # print(step)
                # print(Steps_APIs().categorize_manager(step))
                setps_category_result = Steps_APIs().categorize_manager(step)
                # print(setps_category_result)
                if setps_category_result:
                    #compute similarity
                    Steps_APIs().similarity_between_steps(steps_path, setps_category_result)
                    print("The top-n APIs have been generated for %s!!!" % (file_name.split(".")[0]))
                else:
                    Steps_APIs().similarity_between_steps(steps_path, Steps_APIs().get_apis())
                    print("The top-n APIs have been generated for %s!!!" % (file_name.split(".")[0]))
                for n in [1,3,5,10]:
                    print(n)
                    Steps_APIs().combine_top_n_apis(file_name, n)
                    print("The top-%s APIs combination has been generated for %s!!!" % (n,file_name.split(".")[0]))
    # steps_path = "../Preprocessed S2R/Brave#20628.txt"
    # with open("../Preprocessed S2R/Brave#20628.txt", 'r', encoding='utf-8') as file:
    #     steps = file.readlines()
    #     for step in steps:
    #         for api in Steps_APIs().get_apis():
    #             setps_category_result = Steps_APIs().categorize_manager(step)
    #             if setps_category_result:
    #                 Steps_APIs().similarity_between_steps(steps_path, setps_category_result)
    #                 steps_vector = Steps_APIs().get_sentence_vector(step)
    #                 apis_vector = Steps_APIs().get_sentence_vector(api)
    #                 print(apis_vector)
    #                 print(steps_vector)
    #                 similarity = Steps_APIs().calculate_similarity(steps_vector, apis_vector)
    #                 print(similarity)
                    # print(Steps_APIs().get_apis())


