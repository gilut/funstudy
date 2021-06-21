"""
OCRを使ってみる。

◆Tesseractはpythonのモジュールではないので、要install
Windowsの場合：インストーラ
            # インストーラで言語データを選択しなかった場合は手配置。
            # Tesseract 日本語モデル ダウンロード用URL
            # https://github.com/tesseract-ocr/tessdata/blob/master/jpn.traineddata
Linuxの場合：各ディストリビューションのパッケージ管理ソフトウェア
            # Ubuntuの場合別途言語データの配置が必要
            # sudo wget -P /usr/share/tesseract-ocr/4.00/tessdata/ https://github.com/tesseract-ocr/tessdata/blob/master/jpn.traineddata

◆環境変数の設定
1.インストールしたTesseract-OCRのパスを環境変数「PATH」へ追記する。
2.環境変数「TESSDATA_PREFIX」へ"[インストール先ディレクトリ]\Tesseract-OCR\tessdata"を設定する。 # noqa

◆OCRライブラリ > pythonからTesseractをつかうライブラリ
pip install pyocr

参考：https://rightcode.co.jp/blog/information-technology/python-tesseract-image-processing-ocr

"""
import cv2
import pyocr
import pytesseract
import pandas as pd
import io

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("ERROR：OCRツールが見つかりませんでした")
    print("　　　　環境変数の設定が必要です")
    exit()

# OCR精度向上のための下処理


def preprocessing(img, threshold):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]
    img = cv2.bitwise_not(img)
    return img

# Rankという文字が出現する箇所の座標（4点）を取得


def getRankPoint(img):
    data = pytesseract.image_to_data(img, lang='eng', config='--psm 3')
    df = pd.read_csv(
        io.StringIO(data),
        sep='\t',
        engine="python",
        encoding="utf-8"
    )
    df = df[df['text'] == "Rank"]           # Rankと認識されたデータを抽出
    df = df.reset_index(drop=True)          # インデックスを振り直し
    # print(df)
    # 1つ目のデータ（インデックス0）の各値を取得しているが、
    # conf（確度）でソートしてから最も良いものを選んだり、
    # width, heightが最も頻出するパターンである行を選んだりするともっと精度が上がりそう
    left = df.loc[0, 'left']
    top = df.loc[0, 'top']
    width = df.loc[0, 'width']
    height = df.loc[0, 'height']
    return left, top, width, height


# ギルド名らしい部分のX座標（1点）を取得
def getGuildnamePointX(img):
    data = pytesseract.image_to_data(img, lang='jpn', config='--psm 3')
    df = pd.read_csv(
        io.StringIO(data),
        sep='\t',
        engine="python",
        encoding="utf-8"
    )
    # print(df)
    # print("##########################################################")
    # textが認識されなかったデータを削除
    df = df.dropna(subset=['text'])
    # 確度を指定してデータをフィルタリング
    df = df[df['conf'] >= 80]
    # left(x座標)の順にソート
    df = df.sort_values('left')
    # print(df)
    df = df.reset_index(drop=True)          # インデックスを振り直し
    left = df.loc[0, 'left']
    return left
