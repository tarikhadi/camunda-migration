# ⚡ Como Usar GROQ (10x Mais Rápido)

## 🎯 O que é Groq?

Groq é uma empresa que oferece **inferência ultra-rápida** de modelos de IA usando hardware especializado (LPU).

**Velocidade**: 500-600 tokens/segundo (vs 30-50 do Gemini Pro)  
**Custo**: **GRATUITO** (com limites generosos)  
**Qualidade**: Equivalente ou superior ao Gemini para RAG

---

## 📝 Passo a Passo: Obter API Key (2 minutos)

### 1️⃣ Acesse o Console do Groq

Vá para: **https://console.groq.com**

### 2️⃣ Crie uma Conta (Gratuita)

- Clique em "Sign Up"
- Use Google/GitHub ou email
- Confirme seu email

### 3️⃣ Gere sua API Key

1. Após login, vá para **"API Keys"** no menu lateral
2. Clique em **"Create API Key"**
3. Dê um nome (ex: "Camunda Chatbot")
4. Clique em **"Create"**
5. **Copie a chave** (começa com `gsk_...`)

⚠️ **IMPORTANTE**: Salve a chave! Ela só aparece uma vez.

---

## ⚙️ Configuração no Projeto

### Passo 1: Instale o Groq

```bash
pip install groq
```

### Passo 2: Configure no `config.py`

Abra o arquivo `config.py` e:

1. **Cole sua API Key**:
```python
GROQ_API_KEY = "gsk_sua_chave_aqui"
```

2. **Descomente as linhas do Groq** (remova o `#`):
```python
# De:
# LLM_PROVIDER = "groq"
# MODEL_NAME = "llama-3.1-70b-versatile"

# Para:
LLM_PROVIDER = "groq"
MODEL_NAME = "llama-3.1-70b-versatile"
```

3. **Comente a configuração do Gemini** (adicione `#`):
```python
# De:
LLM_PROVIDER = "gemini"
MODEL_NAME = "gemini-2.5-pro"

# Para:
# LLM_PROVIDER = "gemini"
# MODEL_NAME = "gemini-2.5-pro"
```

### Passo 3: Execute o Chatbot

```bash
streamlit run chatbot_advanced.py
```

✅ **Pronto!** Agora você tem respostas **10x mais rápidas**! ⚡

---

## 🔍 Exemplo de `config.py` Configurado

```python
# ============================================
# API KEYS
# ============================================

GOOGLE_API_KEY = "sua_google_api_key_aqui"
COHERE_API_KEY = "sua_cohere_api_key_aqui"
GROQ_API_KEY = "gsk_sua_chave_groq_aqui"  # ← COLE SUA CHAVE AQUI

# ============================================
# CONFIGURAÇÃO DE LLM
# ============================================

# 🔥 GROQ (ATIVADO)
LLM_PROVIDER = "groq"
MODEL_NAME = "llama-3.1-70b-versatile"

# ✨ GEMINI (DESATIVADO)
# LLM_PROVIDER = "gemini"
# MODEL_NAME = "gemini-2.5-pro"

# ============================================
# CONFIGURAÇÕES DE RAG
# ============================================

RAG_CONFIG = {
    "retrieval_top_k": 100,
    "rerank_top_n": 10,
}
```

---

## 🚀 Modelos Groq Recomendados

### Para Máxima Qualidade:
```python
MODEL_NAME = "llama-3.3-70b-versatile"  # Mais recente
```

### Para Máxima Velocidade:
```python
MODEL_NAME = "mixtral-8x7b-32768"  # Mais rápido
```

### Balanceado (Recomendado):
```python
MODEL_NAME = "llama-3.1-70b-versatile"  # Melhor custo-benefício
```

---

## 📊 Comparação Antes/Depois

| Aspecto | Gemini 2.5 Pro | Groq Llama 3.1 70B |
|---------|----------------|-------------------|
| **Velocidade** | 15-30 segundos | 2-4 segundos ⚡ |
| **Tokens/segundo** | ~30-50 | ~500+ 🚀 |
| **Qualidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Custo** | Pago | Grátis 💰 |
| **Latência Inicial** | ~2s | ~0.5s |

---

## ❓ FAQ

**P: Preciso pagar pelo Groq?**  
R: Não! É gratuito com limites generosos (6000 tokens/min para Llama 70B).

**P: Groq funciona offline?**  
R: Não, é uma API cloud como o Gemini.

**P: Posso voltar para Gemini depois?**  
R: Sim! Basta editar o `config.py` novamente.

**P: E se minha API Key do Groq acabar?**  
R: O sistema automaticamente volta para Gemini (fallback).

**P: Groq suporta português?**  
R: Sim! Os modelos Llama 3.1/3.3 têm excelente suporte a português.

**P: Qual o limite gratuito do Groq?**  
R: Varia por modelo, mas geralmente:
- Llama 3.1 70B: 6000 tokens/minuto
- Mixtral 8x7B: 5000 tokens/minuto

---

## ⚠️ Troubleshooting

### Erro: "Groq não instalado"
```bash
pip install groq
```

### Erro: "GROQ_API_KEY não configurada"
Verifique se você:
1. Colou a chave no `config.py`
2. A chave começa com `gsk_`
3. Não deixou espaços extras

### Erro: "Rate limit exceeded"
Você excedeu o limite gratuito. Soluções:
1. Aguarde 1 minuto
2. O sistema vai automaticamente usar Gemini
3. Considere upgrade do plano Groq (ainda muito barato)

---

## 🎯 Dica Final

Para **MÁXIMA PERFORMANCE**, combine:

```python
# config.py

# Use Groq
LLM_PROVIDER = "groq"
MODEL_NAME = "llama-3.3-70b-versatile"

# Otimize RAG
RAG_CONFIG = {
    "retrieval_top_k": 50,   # Reduzido
    "rerank_top_n": 5,       # Reduzido
}
```

**Resultado**: Respostas em **1-2 segundos** com qualidade excelente! ⚡🚀

---

## 🔗 Links Úteis

- **Groq Console**: https://console.groq.com
- **Documentação**: https://console.groq.com/docs
- **Modelos Disponíveis**: https://console.groq.com/docs/models
- **Pricing**: https://wow.groq.com/pricing (spoiler: é grátis!)

---

**🎉 Aproveite respostas ultra-rápidas com Groq!**

