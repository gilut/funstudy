# This Python file uses the following encoding: utf-8
# pip install android-auto-play-opencv
import android_auto_play_opencv as a2p

adb_path = '..\\platform-tools\\'
a2pmo = a2p.AapoManager(adb_path)

template = {"org_quest_start": './template/quest_start.png',
            "org_player_area": './template/quartet_4p.png',
            "result_back": './template/result_back.png',
            "result_next": './template/result_next.png'}


def main():
    while True:
        # 画面キャプチャ
        a2pmo.screencap()
        # キャプチャした画像を保存
        # a2pmo.imgSave('./screenshot/screenshot.png')
        state = check_state()

        if state == 'PT_OLG' and check_participant():
            # 編成画面かつ出撃条件を満たす場合、出撃ボタンを押してみる。
            # （入室しているプレイヤー全員が準備完了となるまで出撃不可）
            quest_start()

        else:

            pass


def check_state():
    if a2pmo.chkImg(template.get("org_quest_start")):
        return 'PT_OLG'
    elif a2pmo.touchImg(template.get("result_next")) or a2pmo.touchImg(template.get("result_back")):
        return 'RESULT'
    else:
        return 'BATTLE'


def check_participant():
    # 参加者チェック
    # 4pが入室している場合
    return not a2pmo.touchImg(template.get("org_player_area"))


def quest_start():
    a2pmo.touchImg(template.get("org_quest_start"))


if __name__ == '__main__':
    main()
