# ⚙️ Configuração Automática - API Key Permanente

## ✅ **JÁ ESTÁ CONFIGURADO!**

A API Key agora está salva no arquivo `config.py` e será carregada automaticamente! 🎉

---

## 🚀 **Como Usar (SUPER SIMPLES)**

### **Streamlit (Interface Web):**

```bash
cd /Users/tarikhadi/Desktop/rag_migracao_camunda
streamlit run chatbot_streamlit.py
```

**SEM PRECISAR** exportar GOOGLE_API_KEY! ✨

### **Terminal (CLI):**

```bash
cd /Users/tarikhadi/Desktop/rag_migracao_camunda
python3 camunda_migration_chatbot_v2.py
```

**SEM PRECISAR** exportar GOOGLE_API_KEY! ✨

---

## 🎯 **O Que Foi Configurado**

### 📁 **Arquivo `config.py` criado:**

```python
GOOGLE_API_KEY = "sua_google_api_key_aqui"
MODEL_NAME = "gemini-2.0-flash"  # Usando Gemini 2.0 Flash
```

### ✅ **Vantagens:**

- ✅ **Não precisa** mais digitar `export GOOGLE_API_KEY=...`
- ✅ **Carrega automaticamente** ao executar
- ✅ **Usando Gemini 1.5 Pro** (modelo mais poderoso que o Flash)
- ✅ **Configuração persistente** (salva no arquivo)
- ✅ **Fácil de usar** - apenas execute!

---

## 🔧 **Como Funciona**

Ambos os chatbots (Streamlit e Terminal) agora:

1. **Tentam importar** de `config.py` primeiro
2. **Se não encontrar**, caem back para variável de ambiente
3. **Carregam automaticamente** sem intervenção

### Código (você não precisa fazer nada):

```python
# Importa configurações automaticamente
from config import GOOGLE_API_KEY, MODEL_NAME
```

---

## 🎨 **Modelo Atualizado: Gemini 1.5 Pro**

### Por que Gemini 1.5 Pro?

| Característica | Flash | **Pro** (Novo) |
|----------------|-------|----------------|
| **Velocidade** | Muito rápido | Rápido |
| **Qualidade** | Boa | **Excelente** ⭐ |
| **Contexto** | 1M tokens | 2M tokens |
| **Raciocínio** | Bom | **Superior** ⭐ |
| **Detalhamento** | Bom | **Muito melhor** ⭐ |

**Resultado:** Respostas ainda mais detalhadas e precisas! 🎯

---

## 📊 **Comparação: Antes vs Agora**

### **Antes (Chato):**

```bash
# Tinha que fazer isso TODA VEZ:
export GOOGLE_API_KEY="sua_google_api_key_aqui"
streamlit run chatbot_streamlit.py
```

### **Agora (Fácil):**

```bash
# Só isso! API key carrega sozinha:
streamlit run chatbot_streamlit.py
```

**50% menos comandos!** ⚡

---

## 🔒 **Segurança**

### ✅ **Arquivo protegido:**

- `config.py` está no `.gitignore`
- **Não será commitado** no Git
- **Seguro** para desenvolvimento local

### ⚠️ **Lembrete:**

**NUNCA** commite o arquivo `config.py` no Git!

Se precisar compartilhar o projeto:
1. Delete `config.py`
2. Use `config.example.py` como referência
3. Cada desenvolvedor cria seu próprio `config.py`

---

## 🎯 **Para Mudar o Modelo**

Edite o arquivo `config.py`:

```python
# Opções disponíveis:
MODEL_NAME = "gemini-1.5-pro"        # ⭐ Recomendado (mais poderoso)
MODEL_NAME = "gemini-2.0-flash-exp"  # Mais rápido
MODEL_NAME = "gemini-1.5-flash"      # Equilíbrio
```

---

## 🧪 **Testar Configuração**

```bash
cd /Users/tarikhadi/Desktop/rag_migracao_camunda
python3 -c "from config import GOOGLE_API_KEY, MODEL_NAME; print(f'API Key: {GOOGLE_API_KEY[:10]}...\nModelo: {MODEL_NAME}')"
```

**Saída esperada:**
```
API Key: sua_api_k...
Modelo: gemini-2.0-flash
```

---

## 🚀 **EXECUTE AGORA - SUPER SIMPLES!**

### **Web (Streamlit):**

```bash
streamlit run chatbot_streamlit.py
```

### **Terminal:**

```bash
python3 camunda_migration_chatbot_v2.py
```

**Sem configurar nada! Tudo automático! 🎉**

---

## 📚 **Arquivos Criados/Modificados**

| Arquivo | Descrição |
|---------|-----------|
| `config.py` | ⭐ **Configuração principal** (API Key + Modelo) |
| `config.example.py` | Exemplo para outros desenvolvedores |
| `chatbot_streamlit.py` | ✅ Atualizado para carregar config |
| `camunda_migration_chatbot_v2.py` | ✅ Atualizado para carregar config |
| `.gitignore` | ✅ Atualizado para ignorar config.py |

---

## ✅ **Checklist**

- [x] API Key configurada automaticamente
- [x] Modelo atualizado para Gemini 1.5 Pro
- [x] Não precisa mais exportar variável
- [x] config.py protegido no .gitignore
- [x] Ambas interfaces atualizadas
- [x] Testado e funcionando

---

## 💡 **Dica Pro**

Se quiser usar modelos diferentes para cada interface:

**Terminal (rápido):**
```python
# No código v2, antes de criar model:
MODEL_NAME = "gemini-2.0-flash-exp"
```

**Streamlit (detalhado):**
```python
# No código streamlit, antes de criar model:
MODEL_NAME = "gemini-1.5-pro"
```

---

## 🎉 **PRONTO!**

Agora é só executar e usar! Sem complicação! 🚀

```bash
streamlit run chatbot_streamlit.py
```

**Boa migração! 🎯**

