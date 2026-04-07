import streamlit as st
import requests

# URL do backend
API_URL = "https://phishguard-api-xk0e.onrender.com"

st.title("🔐 PhishGuard AI")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------
# REGISTER
# -------------------
if choice == "Register":
    st.subheader("Criar conta")

    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        with st.spinner("Criando conta..."):
            try:
                r = requests.post(
                    f"{API_URL}/register",
                    json={"username": user, "password": senha},
                    timeout=30
                )
                st.write(r.json())
            except:
                st.error("Erro ao conectar com o servidor")

# -------------------
# LOGIN
# -------------------
elif choice == "Login":
    st.subheader("Login")

    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        with st.spinner("Entrando..."):
            try:
                r = requests.post(
                    f"{API_URL}/login",
                    json={"username": user, "password": senha},
                    timeout=30
                )

                if r.status_code == 200:
                    token = r.json()["token"]
                    st.session_state.token = token
                    st.session_state.logado = True
                    st.success("Login realizado!")
                else:
                    st.error("Erro no login")
            except:
                st.error("Servidor demorou para responder")

# -------------------
# SISTEMA PROTEGIDO
# -------------------
if "logado" in st.session_state and st.session_state.logado:
    st.subheader("Analisar URL")

    url = st.text_input("Digite a URL")

    if st.button("Analisar"):
        with st.spinner("Analisando..."):
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state.token}"
                }

                r = requests.post(
                    f"{API_URL}/analisar",
                    json={"url": url},
                    headers=headers,
                    timeout=30
                )

                st.write(r.json())
            except:
                st.error("Erro ao analisar")