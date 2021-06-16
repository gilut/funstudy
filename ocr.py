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

from PIL import Image
import pyocr
import cv2

target = "funlead"

# pyocrへ利用するOCRエンジンをTesseractに指定する。
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("ERROR：OCRツールが見つかりませんでした")
    print("　　　　環境変数の設定が必要です")
    exit()

tool = tools[0]

# OCR下処理
img = cv2.imread(f"./images/sample/{target}.PNG")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(f"./images/sample/trim/{target}_GRAY.PNG", img)


threshold = 180
img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite(
    f'./images/sample/trim/{target}_THRESHOLD{threshold}.PNG', img)

img = cv2.bitwise_not(img)
cv2.imwrite(f'./images/sample/trim/{target}_BITWISE.PNG', img)

# OCR対象の画像ファイルを読み込む
# img = Image.open("./images/concat/result.PNG")
img = Image.open(f'./images/sample/trim/{target}_BITWISE.PNG')

# 画像から文字を読み込む
# tesseract_layout=1~6
builder = pyocr.builders.TextBuilder(tesseract_layout=4)
text = tool.image_to_string(img, lang="jpn", builder=builder)

print(text)
