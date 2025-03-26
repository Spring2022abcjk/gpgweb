# GPG Web **应用程序**

这个项目是一个用于生成使用 RSA 加密的 GPG 密钥的 Web 应用程序。它提供了一个用户友好的界面，供用户选择密钥类型和大小，并生成相应的公钥和私钥。

## 项目结构

```
gpgweb
├── static
│   ├── styles.css       # Web 应用程序的 CSS 样式
│   └── script.js        # 处理用户交互的 JavaScript 代码
├── templates
│   └── index.html       # Web 应用程序的主 HTML 文件
├── main.py              # 应用程序的入口点
└── README.md            # 项目的文档
```

## 设置说明

1. **克隆仓库**：
   ```
   git clone <repository-url>
   cd gpgweb
   ```

2. **安装依赖**：
   确保已安装 Python，然后安装所需的包：
   ```
   pip install Flask flask-cors cryptography
   ```

3. **运行应用程序**：
   通过运行以下命令启动 Flask 应用程序：
   ```
   python main.py
   ```

4. **访问应用程序**：
   打开您的 Web 浏览器并访问 `http://localhost:5000` 以访问 GPG 密钥生成界面。

## 使用方法

1. 选择密钥类型（目前仅支持 RSA）。
2. 选择所需的密钥大小（选项为 1024、2048 或 4096 位）。
3. 点击“生成密钥”按钮生成密钥。
4. 生成的公钥和私钥将显示在输入字段中。请确保安全保存它们。

## 许可证

该项目根据 MIT 许可证授权。有关详细信息，请参阅 LICENSE 文件。