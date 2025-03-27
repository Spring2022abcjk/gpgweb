from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import secrets
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend
import sys
from key_format import format_public_key, convert_public_key

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# 生成密钥对（公钥和私钥）
def generate_key(key_size: int, key_type: str = 'rsa') -> tuple:
    """
    生成密钥对（公钥和私钥）
# 
    参数:
    key_size (int): 密钥大小
    key_type (str): 密钥类型（'rsa' 或 'ecdsa'）

    返回:
    tuple: 密钥对象、私钥PEM和公钥（格式取决于密钥类型）
    """
    if key_type == 'rsa':
        # 生成RSA私钥
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
    elif key_type == 'ecdsa':
        # 生成ECDSA私钥
        key = ec.generate_private_key(
            curve=ec.SECP256R1(),
            backend=default_backend()
        )
    else:
        raise ValueError("Unsupported key type. Use 'rsa' or 'ecdsa'.")
    
    # 将私钥序列化为PEM格式
    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 返回密钥对象、私钥和默认公钥（不处理格式转换）
    return key, private_pem

# 生成密钥对并返回给前端
@app.route('/generate-key', methods=['POST'])
def generate_key_route():
    """
    生成密钥对并返回给前端

    返回:
    Response: JSON格式的私钥和公钥
    """
    data = request.get_json()
    key_size = int(data.get('keyCode', 2048))
    key_type = data.get('keyType', 'rsa')
    public_key_format = data.get('publicKeyFormat', 'openssh')
    
    # 生成密钥对
    key, private_pem = generate_key(key_size, key_type)
    
    # 根据请求的格式生成公钥
    public_key = format_public_key(key, public_key_format)
    
    response = {
        'privateKey': private_pem.decode('utf-8'),
        'publicKey': public_key.decode('utf-8')
    }
    return jsonify(response)

# 渲染主页面
@app.route('/')
def index():
    """
    渲染主页面

    返回:
    str: 渲染后的HTML页面
    """
    return render_template('index.html')

if __name__ == '__main__':
    port = input("请输入要在哪个端口上运行（默认3050）：") or 3050
    port = int(port)
    
    debug_input = input("是否开启Debug模式？输入'T'为开启，'F'为关闭（默认关闭）：") or 'F'
    debug = debug_input.upper() == 'T'
    
    app.run(debug=debug, port=port)