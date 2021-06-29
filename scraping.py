from selenium import webdriver

import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select

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


