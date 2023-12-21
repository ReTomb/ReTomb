from uiautomator import Device
import os
from androguard.core.bytecodes.apk import APK
import subprocess

#The file can get the commands sequednce from the API Mapping results.
class SelectAPIs:

    def get_component(self):
        device = Device()
        pm_list= []
        am_list = []
        widget_list = []
        with open("../API Mapping/results/Brave#20628/top_1/Brave#20628.txt", "r", encoding="utf-8") as step_file:
            step_file_lines = step_file.readlines()
            for step_file_line in step_file_lines:
                if "input" in step_file_line:
                    componet = device.server.adb.cmd("shell", "settings", "put", "secure", "enabled_accessibility_services",
                              "com.example.Flutter_issue_54587.MainACtivity").communicate()
                    for widget in componet:
                        bounds = widget["private"]
                        widget_list.append(bounds)
                if "pm" in step_file_line:
                    package = device.server.adb.cmd("shell", "settings", "put", "secure", "enabled_accessibility_services",
                              "com.example.Flutter_issue_54587.MainACtivity").communicate()
                    for widget in componet:
                        # package = widget["Start"]
                        pm_list.append(package)
                if "am" in step_file_line:
                    activtiy = device.server.adb.cmd("shell", "settings", "put", "secure", "enabled_accessibility_services",
                              "com.example.Flutter_issue_54587.MainACtivity").communicate()
                    for widget in activtiy:
                        bounds = widget["Start"]
                        am_list.append(bounds)
        return pm_list,am_list,widget_list

    def get_main_activity(apk_path):

        apks_mainActivity = {}
        try:
            for filename in os.listdir(apk_path):
                # print(filename)
                if filename.endswith(".apk"):
                    apk_info = os.path.join(apk_path, filename)
                    # print(apk_info,"---------------------")
                    apk = APK(apk_info)
                    print(apk.get_package(), "---------------------")
                    activity = apk.get_activities()
                    for mainactivity in activity:
                        if "MainActivity" in mainactivity or "MainTabs2" in mainactivity or "org.chromium.chrome.browser.ChromeTabbedActivity" == mainactivity:
                            print(apk_path.split("/")[2])
                            apks_mainActivity[apk_path.split("/")[2]] = mainactivity
                            return apks_mainActivity
        except Exception as e:
            print("Error:", str(e))
            return None


if __name__ == '__main__':
    reproduce_adb_result = []
    issue_name = "Brave#20628"
    issue_path = SelectAPIs().api_list_path(issue_name,10)

    for combine_api in os.listdir(issue_path):
        # print(combine_api)
        combine_api_path = issue_path + combine_api
        with open(combine_api_path, "r", encoding="utf-8") as combine_api_file:
            combine_api_list = combine_api_file.readlines()
            for commands in combine_api_list:
                if "pm" in commands:
                    apk_main_activity = SelectAPIs.get_main_activity("../Artifact-Evaluation/Brave_Issue#20628")
                    package_name = apk_main_activity[issue_name].replace(".MainActivity","")
                    commands.replace("<packagename.activity>", package_name)
                    reproduce_adb_result.append(commands)
                elif "am" in commands:
                    apk_activity = SelectAPIs.get_main_activity("../Artifact-Evaluation/Brave_Issue#20628")
                    commands.replace("<packagename.activity>", apk_activity[issue_name])
                    reproduce_adb_result.append(commands)
                elif "input" in commands:
                    compoent = SelectAPIs().get_component()
                    if "<text>" in commands:
                        commands.replace("<text>", compoent[2])
                        reproduce_adb_result.append(commands)
                    elif "<x,y>" in commands:
                        commands.replace("<x,y>", compoent[2])
                        reproduce_adb_result.append(commands)
                    elif "<x1,y1> <x2,y2>" in commands:
                        commands.replace("<x1,y1> <x2,y2>", compoent[2])
                        reproduce_adb_result.append(commands)
                    else:
                        print("Please check the commands.")

    with open("./Artifact-Evaluation/Brave_Issue#20628/automatic script.bat", "w", encoding="utf-8") as adb_file:
            for adb_commands in reproduce_adb_result:
                adb_file.write(adb_commands + "\n")
                result = subprocess.run(adb_commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    if subprocess.run("adb shell").returncode == 0 and subprocess.run("su root").returncode == 0:
                        if "tombstone" in subprocess.run("cd data/tombstones").stdout:
                            print("The command sequence is successful.")
                            with open("./Artifact-Evaluation/Brave_Issue#20628/automatic script.bat", "w", encoding="utf-8") as adb_file:
                                for adb_commands in reproduce_adb_result:
                                    adb_file.write(adb_commands + "\n")
                        else:
                            print("The command sequence is failed.")
                    else:
                        print("The command sequence is failed.")
                else:
                    print("Failed")

    # print( SelectAPIs.get_main_activity("../Artifact-Evaluation/Brave_Issue#20628"))