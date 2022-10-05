import http.client, urllib.request, urllib.parse, urllib.error, base64
import uuid
import json,ast

# x_Reference_Id =  str(uuid.uuid4())
# print(x_Reference_Id)

def api_user_id(x_Ref_Id):
    headers = {
    # Request headers
    'X-Reference-Id': x_Ref_Id,
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'b0bc4fc5ddf3406498291e5f203aa4bc',
    }

    params = urllib.parse.urlencode({
    })

    body = json.dumps({"providerCallbackHost": "https://ee99-154-160-22-170.ngrok.io" })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/v1_0/apiuser?%s" % params, body, headers)
        response = conn.getresponse()
        # print('Response status :',response.status)
        # print('Response reason :',response.reason)
        data = response.read()
        # print(f'response : {response}, data :{data}')
        all_data = {
            "user_id": x_Ref_Id,
            "Response Status : ": response.status,
            "Response reason : ": response.reason,
            "Data": data
        }
        print(all_data)
        conn.close()
        
        return all_data
    except Exception as e:
        return ("[Errno {0}] {1}".format(e.errno, e.strerror))



def user_key(user_id):
    headers = {
    # Request headers
    #add product primary key in the below line where "<product primary key here>" is.
    'Ocp-Apim-Subscription-Key': 'b0bc4fc5ddf3406498291e5f203aa4bc',
    }

    params = urllib.parse.urlencode({
    })
    #add your domain name "<you domain name here>" is.
    body = json.dumps({"providerCallbackHost": "https://ee99-154-160-22-170.ngrok.io" })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        #Add api user ID in the below line where "<api user id here>" is.
        conn.request("POST", "/v1_0/apiuser/"+user_id+"/apikey?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        dict_key = data.decode("UTF-8")
        my_data = ast.literal_eval(dict_key)
        # print('Response status :',response.status)
        # print('Response reason :',response.reason)
        # print(data)
        all_data = {
            "Response Status : ": response.status,
            "Response reason : ": response.reason,
            "Data": my_data.get('apiKey')
        }
        conn.close()
        print(all_data)
        return all_data
    except Exception as e:
        return ("[Errno {0}] {1}".format(e.errno, e.strerror))


# api_user = "4dfcdd00-5a6c-4280-8818-f1b8c9d420f6" #put your api user ID 
# api_key = "e5b433b2842d4ba7bced38d567ddefe1" #put your api key 
# print('Your apkey',len(api_key), 'Your apiuserid', len(api_user))
# api_user_and_key  = api_user+':'+api_key
# #encoded = base64.b64encode(api_user_and_key)
# encoded = base64.b64encode(api_user_and_key.encode()).decode()

def get_token(user_id,user_key):
    api_user_and_key  = user_id+':'+user_key
    #encoded = base64.b64encode(api_user_and_key)
    encoded = base64.b64encode(api_user_and_key.encode()).decode()
    headers = {
        # Request headers
        'Authorization': 'Basic '+encoded,
        #add product primary key in the below line where "<product primary key here>" is.
        'Ocp-Apim-Subscription-Key': 'b0bc4fc5ddf3406498291e5f203aa4bc',
    }

    params = urllib.parse.urlencode({
    })
    #add your domain name where "<you domain name here>" is.
    body = json.dumps({"providerCallbackHost": "https://ee99-154-160-22-170.ngrok.io" })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/collection/token/?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        dict = data.decode("UTF-8")
        my_data = ast.literal_eval(dict)
        # print('Response status :',response.status)
        # print('Response reason :',response.reason)
        # print(my_data)
        all_data = {
            "Response Status : ": response.status,
            "Response reason : ": response.reason,
            "Data": my_data.get('access_token')
        }
        print(all_data)
        return all_data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    finally:
        conn.close()



def request_to_pay(user_id,token,mobile,amount):
    
    # token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSMjU2In0.eyJjbGllbnRJZCI6IjRkZmNkZDAwLTVhNmMtNDI4MC04ODE4LWYxYjhjOWQ0MjBmNiIsImV4cGlyZXMiOiIyMDIxLTA3LTA0VDEzOjA1OjMxLjkwMiIsInNlc3Npb25JZCI6ImVjMjE3OWE3LTZhYzctNDQxNS04OTk5LWU3N2QxOWExYzg4ZiJ9.Natx84pkEeA9eyq5qoY5xzvLRcDql5OExlNlZ2MzKyfx0uTwx5Rg6HZMgPryS80Px7_xePoiCfOBeEbZj2T6OaDnE5aWCu53u3uWu3na8dbPCZpPLkL3D4XNv23c4iKDVhioM29IFNj4JGwUACRRStsjeTFReGh1_2O3yrls-dHniKc--0TtRrhX0qC5q23G988VxeTM_ie5yvJiBcOqtlwoP-Pqd_t4noGNPxeBvADt1c-Kvt1NjoZNZt6yqpUfS9FyGcqrpN-VLW5t7UCQVOrQxhlxBd27AL-2Fmx39EYA6oeKK9jf3PMioaZdZ_q-GPbi9KkWFaD7_qYWF0mhDw"#paste token here

    headers = {
        # Request headers
        'Authorization': 'Bearer '+token,
        #'X-Callback-Url': '<your domain name>',
        'X-Reference-Id': user_id,#add your api user ID
        'X-Target-Environment': 'sandbox',
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'b0bc4fc5ddf3406498291e5f203aa4bc',#add product primary key
    }

    params = urllib.parse.urlencode({
    })


    body = json.dumps({

            "amount": amount,

            #use EUR when working in sandbox
            "currency": "EUR",

            "externalId": "123456",

            "payer": {"partyIdType": "MSISDN","partyId": "250"+mobile}, #phone should start by 250

            "payerMessage": "You have made payment to me, thank you.",

            "payeeNote": "Payment received thank you."

        })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print('Response status :',response.status)
        print('Response reason :',response.reason)
        print(data)
        
        return response.status
        
    except Exception as e:
        print("[Error {0}] {1}".format(e.error, e.strerror))
        return ("[Error {0}] {1}".format(e.error, e.strerror))
    finally:
        conn.close()



