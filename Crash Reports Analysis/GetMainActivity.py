from appium import webdriver
import time
from androguard.core.bytecodes.apk import APK
import uiautomator2 as u2
import os

pm_list = ["install", "create"]
am_list = ["open", "start", "launch", "switch", "run", "reopen", "enter", "move", "go", "navigate", "back",
           "execute", "use", "put", "load"]
widget_list = ["input", "tap", "click", "scroll", "swipe", "search", "press", "change", "read", "pull up", "play",
               "scoll"]


def get_main_activity(apk_path):

    apks_mainActivity = {}
    try:
        for filename in os.listdir(apk_path):
            # print(filename)
            if filename.endswith(".apk"):
                apk_info = os.path.join(apk_path, filename)
                print(apk_info)
                apk = APK(apk_info)
                # print(apk.get_package())
                activity = apk.get_activities()
                for mainactivity in activity:
                    if "MainActivity" in mainactivity or "MainTabs2" in mainactivity or "org.chromium.chrome.browser.ChromeTabbedActivity" == mainactivity:
                        print(apk_path.split("/")[2])
                        apks_mainActivity[apk_path.split("/")[2]] = mainactivity
                        return apks_mainActivity
    except Exception as e:
        print("Error:", str(e))
        return None

def get_S2R(project_issue):
    oredred_adb_result = []
    S2R = []
    with open("../Preprocessed S2R/%s" % (project_issue),"r",encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                for pm_items in pm_list:
                    if pm_items in line:
                        with open("../API Mapping/results/%s/top_1/Brave#20628.txt" % (project_issue), "r", encoding="utf-8") as step_file:
                            step_file_lines = step_file.readlines()
                            for step_file_line in step_file_lines:
                                adb_result = get_main_activity("../Artifact-Evaluation/Brave_Issue#20628")
                                # print("adb_result",adb_result["Brave_Issue#20628"])
                                final_result = step_file_line.replace("<package name>",adb_result["Brave_Issue#20628"])
                                oredred_adb_result.append(final_result)
                                #
                            print("-----------------",step_file_lines)
                for am_items in am_list:
                    if am_items in line:
                        with open("../API Mapping/results/%s/top_10/1.txt" % (project_issue.split(".")[0]), "r", encoding="utf-8") as step_file:
                            step_file_lines = step_file.readlines()
                            for step_file_line in step_file_lines:
                                adb_result = get_main_activity("../Artifact-Evaluation/Brave_Issue#20628")
                                # print("adb_result",adb_result["Brave_Issue#20628"])
                                final_result = step_file_line.replace("<package name>",adb_result["Brave_Issue#20628"])
                                oredred_adb_result.append(final_result)
                for widget_item in widget_list:
                    if widget_item in line:
                        with open("../API Mapping/results/%s/top_1/1.txt" % (project_issue.split(".")[0]), "r", encoding="utf-8") as step_file:
                            step_file_lines = step_file.readlines()
                            for step_file_line in step_file_lines:
                                adb_result = get_main_activity("../Artifact-Evaluation/Brave_Issue#20628")
                                # print("adb_result",adb_result["Brave_Issue#20628"])
                                if "<text>" in step_file_line:
                                    final_result = step_file_line.replace("<text>",adb_result["Brave_Issue#20628"])
                                    oredred_adb_result.append(final_result)
                                elif "<x,y>" in step_file_line:
                                    final_result = step_file_line.replace("<x,y>", adb_result["Brave_Issue#20628"])
                                    oredred_adb_result.append(final_result)
    print(oredred_adb_result)
                        # print("widget",str(line.strip()))

def get_componets(activity):
    text_view_selector = 'new UiSelector().text("Hello, World!")'
    print(text_view_selector)


get_S2R("Brave#20628.txt")

# def extract_elements(package_name,component_name):
#
#     device = u2.connect()
#     device.app_start(package_name)
#     device.app_wait(package_name, timeout=5000)
#
#     #Text, resource-id, class, package, content-desc, checkable, checked, clickable, enabled, focusable, focused, scrollable, long-clickable, password, selected
#     element = device(text=component_name)
#     print("--------------------")
#     print(element.info)
#     x = element.center()[0]
#     y = element.center()[1]
#     print(x,y)

# print(os.listdir("../Artifact-Evaluation/Brave_Issue#20628"))
# print(get_main_activity("../Artifact-Evaluation/Brave_Issue#20628"))
get_componets("org.chromium.android_webview.devui.MainActivity")

# if __name__ == "__main__":
#
#
#     parent_path = os.path.join(os.path.dirname(os.getcwd()), "Artifact-Evaluation")
#     for apk_dir in os.listdir(parent_path):
#         apk_path = os.path.join(parent_path,apk_dir)
#         get_main_activity(apk_path)
#         extract_elements("com.example.Flutter_issue_56584","Test")
#         print(apk_path)
#
#
#     if apks_mainActivity:
#         for apk, activity in apks_mainActivity.items():
#             print(f"{apk}: {activity}")
#     else:
#         print("No APKs found or no main activities found.")

# apk_path = os.path.join(os.path.dirname(os.getcwd()), "Artifact-Evaluation")