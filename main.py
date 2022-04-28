from fast_bitrix24 import Bitrix
import requests
import json

from gsh import AddOrderSheet, UpdateOrderSheet

webhook = "https://altair.bitrix24.ua/rest/1/pq4jor2ovao54xbi/"
b = Bitrix(webhook)

def NovaPoshtaGetOrderByTTN(TTN):
    url = 'https://api.novaposhta.ua/v2.0/json/'

    payload = {
        "apiKey": "ffde97724b90d89cdf0ecb016625716c",
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "CheckWeightMethod": "",
            "CalculatedWeight": "",
            "Documents": [
                {
                    "DocumentNumber": TTN,
                    "Phone": ""
                }
            ]
        }
    }

    r = requests.get(url=url, data=json.dumps(payload))

    return r.json()['data'][0]

def BitrixGetDeal():

    deals = b.get_all(
        'crm.deal.list',
        params={
            'select': ['*', 'UF_*'],
            'filter': {'STAGE_ID': ['C29:UC_ZC5KWF', 'C29:UC_BJRWKU']}
    })

    return deals

def BitrixChangeStage(deal_id, stage_id):
    method = 'crm.deal.update'
    params = {'ID': deal_id, 'fields': {'STAGE_ID': stage_id}}
    b.call(method, params)

def NewOrder(order_id):
    deal = b.get_all(
        'crm.deal.list',
        params={
            'select': ['*', 'UF_*'],
            'filter': {'ID': str(order_id)}
    })[0]


    contact = b.get_all(
        'crm.contact.list',
        params={
            'select': ['Name', 'PHONE', "*"],
            'filter': {'ID': deal["CONTACT_ID"]}
    })[0]

    order_id = deal["ID"]
    order_date = str(deal["BEGINDATE"].split("T")[0])
    order_status = "На отправку"
    order_prepayment = deal["UF_CRM_1633275701280"]
    order_sum = deal["OPPORTUNITY"]
    order_discount = 0
    order_count = deal["UF_CRM_1649747064818"][0]
    order_adress = deal["UF_CRM_1633274704683"]
    order_phone = contact["PHONE"][0]["VALUE"]
    order_holdername = contact["NAME"]
    order_ttn = deal["UF_CRM_1645092420180"]

    if deal["UF_CRM_1650966063918"] == '45':
        order_item = "Бронежелет MARK IV"

    print(order_date)
    
    AddOrderSheet(
        order_id,
        order_date,
        order_status,
        order_prepayment,
        order_sum,
        order_discount,
        order_count,
        order_item,
        order_adress,
        order_phone,
        order_holdername,
        order_ttn)
        

def SentOrder(order_id):
    BitrixChangeStage(order_id, "C29:UC_ZC5KWF")



def BitrixControlStatus(order_id, status_code, stage_id):
    status_keys = {
            "7": "C29:UC_BJRWKU",
            "9": "C29:WON",
            "102": "C29:LOSE",
            "103": "C29:LOSE",
        }


    if stage_id != status_keys[status_code]:
        BitrixChangeStage(order_id, status_keys[status_code])


def gshControlStatus(order_id, status_code, stage_id):

    status_keys = {
            "7": "Прибыл на отделение",
            "9": "Получил",
            "102": "Отказался",
            "103": "Отказался",
        }

    UpdateOrderSheet(order_id, {"C": status_keys[status_code]})

def ControlOrderStatus():
    deals = BitrixGetDeal()

    for deal in deals:
        order = NovaPoshtaGetOrderByTTN(deal['UF_CRM_1645092420180'])

        order_id = deal["ID"]
        status_code = order["StatusCode"]
        stage_id = deal["STAGE_ID"]

        gshControlStatus(order_id, status_code, stage_id)
        BitrixControlStatus(order_id, status_code, stage_id)


# ControlOrderStatus()