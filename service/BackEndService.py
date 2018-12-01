import json
import sys
import uuid
sys.path.append("../")
import helper.RekeningHelper as RekeningHelper
import helper.TransaksiHelper as TransaksiHelper
import service.UserService as UserService
import service.FrontEndService as FrontEndService
import pandas as pd
from pandas import DataFrame


def TambahRekening():
    data_user = UserService.RetrieveAllUser()
    data_rekening = RekeningHelper.RetrieveDataRekening()
    # data user baru
    nama_user_baru = input('masukan nama untuk user baru :')
    data_user_baru = {
        "id" : str(int(uuid.uuid4()))[:6],
        "pin" : str(int(uuid.uuid4()))[:6],
        "name" : nama_user_baru,
        "status" : "front_office",
        "alter_password": "false"
    }
    data_rekening_baru = {
        "rekening_id": str(int(uuid.uuid4()))[:8],
        "user_id": data_user_baru['id'],
        "total_saldo": 0,
        "status" : "active"
    }
    data_user['data'].append(data_user_baru)
    data_rekening['data'].append(data_rekening_baru)
    with open('../static/DataRekening.json','w') as f:
        json.dump(data_rekening, f, indent=2)
    with open('../static/DataUserGlobal.json','w') as f:
        json.dump(data_user, f, indent=2)

def RemoveRekening():
    data_rekening = RekeningHelper.RetrieveDataRekening()
    data_user = UserService.RetrieveAllUser()
    rekening_yang_di_hapus = input('masukan rekening yang hendak dihapus:')
    keterangan_rekening = "tidak ada"
    keterangan_user = "tidak ada"
    data_rekening_ke = 0
    data_user_ke = 0
    for rekening in data_rekening['data']:
        if rekening['rekening_id'] == rekening_yang_di_hapus:
            keterangan_rekening = "ada"
            del data_rekening['data'][data_rekening_ke]
            with open('../static/DataRekening.json','w') as f:
                json.dump(data_rekening, f, indent=2)
            id_user_yang_akan_dihapus = rekening['user_id']
            break
        data_rekening_ke = data_rekening_ke + 1

    for user in data_user['data']:
        if user['id'] == id_user_yang_akan_dihapus:
            keterangan_user = "ada"
            del data_user['data'][data_user_ke]
            with open('../static/DataUserGlobal.json','w') as f:
                json.dump(data_user, f, indent=2)
            break
        data_user_ke = data_user_ke + 1

    if keterangan_rekening == "ada":
        print('data rekening berhasil dihapus')
    else:
        print("data rekening yang anda masukan tidak valid")

    if keterangan_rekening == "ada":
        print('data user berhasil dihapus')

def BlockRekening():
    id_yang_di_blokir = input('masukan no rekening yang hendak di blokir :')
    data_rekening = RekeningHelper.RetrieveDataRekening()
    for rekening in data_rekening['data']:
        if rekening['rekening_id'] == id_yang_di_blokir:
            rekening['status'] = "block"
            print("rekenign dengan no" + id_yang_di_blokir + "telah di blokir")
            break
    with open('../static/DataRekening.json','w') as f:
        json.dump(data_rekening, f, indent=2)

def CekSaldoUser():
    rekening_user = input('masukan rekening user yang hendak di cek saldo :')
    # gunakan front user service
    FrontEndService.CekSaldoService(rekening_user)

def CekHistoryTransaksiUser():
    rekening_user = input('Masukan rekening yang hendak di list transaksinya :')
    data_rekening = RekeningHelper.ValidasiRekening(rekening_user)
    data_transaksi = TransaksiHelper.RetrieveDataTransaksi()
    new_transaksi_list = {}
    new_transaksi_list['data'] = []
    for data in data_transaksi['data']:
        if data_rekening['user_id'] == data['user_id']:
            new_transaksi_list['data'].append(data)

    df = pd.DataFrame.from_dict(new_transaksi_list['data'], orient='columns')
    print("==============================")
    print(df)

def TambahAddmin():
    data_user_global = UserService.RetrieveAllUser()
    # data admin baru
    id_admin_baru = input('masukan id untuk admin baru :')
    pass_admin_baru = input('masukan pass untuk user baru :')
    for data in data_user_global['data']:
        if data['id'] == id_admin_baru:
            print('id yang dimasukkan telah ada, mohon masukan ID lainnya')
            break

    data_user_baru = {
        "id" : id_admin_baru,
        "pin" : pass_admin_baru,
        "status" : "back_office",
        "alter_password": "false"
    }

    data_user_global['data'].append(data_user_baru)

    with open('../static/DataUserGlobal.json','w') as f:
        json.dump(data_user_global, f, indent=2)

    print("admin dengan ID: "+id_admin_baru+" telah berhasil ditambah" )

def RemoveAdmin():
    id_admin = input("masukan ID admin yang hendak dihapus :")
    data_user_global = UserService.RetrieveAllUser()
    data_user_ke = 0
    for user in data_user_global['data']:
        if user['id'] == id_admin:
            del data_user_global['data'][data_user_ke]
            with open('../static/DataUserGlobal.json','w') as f:
                json.dump(data_user_global, f, indent=2)
            print("admin dengan ID: "+id_admin+" telah berhasil dihapus" )
            break
        data_user_ke = data_user_ke + 1
    
def EditRekening():
    rekening_id = input("masukan data rekening yang hendak di edit :")
    rekening_user = RekeningHelper.ValidasiRekening(rekening_id)
    if rekening_user != 0:
        print("Jenis edit yang hendak dilakukan")
        print("==============================")
        print("1. Edit saldo")
        print("2. Edit status")
        choice = int(input("pilihan anda adalah :"))
        if choice == 1:
            saldo_baru = input("saldo baru yang hendak dimasukan adalah :")
            rekening_user['total_saldo'] = int(saldo_baru)
        if choice == 2:
            print("status rekening saat ini adalah :" + rekening_user['status'])
            status_choice = input("apakah anda ingin mengubahnya ? (Yes / No)")
            if status_choice.lower() == "yes":
                if rekening_user['status'] == "active":
                    rekening_user['status'] = "block"
                else:
                    rekening_user['status'] = "active"
                print("status rekening saat ini adalah :" + rekening_user['status'])
        
        data_rekening = RekeningHelper.RetrieveDataRekening()
        for data in data_rekening["data"]:
            if data['rekening_id'] == rekening_user['rekening_id']:
                data['total_saldo'] = rekening_user['total_saldo']
                data['status'] = rekening_user['status']
        with open('../static/DataRekening.json','w') as f:
            json.dump(data_rekening, f, indent=2)

def EditAdmin():
    admin_id = input("masukan data rekening yang hendak di edit :")
    admin = UserService.ValidasiUser(admin_id)
    if admin != 0:
        print("Jenis edit yang hendak dilakukan")
        print("==============================")
        print("1. Edit nama")
        print("2. Edit password")
        choice = int(input("pilihan anda adalah :"))
        if choice == 1:
            nama_baru = input("nama baru yang hendak dimasukan adalah :")
            admin['name'] = nama_baru
            print("nama telah diganti menjadi " + nama_baru)
        if choice == 2:
            password_baru = input("password baru yang hendak dimasukan adalah :")
            admin['password'] = password_baru

        data_user = UserService.RetrieveAllUser()
        for data in data_user['data']:
            if data['id'] == admin_id:
                data['name'] = admin['name']
                data['password'] = admin['password']
        with open('../static/DataUserGlobal.json','w') as f:
            json.dump(data_user, f, indent=2)
