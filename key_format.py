from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def format_public_key(key, format_type='openssh'):
    """
    将公钥对象格式化为指定格式
    
    参数:
    key: 公钥对象或包含公钥的私钥对象
    format_type: 'openssh' 或 'pem'
    
    返回:
    bytes: 指定格式的公钥
    """
    # 如果输入是私钥，先获取公钥
    if hasattr(key, 'public_key'):
        public_key = key.public_key()
    else:
        public_key = key
    
    if format_type == 'openssh':
        try:
            # 尝试使用OpenSSH格式（适用于RSA）
            return public_key.public_bytes(
                encoding=serialization.Encoding.OpenSSH,
                format=serialization.PublicFormat.OpenSSH
            )
        except ValueError:
            # 某些密钥类型（如ECDSA）可能不支持OpenSSH格式
            # 在这种情况下，回退到PEM格式
            return format_public_key(public_key, 'pem')
    
    elif format_type == 'pem':
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    else:
        raise ValueError(f"Unsupported format type: {format_type}")

def convert_public_key(public_key_bytes, input_format='openssh', output_format='pem'):
    """
    将一种格式的公钥转换为另一种格式
    
    参数:
    public_key_bytes: 公钥字节串
    input_format: 输入公钥的格式 ('openssh' 或 'pem')
    output_format: 输出公钥的格式 ('openssh' 或 'pem')
    
    返回:
    bytes: 转换后格式的公钥
    """
    # 根据输入格式加载公钥
    if input_format == 'openssh':
        key = serialization.load_ssh_public_key(public_key_bytes, backend=default_backend())
    elif input_format == 'pem':
        key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
    else:
        raise ValueError(f"Unsupported input format: {input_format}")
    
    # 格式化为目标格式
    return format_public_key(key, output_format)