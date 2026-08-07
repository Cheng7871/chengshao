from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return f"访客IP：{real_ip}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
