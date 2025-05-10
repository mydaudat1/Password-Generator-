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
            font-family: 'MyCustomFont';
            src: url('/static/font.ttf') format('truetype');
            font-weight: normal;
            font-style: normal;
        }

        body {
            font-family: 'MyCustomFont', sans-serif;
            background-color: white;
            color: #333;
            margin: 0;
            padding: 0;
        }

        .container {
            display: flex;
            min-height: 100vh;
            align-items: center;
            justify-content: center;
            flex-direction: row;
            padding: 40px;
        }

        .left, .right {
            flex: 1;
            padding: 20px;
        }

        .left img {
            max-width: 100%;
            height: auto;
        }

        .right h2 {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .config-section {
            margin-top: 20px;
            border-top: 1px solid #ccc;
            padding-top: 20px;
        }

        .slider-label {
            display: block;
            margin-bottom: 5px;
        }

        input[type="range"] {
            width: 100%;
        }

        .checkboxes label {
            display: block;
            margin: 5px 0;
        }

        .btn {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 12px;
            cursor: pointer;
            margin-top: 10px;
        }

        .btn:hover {
            background-color: #0b7dda;
        }

        #password {
            font-size: 20px;
            margin-top: 20px;
            padding: 10px;
            border-radius: 10px;
            background-color: #eee;
        }

        .strength {
            font-weight: bold;
            margin-top: 10px;
        }

        .weak {
            color: red;
        }
        .medium {
            color: orange;
        }
        .strong {
            color: green;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <img src="/static/art.png" alt="Art">
        </div>
        <div class="right">
            <h2>Random Password Generator</h2>
            <button class="btn" onclick="generatePassword()">Generate</button>
            <div id="password"></div>
            <div id="strength" class="strength"></div>

            <div class="config-section">
                <label class="slider-label" for="length">Length: <span id="lengthValue">12</span></label>
                <input type="range" id="length" min="4" max="64" value="12" oninput="updateLength(this.value)">
                <div class="checkboxes">
                    <label><input type="checkbox" id="useLetters" checked> Letters</label>
                    <label><input type="checkbox" id="useNumbers" checked> Numbers</label>
                    <label><input type="checkbox" id="useSymbols"> Symbols</label>
                    <label><input type="checkbox" id="useEmoji"> Emojis</label>
                </div>
            </div>
        </div>
    </div>
    <script>
        function updateLength(val) {
            document.getElementById('lengthValue').innerText = val;
        }

        function getStrength(password) {
            let strength = 0;
            if (password.length >= 8) strength++;
            if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[^a-zA-Z0-9]/.test(password)) strength++;
            return strength;
        }

        function generatePassword() {
            const length = document.getElementById('length').value;
            const useLetters = document.getElementById('useLetters').checked;
            const useNumbers = document.getElementById('useNumbers').checked;
            const useSymbols = document.getElementById('useSymbols').checked;
            const useEmoji = document.getElementById('useEmoji').checked;

            const query = `length=${length}&letters=${useLetters}&numbers=${useNumbers}&symbols=${useSymbols}&emoji=${useEmoji}`;
            fetch('/generate?' + query)
                .then(response => response.json())
                .then(data => {
                    const password = data.password;
                    const strength = getStrength(password);
                    document.getElementById('password').innerText = password;
                    const strengthDiv = document.getElementById('strength');
                    if (strength <= 1) {
                        strengthDiv.innerText = 'Weak';
                        strengthDiv.className = 'strength weak';
                    } else if (strength == 2 || strength == 3) {
                        strengthDiv.innerText = 'Medium';
                        strengthDiv.className = 'strength medium';
                    } else {
                        strengthDiv.innerText = 'Strong';
                        strengthDiv.className = 'strength strong';
                    }
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
    use_letters = request.args.get('letters', default='true') == 'true'
    use_numbers = request.args.get('numbers', default='true') == 'true'
    use_symbols = request.args.get('symbols', default='false') == 'true'
    use_emoji = request.args.get('emoji', default='false') == 'true'

    chars = ''
    if use_letters:
        chars += string.ascii_letters
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    if use_emoji:
        chars += '😀😁😂🤣😃😄😅😆😉😊😋😎😍😘'  # ví dụ một số emoji phổ biến

    if not chars:
        return jsonify({'password': ''})

    password = ''.join(random.choices(chars, k=length))
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
