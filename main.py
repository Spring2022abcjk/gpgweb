from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import secrets
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend
import sys

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# 生成密钥对（公钥和私钥）
def generate_key(key_size: int, key_type: str = 'rsa') -> tuple:
    """
    生成密钥对（公钥和私钥）

    参数:
    key_size (int): 密钥大小
    key_type (str): 密钥类型（'rsa' 或 'ecdsa'）

    返回:
    tuple: 私钥和公钥
    """
    if key_type == 'rsa':
        # 生成RSA私钥
        key = rsa.generate_private_key(
            public_exponent=65537,  # 公共指数，通常使用65537
            key_size=key_size,  # 密钥大小（以位为单位，例如2048或4096）
            backend=default_backend()  # 使用默认的加密后端
        )
        
        # 将私钥序列化为PEM格式
        private_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,  # 编码格式为PEM
            format=serialization.PrivateFormat.TraditionalOpenSSL,  # 私钥格式为传统的OpenSSL格式
            encryption_algorithm=serialization.NoEncryption()  # 不加密私钥
        )

        # 将公钥序列化为OpenSSH格式
        public_key = key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,  # 编码格式为OpenSSH
            format=serialization.PublicFormat.OpenSSH  # 公钥格式为OpenSSH
        )
    elif key_type == 'ecdsa':
        # 生成ECDSA私钥
        key = ec.generate_private_key(
            curve=ec.SECP256R1(),  # 使用SECP256R1曲线
            backend=default_backend()  # 使用默认的加密后端
        )
        
        # 将私钥序列化为PEM格式
        private_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,  # 编码格式为PEM
            format=serialization.PrivateFormat.TraditionalOpenSSL,  # 私钥格式为传统的OpenSSL格式
            encryption_algorithm=serialization.NoEncryption()  # 不加密私钥
        )

        # 将公钥序列化为PEM格式
        public_key = key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,  # 编码格式为PEM
            format=serialization.PublicFormat.SubjectPublicKeyInfo  # 公钥格式为SubjectPublicKeyInfo
        )
    else:
        raise ValueError("Unsupported key type. Use 'rsa' or 'ecdsa'.")
    
    # 返回私钥和公钥的字节串
    return key, private_pem, public_key

def convert_public_key_to_pem(public_key: bytes) -> bytes:
    """
    将公钥转换为PEM格式

    参数:
    public_key (bytes): 公钥的字节串

    返回:
    bytes: PEM格式的公钥
    """
    key = serialization.load_ssh_public_key(public_key, backend=default_backend())
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem

# 生成密钥对并返回给前端
@app.route('/generate-key', methods=['POST'])
def generate_key_route():
    """
    生成密钥对并返回给前端

    返回:
    Response: JSON格式的私钥和公钥
    """
    data = request.get_json()
    key_size = int(data.get('keyCode', 2048))  # 默认值为2048
    key_type = data.get('keyType', 'rsa')  # 默认值为'rsa'
    key, private_pem, public_key = generate_key(key_size, key_type)
    
    public_key_format = data.get('publicKeyFormat', 'openssh')
    if public_key_format == 'pem':
        public_key = convert_public_key_to_pem(public_key)
    
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