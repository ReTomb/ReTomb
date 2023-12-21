::Automatic reproduce step

adb shell am start -n com.brave.browser_nightly/org.chromium.chrome.browser.ChromeTabbedActivity

adb shell input tap 1000 2150

adb shell input tap 500 600

adb shell input tap 1000 2150

adb shell input tap 500 600

adb shell input tap 500 200

adb shell input text "test"

adb shell input keyevent 66

