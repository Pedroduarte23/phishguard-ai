import streamlit as st
import requests

API_URL = "https://phishguard-api-xk0e.onrender.com"

st.title("🔐 PhishGuard AI")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)


if choice == "Register":
    st.subheader("Criar conta")

    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        r = requests.post(
            f"{API_URL}/register",
            json={"username": user, "password": senha}
        )

        st.write(r.json())


elif choice == "Login":
    st.subheader("Login")

    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        r = requests.post(
            f"{API_URL}/login",
            json={"username": user, "password": senha}
        )

        if r.status_code == 200:
            token = r.json()["token"]
            st.session_state.token = token
            st.session_state.logado = True
            st.success("Login realizado!")
        else:
            st.error("Erro no login")


if "logado" in st.session_state and st.session_state.logado:
    st.subheader("Analisar URL")

    url = st.text_input("Digite a URL")

    if st.button("Analisar"):
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        r = requests.post(
            f"{API_URL}/analisar",
            json={"url": url},
            headers=headers
        )

        st.write(r.json())