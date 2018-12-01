import json

def RetrieveAllUser():
    with open("../static/DataUserGlobal.json") as all_user:
        return json.load(all_user)

def RetrieveAllAdmin():
    user_list = RetrieveAllUser()
    admin_list = {
        "data": []
    }
    for admin in user_list['data']:
        if admin["status"] == "back_office":
            admin_list['data'].append(admin)
    return admin_list

def ValidasiUser(user_id):
    data_user = RetrieveAllUser()
    for data in data_user['data']:
        if data['id'] == user_id:
            return data
    print("==============================")
    print("Your ID are not registered, please contact our officer")
    return 0


def Login(user_data, user_id, total_user):
    for user in user_data["data"]:    
        if user_id == user["id"]:
            print("==============================")
            print("Welcome back user :",user["id"])
            if user["status"] == "front_office":
                user_pin = input("please insert your pin (6 digit) :")
                if user_pin == user["pin"]:
                    print("==============================")
                    print("pin is correct !!!")
                    print("==============================")
                    login_user = user
                    return login_user
                else:
                    print("==============================")
                    print("pin is incorrect")
                    print("==============================")
                    return 0
            else:
                admin_password = input("please insert your password :")
                if admin_password == user["password"]:
                    print("==============================")
                    print("password is correct !!!")
                    print("==============================")
                    login_user = user
                    return login_user
                else:
                    print("==============================")
                    print("password is incorrect")
                    print("==============================")
                    return 0
        total_user = total_user + 1
        if total_user == len(user_data["data"]):
            break
