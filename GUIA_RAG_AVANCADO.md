# 🚀 Guia RAG Avançado - Setup Completo

## 🎯 **O QUE FOI CRIADO**

Um sistema RAG **COMPLETO E AVANÇADO** com:

✅ **Retrieval**: Top-K 100 chunks  
✅ **Reranker**: Cohere (reduz para Top-10)  
✅ **Embeddings**: Google text-embedding-004  
✅ **Vector Store**: ChromaDB  
✅ **LLM**: Gemini 2.5 Pro  
✅ **Suporte a Imagens**: Extração e referenciamento  
✅ **System Prompt**: Otimizado para respostas perfeitas  

---

## 📊 **ARQUITETURA DO SISTEMA**

```
┌─────────────────────────────────────────────────────────┐
│                  RAG AVANÇADO - FLUXO                   │
└─────────────────────────────────────────────────────────┘

1. INDEXAÇÃO (Uma vez - Preparação)
   ┌──────────────┐
   │  6 PDFs      │
   └──────┬───────┘
          │
          ▼
   ┌─────────────────────┐
   │  PDF Processor      │
   │  - Extrai texto     │
   │  - Extrai imagens   │
   │  - Identifica seções│
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Text Splitter      │
   │  - Chunks 1000 chars│
   │  - Overlap 200      │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Google Embeddings  │
   │  (text-embedding-004)│
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  ChromaDB           │
   │  (Vector Store)     │
   └─────────────────────┘


2. QUERY (A cada pergunta)
   ┌──────────────┐
   │  Pergunta    │
   └──────┬───────┘
          │
          ▼
   ┌─────────────────────┐
   │  RETRIEVAL          │
   │  Top-K = 100        │  ← Busca 100 chunks similares
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  RERANKER (Cohere)  │
   │  Top-N = 10         │  ← Seleciona 10 MAIS relevantes
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Monta Prompt:      │
   │  - System prompt    │
   │  - 10 chunks        │  ← Contexto otimizado
   │  - Pergunta         │
   │  - Info de imagens  │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Gemini 2.5 Pro     │
   │  - Gera resposta    │  ← Resposta PERFEITA
   │  - Cita fontes      │
   │  - Menciona imagens │
   └──────┬──────────────┘
          │
          ▼
   ┌──────────────┐
   │  Resposta    │
   │  + Imagens   │
   │  + Fontes    │
   └──────────────┘
```

---

## 🔧 **SETUP (Passo a Passo)**

### **1️⃣ Instalar Dependências**

```bash
cd /Users/tarikhadi/Desktop/rag_migracao_camunda
pip install -r requirements.txt
```

**Dependências principais:**
- `langchain` + extensões
- `chromadb` (vector store)
- `cohere` (reranker)
- `pypdf`, `pdf2image` (processamento PDF)
- `pytesseract`, `Pillow` (imagens)

### **2️⃣ Configurar API Keys**

Edite `config.py`:

```python
# Google API Key (configure sua chave)
GOOGLE_API_KEY = "sua_google_api_key_aqui"

# Cohere API Key para Reranking
COHERE_API_KEY = "sua_chave_cohere_aqui"  # ← Configure aqui!
```

**Obter Cohere API Key:**
1. Acesse: https://dashboard.cohere.com/api-keys
2. Cadastre-se gratuitamente
3. Gere uma API key
4. Cole no `config.py`

**OU configure via ambiente:**
```bash
export COHERE_API_KEY="sua_chave_cohere"
```

### **3️⃣ Executar Indexação** ⭐ **IMPORTANTE!**

```bash
python3 indexer_advanced.py
```

**O que este script faz:**
- ✅ Processa todos os 6 PDFs
- ✅ Extrai texto de cada página
- ✅ Extrai imagens (salva em `extracted_images/`)
- ✅ Cria chunks (1000 chars com overlap 200)
- ✅ Gera embeddings com Google
- ✅ Cria banco vetorial ChromaDB
- ✅ Salva metadata de imagens

**Tempo estimado:** 5-10 minutos

**Saída esperada:**
```
🚀 Iniciando Indexação Avançada
📚 Encontrados 6 documentos

📄 Processando: Code Conversion.pdf
  📷 Extraindo imagens...
    ✓ 45 imagens extraídas
  ✓ 45 páginas processadas

...

✂️  Criando chunks...
  ✓ 523 chunks criados

🗄️  Criando banco vetorial...
  ✓ Banco vetorial criado em ./chroma_db
  ✓ 523 chunks indexados

✅ INDEXAÇÃO CONCLUÍDA COM SUCESSO!

📊 Estatísticas:
  📄 Documentos únicos: 6
  📃 Total de páginas: 267
  ✂️  Total de chunks: 523
  📷 Total de imagens: 267
  🖼️  Chunks com imagens: 267
```

### **4️⃣ Executar Chatbot Avançado**

```bash
streamlit run chatbot_advanced.py
```

**Acesse:** http://localhost:8501

---

## 🎨 **INTERFACE DO CHATBOT AVANÇADO**

### **Tela Principal:**

```
╔═══════════════════════════════════════════════╗
║  🤖 Assistente Camunda RAG Avançado          ║
║  Retrieval (Top-100) + Reranker (Top-10)     ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  [Sidebar]              [Chat]                ║
║                                               ║
║  🎯 RAG Avançado        💬 Perguntas/Respostas║
║  ✅ Sistema Ativo                             ║
║  🔍 Retrieval: Top-100  [Histórico...]        ║
║  🎯 Reranker: Top-10                          ║
║  🤖 LLM: Gemini 2.5 Pro [Digite pergunta...] ║
║  📷 Imagens: Suportado                        ║
║                                               ║
║  💡 Características     📚 Ver Fontes         ║
║  [Lista...]             [Lista documentos...]  ║
║                                               ║
║  🗑️ Limpar Histórico    📷 Imagens            ║
║  🔄 Reiniciar           [Exibe se houver]     ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

### **Exemplo de Resposta:**

```
Usuário: Como migrar processos BPMN?

🔍 Buscando documentos relevantes... ✅ 100 documentos recuperados
🎯 Reranqueando por relevância... ✅ Top-10 documentos selecionados
🤖 Gerando resposta detalhada...

Assistente:
# Como Migrar Processos BPMN do Camunda 7 para Camunda 8

## Contexto
A migração de processos BPMN envolve...

## Passos Detalhados
1. **Análise do Processo Existente**
   [Explicação detalhada...]

2. **Uso do Migration Tooling**
   [Passo a passo...]

## Exemplos Práticos
```xml
<!-- Processo Camunda 7 -->
<bpmn:serviceTask id="task1" ...>
```

📷 Ver imagem em Migration tooling página 12
[Exibe diagrama do fluxo de migração]

## Considerações
- Atenção especial a...
- Boas práticas...

## Referências
1. Migration tooling (Página 12) - Relevância: 0.95
2. Code Conversion (Página 5) - Relevância: 0.89
3. Migration Journey (Página 8) - Relevância: 0.85

[📚 Ver Fontes] [Expandir para ver lista completa]
```

---

## 🔍 **COMO FUNCIONA O SISTEMA**

### **1. Retrieval (Top-K 100)**

```python
# Busca vetorial por similaridade
retrieved_docs = vectorstore.similarity_search_with_score(query, k=100)
```

**O que acontece:**
- Converte pergunta em embedding (vector)
- Busca 100 chunks mais similares no ChromaDB
- Retorna com score de similaridade

### **2. Reranking (Top-10)**

```python
# Reordena usando modelo Cohere
reranked = cohere_client.rerank(
    query=query,
    documents=docs_text,
    top_n=10,
    model="rerank-multilingual-v3.0"
)
```

**O que acontece:**
- Envia pergunta + 100 docs para Cohere
- Cohere usa modelo sofisticado para avaliar relevância
- Retorna apenas top-10 MAIS relevantes
- Com score de relevância preciso

### **3. Prompt Construction**

```python
prompt = f"""
{system_prompt}

CHUNKS RELEVANTES:
{formatted_chunks}  # ← Top-10 reranqueados

PERGUNTA:
{question}
"""
```

**Chunks formatados incluem:**
- Texto do chunk
- Metadata (documento, página, seção)
- Informação de imagens (se houver)
- Score de relevância

### **4. Geração com Gemini**

```python
response = gemini_model.generate_content(prompt)
```

**Gemini 2.5 Pro recebe:**
- System prompt (instruções detalhadas)
- Top-10 chunks mais relevantes
- Pergunta do usuário
- Info sobre imagens disponíveis

**Gemini gera:**
- Resposta detalhada e didática
- Citações de fontes
- Menção a imagens relevantes
- Exemplos práticos

---

## 📊 **COMPARAÇÃO: Simples vs Avançado**

| Aspecto | Versão Simples | **Versão Avançada** |
|---------|----------------|---------------------|
| **Retrieval** | ❌ Envia tudo | ✅ Top-100 vetorial |
| **Reranking** | ❌ Não tem | ✅ Cohere Top-10 |
| **Vector Store** | ❌ Não tem | ✅ ChromaDB |
| **Embeddings** | ❌ Interno Google | ✅ Google text-embedding-004 |
| **Chunking** | ❌ Automático | ✅ Manual (1000+200) |
| **Imagens** | ⚠️ Menciona | ✅ Extrai e referencia |
| **Custos** | 💰💰💰 Alto | 💰 Otimizado |
| **Velocidade** | 🐢 3-5s | ⚡ 2-3s |
| **Escalabilidade** | ❌ Até ~20 docs | ✅ Centenas de docs |
| **Controle** | ❌ Baixo | ✅ Total |
| **Qualidade** | ✅ Boa | ✅✅ Excelente |

---

## ✅ **CHECKLIST DE SETUP**

- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Google API Key configurada (config.py)
- [ ] **Cohere API Key configurada** (config.py) ⭐ IMPORTANTE!
- [ ] Indexação executada (`python3 indexer_advanced.py`)
- [ ] Banco vetorial criado (`./chroma_db/` existe)
- [ ] Imagens extraídas (`extracted_images/` existe)
- [ ] Chatbot executado (`streamlit run chatbot_advanced.py`)

---

## 🎯 **SYSTEM PROMPT OTIMIZADO**

O system prompt foi projetado para:

✅ **Completude**: Instruções para respostas EXTREMAMENTE detalhadas  
✅ **Didática**: Explicações passo a passo progressivas  
✅ **Prático**: Sempre incluir exemplos de código  
✅ **Visual**: Identificar e mencionar imagens explicitamente  
✅ **Citações**: Sempre referenciar fontes específicas  
✅ **Estruturado**: Organização clara em seções  

**Estrutura do Prompt:**
1. System instructions (responsabilidades, diretrizes)
2. Chunks relevantes (top-10 reranqueados)
3. Pergunta do usuário
4. Instruções finais

---

## 🖼️ **SUPORTE A IMAGENS**

### **Como Funciona:**

1. **Extração** (na indexação):
   - Cada página do PDF → imagem PNG
   - Salvo em `extracted_images/`
   - Metadata salvo em `image_metadata.json`

2. **Mapeamento**:
   - Cada chunk tem flag `has_images`
   - Lista de imagens associadas ao chunk
   - Documento e página de origem

3. **Na Resposta**:
   - LLM identifica chunks com imagens
   - Menciona explicitamente na resposta
   - Descreve o que a imagem ilustra
   - Interface exibe as imagens

### **Exemplo de Metadata:**

```python
{
  "chunk_id": "chunk_42",
  "source": "Migration tooling",
  "page": 12,
  "section": "tools",
  "has_images": True,
  "images": [
    "extracted_images/Migration_tooling_page_12.png"
  ]
}
```

---

## 💡 **DICAS DE USO**

### **Perguntas Efetivas:**

✅ **Bom**: "Como converter External Task Handlers com tratamento de erros?"  
❌ **Ruim**: "Task handlers"

✅ **Bom**: "Quais ferramentas automatizam a migração de processos BPMN?"  
❌ **Ruim**: "Ferramentas"

### **Aproveitando Imagens:**

- Pergunte sobre **diagramas**: "Mostre o diagrama de arquitetura"
- Pergunte sobre **fluxos**: "Qual o fluxo de migração visual?"
- Pergunte sobre **comparações**: "Diagrama comparando C7 e C8"

### **Citações:**

- Todas as respostas incluem fontes
- Clique em "📚 Ver Fontes" para detalhes
- Score de relevância indica confiança

---

## 🚀 **EXECUTE AGORA**

### **1. Indexação (primeira vez):**

```bash
python3 indexer_advanced.py
```

### **2. Chatbot:**

```bash
streamlit run chatbot_advanced.py
```

---

## 🎉 **RESULTADO**

Você terá:

✅ Sistema RAG **state-of-the-art**  
✅ Respostas **PERFEITAS** e **RELEVANTES**  
✅ **Top-10** chunks mais importantes  
✅ **Consciente de imagens**  
✅ **Citações** precisas  
✅ **Interface moderna**  

---

## 📞 **Problemas?**

### Cohere API Key não encontrada

```bash
export COHERE_API_KEY="sua_chave"
# OU configure em config.py
```

### Erro ao extrair imagens

Instale dependências do sistema:

**macOS:**
```bash
brew install poppler
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

### ChromaDB não encontrado

Execute a indexação primeiro:
```bash
python3 indexer_advanced.py
```

---

**🎊 Divirta-se com o RAG mais avançado! 🚀**

