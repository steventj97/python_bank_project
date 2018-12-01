import json
import sys
sys.path.append("../")
import helper.TransaksiHelper as TransaksiHelper

def AddRekening(rekening_id, pin, saldo):
    print("add rekening")

def RetrieveDataRekening():
    with open("../static/DataRekening.json") as data_rekening:
        return json.load(data_rekening)

def FindRekeningById(user_id):
    for data in RetrieveDataRekening()['data']:
        if user_id == data['user_id']:
            rekening_user = data

    return rekening_user

def ValidasiRekening(rekening_id):
    DataRekening = RetrieveDataRekening()
    for data in DataRekening['data']:
        if data['rekening_id'] == rekening_id:
            print('data rekening ada')
            return data
    print("==============================")    
    print('data rekening tidak ada')
    return 0

def CekSaldo(rekening_id):

    #load data rekening
    data_rekening = RetrieveDataRekening()
    for data in data_rekening["data"]:
        if data['rekening_id'] == rekening_id:
            data_rekening_user = data

    #print saldo
    print("==============================")
    print("Total saldo anda adalah :",data_rekening_user["total_saldo"])
    print("==============================")

def TarikTunai(nominal_tarik, rekening_id):
    
    total_saldo = DecreasingBalance(nominal_tarik, rekening_id)

    print("==============================")
    print("Jumlah nominal yang ditarik adalah :",nominal_tarik)
    print("Total Saldo hingga saat ini adalah :",total_saldo)
    print("==============================")

def SetorTunai(nominal_setor, rekening_id):
    
    total_saldo = IncreasingBalance(nominal_setor, rekening_id)

    print("==============================")
    print("Jumlah nominal yang disetor adalah :",nominal_setor)
    print("Total Saldo hingga saat ini adalah :",total_saldo)
    print("==============================")

def TransferSaldo(nominal_transfer, source_id, destination_id):
    if ValidasiRekening(destination_id) != 0:
        total_saldo = DecreasingBalance(nominal_transfer, source_id) 
        if total_saldo != 0:
            IncreasingBalance(nominal_transfer,destination_id)
            #untuk record transaksi
            TransaksiHelper.StoreDataTransaksi(nominal_transfer, source_id, "OUT")
            #untuk store transaksi
            TransaksiHelper.StoreDataTransaksi(nominal_transfer, destination_id, "IN")
            print("==============================")
            print("Jumlah nominal yang ditransfe adalah :",nominal_transfer)
            print("Total Saldo hingga saat ini adalah :",total_saldo)
            print("==============================")
    else:
        print("Rekening yang anda masukan tidak valid")
        print("==============================")

def IncreasingBalance(nominal ,rekening_id):
    data_rekening = RetrieveDataRekening()
    for data in data_rekening["data"]:
        if data['rekening_id'] == rekening_id:
            data["total_saldo"] = int( data["total_saldo"]) + nominal
            total_saldo = data["total_saldo"]

    with open('../static/DataRekening.json','w') as f:
        json.dump(data_rekening, f, indent=2)

    return total_saldo

def DecreasingBalance(nominal, rekening_id):
    data_rekening = RetrieveDataRekening()
    for data in data_rekening["data"]:
        if data['rekening_id'] == rekening_id:
            if int( data["total_saldo"]) > nominal:
                data["total_saldo"] = int( data["total_saldo"]) - nominal
                total_saldo = data["total_saldo"]
            else:
                print("Maaf saldo anda tidak mencukupi")
                return 0
    with open('../static/DataRekening.json','w') as f:
        json.dump(data_rekening, f, indent=2)
    
    return total_saldo