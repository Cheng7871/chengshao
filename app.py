from flask import Flask,request
app = Flask(__name__)
@app.route('/')
def index():
ip = request.remote_addr
return f"访客IP:{ip}"
if name == '__main__':
app.run()
