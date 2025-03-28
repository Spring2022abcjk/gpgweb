// filepath: gpgweb/static/script.js
// 获取页面元素
const form = document.getElementById('key-form');
const keyTypeSelect = document.getElementById('key-type');
const keyCodeSelect = document.getElementById('key-size');
const publicKeyFormatSelect = document.getElementById('public-key-format');  // 新增公钥格式选择
const generateKeyButton = document.getElementById('generate-key');
const publicKeyInput = document.getElementById('public-key');
const privateKeyInput = document.getElementById('private-key');

// 添加事件监听器
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const keyType = keyTypeSelect.value;
    const keyCode = keyCodeSelect.value;
    const publicKeyFormat = publicKeyFormatSelect.value;  // 获取公钥格式

    // 发送请求生成密钥
    fetch('/generate-key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            keyType,
            keyCode: parseInt(keyCode),  // 确保 keyCode 作为整数传递
            publicKeyFormat  // 传递公钥格式
        })
    })
    .then((response) => response.json())
    .then((data) => {
        // 显示生成的密钥
        const publicKey = data.publicKey;
        const privateKey = data.privateKey;

        alert(`注意保存好你的密钥对`);
        publicKeyInput.value = publicKey;
        privateKeyInput.value = privateKey;  // 确保私钥输入框的值被正确设置
    })
    .catch((error) => console.error(error));
});