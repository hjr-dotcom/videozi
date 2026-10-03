import streamlit as st
from google import genai

st.set_page_config(page_title="Meu Estúdio Pessoal", layout="centered")
st.title("⚡ Estúdio Pessoal com Gemini")

# Configuração da chave de API via Streamlit Secrets ou input lateral
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Cole sua Gemini API Key:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    prompt = st.text_area("O que você deseja criar ou consultar?", height=120)
    
    if st.button("Executar na Nuvem", type="primary"):
        if prompt:
            with st.spinner("Processando nos servidores do Google..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                    st.markdown("### Resposta:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
        else:
            st.warning("Por favor, insira um comando ou prompt.")
else:
    st.info("Insira sua chave de API do Google AI Studio para continuar.")