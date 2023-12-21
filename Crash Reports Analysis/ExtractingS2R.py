import requests
import json
import base64
import re

class ExtractingS2R:

    headers = {
        "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "referer": "https://github.com/search?o=desc&q=java&s=stars&type=Repositories",
        "cookie": "_octo=GH1.1.1646576303.1626246767; _device_id=6492f38a7668d1613515bf5c0217cefb; user_session=uwQ5wAbT1akawkOuC9VyLQWwl1d1UBM6PHphNrGz1QsHidRL; __Host-user_session_same_site=uwQ5wAbT1akawkOuC9VyLQWwl1d1UBM6PHphNrGz1QsHidRL; logged_in=yes; dotcom_user=lusaty; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; tz=Asia%2FShanghai; has_recent_activity=1; _gh_sess=Gw1j4QPKnKoLxltElkBUxR%2Fp3nAo9l4AG%2FgdTDj%2FqDJ5HArQAhGyjLZmdBg%2F89EvHRZAkR8h%2FzAW7tMaLTGwlMy5us2NZ2hMHLNkiwND9GtipNhotA9wPhK7ltjyG1K0VJOmRMQHw9tkgVLmLyeMdechczPKiqRr9TLUnQvwrE7TdLB6tqI%2BfxgSXYAhm1V68kUoFjFseNNoOukftmsN25U6f4s9XlgtTx1Vv%2B%2F%2BxUmIQUpvDVJeDjXiIB9V%2FEmy8vQ%2B3D1GfRmJWLQITOZpteFqcacOVo0%2BxA6sP411ieVKcD9wI3AK2bzPNV8ZtZXMFBjCGe%2BEJ%2BGnXzEV4QZvb1PZWV7uv2cal0cZELav6J79UgmJY7JUSAsq80b9jvRyNegvoUbW6iBq65wvM8QcBAn2idslP4hEzNf2pbq960nxPqr6rZf5Xxozi4OOZEewx8NF1LvVpHHjUXV4CrOH6GKminH5Pq%2FfPGZRb3qlY8pQAd1tRJd0tg2YoP3Kubj9%2FEyhbZKLOwU7efQNweXnXcKTE061CK%2F623n2QA%3D%3D--eY9ow0LPX4yAAR9S--5b2BZcT1o9WzuHZNdgHKvg%3D%3D",
        "authority": "token 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",
        "path": "/search?l=Java&o=desc&q=java&s=stars&type=Repositories",
        "scheme": "https",
        "method": "GET",
        'Authorization': 'token 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',
        "Accept": "application/vnd.github.v3+json"

    }

    #get an the body of issue.
    def extractRawS2R(self,repositories,issue_number):
        raw_S2R = ""
        preproceedS2R = ""
        if repositories == "Flutter":
            repositories_Url = "https://api.github.com/repos/flutter/flutter/issues/%s"%issue_number
            response = requests.get(url=repositories_Url, headers=self.headers).text
            crash_report = json.loads(response)
            crash_body = crash_report["body"]
            if str(issue_number) == "97904" :
                raw_S2R = crash_body.split("\r\n\r\n")[3]

                preproceedS2R = raw_S2R.replace(")","")[:-27]
            elif str(issue_number) == "97267":
                repositories_Url = "https://api.github.com/repos/flutter/flutter/issues/97267/comments"
                response = requests.get(url=repositories_Url, headers=self.headers).text
                crash_report = json.loads(response)
                crash_body = crash_report[7]["body"]
                raw_S2R = crash_body.split("\r\n")[2]

                preproceedS2R = "1." + raw_S2R.split("-")[2] + "\n" + \
                                "2." + raw_S2R.split("-")[3] + "\n" + \
                                "3." + raw_S2R.split("-")[4]
            elif str(issue_number) == "97732" :
                raw_S2R = crash_body.split("\r\n\r\n")[5]

                preproceedS2R = raw_S2R.split("flutter pub get")[1]\
                    .replace("6","1").replace("7","2").replace("8","3")[:-19]

            elif str(issue_number) == "98155":
                raw_S2R = crash_body.split("\r\n\r\n")[2]

                preproceedS2R = raw_S2R.replace("Add into list `webview` and `videoplayer` widget",
                                                "start application flutter_issue_98155")[:-18]
            elif str(issue_number) == "100441":
                raw_S2R =crash_body.split("\r\n\r\n")[7] \
                         +crash_body.split("\r\n\r\n")[8]

                preproceedS2R = re.sub(r"<[^>]+>","",crash_body.split("\r\n\r\n")[8]
                                       .split("```")[2]).replace("4","1").replace("5","2")

            elif str(issue_number) == "99533":
                raw_S2R = crash_body.split("\r\n\r\n")[4]

                preproceedS2R = raw_S2R[:-25]
            elif str(issue_number) == "87635":
                repositories_Url = "https://api.github.com/repos/ColdPaleLight/flutter_example_87635/readme"
                response = requests.get(url=repositories_Url, headers=self.headers).text
                crash_report = json.loads(response)
                content = crash_report["content"]
                raw_S2R = base64.b64decode(content).decode('utf-8').split("\n")[0]

                preproceedS2R = raw_S2R

            elif str(issue_number) == "122882":
                raw_S2R = crash_body.split("\r\n\r\n")[2].split(".")[1]

                preproceedS2R = raw_S2R
            elif str(issue_number) == "56584":
                # raw_S2R = crash_body.split("\r\n\r\n")[1].split("\r\n")[1]
                raw_S2R = crash_body.split("\r\n\r\n")[1]

                preproceedS2R = crash_body.split("\r\n\r\n")[1].split("\r\n")[1]

            elif str(issue_number) == "54587":
                raw_S2R = crash_body.split("\r\n\r\n")[0].split(":")[0]

                preproceedS2R = raw_S2R

            elif str(issue_number) == "90165":
                raw_S2R = crash_body.split("\r\n\r\n")[6] +\
                          crash_body.split("\r\n\r\n")[7]

                preproceedS2R = "1."+crash_body.split("\r\n\r\n")[6].split("\r\n")[6].strip()+\
                                "\n" + crash_body.split("\r\n\r\n")[7][:-34]

            elif str(issue_number) == "73767":
                raw_S2R = crash_body.split("\r\n\r\n")[2] + \
                          crash_body.split("\r\n\r\n")[3] + \
                          crash_body.split("\r\n\r\n")[4] + \
                          crash_body.split("\r\n\r\n")[5] + \
                          crash_body.split("\r\n\r\n")[6]

                preproceedS2R = crash_body.split("\r\n\r\n")[6].replace("5","1")
            elif str(issue_number) == "115143" :
                raw_S2R = crash_body.split("\r\n\r\n")[1]

                preproceedS2R = raw_S2R.split(".")[0]

            elif str(issue_number) == "108678" :
                raw_S2R = crash_body.split("\r\n\r\n")[1]

                #preprocecssing S2R
                preproceedS2R = raw_S2R.split(".")[1]

            elif str(issue_number) == "87858":
                raw_S2R = crash_body.split("\r\n\r\n")[1]

                preproceedS2R = "1." + raw_S2R.split(".")[0].replace("Use this demo","start application com.example.unable_to_merge_raster_demo").split("and")[0] +"\n" +\
                                "2." + raw_S2R.split(".")[0].split("and")[1]
            elif str(issue_number) == "99352":
                raw_S2R = crash_body.split("\r\n\r\n")[1]
                preproceedS2R = raw_S2R.split("Have a ListView on the second tab")[1]\
                    .replace("4","1").replace("5","2").replace("6","3")

                                # + raw_S2R.split("\r\n")[4].replace("5","2") + \
                                # raw_S2R.split("\r\n")[5].replace("6","3")

            elif str(issue_number) == "125197":
                raw_S2R = crash_body.split("\r\n\r\n")[3]
            elif str(issue_number) == "120853":
                raw_S2R = crash_body.split("\r\n\r\n")[5]

                preproceedS2R = re.sub(r"\([^)]*\)","",raw_S2R.strip())[:-24]
            elif str(issue_number) == "90602":
                raw_S2R = crash_body.split("\r\n\r\n")[2].split(":")[1][:-16]

                preproceedS2R = "1." + raw_S2R.split(",")[0].strip() + "\n" +\
                                "2." + raw_S2R.split(",")[1].split("and")[0].strip() + "\n" +\
                                "3." + raw_S2R.split(",")[1].split("and")[1].strip() + "\n" +\
                                "4." + raw_S2R.split(",")[2][9:].strip()

        elif repositories == "Tachiyomi":
            repositories_Url = "https://api.github.com/repos/tachiyomiorg/tachiyomi/issues/%s" % issue_number
            response = requests.get(url=repositories_Url, headers=self.headers).text
            crash_report = json.loads(response)
            crash_body = crash_report["body"]
            raw_S2R = crash_body.split("\r\n\r\n")[1]

            preproceedS2R = raw_S2R.split("\r\n")[0] + "\n" +raw_S2R.split("\r\n")[1]

        elif repositories == "Koreader":
            repositories_Url = "https://api.github.com/repos/koreader/koreader/issues/%s" % issue_number
            response = requests.get(url=repositories_Url, headers=self.headers).text
            crash_report = json.loads(response)
            crash_body = crash_report["body"]
            if str(issue_number) == "9297":
                raw_S2R = crash_body.split("\r\n\r\n")[1].split("\r\n")[1]

                preproceedS2R = raw_S2R
            else:
                raw_S2R = crash_body.split("\r\n\r\n")[2][23:].strip()

                preproceedS2R =raw_S2R

        elif repositories == "Brave":
            repositories_Url = "https://api.github.com/repos/brave/brave-browser/issues/%s" % issue_number
            response = requests.get(url=repositories_Url, headers=self.headers).text
            crash_report = json.loads(response)
            crash_body = crash_report["body"]

            if str(issue_number) == "20628":
                raw_S2R = crash_body.split("\r\n\r\n")[5]

                preproceedS2R = raw_S2R[20:].replace("2","1").replace("3","2")\
                    .replace("4","3").replace("5","4").replace("6","5")

            else:
                raw_S2R = crash_body.split("\r\n\r\n")[6]

                preproceedS2R = raw_S2R

        elif repositories == "Status":
            repositories_Url = "https://api.github.com/repos/status-im/status-mobile/issues/%s" % issue_number
            response = requests.get(url=repositories_Url, headers=self.headers).text
            crash_report = json.loads(response)
            crash_body = crash_report["body"]
            if str(issue_number) == "13811":
                raw_S2R = crash_body.split("\r\n\r\n")[8]

                preproceedS2R = raw_S2R.replace("4.a. The network logo remains grey -> no problem, app does not crash","").replace("4.b. the network logo disappears -> app crashes","")
            else:
                raw_S2R = crash_body.split("###")[3].split("\n\n")[2]
                preproceedS2R = raw_S2R

        elif repositories == "LibreraReader":
            repositories_Url = "https://api.github.com/repos/foobnix/LibreraReader/issues/%s" % issue_number
            response = requests.get(url=repositories_Url, headers=self.headers).text
            crash_report = json.loads(response)
            raw_S2R = crash_report["title"]

            preproceedS2R = raw_S2R

        return repositories,issue_number,raw_S2R,preproceedS2R



    def preprocessS2R(self,raw_S2R_info):
        print(raw_S2R_info[2])

        pass
    def writeRawReport(self,raw_S2R_info):

        with open("Raw reports/%s","w" ,encoding="utf-8") as file:
            file.write(raw_S2R_info)
        pass

if __name__ == '__main__':

    project = {"Flutter" : ["108678","120853","90602","115143","100441","73767","90165",
                           "54587","56584","122882","87635","99533","98155","99352",
                           "97732","97267","97904","87858"],
               "Tachiyomi" : ["8599"],
               "Koreader" : ["9297","10100"],
               "Brave" : ["27572","20628"],
               "Status" : ["13811","11441"],
               "LibreraReader" : ["803"]}
    result = ExtractingS2R()

    for projectName, issues in project.items():
        for issue in issues:
            # print(projectName,issue)
            raw_S2R_info = result.extractRawS2R(projectName, issue)
            print(raw_S2R_info[0],raw_S2R_info[1],raw_S2R_info[2],raw_S2R_info[3])
            # result.preprocessS2R(raw_S2R_info)
            # print(raw_S2R_info)
            with open("../Raw reports/%s_%s.txt"%(raw_S2R_info[0],raw_S2R_info[1]), "w", encoding="utf-8") as file:
                file.write(raw_S2R_info[2])

            with open("../Preprocessed S2R/%s#%s.txt" % (raw_S2R_info[0], raw_S2R_info[1]), "w", encoding="utf-8") as file:
                file.write(raw_S2R_info[3])
