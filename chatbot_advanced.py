#!/usr/bin/env python3
"""
Chatbot Avançado com RAG Completo
==================================
Retrieval (Top-K 100) + Reranker Cohere (Top-10) + Suporte a Imagens
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Tuple

import streamlit as st
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import cohere

# Importa Groq (opcional)
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Importa configurações
try:
    from config import (
        GOOGLE_API_KEY, 
        MODEL_NAME, 
        GENERATION_CONFIG, 
        COHERE_API_KEY,
        LLM_PROVIDER,
        RAG_CONFIG
    )
    try:
        from config import GROQ_API_KEY
    except ImportError:
        GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
except ImportError:
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    COHERE_API_KEY = os.environ.get('COHERE_API_KEY')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    LLM_PROVIDER = "gemini"
    MODEL_NAME = "gemini-2.5-pro"
    GENERATION_CONFIG = {
        'temperature': 0.2,
        'top_p': 0.95,
        'top_k': 40,
        'max_output_tokens': 8192,
    }
    RAG_CONFIG = {
        "retrieval_top_k": 100,
        "rerank_top_n": 10,
    }

# Configuração da página
st.set_page_config(
    page_title="Assistente - Migração Camunda 7 → 8",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
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
</style>
""", unsafe_allow_html=True)


class AdvancedRAGChatbot:
    """Chatbot com RAG avançado: Retrieval + Reranking + Imagens"""
    
    def __init__(self, google_api_key: str, cohere_api_key: str = None, groq_api_key: str = None):
        self.google_api_key = google_api_key
        self.cohere_api_key = cohere_api_key or COHERE_API_KEY or os.environ.get('COHERE_API_KEY')
        self.groq_api_key = groq_api_key or GROQ_API_KEY or os.environ.get('GROQ_API_KEY', '')
        
        # Detecta provider
        self.llm_provider = LLM_PROVIDER
        
        # Inicializa componentes
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=google_api_key
        )
        
        # Carrega vectorstore
        self.vectorstore = None
        self.load_vectorstore()
        
        # Inicializa Cohere para reranking
        if self.cohere_api_key:
            self.cohere_client = cohere.Client(self.cohere_api_key)
        else:
            self.cohere_client = None
        
        # Carrega metadata de imagens
        self.image_metadata = self.load_image_metadata()
        
        # Inicializa LLM baseado no provider
        if self.llm_provider == "groq":
            if not GROQ_AVAILABLE:
                self.llm_provider = "gemini"
            elif not self.groq_api_key:
                self.llm_provider = "gemini"
            else:
                self.groq_client = Groq(api_key=self.groq_api_key)
        
        if self.llm_provider == "gemini":
            genai.configure(api_key=google_api_key)
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                generation_config=GENERATION_CONFIG
            )
    
    def load_vectorstore(self):
        """Carrega o banco vetorial"""
        try:
            self.vectorstore = Chroma(
                persist_directory="./chroma_db",
                embedding_function=self.embeddings,
                collection_name="camunda_migration"
            )
            return True
        except Exception as e:
            st.error(f"❌ Erro ao carregar vectorstore: {e}")
            return False
    
    def load_image_metadata(self) -> Dict:
        """Carrega metadata de imagens"""
        try:
            if Path("image_metadata.json").exists():
                with open("image_metadata.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            st.warning(f"⚠️ Não foi possível carregar metadata de imagens: {e}")
        return {}
    
    def get_system_prompt(self) -> str:
        """Retorna o system prompt otimizado"""
        return """Você é um assistente especializado em migração Camunda 7→8.

⚡ REGRAS OBRIGATÓRIAS:
- MÁXIMO 500 TOKENS (aprox. 400 palavras)
- SEJA EXTREMAMENTE DIRETO E OBJETIVO
- Use bullet points para clareza
- Exemplo de código: máximo 5 linhas
- ZERO enrolação ou introduções longas

📝 ESTRUTURA (use APENAS o necessário):
1. Resposta direta (2-3 linhas)
2. Pontos-chave (3-5 bullets)
3. Código/comando (SE necessário, máx 5 linhas)
4. Fonte (documento, página)

🚫 PROIBIDO:
- Introduções longas
- Repetir a pergunta
- Explicações excessivas
- Mais de 5 pontos em listas
- Código maior que 5 linhas

✅ SOBRE IMAGENS:
Se houver (⚠️), mencione: "📷 [doc] p.[X]" (1 linha apenas)

Responda APENAS com informação dos chunks. Seja ULTRA conciso:"""
    
    def generate_response(self, prompt: str) -> str:
        """Gera resposta usando o provider configurado"""
        if self.llm_provider == "groq":
            try:
                completion = self.groq_client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=GENERATION_CONFIG.get('temperature', 0.2),
                    max_tokens=GENERATION_CONFIG.get('max_output_tokens', 8192),
                    top_p=GENERATION_CONFIG.get('top_p', 0.95),
                )
                return completion.choices[0].message.content
            except Exception as e:
                # Fallback silencioso para Gemini
                if not hasattr(self, 'model'):
                    genai.configure(api_key=self.google_api_key)
                    self.model = genai.GenerativeModel(
                        model_name="gemini-2.5-pro",
                        generation_config=GENERATION_CONFIG
                    )
                response = self.model.generate_content(prompt)
                return response.text
        else:  # gemini
            response = self.model.generate_content(prompt)
            return response.text
    
    def retrieve_documents(self, query: str, k: int = 100) -> List[Tuple]:
        """Retrieval: busca top-K documentos similares"""
        if not self.vectorstore:
            return []
        
        try:
            # Busca com similaridade
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            st.error(f"❌ Erro no retrieval: {e}")
            return []
    
    def rerank_documents(self, query: str, documents: List, top_n: int = 10) -> List:
        """Reranking: reordena documentos por relevância usando Cohere"""
        if not self.cohere_client:
            # Retorna no formato correto (doc, score, relevance) mesmo sem reranking
            return [(doc, score, score) for doc, score in documents[:top_n]]
        
        try:
            # Prepara documentos para reranking
            docs_text = [doc[0].page_content for doc in documents]
            
            # Rerank com Cohere
            reranked = self.cohere_client.rerank(
                query=query,
                documents=docs_text,
                top_n=top_n,
                model="rerank-multilingual-v3.0"
            )
            
            # Reordena documentos originais
            reranked_docs = []
            for result in reranked.results:
                original_doc = documents[result.index]
                reranked_docs.append((
                    original_doc[0],
                    original_doc[1],
                    result.relevance_score
                ))
            
            return reranked_docs
            
        except Exception as e:
            st.error(f"❌ Erro no reranking: {e}")
            return documents[:top_n]
    
    def format_chunks_for_prompt(self, reranked_docs: List) -> Tuple[str, List]:
        """Formata chunks para o prompt, incluindo informações de imagens"""
        chunks_text = []
        images_info = []
        
        for i, (doc, score, relevance) in enumerate(reranked_docs, 1):
            chunk_text = f"""
---
CHUNK {i} (Relevância: {relevance:.2f})
Documento: {doc.metadata.get('source', 'N/A')}
Página: {doc.metadata.get('page', 'N/A')}
Seção: {doc.metadata.get('section', 'general')}
"""
            
            # Verifica se tem imagens
            if doc.metadata.get('has_images'):
                # Parse JSON das imagens
                images_list = json.loads(doc.metadata.get('images', '[]'))
                chunk_text += f"⚠️ ESTE CHUNK CONTÉM IMAGENS RELEVANTES\n"
                chunk_text += f"Imagens: {', '.join([Path(img).name for img in images_list])}\n"
                
                # Adiciona à lista de imagens para potencial exibição
                images_info.extend(images_list)
            
            chunk_text += f"\nCONTEÚDO:\n{doc.page_content}\n"
            chunks_text.append(chunk_text)
        
        return "\n".join(chunks_text), images_info
    
    def ask(self, question: str) -> Dict:
        """Faz uma pergunta com RAG completo"""
        
        # 1. RETRIEVAL (Top-K configurável)
        retrieval_k = RAG_CONFIG.get('retrieval_top_k', 100)
        with st.spinner("🤖 Processando sua pergunta..."):
            retrieved_docs = self.retrieve_documents(question, k=retrieval_k)
        
            if not retrieved_docs:
                return {
                    'answer': "❌ Não foi possível recuperar documentos. Verifique se a indexação foi executada.",
                    'images': [],
                    'sources': []
                }
            
            # 2. RERANKING (Top-N configurável)
            rerank_n = RAG_CONFIG.get('rerank_top_n', 10)
            reranked_docs = self.rerank_documents(question, retrieved_docs, top_n=rerank_n)
        
        # 3. FORMATA CHUNKS
        chunks_formatted, images = self.format_chunks_for_prompt(reranked_docs)
        
        # 4. MONTA PROMPT FINAL
        final_prompt = f"""{self.get_system_prompt()}

==================================================
CHUNKS RELEVANTES DA DOCUMENTAÇÃO:
==================================================

{chunks_formatted}

==================================================
PERGUNTA DO DESENVOLVEDOR:
==================================================

{question}

==================================================
INSTRUÇÕES FINAIS:
==================================================

Com base EXCLUSIVAMENTE nos chunks acima, forneça uma resposta completa e didática.
Se houver chunks com imagens (marcados com ⚠️), mencione-as na resposta e descreva o que ilustram.
Cite sempre as fontes (documento e página) de onde tirou cada informação.
"""
        
        # 5. GERA RESPOSTA
        try:
            answer = self.generate_response(final_prompt)
        except Exception as e:
            answer = f"❌ Erro ao gerar resposta: {e}"
            images = []
        
        # 6. EXTRAI FONTES
        sources = []
        for doc, score, relevance in reranked_docs[:5]:  # Top-5 fontes
            sources.append({
                'document': doc.metadata.get('source', 'N/A'),
                'page': doc.metadata.get('page', 'N/A'),
                'section': doc.metadata.get('section', 'general'),
                'relevance': f"{relevance:.2f}"
            })
        
        return {
            'answer': answer,
            'images': images,
            'sources': sources
        }


def initialize_session_state():
    """Inicializa estado da sessão"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    
    if 'setup_done' not in st.session_state:
        st.session_state.setup_done = False


def setup_chatbot():
    """Setup do chatbot"""
    if not GOOGLE_API_KEY:
        st.error("⚠️ GOOGLE_API_KEY não configurada!")
        st.stop()
    
    # Verifica se vectorstore existe
    if not Path("./chroma_db").exists():
        st.error("❌ Banco vetorial não encontrado!")
        st.info("Execute primeiro: python indexer_advanced.py")
        st.stop()
    
    if not st.session_state.setup_done:
        with st.spinner("⚡ Inicializando..."):
            st.session_state.chatbot = AdvancedRAGChatbot(
                google_api_key=GOOGLE_API_KEY
            )
            st.session_state.setup_done = True
        st.rerun()


def main():
    """Função principal"""
    
    initialize_session_state()
    
    # Header
    retrieval_k = RAG_CONFIG.get('retrieval_top_k', 100)
    rerank_n = RAG_CONFIG.get('rerank_top_n', 10)
    provider = "GROQ (Ultra Rápido ⚡)" if LLM_PROVIDER == "groq" else "Gemini"
    
    st.markdown('<div class="main-header">Assistente - Migração Camunda 7 → 8</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center; color: #666; margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    
    # Sidebar
    # with st.sidebar:
    #     st.markdown("")
    #     st.markdown("")
        
    #     if st.session_state.setup_done:
    #         provider_emoji = "⚡" if LLM_PROVIDER == "groq" else "✨"
    #         provider_text = "GROQ (Ultra Rápido)" if LLM_PROVIDER == "groq" else "Gemini"
    #         retrieval_k = RAG_CONFIG.get('retrieval_top_k', 100)
    #         rerank_n = RAG_CONFIG.get('rerank_top_n', 10)
            
    #         st.markdown(f"""
    #         <div class="success-box">
    #             <strong>✅ Sistema Ativo</strong><br>
    #             🔍 Retrieval: Top-{retrieval_k}<br>
    #             🎯 Reranker: Top-{rerank_n}<br>
    #             {provider_emoji} LLM: {provider_text}<br>
    #             🤖 Modelo: {MODEL_NAME}<br>
    #             📷 Imagens: Suportado
    #         </div>
    #         """, unsafe_allow_html=True)
    #     else:
    #         st.info("⚙️ Inicializando...")
        
    #     st.markdown("---")
    #     st.markdown("### 💡 Características")
    #     retrieval_k = RAG_CONFIG.get('retrieval_top_k', 100)
    #     rerank_n = RAG_CONFIG.get('rerank_top_n', 10)
    #     st.markdown(f"""
    #     - ✅ Busca vetorial (Google Embeddings)
    #     - ✅ Top-{retrieval_k} documentos recuperados
    #     - ✅ Reranking com Cohere
    #     - ✅ Top-{rerank_n} mais relevantes
    #     - ✅ Consciente de imagens
    #     - ✅ Citações de fontes
    #     """)
        
    #     st.markdown("---")
        
    #     if st.button("🗑️ Limpar Histórico"):
    #         st.session_state.messages = []
    #         st.rerun()
        
    #     if st.button("🔄 Reiniciar Sistema"):
    #         st.session_state.clear()
    #         st.rerun()
    
    # Setup
    if not st.session_state.setup_done:
        setup_chatbot()
    
    # Chat
    st.markdown("---")
    
    # Histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Exibe imagens se houver
            if message.get("images"):
                st.markdown("---")
                st.markdown("### 📷 Imagens Relacionadas")
                
                # Agrupa imagens por documento
                images_by_doc = {}
                for img_path in message["images"]:
                    if Path(img_path).exists():
                        # Extrai info do nome do arquivo
                        # Formato: documento_pX_imgY.png
                        filename = Path(img_path).stem
                        parts = filename.split('_p')
                        doc_name = parts[0] if parts else "Documento"
                        
                        if doc_name not in images_by_doc:
                            images_by_doc[doc_name] = []
                        images_by_doc[doc_name].append(img_path)
                
                # Exibe imagens agrupadas
                for doc_name, img_paths in images_by_doc.items():
                    st.markdown(f"**Documento:** {doc_name.replace('_', ' ')}")
                    
                    # Cria colunas para múltiplas imagens
                    if len(img_paths) == 1:
                        st.image(img_paths[0], use_column_width=True)
                    elif len(img_paths) == 2:
                        col1, col2 = st.columns(2)
                        col1.image(img_paths[0], use_column_width=True)
                        col2.image(img_paths[1], use_column_width=True)
                    else:
                        for img_path in img_paths[:4]:  # Max 4 imagens
                            st.image(img_path, use_column_width=True)
                    
                    st.markdown("")  # Espaçamento
            
            # Exibe fontes
            if message.get("sources"):
                with st.expander("📚 Ver Fontes"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}. {source['document']}** (Página {source['page']}) - Relevância: {source['relevance']}")
    
    # Input
    if prompt := st.chat_input("Digite sua pergunta sobre migração Camunda 7 → 8..."):
        # Adiciona pergunta
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gera resposta
        with st.chat_message("assistant"):
            result = st.session_state.chatbot.ask(prompt)
            
            st.markdown(result['answer'])
            
            # Exibe imagens
            if result.get('images') and len(result['images']) > 0:
                st.markdown("---")
                st.markdown("### 📷 Imagens Relacionadas")
                
                # Agrupa imagens por documento
                images_by_doc = {}
                for img_path in result['images']:
                    if Path(img_path).exists():
                        # Extrai info do nome do arquivo
                        filename = Path(img_path).stem
                        parts = filename.split('_p')
                        doc_name = parts[0] if parts else "Documento"
                        
                        if doc_name not in images_by_doc:
                            images_by_doc[doc_name] = []
                        images_by_doc[doc_name].append(img_path)
                
                # Exibe imagens agrupadas
                for doc_name, img_paths in images_by_doc.items():
                    st.markdown(f"**Documento:** {doc_name.replace('_', ' ')}")
                    
                    # Cria colunas para múltiplas imagens
                    if len(img_paths) == 1:
                        st.image(img_paths[0], use_column_width=True)
                    elif len(img_paths) == 2:
                        col1, col2 = st.columns(2)
                        col1.image(img_paths[0], use_column_width=True)
                        col2.image(img_paths[1], use_column_width=True)
                    else:
                        for img_path in img_paths[:4]:  # Max 4 imagens
                            st.image(img_path, use_column_width=True)
                    
                    st.markdown("")  # Espaçamento
            
            # Exibe fontes
            if result.get('sources'):
                with st.expander("📚 Ver Fontes"):
                    for i, source in enumerate(result['sources'], 1):
                        st.markdown(f"**{i}. {source['document']}** (Página {source['page']}) - Relevância: {source['relevance']}")
        
        # Salva resposta
        st.session_state.messages.append({
            "role": "assistant",
            "content": result['answer'],
            "images": result.get('images', []),
            "sources": result.get('sources', [])
        })


if __name__ == "__main__":
    main()

