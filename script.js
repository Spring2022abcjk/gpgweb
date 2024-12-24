// 获取页面元素
const form = document.getElementById('key-form');
const keyTypeSelect = document.getElementById('key-type');
const keyCodeSelect = document.getElementById('key-size');
const generateKeyButton = document.getElementById('generate-key');
const publicKeyInput = document.getElementById('public-key');
const privateKeyInput = document.getElementById('private-key');

// 添加事件监听器
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const keyType = keyTypeSelect.value;
    const keyCode = keyCodeSelect.value;

    // 发送请求生成密钥
    fetch('http://localhost:3050/generate-key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            keyType,
            keyCode
        })
    })
    .then((response) => response.json())
    .then((data) => {
        // 显示生成的密钥
        const publicKey = data.publicKey;
        const privateKey = data.privateKey;

        alert(`注意保存好你的密钥对`);
        publicKeyInput.value = publicKey;
        privateKeyInput.value = privateKey;
    })
    .catch((error) => console.error(error));
});