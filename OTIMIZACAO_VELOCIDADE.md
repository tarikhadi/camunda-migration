# ⚡ Guia de Otimização de Velocidade

## 🚀 3 Formas de Acelerar o Chatbot

### 🔥 **OPÇÃO 1: GROQ (RECOMENDADO - 10x MAIS RÁPIDO)**

**Velocidade**: 500+ tokens/segundo ⚡⚡⚡  
**Qualidade**: Excelente (Llama 3.1 70B)  
**Custo**: GRATUITO (com limites generosos)

#### Como Ativar:

1. **Obtenha sua API Key**:
   - Acesse: https://console.groq.com
   - Crie uma conta (gratuita)
   - Gere uma API Key

2. **Instale o Groq**:
```bash
pip install groq
```

3. **Configure no `config.py`**:
```python
# Adicione sua chave
GROQ_API_KEY = "gsk_..."  # Sua chave aqui

# Descomente as linhas:
LLM_PROVIDER = "groq"
MODEL_NAME = "llama-3.1-70b-versatile"
```

4. **Execute normalmente**:
```bash
streamlit run chatbot_advanced.py
```

✅ **Resultado**: Respostas em **2-4 segundos** (vs 15-30 segundos com Gemini Pro)

---

### ⚡ **OPÇÃO 2: GEMINI FLASH (3x MAIS RÁPIDO)**

**Velocidade**: ~100-150 tokens/segundo  
**Qualidade**: Boa (inferior ao Pro, mas suficiente)  
**Custo**: Mais barato que Pro

#### Como Ativar:

No `config.py`, altere:
```python
# Mantenha Gemini mas use Flash
LLM_PROVIDER = "gemini"
MODEL_NAME = "gemini-2.0-flash-exp"
```

✅ **Resultado**: Respostas em **5-8 segundos**

---

### 🎯 **OPÇÃO 3: REDUZIR CHUNKS (Mais Rápido mas Menos Contexto)**

**Velocidade**: Marginal (~20% mais rápido)  
**Qualidade**: Pode perder contexto relevante  

#### Como Ativar:

No `config.py`, ajuste:
```python
RAG_CONFIG = {
    "retrieval_top_k": 50,   # Era 100
    "rerank_top_n": 5,       # Era 10
}
```

⚠️ **Trade-off**: Menos chunks = respostas mais rápidas mas potencialmente menos completas

---

## 📊 Comparação de Velocidade

| Opção | Velocidade (tokens/s) | Tempo Resposta | Qualidade | Custo |
|-------|----------------------|----------------|-----------|-------|
| **Groq Llama 3.1 70B** | 500+ | 2-4s | ⭐⭐⭐⭐⭐ | Grátis |
| **Groq Mixtral 8x7B** | 600+ | 1-3s | ⭐⭐⭐⭐ | Grátis |
| **Gemini Flash** | 100-150 | 5-8s | ⭐⭐⭐⭐ | $ |
| **Gemini Pro** | 30-50 | 15-30s | ⭐⭐⭐⭐⭐ | $$ |

---

## 🎯 Recomendação Final

### Para MÁXIMA VELOCIDADE:
```python
# config.py
GROQ_API_KEY = "sua_chave"
LLM_PROVIDER = "groq"
MODEL_NAME = "llama-3.1-70b-versatile"

RAG_CONFIG = {
    "retrieval_top_k": 50,
    "rerank_top_n": 5,
}
```

**Resultado**: Respostas em **1-3 segundos** mantendo excelente qualidade! ⚡🚀

---

## 🔍 Modelos Groq Disponíveis

| Modelo | Velocidade | Qualidade | Contexto |
|--------|-----------|-----------|----------|
| `llama-3.3-70b-versatile` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 128K tokens |
| `llama-3.1-70b-versatile` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 128K tokens |
| `mixtral-8x7b-32768` | ⚡⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 32K tokens |

**Recomendado**: `llama-3.3-70b-versatile` (mais recente e poderoso)

---

## ❓ FAQ

**P: Groq é realmente gratuito?**  
R: Sim! Com limites generosos (6000 tokens/minuto para Llama 70B).

**P: Preciso trocar todo o código?**  
R: Não! Apenas configure no `config.py` e pronto.

**P: Groq funciona offline?**  
R: Não, é uma API online como Gemini.

**P: Posso usar Groq + Gemini?**  
R: Sim! O código tem fallback automático: se Groq falhar, usa Gemini.

**P: Qual a diferença de qualidade Groq vs Gemini Pro?**  
R: Na prática, para este caso de uso (RAG), a qualidade é **equivalente**.

---

## 🚀 Conclusão

Para **MÁXIMA VELOCIDADE SEM PERDER QUALIDADE**:

1. ✅ Use **GROQ** com **Llama 3.3 70B**
2. ✅ Configure `retrieval_top_k: 50` e `rerank_top_n: 5`
3. ✅ Mantenha Cohere reranker ativo

**Resultado**: Sistema **10x mais rápido** mantendo respostas excelentes! ⚡🎯

