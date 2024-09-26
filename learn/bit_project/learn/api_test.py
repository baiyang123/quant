import json
import requests
import okx.PublicData as PublicData

'''
https://my.okx.com/docs-v5/zh/?python#overview-rest-authentication 接口文档
https://www.okx.com/zh-hans
'''
def bit_connect_test():
    response = requests.get('https://my.okx.com/api/v5/account/config')
    data = json.loads(response.text)
    print(data)


if __name__ == '__main__':
    bit_connect_test()
