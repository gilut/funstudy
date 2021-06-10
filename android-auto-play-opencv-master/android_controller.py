# This Python file uses the following encoding: utf-8
# pip install android-auto-play-opencv
import android_auto_play_opencv as am

adbpath = '..\\platform-tools\\'


def main():
    aapo = am.AapoManager(adbpath)

    while True:
        # 画面キャプチャ
        aapo.screencap()
        # キャプチャした画像を保存
        aapo.imgSave('./screenshot/screenshot.png')

        if check_participant():
            quest_start(aapo)


def check_participant():
    # 参加者チェック
    return True


def quest_start(aapo):
    aapo.touchImg('./template/quest_start.png')


if __name__ == '__main__':
    main()
