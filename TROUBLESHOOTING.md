# 🔧 Troubleshooting - Camunda Migration Assistant

Guia para resolver problemas comuns ao usar o chatbot.

## 🚨 Problemas Comuns

### 1. Erro: "GOOGLE_API_KEY não encontrada"

**Sintoma:**
```
❌ GOOGLE_API_KEY não encontrada!
```

**Soluções:**

**A. Configurar via variável de ambiente:**
```bash
# macOS/Linux
export GOOGLE_API_KEY="sua_chave_aqui"

# Windows (CMD)
set GOOGLE_API_KEY=sua_chave_aqui

# Windows (PowerShell)
$env:GOOGLE_API_KEY="sua_chave_aqui"
```

**B. Criar arquivo .env:**
```bash
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env
```

**C. Passar diretamente no código:**
```python
chatbot = CamundaMigrationChatbot(api_key="sua_chave_aqui")
```

**Obter API Key:**
1. Acesse: https://aistudio.google.com/app/apikey
2. Faça login com conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

---

### 2. Erro: ModuleNotFoundError

**Sintoma:**
```
ModuleNotFoundError: No module named 'google.genai'
```
ou
```
ModuleNotFoundError: No module named 'rich'
```

**Solução:**
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Ou instalar individualmente
pip install google-genai rich python-dotenv

# Se usar ambiente virtual, certifique-se de ativá-lo primeiro
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

### 3. Erro: "Nenhum PDF encontrado"

**Sintoma:**
```
❌ Nenhum PDF encontrado em documentação_migracao_camunda/
```

**Verificações:**
1. Confirme que a pasta existe:
```bash
ls documentação_migracao_camunda/
```

2. Verifique se há PDFs na pasta:
```bash
ls documentação_migracao_camunda/*.pdf
```

3. Estrutura esperada:
```
rag_migracao_camunda/
└── documentação_migracao_camunda/
    ├── Code Conversion.pdf
    ├── Conceptual differences.pdf
    ├── Data Migrator.pdf
    ├── Migration Journey.pdf
    ├── Migration tooling.pdf
    └── Migration-ready solutions.pdf
```

**Solução:**
Se os arquivos estiverem em outro local, mova-os para a pasta correta ou ajuste o caminho no código.

---

### 4. Erro: API Rate Limit

**Sintoma:**
```
Error 429: Rate limit exceeded
```
ou
```
Quota exceeded for quota metric 'Generate requests'
```

**Causas:**
- Muitas requisições em pouco tempo
- Limite gratuito da API atingido

**Soluções:**
1. **Aguarde**: Respeite os limites de taxa
2. **Verifique cotas**: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
3. **Configure faturamento**: Para limites maiores, configure billing no Google Cloud
4. **Use temperatura mais baixa**: Já configurado em `temperature=0.2`

---

### 5. Erro: API Key inválida

**Sintoma:**
```
Error 401: Invalid API key
```
ou
```
Error 403: Permission denied
```

**Verificações:**
1. API Key está correta (sem espaços extras)
2. API está ativada: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
3. Billing configurado (se necessário)

**Solução:**
```bash
# Verificar API key atual
echo $GOOGLE_API_KEY

# Gerar nova API key
# Acesse: https://aistudio.google.com/app/apikey
```

---

### 6. Erro: Timeout durante upload

**Sintoma:**
```
TimeoutError: Operation timed out
```

**Causas:**
- Conexão instável
- PDFs muito grandes
- Servidor sobrecarregado

**Soluções:**
1. **Aumentar timeout**:
```python
# Em camunda_migration_chatbot.py, ajuste o tempo de espera
while not operation.done:
    time.sleep(5)  # Aumentar este valor
    operation = self.client.operations.get(operation)
```

2. **Verificar conexão**:
```bash
ping google.com
```

3. **Upload individual**:
Faça upload de um PDF por vez para identificar problemas.

---

### 7. Erro: Resposta vazia ou incompleta

**Sintoma:**
- Chatbot retorna resposta muito curta
- Resposta não relacionada à pergunta
- Nenhuma citação aparece

**Causas:**
- Pergunta muito vaga
- Documentação não foi indexada corretamente
- Chunks não contêm informação relevante

**Soluções:**
1. **Seja mais específico**:
```python
# ❌ Vago
"Me fale sobre Camunda"

# ✅ Específico
"Quais são as diferenças entre a arquitetura do Camunda 7 e Camunda 8?"
```

2. **Refaça o setup**:
```python
# Deleta o store anterior e cria novo
chatbot.setup()
```

3. **Ajuste o chunking**:
Modifique os parâmetros em `upload_documentation()`:
```python
'max_tokens_per_chunk': 500,  # Aumentar para mais contexto
'max_overlap_tokens': 100      # Aumentar para melhor continuidade
```

---

### 8. Erro: Rich não exibe corretamente

**Sintoma:**
- Caracteres estranhos no terminal
- Formatação quebrada
- Cores não aparecem

**Soluções:**

1. **Terminal compatível**:
Use terminal moderno (iTerm2, Windows Terminal, etc.)

2. **Forçar modo simples**:
```python
# No início do arquivo camunda_migration_chatbot.py
console = Console(force_terminal=False)  # Desabilita formatação rica
```

3. **Alternativa**:
Use o notebook Jupyter (`chatbot_notebook.ipynb`) que tem melhor suporte de formatação.

---

### 9. Problema: Upload muito lento

**Sintoma:**
Upload dos PDFs demora muito (> 10 minutos)

**Verificações:**
1. **Tamanho dos PDFs**:
```bash
du -sh documentação_migracao_camunda/*.pdf
```

2. **Velocidade da internet**:
```bash
curl -o /dev/null http://speedtest.wdc01.softlayer.com/downloads/test10.zip
```

**Otimizações:**
1. **Upload em paralelo** (avançado):
Modifique `upload_documentation()` para usar threading

2. **Cache local**:
Após primeiro upload, anote o `file_search_store.name` e reutilize:
```python
chatbot.file_search_store = chatbot.client.file_search_stores.get(
    name='fileSearchStores/seu-store-id'
)
```

---

### 10. Erro: ImportError ao importar chatbot

**Sintoma:**
```
ImportError: cannot import name 'CamundaMigrationChatbot'
```

**Soluções:**
1. **Verifique o arquivo**:
```bash
ls camunda_migration_chatbot.py
```

2. **Python path**:
```python
import sys
print(sys.path)
```

3. **Execute do diretório correto**:
```bash
cd /Users/tarikhadi/Desktop/rag_migracao_camunda
python camunda_migration_chatbot.py
```

---

## 🛠️ Ferramentas de Diagnóstico

### Script de Verificação

Execute o script de setup para diagnóstico automático:

```bash
python setup.py
```

Este script verifica:
- ✅ Versão do Python
- ✅ Dependências instaladas
- ✅ Documentação presente
- ✅ API Key configurada
- ✅ Importação do chatbot

### Verificação Manual

```python
# Test básico
import os
from camunda_migration_chatbot import CamundaMigrationChatbot

# 1. Verificar API Key
print("API Key:", "✅ Configurada" if os.environ.get('GOOGLE_API_KEY') else "❌ Não configurada")

# 2. Verificar importação
print("Importação: ✅")

# 3. Inicializar chatbot
try:
    chatbot = CamundaMigrationChatbot()
    print("Chatbot: ✅ Inicializado")
except Exception as e:
    print(f"Chatbot: ❌ {e}")
```

---

## 📊 Logs e Debugging

### Habilitar logs detalhados

```python
import logging

# No início do script
logging.basicConfig(level=logging.DEBUG)
```

### Inspecionar resposta

```python
response = chatbot.ask("Sua pergunta")

if response:
    print("=== DEBUG INFO ===")
    print(f"Texto: {response.text[:100]}...")
    print(f"Candidates: {len(response.candidates)}")
    
    if response.candidates:
        candidate = response.candidates[0]
        print(f"Finish reason: {candidate.finish_reason}")
        print(f"Grounding metadata: {hasattr(candidate, 'grounding_metadata')}")
```

---

## 🆘 Ainda com Problemas?

### 1. Verifique versões

```bash
python --version          # Deve ser 3.8+
pip show google-genai     # Versão da biblioteca
pip show rich             # Versão da biblioteca
```

### 2. Reinstale do zero

```bash
# Remove ambiente virtual
rm -rf venv

# Cria novo ambiente
python3 -m venv venv
source venv/bin/activate

# Reinstala dependências
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Teste em ambiente limpo

```bash
# Clone ou baixe novamente o projeto
# Configure API key
# Execute setup.py
python setup.py
```

### 4. Recursos Externos

- **Google AI Documentation**: https://ai.google.dev/docs
- **Google Cloud Console**: https://console.cloud.google.com/
- **File Search API Docs**: https://ai.google.dev/gemini-api/docs/file-search
- **Rich Library**: https://rich.readthedocs.io/

---

## 💡 Dicas de Prevenção

1. **Sempre use ambiente virtual**
2. **Mantenha API key segura** (nunca commite no Git)
3. **Monitore cotas da API**
4. **Faça backup do store name** após primeiro setup
5. **Use versões estáveis das dependências**
6. **Teste perguntas simples primeiro**

---

**Se o problema persistir, revise os logs, tente o exemplo básico em `example_usage.py`, ou consulte a documentação oficial da Google AI API.**

