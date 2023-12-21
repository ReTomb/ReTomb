::Automatic reproduce step

adb shell am start com.example.ivs_player_example/.MainActivity

adb shell sleep 10

adb shell input tap 1200 200

adb shell sleep 5

adb shell input tap 1200 2200
adb shell sleep 5

adb shell input keyevent 3
adb shell sleep 5

adb shell settings put system user_rotation 1
adb shell sleep 3

adb shell settings put system user_rotation 0
adb shell sleep 3
adb shell am start com.example.ivs_player_example/.MainActivity


