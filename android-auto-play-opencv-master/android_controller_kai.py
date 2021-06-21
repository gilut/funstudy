"""
◆準備
１.pip install android-auto-play-opencv
２.SDK Platform-Toolsをダウンロード
   https://developer.android.com/studio/releases/platform-tools
３.platform-toolsディレクトリをandroid-auto-play-opencv-masterと同じディレクトリに格納
"""

# This Python file uses the following encoding: utf-8
# pip install android-auto-play-opencv

import time
import android_auto_play_opencv as a2p

import importlib

# get time when the program stated
start_time = time.time()

adb_path = '..\\platform-tools\\'
# adb_path = 'C:\\Program Files (x86)\\Nox\\bin\\'
a2pmo = a2p.AapoManager(adb_path)

game_mode = ('void', 'host', 'guest')


def main():
    # game_mode毎にゲームの状態を判別し、状態に合わせた処理を行う
    target_mode = game_mode[2]

    # 個別にインポートせず、対象クエストのチャートインスタンスを取得
    quest = importlib.import_module(target_mode)
    quest_chart = quest.QuestChart(a2pmo)

    while True:
        # 画面キャプチャ
        a2pmo.screencap()

        # キャプチャした画像を保存
        # a2pmo.imgSave('./screenshot/screenshot.png')

        now_state = print_state(quest_chart.check_state())
        quest_chart.do_state_process(now_state)


def print_state(state):
    print(get_time_str(), " 【", state, "】#########################")
    return state


def get_time_str():
    elapsed_time = int(time.time() - start_time)

    # convert second to hour, minute and seconds
    elapsed_hour = elapsed_time // 3600
    elapsed_minute = (elapsed_time % 3600) // 60
    elapsed_second = (elapsed_time % 3600 % 60)

    # return as 00:00:00
    return str(elapsed_hour).zfill(2) + ":" + str(elapsed_minute).zfill(2) + ":" + str(elapsed_second).zfill(2)


if __name__ == '__main__':
    main()
