::Automatic reproduce step

adb shell am start com.example.flutter_issue_99352/.MainActivity

adb shell input keyevent KEYCODE_PAGE_DOWN

adb shell input keyevent KEYCODE_PAGE_UP

adb shell input keyevent KEYCODE_HOME

adb shell am start com.example.flutter_issue_99352/.MainActivity