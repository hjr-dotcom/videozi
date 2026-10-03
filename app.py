import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

st.set_page_config(page_title="Meu Estúdio Pessoal", layout="centered")
st.title("⚡ Estúdio Pessoal com Gemini (Multimídia)")

# Configuração da chave de API via Streamlit Secrets ou input lateral
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Cole sua Gemini API Key:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    # Seletor de modo para escolher entre Texto/Roteiro e Geração de Imagem
    modo = st.radio("Escolha o que deseja criar:", ["Texto / Roteiros", "Gerar Imagem"], horizontal=True)
    
    prompt = st.text_area("Descreva o seu pedido ou prompt:", height=120)
    
    if st.button("Executar na Nuvem", type="primary"):
        if prompt:
            with st.spinner("Processando nos servidores do Google..."):
                try:
                    if modo == "Texto / Roteiros":
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt,
                        )
                        st.markdown("### Resposta:")
                        st.markdown(response.text)
                    else:
                        # Geração de imagem com o modelo Gemini 2.5 Flash Image
                        response = client.models.generate_content(
                            model="gemini-2.5-flash-image",
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                response_modalities=["IMAGE"],
                            ),
                        )
                        
                        st.markdown("### Imagem Gerada:")
                        image_found = False
                        for part in response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                image = Image.open(io.BytesIO(part.inline_data.data))
                                st.image(image, caption=prompt, use_container_width=True)
                                image_found = True
                        if not image_found:
                            st.warning("O modelo não retornou uma imagem para este prompt.")
                            
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
        else:
            st.warning("Por favor, insira um comando ou prompt.")
else:
    st.info("Insira sua chave de API do Google AI Studio para continuar.")
