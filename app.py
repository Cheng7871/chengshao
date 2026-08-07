from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    visitor_ip = request.headers.get("X-Forwarded-For",request.remote_addr)
    with open("index.html","r",encoding="utf-8")as file:
        html_content = file.read()
    html_content = html_content.replace("{{ip}}",visitor_ip)
    return html_content

if __name__=="__main__":
    app.run(host="0.0.0.0")
