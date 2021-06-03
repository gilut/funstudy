import codecs
import os
import pickle
import json

from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRETS_FILE = 'client_secret.json'  # 各自のclient_secret.jsonファイルへのパスを設定
USER_CREDENTIALS_FILE = os.environ['USERNAME'] + '.credentials'  # ユーザ毎の認証データ保存
SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'


def get_authenticated_service():
    credentials = None
    if os.path.exists(USER_CREDENTIALS_FILE):
        try:
            with open(USER_CREDENTIALS_FILE, 'rb') as fi:
                credentials = pickle.load(fi)

            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())  # 期限の更新を試みる
        except EOFError as e:
            pass

    if credentials is None or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()

    with open(USER_CREDENTIALS_FILE, 'wb') as fo:  # 認証情報をファイルに保存
        pickle.dump(credentials, fo)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def list_drive_files(service, **kwargs):
    results = service.files().list(**kwargs).execute()
    return results


def get_drive_file_info(service, path):
    """指定パスのファイル情報を取得"""
    parent_id = 'root'
    path_depth = len(path)
    info = None
    for depth, name in enumerate(path):
        if depth < (path_depth - 1):
            mimeType = "mimeType = 'application/vnd.google-apps.folder' and "
        else:
            mimeType = ""
        res = list_drive_files(service,
                               q=f"'{parent_id}' in parents and "
                                 f"{mimeType} "
                                 f"name = '{name}'")
        if 'files' not in res or len(res['files']) < 1:
            return None
        info = res['files'][0]
        parent_id = res['files'][0]['id']

    return info


def get_drive_folder_id(service, folder_path):
    """指定パスフォルダのfileIdを取得"""
    parent_id = 'root'
    for name in folder_path:
        res = list_drive_files(service,
                               q=f"'{parent_id}' in parents and "
                                 "mimeType = 'application/vnd.google-apps.folder' and "
                                 f"name = '{name}'")
        if 'files' not in res or len(res['files']) < 1:
            return None
        parent_id = res['files'][0]['id']

    return parent_id


def download_file(service, file_info, output_dir):
    """指定ファイルのダウンロード"""
    req = service.files().get_media(fileId=file_info['id'])
    with open(os.path.join(output_dir, file_info['name']), 'wb') as f:
        downloader = MediaIoBaseDownload(f, req)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {status.progress() * 100}%")


service = get_authenticated_service()

'''
# すべてのファイルの一覧を取得 (全ページ)
nextPageToken = None
while True:
    result = list_drive_files(service, pageSize=100, pageToken=nextPageToken)
    print(result)
    if 'nextPageToken' not in result:
        break
    nextPageToken = result['nextPageToken']

# マイドライブ(トップフォルダ)にあるファイル一覧の取得
result = list_drive_files(service, q="'root' in parents")

'''
# マイドライブ(トップフォルダ)にあるファイル一覧の取得
result = list_drive_files(service, q="'root' in parents")
print(result)

'''
# 指定のフォルダにあるファイル一覧を取得
folder_id = get_drive_folder_id(service, ['ffbe-wotv-guild-analyze'])
result = list_drive_files(service, fields='*', q=f"'{folder_id}' in parents")
print(result)
'''

file_path = "./sample.json"
fw = codecs.open(file_path, 'w', 'utf-8')

with open(file_path, 'w') as outfile:
    json.dump(result, fw, indent=4, ensure_ascii=False)
