import json
import datetime

def RetrieveDataTransaksi():
    with open("../static/DataTransaksi.json") as data_transaksi:
        return json.load(data_transaksi)

def StoreDataTransaksi(amount, id, jenis_transaksi):
    data_transaksi = RetrieveDataTransaksi()
    tanggal_store = datetime.datetime.now().strftime("%d %B %Y")
    data_transaksi_baru =  {
        "transaksi_id" : int(len(data_transaksi["data"])),
        "user_id" : id,
        "nominal" : amount,
        "jenis_transaksi" : jenis_transaksi,
        "created_time" : tanggal_store
    }
    data_transaksi["data"].append(data_transaksi_baru)
    with open('../static/DataTransaksi.json','w') as f:
        json.dump(data_transaksi, f, indent=2)
    


    