#!/usr/bin/env python3
"""
Camunda Migration Assistant - Interface Streamlit
==================================================
Interface web moderna para o assistente de migração Camunda 7 → 8
"""

import os
import time
from pathlib import Path
import streamlit as st
import google.generativeai as genai

# Importa configurações
try:
    from config import GOOGLE_API_KEY, MODEL_NAME, GENERATION_CONFIG
except ImportError:
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    MODEL_NAME = "gemini-2.5-pro"
    GENERATION_CONFIG = {
        'temperature': 0.2,
        'top_p': 0.95,
        'top_k': 40,
        'max_output_tokens': 8192,
    }

# Configuração da página
st.set_page_config(
    page_title="Assistente Migração Camunda 7 → 8",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
    }
    .upload-status {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .doc-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        margin: 0.2rem;
        background-color: #e8f4f8;
        border-radius: 15px;
        font-size: 0.85rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CamundaChatbot:
    """Wrapper do chatbot para Streamlit"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.uploaded_files = []
        self.docs_path = Path(__file__).parent / "documentação_migracao_camunda"
        self.model = None
        
    def upload_documentation(self, progress_callback=None):
        """Upload dos PDFs com callback de progresso"""
        pdf_files = list(self.docs_path.glob("*.pdf"))
        
        if not pdf_files:
            return False, "Nenhum PDF encontrado"
        
        for i, pdf_file in enumerate(pdf_files):
            try:
                if progress_callback:
                    progress_callback(i + 1, len(pdf_files), pdf_file.name)
                
                uploaded_file = genai.upload_file(
                    path=str(pdf_file),
                    display_name=pdf_file.stem
                )
                
                # Aguarda processamento
                while uploaded_file.state.name == 'PROCESSING':
                    time.sleep(1)
                    uploaded_file = genai.get_file(uploaded_file.name)
                
                if uploaded_file.state.name != 'FAILED':
                    self.uploaded_files.append(uploaded_file)
                    
            except Exception as e:
                st.error(f"Erro ao processar {pdf_file.name}: {str(e)}")
        
        return len(self.uploaded_files) > 0, f"{len(self.uploaded_files)} documentos carregados"
    
    def get_system_prompt(self):
        """Prompt otimizado do sistema"""
        return """Você é um assistente especializado em migração do Camunda 7 para o Camunda 8.

SUAS RESPONSABILIDADES:
1. Fornecer respostas EXTREMAMENTE DETALHADAS, PRECISAS e DIDÁTICAS
2. Ser paciente e explicativo
3. Usar exemplos práticos sempre que possível
4. Citar as fontes da documentação oficial

DIRETRIZES:
- Seja COMPLETO e DIDÁTICO
- Inclua exemplos de código quando aplicável
- Organize as informações claramente
- Mencione diagramas ou imagens relevantes
- Use formatação Markdown para melhor legibilidade

IMPORTANTE:
- Base-se EXCLUSIVAMENTE na documentação fornecida
- Se não souber, seja honesto
- Priorize precisão técnica"""

    def ask(self, question: str):
        """Faz uma pergunta ao chatbot"""
        if not self.uploaded_files:
            return "⚠️ Documentação não carregada. Por favor, reinicie a aplicação."
        
        try:
            if not self.model:
                self.model = genai.GenerativeModel(
                    model_name=MODEL_NAME,
                    generation_config=GENERATION_CONFIG
                )
            
            # Monta prompt
            prompt_parts = [
                self.get_system_prompt(),
                "\nDOCUMENTAÇÃO DISPONÍVEL:",
            ]
            
            for file in self.uploaded_files:
                prompt_parts.append(f"- {file.display_name}")
            
            prompt_parts.extend([
                f"\nPERGUNTA:\n{question}",
                "\nBase sua resposta na documentação fornecida."
            ])
            
            prompt_parts.extend(self.uploaded_files)
            
            response = self.model.generate_content(prompt_parts)
            return response.text
            
        except Exception as e:
            return f"❌ Erro ao processar pergunta: {str(e)}"


def initialize_session_state():
    """Inicializa o estado da sessão"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    
    if 'setup_done' not in st.session_state:
        st.session_state.setup_done = False
    
    if 'doc_count' not in st.session_state:
        st.session_state.doc_count = 0


def setup_chatbot():
    """Configura e faz upload da documentação"""
    api_key = GOOGLE_API_KEY  # Agora vem do config.py
    
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY não configurada!")
        st.info("Configure no arquivo config.py ou variável de ambiente:\n```bash\nexport GOOGLE_API_KEY='sua_chave'\n```")
        st.stop()
    
    if not st.session_state.setup_done:
        with st.spinner("🔧 Inicializando assistente..."):
            st.session_state.chatbot = CamundaChatbot(api_key)
        
        st.info("📚 Fazendo upload da documentação... Isso pode levar alguns minutos.")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(current, total, filename):
            progress = current / total
            progress_bar.progress(progress)
            status_text.text(f"Processando ({current}/{total}): {filename}")
        
        success, message = st.session_state.chatbot.upload_documentation(update_progress)
        
        progress_bar.empty()
        status_text.empty()
        
        if success:
            st.session_state.setup_done = True
            st.session_state.doc_count = len(st.session_state.chatbot.uploaded_files)
            st.success(f"✅ {message} com sucesso!")
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"❌ Erro: {message}")
            st.stop()


def main():
    """Função principal da aplicação Streamlit"""
    
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🤖 Assistente de Migração Camunda 7 → 8</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Seu guia completo para migração baseado na documentação oficial</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 Camunda Assistant")
        st.markdown("---")
        
        st.markdown("### 📊 Status")
        
        if st.session_state.setup_done:
            st.markdown(f"""
            <div class="success-box">
                <strong>✅ Sistema Pronto</strong><br>
                📚 {st.session_state.doc_count} documentos carregados
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                <strong>⚙️ Inicializando...</strong><br>
                Aguarde o upload dos documentos
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📚 Documentação Disponível")
        docs = [
            "Code Conversion",
            "Conceptual Differences",
            "Data Migrator",
            "Migration Journey",
            "Migration Tooling",
            "Migration-ready Solutions"
        ]
        
        for doc in docs:
            st.markdown(f'<span class="doc-badge">📄 {doc}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 💡 Exemplos de Perguntas")
        st.markdown("""
        - Quais as principais diferenças?
        - Como migrar processos BPMN?
        - O que é o Zeebe?
        - Como converter código Java?
        - Como funciona o Data Migrator?
        - Quais ferramentas disponíveis?
        """)
        
        st.markdown("---")
        
        if st.button("🗑️ Limpar Histórico"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🔄 Reiniciar Sistema"):
            st.session_state.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ Sobre")
        st.markdown("""
        Este assistente usa **Google Gemini** e **RAG** para fornecer 
        respostas precisas baseadas na documentação oficial do Camunda.
        
        **Tecnologias:**
        - 🤖 Gemini 2.0 Flash
        - 📚 RAG (Retrieval-Augmented Generation)
        - 🎨 Streamlit
        """)
    
    # Setup do chatbot (se necessário)
    if not st.session_state.setup_done:
        setup_chatbot()
    
    # Área de chat
    st.markdown("---")
    
    # Exibe mensagens do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua pergunta sobre migração Camunda 7 → 8..."):
        # Adiciona mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gera resposta
        with st.chat_message("assistant"):
            with st.spinner("🤔 Pensando..."):
                response = st.session_state.chatbot.ask(prompt)
                st.markdown(response)
        
        # Adiciona resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Mensagem inicial se não houver histórico
    if len(st.session_state.messages) == 0:
        st.info("👋 Olá! Faça sua primeira pergunta sobre migração do Camunda 7 para o Camunda 8!")
        
        # Botões de sugestão
        st.markdown("### 🎯 Sugestões de perguntas:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Diferenças principais"):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": "Quais são as principais diferenças entre Camunda 7 e Camunda 8?"
                })
                st.rerun()
        
        with col2:
            if st.button("🔄 Migrar BPMN"):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": "Como migrar um processo BPMN do Camunda 7 para o Camunda 8?"
                })
                st.rerun()
        
        with col3:
            if st.button("⚙️ O que é Zeebe?"):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": "O que é o Zeebe e como ele funciona?"
                })
                st.rerun()


if __name__ == "__main__":
    main()

