"""
Arquivo de configuração do chatbot - EXEMPLO
⚠️ Copie este arquivo para config.py e configure suas chaves!

Passos:
1. Copie: cp config.example.py config.py
2. Edite config.py e adicione suas API keys
3. Execute: streamlit run chatbot_streamlit.py
"""

# ============================================
# API KEYS
# ============================================

# Google Generative AI
# Obtenha em: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY = "sua_google_api_key_aqui"

# Cohere (Reranking) - OPCIONAL
# Obtenha em: https://dashboard.cohere.com/api-keys
COHERE_API_KEY = "sua_cohere_api_key_aqui"

# Groq (Alternativa ULTRA RÁPIDA ⚡) - OPCIONAL
# Obtenha em: https://console.groq.com
GROQ_API_KEY = "sua_groq_api_key_aqui"

# ============================================
# CONFIGURAÇÃO DE LLM
# ============================================

# ⚡ GEMINI FLASH (ATIVADO - RÁPIDO E ESTÁVEL)
LLM_PROVIDER = "gemini"
MODEL_NAME = "gemini-2.0-flash"

# ✨ GEMINI PRO (DESATIVADO - mais poderoso, mais lento)
# LLM_PROVIDER = "gemini"
# MODEL_NAME = "gemini-2.5-pro"

# 🔥 GROQ (DESATIVADO - requer GROQ_API_KEY)
# LLM_PROVIDER = "groq"
# MODEL_NAME = "llama-3.3-70b-versatile"

# ============================================
# CONFIGURAÇÕES DE GERAÇÃO
# ============================================

GENERATION_CONFIG = {
    'temperature': 0.2,  # Baixa temperatura para respostas precisas
    'top_p': 0.95,
    'top_k': 40,
    'max_output_tokens': 500,  # ⚡ LIMITE: Respostas objetivas (máx 500 tokens)
}

# ============================================
# CONFIGURAÇÕES DE RAG (Ajuste para velocidade)
# ============================================

RAG_CONFIG = {
    "retrieval_top_k": 50,   # ⚡ Otimizado para velocidade
    "rerank_top_n": 5,       # ⚡ Top-5 mais relevantes
}
