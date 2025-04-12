from flask import Flask, render_template_string, request, jsonify
import random
import string

app = Flask(__name__)

template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Password Generator</title>
    <style>
        @font-face {
            font-family: 'CustomFont';
            src: url("/static/font.ttf") format("truetype");
            font-weight: normal;
            font-style: normal;
        }
        body {
            font-family: 'CustomFont', Arial, sans-serif;
            background: #FFDFC4;
            text-align: center;
            padding: 100px 20px;
            margin: 0;
        }
        h2 {
            font-size: 28px;
            margin-bottom: 20px;
        }
        .btn {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 12px 28px;
            text-align: center;
            font-size: 16px;
            margin: 10px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background-color: #45a049;
        }
        #password {
            font-size: 20px;
            margin-top: 10px;
            min-height: 30px;
            opacity: 0;
            transition: opacity 1s ease-in-out;
            word-wrap: break-word;
            max-width: 90%;
            margin-left: auto;
            margin-right: auto;
        }
        #copyBtn {
            display: none;
            background-color: #2196F3;
        }
        #copyBtn:hover {
            background-color: #0b7dda;
        }
        input[type="number"] {
            padding: 10px;
            border-radius: 12px;
            border: 1px solid #ccc;
            font-size: 16px;
            width: 80px;
        }
    </style>
</head>
<body>
    <h2>Random Password Generator</h2>
    <label for="length">Length:</label>
    <input type="number" id="length" min="4" max="64" value="12">
    <br>
    <button class="btn" onclick="generatePassword()">Generate</button>
    <div id="password"></div>
    <button id="copyBtn" class="btn" onclick="copyPassword()">Copy password</button>

    <script>
        function generatePassword() {
            const length = document.getElementById('length').value;
            fetch('/generate?length=' + length)
                .then(response => response.json())
                .then(data => {
                    const text = data.password;
                    const passwordDiv = document.getElementById('password');
                    const copyBtn = document.getElementById('copyBtn');

                    passwordDiv.style.opacity = 0;
                    passwordDiv.innerText = '';
                    copyBtn.style.display = 'none';

                    setTimeout(() => {
                        let index = 0;
                        const interval = setInterval(() => {
                            passwordDiv.innerText += text[index];
                            index++;
                            if (index >= text.length) {
                                clearInterval(interval);
                                copyBtn.style.display = 'inline-block';
                            }
                        }, 5000 / text.length);
                        passwordDiv.style.opacity = 1;
                    }, 500);
                });
        }

        function copyPassword() {
            const passwordText = document.getElementById('password').innerText;
            navigator.clipboard.writeText(passwordText).then(() => {
                const btn = document.getElementById('copyBtn');
                btn.innerText = "Copied!";
                setTimeout(() => btn.innerText = "Copy password", 1500);
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(template)

@app.route('/generate')
def generate():
    length = request.args.get('length', default=12, type=int)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(chars, k=length))
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
