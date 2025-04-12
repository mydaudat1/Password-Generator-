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
        /* Import custom font từ file font.ttf trong thư mục static */
        @font-face {
            font-family: 'CustomFont';
            src: url("/static/font.ttf") format("truetype");
            font-weight: normal;
            font-style: normal;
        }
        body {
            font-family: 'CustomFont', Arial, sans-serif;
            background: #FFDFC4; /* Màu da nhạt */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            background: white;
        }
        .btn {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 12px 28px;
            text-align: center;
            font-size: 16px;
            margin: 20px 0;
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
    <div class="container">
        <h2>Random Password Generator</h2>
        <label for="length">Length:</label>
        <input type="number" id="length" min="4" max="64" value="12">
        <br>
        <button class="btn" onclick="generatePassword()">Generate</button>
        <div id="password"></div>
    </div>

    <script>
        function generatePassword() {
            const length = document.getElementById('length').value;
            fetch('/generate?length=' + length)
                .then(response => response.json())
                .then(data => {
                    const text = data.password;
                    const passwordDiv = document.getElementById('password');
                    passwordDiv.style.opacity = 0;
                    passwordDiv.innerText = '';

                    // Sau 500ms bắt đầu hiệu ứng gõ từng ký tự
                    setTimeout(() => {
                        let index = 0;
                        const interval = setInterval(() => {
                            passwordDiv.innerText += text[index];
                            index++;
                            if (index >= text.length) {
                                clearInterval(interval);
                            }
                        }, 5000 / text.length);  // hiệu ứng typing trải đều trong 5 giây
                        passwordDiv.style.opacity = 1;
                    }, 500);
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