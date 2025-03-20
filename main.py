from flask import Flask, request, jsonify
from flask_cors import CORS
import secrets
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
CORS(app)

# 生成密钥对（公钥和私钥）
def generate_key(key_size):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    return private_pem, public_key

# 生成密钥对并返回给前端
@app.route('/generate-key', methods=['POST'])
def generate_key_route():
    data = request.get_json()
    key_size = int(data.get('keyCode', 2048))  # 默认值为2048
    private_pem, public_key = generate_key(key_size)
    response = {
        'privateKey': private_pem.decode('utf-8'),
        'publicKey': public_key.decode('utf-8')
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=3050)
