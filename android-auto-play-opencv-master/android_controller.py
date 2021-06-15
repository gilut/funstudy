# This Python file uses the following encoding: utf-8
# pip install android-auto-play-opencv

import time
import android_auto_play_opencv as a2p

# get time when the program stated
start_time = time.time()

adb_path = '..\\platform-tools\\'
a2pmo = a2p.AapoManager(adb_path)

game_mode = ('void', 'multi', 'raid')

template_multi = {"org_quest_start": './template/quest_start.png',
                  "org_player_area": './template/quartet_trio.png',
                  "org_start_alert": './template/quest_start_check.png',
                  "battle_auto": './template/battle_auto.png',
                  "result_back": './template/result_back.png',
                  "result_next": './template/result_next.png'}

template_raid = {"boss_omega": './template/raid/boss_omega.png',
                 "raid_start": './template/raid/raid_challenge.png'}


def g_state(args):
    pass


def main():
    while True:
        # 画面キャプチャ
        a2pmo.screencap()

        # キャプチャした画像を保存
        # a2pmo.imgSave('./screenshot/screenshot.png')

        # game_mode毎にゲームの状態を判別し、状態に合わせた処理を行う
        select_mode = 'multi'
        now_state = check_state(select_mode)
        do_state_process(now_state, select_mode)


def check_state(g_mode):
    if game_mode[1] == g_mode:
        return check_multi_state()
    elif game_mode[2] == g_mode:
        return check_raid_state()
    else:
        return ""


def check_multi_state():
    if a2pmo.touchImg(template_multi.get("org_start_alert")):
        return print_state('START')
    elif a2pmo.chkImg(template_multi.get("org_quest_start")):
        return print_state('PT_OLG')
    elif a2pmo.touchImg(template_multi.get("result_next")) or a2pmo.touchImg(template_multi.get("result_back")):
        return print_state('RESULT')
    elif a2pmo.chkImg(template_multi.get("battle_auto")):
        return print_state('BATTLE')
    else:
        return print_state('NONE')


def check_raid_state():
    if a2pmo.touchImg(template_raid.get("boss_omega")):
        return print_state('START')
    else:
        return print_state('NONE')


def do_state_process(now_state, select_mode):
    if game_mode[1] == select_mode:
        do_multi_state_process(now_state)
    elif game_mode[2] == select_mode:
        do_raid_state_process(now_state)
    else:
        pass


def do_multi_state_process(state):
    print(state)
    if state == 'PT_OLG' and check_participant():
        # 編成画面かつ出撃条件を満たす場合、出撃ボタンを押してみる。
        # （入室しているプレイヤー全員が準備完了となるまで出撃不可）
        quest_start()
        a2pmo.sleep(1)
    elif state == 'START':
        print("クエスト開始:30秒処理停止")
        a2pmo.sleep(30)
    elif state == 'RESULT':
        print("リザルト")
    else:
        pass


def do_raid_state_process(state):
    print(state)


def check_participant():
    # 参加者チェック
    # 3p、4pがどちらも空き状態でなければtrue
    return not a2pmo.chkImg(template_multi.get("org_player_area"))


def quest_start():
    a2pmo.touchImg(template_multi.get("org_quest_start"))


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
