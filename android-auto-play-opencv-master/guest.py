import sys

template = {"guest_list": './template/quest_list.png',
            "guest_ready": './template/guest_ready.png',
            "guest_unprepared": './template/guest_unprepared.png',
            "battle_auto": './template/battle_auto.png',
            "result_back": './template/result_back.png',
            "result_next": './template/result_next.png'}

quest_template = {"pink_ball": './template/quest/quest_pink_ball_hard.png'}


class QuestChart:

    def __init__(self, a2pmo):
        self.a2pmo = a2pmo

    def check_state(self):
        if self.a2pmo.touchImg(template.get("guest_ready")):
            return 'READY'
        elif self.a2pmo.touchImg(template.get("result_next")) \
                or self.a2pmo.touchImg(template.get("result_back")):
            return 'RESULT'
        elif self.a2pmo.chkImg(template.get("battle_auto")):
            return 'BATTLE'
        elif self.a2pmo.chkImg(template.get("guest_unprepared")):
            return 'WAIT'
        elif self.a2pmo.chkImg(template.get("guest_list")):
            return 'LIST'
        else:
            return 'NONE'

    def do_state_process(self, now_state):
        if now_state == 'LIST':
            # TODO
            #  :クエスト一覧からお目当てのクエストを選択して入室したい。
            #   画像のマッチングで対応しようとしたが、意図しない部屋へ入るためNG
            #   OCRによる精度向上が必要？？

            # 現時点ではLISTへの戻り検知でループ終了
            sys.exit()

        elif now_state == 'WAIT':
            # TODO
            #  :復帰の遅い他プレイヤーの検知により退出する機能
            self.a2pmo.sleep(5)

        elif now_state == 'RESULT':
            print("リザルト")

        else:
            pass
