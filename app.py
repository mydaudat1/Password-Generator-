from flask import Flask, render_template_string, request, jsonify
import random
import string
import re

app = Flask(__name__)

template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ 'Password Generator' if lang == 'en' else 'Trình tạo mật khẩu' }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: var(--bg);
            color: var(--fg);
            text-align: center;
            padding: 50px 20px;
            margin: 0;
        }
        h2 { font-size: 28px; margin-bottom: 20px; }
        .btn {
            background-color: #007BFF;
            border: none;
            color: white;
            padding: 12px 28px;
            margin: 10px;
            font-size: 16px;
            border-radius: 12px;
            cursor: pointer;
        }
        .btn:hover { background-color: #0056b3; }
        #password {
            font-size: 20px;
            margin-top: 10px;
            word-wrap: break-word;
        }
        .slider-container {
            width: 300px;
            margin: auto;
        }
        input[type=range] {
            width: 100%;
        }
        .options label {
            display: block;
        }
        :root {
            --bg: #ffffff;
            --fg: #000000;
        }
        body.dark-mode {
            --bg: #121212;
            --fg: #f0f0f0;
        }
    </style>
</head>
<body class="{{ 'dark-mode' if dark else '' }}">
    <h2>{{ 'Random Password Generator' if lang == 'en' else 'Trình tạo mật khẩu ngẫu nhiên' }}</h2>
    <div class="slider-container">
        <label>{{ 'Length' if lang == 'en' else 'Độ dài' }}: <span id="lengthLabel">12</span></label>
        <input type="range" min="4" max="64" value="12" id="length" oninput="updateLengthLabel()">
    </div>
    <div class="options">
        <label><input type="checkbox" id="useLetters" checked> {{ 'Letters' if lang == 'en' else 'Chữ cái' }}</label>
        <label><input type="checkbox" id="useDigits" checked> {{ 'Digits' if lang == 'en' else 'Số' }}</label>
        <label><input type="checkbox" id="useSymbols"> {{ 'Symbols' if lang == 'en' else 'Ký tự đặc biệt' }}</label>
        <label><input type="checkbox" id="useEmoji"> {{ 'Emoji & Symbol' if lang == 'en' else 'Biểu tượng & Emoji' }}</label>
    </div>
    <button class="btn" onclick="generatePassword()">{{ 'Generate' if lang == 'en' else 'Tạo' }}</button>
    <div id="password"></div>
    <div id="strength"></div>
    <button id="copyBtn" class="btn" style="display:none" onclick="copyPassword()">{{ 'Copy' if lang == 'en' else 'Sao chép' }}</button>
    <script>
        const updateLengthLabel = () => {
            document.getElementById('lengthLabel').innerText = document.getElementById('length').value;
        };

        function generatePassword() {
            const length = document.getElementById('length').value;
            const letters = document.getElementById('useLetters').checked;
            const digits = document.getElementById('useDigits').checked;
            const symbols = document.getElementById('useSymbols').checked;
            const emoji = document.getElementById('useEmoji').checked;

            fetch(`/generate?length=${length}&letters=${letters}&digits=${digits}&symbols=${symbols}&emoji=${emoji}`)
                .then(r => r.json())
                .then(data => {
                    const pw = data.password;
                    document.getElementById('password').innerText = pw;
                    document.getElementById('strength').innerText = `{{ 'Strength' if lang == 'en' else 'Độ mạnh' }}: ` + data.strength;
                    document.getElementById('copyBtn').style.display = 'inline-block';
                });
        }

        function copyPassword() {
            navigator.clipboard.writeText(document.getElementById('password').innerText)
                .then(() => {
                    const btn = document.getElementById('copyBtn');
                    btn.innerText = "{{ 'Copied!' if lang == 'en' else 'Đã sao chép!' }}";
                    setTimeout(() => btn.innerText = "{{ 'Copy' if lang == 'en' else 'Sao chép' }}", 1500);
                });
        }
    </script>
</body>
</html>
'''

EMOJI = ['😀', '😂', '✨', '❤️', '🔥', '🌟', '🎉', '🥳', '🧠', '💡']

@app.route('/')
def home():
    lang = request.args.get('lang', 'en')
    dark = request.args.get('dark', 'false').lower() == 'true'
    return render_template_string(template, lang=lang, dark=dark)

def calculate_strength(pw):
    score = 0
    if len(pw) >= 8: score += 1
    if re.search(r"[a-z]", pw) and re.search(r"[A-Z]", pw): score += 1
    if re.search(r"[0-9]", pw): score += 1
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\\\"|,.<>/?]", pw): score += 1
    if any(char in EMOJI for char in pw): score += 1
    levels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
    return levels[score] if score < len(levels) else levels[-1]

@app.route('/generate')
def generate():
    length = request.args.get('length', default=12, type=int)
    use_letters = request.args.get('letters', 'true') == 'true'
    use_digits = request.args.get('digits', 'true') == 'true'
    use_symbols = request.args.get('symbols', 'false') == 'true'
    use_emoji = request.args.get('emoji', 'false') == 'true'

    chars = ''
    if use_letters:
        chars += string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    if use_emoji:
        chars += ''.join(EMOJI)

    if not chars:
        return jsonify({'password': '', 'strength': 'None'})

    pw = ''.join(random.choices(chars, k=length))
    strength = calculate_strength(pw)
    return jsonify({'password': pw, 'strength': strength})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
