import json
import os
import requests

appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
openId = os.environ.get("USER_ID")
template_id = os.environ.get("YUAN_SHEN_TEMPLATE_ID")
cookie = os.environ.get("YUAN_SHEN_COOKIE")
token = os.environ.get("YUAN_SHEN_TOKEN")

def get_access_token():
    global appID, appSecret
    # 获取access token的url
    print("正在获取 access_token...")
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print("获取到的 access_token 响应：", response)
    access_token = response.get('access_token')
    if access_token:
        print("成功获取到 access_token")
    else:
        print("未能获取到 access_token")
    return access_token


def send(access_token, ltime, status):
    body = {
        "touser": openId.strip(),
        "template_id": template_id,
        "url": "",
        "data": {
            "status": {
                "value": status,
                "color": "#173173"
            },
            "last_time": {
                "value": ltime,
                "color": "#173173"
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    print("正在发送模板消息...")
    response = requests.post(url, json.dumps(body))
    print("发送响应：", response.text)


# 账号信息
url = "https://api-cloudgame.mihoyo.com/hk4e_cg_cn/wallet/wallet/get"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
    "Referer": "https://ys.mihoyo.com/",
    "Cookie": cookie,
    "X-Rpc-App_id": "",
    "X-Rpc-App_version": "4.4.0",
    "X-Rpc-Cg_game_biz": "hk4e_cn",
    "X-Rpc-Channel": "mihoyo",
    "X-Rpc-Client_type": "16",
    "X-Rpc-Combo_token": token,
    "X-Rpc-Cps": "pc_mihoyo",
    "X-Rpc-Device_id": "8e3ee7ea-d701-41f1-8e02-e5bc1396e365",
    "X-Rpc-Device_model": "Unknown",
    "X-Rpc-Device_name": "Unknown",
    "X-Rpc-Language": "zh-cn",
    "X-Rpc-Op_biz": "clgm_cn",
    "X-Rpc-Sys_version": "windows 10",
    "X-Rpc-Vendor_id": "2"
}

print("正在获取游戏数据...")
response = requests.get(url, headers=headers)
response.encoding = "utf-8"
data = json.loads(response.text)
print("获取到的游戏数据：", data)

if data["retcode"] != 0:
    c = "签到失败"
    t = "获取失败"
    print("签到失败")
else:
    coin = data["data"]["coin"]["coin_num"]
    time = data["data"]["free_time"]["free_time"]
    c = f"签到成功"
    t = time + "分钟"
    print(f"签到成功，获取到的时间: {time}分钟")

access_token = get_access_token()
send(access_token, t, c)
