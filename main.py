import os
import time

from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from lxml import etree
from googleapiclient.discovery import build
from google.oauth2 import service_account
import psycopg2
import datetime
import requests


load_dotenv()

def get_data_form_table():
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    SAMPLE_SPREADSHEET_ID = '10zdMrhZFUdn5U3CFzfhMp0-KGZ8KbuoFR23BPL6xlKM'

    service = build('sheets', 'v4', credentials=creds)

    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A1:D60").execute()

        # request = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, fields='sheets(properties(title),data(rowData(values(userEnteredValue,effectiveValue,formattedValue))))').execute()
        # print(request)
        return result.get('values')

    except Exception as ex:
        print(f"Ошибка при прочтении таблицы {ex}")


def get_value_USD():
    xml_content = requests.get(f"https://cbr.ru/scripts/XML_daily.asp").content
    root = etree.XML(xml_content)
    usd = [float(child.find("Value").text.replace(",",".")) for child in root if child.find("CharCode").text == "USD"]
    return usd[0]


def db_work(usd, datas):
    try:
        conn = psycopg2.connect(dbname=os.getenv('NAME'), user=os.getenv('USER'), password=os.getenv('PASSWORD'), host=os.getenv('HOST'), port=os.getenv('PORT'))
        conn.autocommit = True

        with conn.cursor() as cursor:
            for i in range(1, len(datas)):
                number = int(datas[i][0])
                order = int(datas[i][1])
                price = int(datas[i][2])
                data = datas[i][3]
                cursor.execute(
                    f""" INSERT INTO backend_api_kanalservis (№, заказ№, стоимость$, стоимостьРуб, срок_поставки) VALUES ({number}, {order}, {price},{price*usd},'{data}')"""
                )
            print("Добавил")
        cursor.close()
        conn.close()
    except Exception as ex:
        print("Ошибка при работе с PostgreSQL", ex)


def old_sql():
    try:
        conn = psycopg2.connect(dbname=os.getenv('NAME'), user=os.getenv('USER'), password=os.getenv('PASSWORD'), host=os.getenv('HOST'), port=os.getenv('PORT'))

        records = []
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM backend_api_kanalservis"""
            )
            rows = cursor.fetchall()
            for row in rows:
                records.append([row[0],row[1],row[2],row[4]])

        cursor.close()
        conn.close()
        return records

    except Exception as ex:
        print("Ошибка при работе с PostgreSQL", ex)



def find_changes(list1, list2):
    for i, (x, y) in enumerate(zip(list1, list2)):
        if isinstance(x, list) and isinstance(y, list):
            sub_index = find_changes(x, y)
            if sub_index:
                return (i,) + sub_index
        elif x != y:
            return (i,)
    if len(list1) < len(list2):
        return (len(list1),)
    elif len(list1) > len(list2):
        return (len(list2),)
    return None


def main():

    print(old_sql())
    print(get_data_form_table())
    # while True:
    #     new_datas = get_data_form_table()
    #     if old_datas != new_datas:
    #         print(find_changes(old_datas,new_datas))
    #         old_datas = new_datas
    #         # print(len(changes))
    #     time.sleep(10)
    # db_work(get_value_USD(), datas)


if __name__=="__main__":
    main()
