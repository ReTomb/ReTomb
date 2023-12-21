::Automatic reproduce step

adb shell am start im.status.ethereum/.MainActivity

adb shell input text 123456

adb shell input tap 700 1400

adb shell svc wifi disable
