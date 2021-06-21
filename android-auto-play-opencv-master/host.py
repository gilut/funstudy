template = {"org_quest_start": './template/quest_start.png',
            "org_player_area": './template/quartet_trio.png',
            "org_start_alert": './template/quest_start_check.png',
            "battle_auto": './template/battle_auto.png',
            "result_back": './template/result_back.png',
            "result_next": './template/result_next.png'}


class QuestChart:

    def __init__(self, a2pmo):
        self.a2pmo = a2pmo

    def check_state(self):
        if self.a2pmo.touchImg(template.get("org_start_alert")):
            return 'START'
        elif self.a2pmo.chkImg(template.get("org_quest_start")):
            return 'PT_OLG'
        elif self.a2pmo.touchImg(template.get("result_next")) \
                or self.a2pmo.touchImg(template.get("result_back")):
            return 'RESULT'
        elif self.a2pmo.chkImg(template.get("battle_auto")):
            return 'BATTLE'
        else:
            return 'NONE'

    def do_state_process(self, now_state):
        if now_state == 'PT_OLG' and check_participant(self.a2pmo):
            # 編成画面かつ出撃条件を満たす場合、出撃ボタンを押してみる。
            # （入室しているプレイヤー全員が準備完了となるまで出撃不可）
            quest_start(self.a2pmo)
            self.a2pmo.sleep(1)
        elif now_state == 'START':
            print("クエスト開始:30秒処理停止")
            self.a2pmo.sleep(30)
        elif now_state == 'RESULT':
            print("リザルト")
        else:
            pass


def check_participant(a2pmo):
    # 参加者チェック
    # 3p、4pがどちらも空き状態でなければtrue
    return not a2pmo.chkImg(template.get("org_player_area"))


def quest_start(a2pmo):
    a2pmo.touchImg(template.get("org_quest_start"))
