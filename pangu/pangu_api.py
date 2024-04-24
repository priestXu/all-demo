import http.client
import requests
import ssl
import json

url = "https://iam.cn-southwest-2.myhuaweicloud.com/v3/auth/tokens"

payload = json.dumps({
    "auth": {
        "identity": {
            "methods": [
                "hw_ak_sk"
            ],
            "hw_ak_sk": {
                "access": {
                    "key": "SQE92TW16VX8UDAHSVRC"
                },
                "secret": {
                    "key": "naxu0nOEc7XGooz54lgc2Gov8GIc23vYADmFeIzr"
                }
            }
        },
        "scope": {
            "project": {
                "name": "cn-southwest-2"
            }
        }
    }
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
token = response.headers['X-Subject-Token']

print(token)

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
conn = http.client.HTTPSConnection(
    "pangu.cn-southwest-2.myhuaweicloud.com", context=context)
payload = {
    "prompt": "背诵下出师表。",
    "user": "User1",
    "max_tokens": 50,
    "temperature": 0.5,
    "n": 1
}

payload_json = json.dumps(payload)
headers = {
    'X-Auth-Token': token,
    'Content-Type': 'application/json'
}
conn.request("POST",
             "v1/infers/7c996ea5-a08d-4480-9b47-29b71df679ce/v1/09a906f6d980f4862fd3c01a3eb661bb/deployments/870e96e8-08c8-4063-b0c5-b167e3942214/text/completions",
             payload_json, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
