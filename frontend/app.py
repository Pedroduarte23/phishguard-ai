import streamlit as st
import requests

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
        r = requests.post(
            "http://127.0.0.1:5000/register",
            json={"username": user, "password": senha}
        )

        st.write(r.json())

# -------------------
# LOGIN
# -------------------
elif choice == "Login":
    st.subheader("Login")

    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        r = requests.post(
            "http://127.0.0.1:5000/login",
            json={"username": user, "password": senha}
        )

        if r.status_code == 200:
            token = r.json()["token"]
            st.session_state.token = token
            st.session_state.logado = True
            st.success("Login realizado!")
        else:
            st.error("Erro no login")

# -------------------
# SISTEMA PROTEGIDO
# -------------------
if "logado" in st.session_state and st.session_state.logado:
    st.subheader("Analisar URL")

    url = st.text_input("Digite a URL")

    if st.button("Analisar"):
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        r = requests.post(
            "http://127.0.0.1:5000/analisar",
            json={"url": url},
            headers=headers
        )

        st.write(r.json())