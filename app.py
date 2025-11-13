from flask import Flask, jsonify, request, render_template_string, redirect, url_for
import requests

app = Flask(__name__)

POCKETBASE_API = "http://localhost:8090/api/collections"
POCKETBASE_RECORD_API = "http://localhost:8090/api/collections/demo/records"
POCKETBASE_AUTH_API = "http://localhost:8090/api/admins/auth-with-password"
SUPERUSER_EMAIL = "filippalyza@proton.me"
SUPERUSER_PASS = "FilipHeslo"


# HTML šablona s formulářem
FORM_HTML = '''
<html>
<head>
<title>PocketBase Demo Form</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: linear-gradient(120deg, #e3f2fd 0%, #fce4ec 100%);
    margin: 0; padding: 0;
}
.container {
    max-width: 420px;
    margin: 48px auto;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 24px #0002;
    padding: 40px 32px 32px 32px;
    animation: fadein 0.7s;
}
@keyframes fadein {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: none; }
}
h2 {
    text-align: center;
    color: #1976d2;
    margin-bottom: 24px;
}
form {
    display: flex;
    flex-direction: column;
    gap: 18px;
}
label {
    color: #37474f;
    font-weight: 500;
    margin-bottom: 4px;
}
input, textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #b0bec5;
    border-radius: 7px;
    font-size: 1em;
    background: #f7fbff;
    transition: border 0.2s;
}
input:focus, textarea:focus {
    border-color: #1976d2;
    outline: none;
}
button {
    background: linear-gradient(90deg, #1976d2 60%, #ec407a 100%);
    color: #fff;
    border: none;
    padding: 12px 0;
    border-radius: 7px;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 2px 8px #1976d233;
    transition: background 0.2s, box-shadow 0.2s;
}
button:hover {
    background: linear-gradient(90deg, #1565c0 60%, #d81b60 100%);
    box-shadow: 0 4px 16px #1976d233;
}
.link {
    display: block;
    text-align: center;
    margin-top: 22px;
    color: #1976d2;
    text-decoration: none;
    font-weight: 500;
    letter-spacing: 0.5px;
}
.link:hover {
    text-decoration: underline;
}
@media (max-width: 600px) {
    .container { padding: 18px 8px; }
}
</style>
</head>
<body>
<div class="container">
<h2>Demo formulář pro PocketBase</h2>
<form method="post" action="/submit">
        <label>Jméno:<br><input type="text" name="name" required></label>
        <label>Email:<br><input type="email" name="email" required></label>
        <label>Zpráva:<br><textarea name="message" rows="4" required></textarea></label>
        <button type="submit">Odeslat</button>
</form>
<a class="link" href="/collections">Zobrazit kolekce</a>
</div>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(FORM_HTML)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    # Odeslání dat do PocketBase (kolekce 'demo') bez tokenu
    data = {"name": name, "email": email, "message": message}
    resp = requests.post(POCKETBASE_RECORD_API, json=data)
    if resp.status_code == 200:
        return redirect(url_for("index"))
    return f"Chyba při odesílání: {resp.text}", 400

@app.route("/collections")
def collections():
    resp = requests.get(POCKETBASE_API)
    if resp.status_code == 200:
        return jsonify(resp.json())
    return jsonify({"error": "Could not fetch collections"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
