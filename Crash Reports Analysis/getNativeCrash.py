import requests
import json



# get the number of issues with native crash from top-180 porjects on GitHub.

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

# repositories_Url = "https://api.github.com/search/repositories?q=android&sort=stars&order=desc&page=2"
repositories_Url = "https://api.github.com/search/repositories"
params = {'q': 'android', 'sort': 'stars', 'order': 'desc'}

for i in range(7,8):
    params["page"] = i

    response = requests.get(url=repositories_Url,params=params, headers=headers).text
    android_Repositories = json.loads(response)
    # print(type(android_Repositories))
    top_number = 1

    for repositories_Name in android_Repositories["items"]:
        repository_dict = {}
        issue_SIGSEGV_list = []
        issue_SIGILL_list = []
        issue_SIGABRT_list = []
        issue_SIGBUS_list = []
        issue_SIGFPE_list = []
        issue_SIGPIPE_list = []
        all_nativeCrash_Issues = []

        # print(repositories_Name["full_name"])
        per_repository_url = "https://api.github.com/repos/" +repositories_Name["full_name"]+"/issues?state=closed&per_page=100&page=0"

        response = requests.get(url=per_repository_url,headers=headers).text
        json_data = json.loads(response)
        page_number = 0

        while len(json_data) != 0:
            page_number += 1
            issue_page = "https://api.github.com/repos/" +repositories_Name["full_name"]+"/issues?state=closed&per_page=100&page="+str(page_number)
            response = requests.get(url=issue_page, headers=headers).text
            json_data = json.loads(response)

            # get the body of each report.
            for json_body in json_data:

                if "pull_request" not in json_body.keys() and json_body["body"]:
                    top_number += 1

                    if "SIGSEGV" in json_body["body"] and "ios" not in json_body["body"]:

                        # print(json_body["body"])

                        print("+++++++++++++++++++++")
                        print("Getting"+repositories_Name["full_name"]+"native crash......")

                        repository_dict["repository"] = repositories_Name["full_name"]
                        issue_SIGSEGV_list.append(json_body["number"])
                        repository_dict["SIGSEGV"] = issue_SIGSEGV_list

                    elif "SIGILL" in json_body["body"] and "ios" not in json_body["body"]:
                        print("/////////////////////////")
                        repository_dict["repository"] = repositories_Name["full_name"]
                        issue_SIGILL_list.append(json_body["number"])
                        repository_dict["SIGILL"] = issue_SIGILL_list
                    elif "SIGABRT" in json_body["body"] and "ios" not in json_body["body"]:
                        print("zzzzzzzzzzzzzzzzzzzzz")
                        repository_dict["repository"] = repositories_Name["full_name"]
                        issue_SIGABRT_list.append(json_body["number"])
                        repository_dict["SIGABRT"] = issue_SIGABRT_list
                    elif "SIGBUS" in json_body["body"] and "ios" not in json_body["body"]:
                        print(".....................")
                        repository_dict["repository"] = repositories_Name["full_name"]
                        issue_SIGBUS_list.append(json_body["number"])
                        repository_dict["SIGBUS"] = issue_SIGBUS_list
                    elif "SIGFPE " in json_body["body"] and "ios" not in json_body["body"]:
                        print("#######################")
                        repository_dict["repository"] = repositories_Name["full_name"]
                        issue_SIGFPE_list.append(json_body["number"])
                        repository_dict["SIGFPE"] = issue_SIGFPE_list
                    elif "SIGPIPE " in json_body["body"] and "ios" not in json_body["body"]:
                        print("$$$$$$$$$$$$$$$$$$$$$")
                        repository_dict["repository"] = repositories_Name["full_name"]
                        issue_SIGPIPE_list.append(json_body["number"])
                        repository_dict["SIGPIPE"] = issue_SIGPIPE_list

        print(repository_dict)
        if repository_dict:
            all_nativeCrash_Issues.append(repository_dict)

        if all_nativeCrash_Issues:
            with open("F:\\TombstonePaper\\Scripts\\top_180_crash\\" + repositories_Name["full_name"].split("/")[1] + ".json", "w",
                      encoding="utf-8") as file:
                file.write(json.dumps(all_nativeCrash_Issues, indent=4))

                print("######Got it######")



