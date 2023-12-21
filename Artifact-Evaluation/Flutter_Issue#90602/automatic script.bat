::Automatic reproduce step

adb shell am start com.example.bug/.MainActivity

adb shell input keyevent 4

adb shell am start com.example.bug/.MainActivity