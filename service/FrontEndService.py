import sys
import json
sys.path.append("../")
import helper.RekeningHelper as RekeningHelper
import helper.TransaksiHelper as TransaksiHelper

def TarikTunaiService(nominal_tarik, rekening_id):
    #untuk penarikan rekening
    RekeningHelper.TarikTunai(nominal_tarik,rekening_id)
    #untuk record transaksi
    TransaksiHelper.StoreDataTransaksi(nominal_tarik, rekening_id, "OUT")

def SetorTunaiService(nominal_setor, rekening_id ):
    #untuk penarikan rekening
    RekeningHelper.SetorTunai(nominal_setor, rekening_id)
    #untuk record transaksi
    TransaksiHelper.StoreDataTransaksi(nominal_setor, rekening_id, "IN")

def CekSaldoService(rekening_id):
    #untuk cek saldo
    RekeningHelper.CekSaldo(rekening_id)

def TransferSaldoService(nominal_setor, source_id, destination_id):
    #transfer rekening
    RekeningHelper.TransferSaldo(nominal_setor, source_id, destination_id)