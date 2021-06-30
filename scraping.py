from selenium import webdriver

import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select
import pandas as pd

# 在庫管理 サイト を 開く
driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://iteng.lovesick.jp/index.php')

# xpath で 指定
userID = driver.find_element_by_xpath('/html/body/form/fieldset/input[1]')
# #ユーザ ID を 入力
userID.send_keys("0001")

# nameで指定
userPass = driver.find_element_by_name('pass')
# パスワードを入力
userPass.send_keys("test01")

# nameで指定
login = driver.find_element_by_name('soushin')

# ログインをクリック
login.click()

# ウィンドウハンドルを取得する
handle_array = driver.window_handles

# 入庫履歴ボタンをxpathで指定
into = driver.find_element_by_xpath('/html/body/p[2]/a[5]/img')

# クリックして別タブで開く操作
ActionChains(driver).move_to_element(into).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()

# 入庫履歴画面へ切り替え
driver.switch_to.window(driver.window_handles[-1])

# 要素が表示されるまで待機
driver.implicitly_wait(10)

# メーカーリストよりパナソニックを指定
dropdown = driver.find_element_by_name('MAKER')
select = Select(dropdown)

# valueが"パナソニック"のoptionタグを選択状態にする
select.select_by_value("パナソニック")

# 要素が表示されるまで待機
driver.implicitly_wait(10)

# 品目リストよりバッテリーを指定
dropdown1 = driver.find_element_by_name('PARTSNAME')
select1 = Select(dropdown1)

# valueが"バッテリー"のoptionタグを選択状態にする
select1.select_by_value("バッテリー")

# 部品名検索ボタンをxpathで指定
search = driver.find_element_by_xpath('/html/body/form/input[3]')
search.click()

# 表示されるまで待機
driver.implicitly_wait(5)

# 空リストの作成
values1 = []  # 型番
values2 = []  # 数量
values3 = []  # 日時

# テーブルのボディ部分を選択し、さらにその中にあるtrタグを全部取得
table = driver.find_element_by_tag_name('tbody')
elements = table.find_elements_by_tag_name('tr')

for element in elements:
    val1 = element.find_element_by_css_selector('td:nth-child(3)').text
    val2 = element.find_element_by_css_selector('td:nth-child(7)').text
    val3 = element.find_element_by_css_selector('td:nth-child(12)').text

    values1.append(val1)
    values2.append(val2)
    values3.append(val3)

print(values1, values2, values3)

# メインメニューへ切り替え
driver.switch_to.window(driver.window_handles[0])

into = driver.find_element_by_xpath('html/body/p[2]/a[4]/img')

ActionChains(driver).move_to_element(into).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()

driver.switch_to.window(driver.window_handles[-1])

driver.implicitly_wait(10)

search1 = driver.find_element_by_xpath('/html/body/form/input[2]')
search1.click()

driver.quit()

df = pd.DataFrame({'型番': values1, '数量': values2, '日時': values3})
df.to_csv("入庫履歴.csv", encoding="shift-jis")
