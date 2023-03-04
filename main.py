from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api', methods=['POST'])
def handle_request():
    data = request.json
    name = data['key1']
    print(data)
    print(name)
    # İstek verilerini işleyin
    return name


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
