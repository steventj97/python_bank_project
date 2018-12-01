import json
import sys
sys.path.append("../")
import service.UserService as UserService
import helper.RekeningHelper as RekeningHelper

def PrintAdminListService():
    df = UserService.RetrieveAllAdmin()['data']
    print("==================================")
    print("no " + "| " + "id    " + " | " + "pin   " + " | " + "status")
    print("==================================")
    no = 1
    for data in df:
        print(str(no) + "  | " + data['id'] + " | " + data['id'] + " | " + data['status'])
        no = no + 1
        print("----------------------------------")

def PrintRekeningListService():
    df = RekeningHelper.RetrieveDataRekening()['data']
    print("====================================================")
    print("no " + "|" + " rekening id  " + "|" + " user id   " + "|" + " total saldo " + "|" + " status ")
    print("====================================================")
    no = 1
    for data in df:
        print(" "+str(no) + " | " + data['rekening_id'] + "   | " + data['user_id'] + "    | " + str(data['total_saldo']) + "      | " +data['status'])
        no = no + 1
        print("----------------------------------------------------")        