from flask import Flask, request, jsonify
from core.modelo import prever
from backend.database import conectar, criar_tabelas

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "phishguard-secret"

jwt = JWTManager(app)

criar_tabelas()


@app.route("/register", methods=["POST"])
def register():
    data = request.json

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (data["username"], data["password"])
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "Usuário criado"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )

    user = cursor.fetchone()

    if user:
        token = create_access_token(identity=data["username"])
        return jsonify({"token": token})
    else:
        return jsonify({"erro": "Credenciais inválidas"}), 401


@app.route("/analisar", methods=["POST"])
@jwt_required()
def analisar():
    user = get_jwt_identity()
    url = request.json["url"]

    resultado = prever(url)

    return jsonify({
        "user": user,
        "url": url,
        "resultado": resultado
    })


if __name__ == "__main__":
    import os

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)