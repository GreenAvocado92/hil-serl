import json
import requests
import os

offline_address = "http://127.0.0.1:5001/clearerr"

def online_pre():
    offline_data = {
        "producttype":"KFR-72W/6121",
        "frame": "world",
        "sign":1
    }
    respon = requests.request("POST", offline_address, json=offline_data)
    res = respon.json()
    print("offline res = ", res)

def o():
    res = requests.post(offline_address, json={}).json()
    print("ooo res = ", res)

                  
if __name__ == '__main__':
    online_pre()
    o()
