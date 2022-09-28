import httplib2, sqlite3
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from parser import sheet

# Файл, отриманий в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1FuRS9PYHWX4mCmG73rZn-tREJh_53GcLqCr8BQ60ItI'

# Авторизуємось та отримуєм service — екземпляр доступу до API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
# створюємо rows, columns
HEADERS = ('Title', 'Date', 'Url Image')
n = 0
title = []
date = []
url_image = []
all_parameter = []

# named tuple який отримали в файлі парсер розділюємо по необхідним колонкам
while n < 45:
    title.append(sheet[n][0])
    date.append(sheet[n][1])
    url_image.append(sheet[n][2])
    all_parameter.append((sheet[n][0], sheet[n][1], sheet[n][2]))
    n += 1
# додаємо дані в sqlite
conn = sqlite3.connect("mydata.db")
cursor = conn.cursor()
cursor.executemany("INSERT INTO parsing_site VALUES (?,?,?)", all_parameter)
conn.commit()
# додаємо дані в googlesheets
values = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "A1:C1",
             "majorDimension": "ROWS",
             "values": [HEADERS]},
            {"range": f"A2:A46",
             "majorDimension": "COLUMNS",
             "values": [title]},
            {"range": f"B2:B46",
             "majorDimension": "COLUMNS",
             "values": [date]},
            {"range": f"C2:C46",
             "majorDimension": "COLUMNS",
             "values": [url_image]}]
    }
).execute()

# print(all_parameter)

