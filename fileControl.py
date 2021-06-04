import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# GoogleDriveから対戦相手の戦績を含む画像をダウンロード
# 対象は ffbe-wotv-guild-analyze フォルダの中身
def download_target_dir():
    print("fileControl.download_target_dir() START")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    dir_id = drive.ListFile(
        {'q': 'title = "ffbe-wotv-guild-analyze"'}).GetList()[0]['id']
    for file_id in drive.ListFile(
            {'q': '"{}" in parents and trashed = false'.format(dir_id)}
    ).GetList():
        print(file_id['title'])
        f = drive.CreateFile({'id': file_id['id']})
        localPath = "images/download/" + file_id['title']
        f.GetContentFile(localPath)
    print("fileControl.download_target_dir() END")


download_target_dir()
