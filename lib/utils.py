import json
from typing import List, Dict
import selenium
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def extractTalentOccupation(
    accept_company: List[str],
    except_occupation: List[str],
    positions: List[str],
    companies: List[str],
    positionData: List,
    talentData: Dict,
    talentDataKey: str):

    for data in positionData:
        position = data.text.split(" at")
        acception = False

        if position[0] != '':

            for ac in accept_company:
                if ac in position[-1]: # 対象企業があれば、タレントとしてカウントする
                    acception = True
                    break

            if acception:# 対象企業でも、対象職種でなければ、カウント外とする
                for ex in except_occupation:
                    if ex in position[0]:
                        acception = False

            if acception:
                positions.append(position[0])
                companies.append(position[-1])

    positions_text = '\n'.join([c.text for c in positionData])
    talentData[talentDataKey].append(positions_text)
    return positions, companies, talentData, positions_text


def getSpreadSheet(sheet_key: str, sheet_name: str):
    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    # https://docs.google.com/spreadsheets/d/◯◯◯◯◯◯/edit#gid=0の「◯」の部分


    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name('prj-pythonautomate-00d3fa1dadec.json', SCOPE)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートのシート1を開く
    workbook = gc.open_by_key(sheet_key)
    worksheet = workbook.worksheet(sheet_name)

    return worksheet
