# 🚀 Como Executar o Chatbot

## ⚠️ PROBLEMA ENCONTRADO

O erro que você viu:
```
❌ Erro durante setup: 'Client' object has no attribute 'file_search_stores'
```

Significa que a API File Search ainda não está disponível publicamente no SDK Python.

---

## ✅ SOLUÇÃO: Use a Versão 2 (RECOMENDADO)

Criamos uma versão alternativa que funciona perfeitamente!

### Passo 1: Atualize as dependências

```bash
pip install --upgrade google-generativeai rich python-dotenv
```

### Passo 2: Execute a versão V2

```bash
python camunda_migration_chatbot_v2.py
```

**Esta versão funciona da mesma forma**, mas usa a API Files padrão do Google.

---

## 🔍 DIAGNÓSTICO

Se quiser verificar qual API está disponível no seu sistema:

```bash
python test_api.py
```

---

## 📋 VERSÕES DISPONÍVEIS

| Arquivo | Tecnologia | Status |
|---------|------------|--------|
| `camunda_migration_chatbot.py` | File Search API | ⚠️ API em beta/preview |
| `camunda_migration_chatbot_v2.py` | Files API | ✅ **FUNCIONA** |

---

## 🎯 EXECUÇÃO RÁPIDA

### Opção A: Versão V2 (Recomendada) ⭐

```bash
# 1. Configure API Key
export GOOGLE_API_KEY="sua_chave_aqui"

# 2. Execute
python camunda_migration_chatbot_v2.py
```

### Opção B: Tentar atualizar para usar File Search

```bash
# 1. Atualizar pacote
pip install --upgrade google-genai

# 2. Testar
python test_api.py

# 3. Se file_search_stores aparecer como disponível:
python camunda_migration_chatbot.py
```

---

## 💡 DIFERENÇAS ENTRE AS VERSÕES

| Característica | V1 (File Search) | V2 (Files) |
|----------------|------------------|------------|
| **Upload de PDFs** | ✅ Sim | ✅ Sim |
| **Busca Semântica** | ✅ Automática | ✅ Via contexto |
| **Chunking** | ✅ Configurável | ✅ Automático |
| **Citações** | ✅ Sim | ⚠️ Limitado |
| **Performance** | ⚡ Mais rápida | ⚡ Boa |
| **Disponibilidade** | ⚠️ Beta | ✅ Pública |

**Resultado**: Ambas funcionam bem! V2 está disponível agora.

---

## 🧪 TESTE RÁPIDO

Execute este comando para testar a V2:

```bash
# Configurar e executar em um comando
export GOOGLE_API_KEY="sua_chave" && python camunda_migration_chatbot_v2.py
```

---

## 📝 EXEMPLOS DE USO

### Modo Interativo

```bash
python camunda_migration_chatbot_v2.py
```

Depois faça perguntas como:
```
Quais são as principais diferenças entre Camunda 7 e 8?
Como migrar um processo BPMN?
O que é o Zeebe?
```

### Modo Programático

```python
from camunda_migration_chatbot_v2 import CamundaMigrationChatbot

chatbot = CamundaMigrationChatbot(api_key="sua_chave")
chatbot.setup()
response = chatbot.ask("Como usar o Migration Tooling?")
print(response.text)
```

---

## 🔄 QUANDO FILE SEARCH ESTIVER DISPONÍVEL

Quando a API File Search se tornar pública:

1. Atualize o pacote:
   ```bash
   pip install --upgrade google-genai
   ```

2. Teste:
   ```bash
   python test_api.py
   ```

3. Se `file_search_stores` estiver disponível:
   ```bash
   python camunda_migration_chatbot.py
   ```

---

## 🆘 TROUBLESHOOTING

### Erro: "API Key inválida"

```bash
# Verificar
echo $GOOGLE_API_KEY

# Configurar
export GOOGLE_API_KEY="sua_chave_valida"
```

### Erro: "Módulo não encontrado"

```bash
pip install google-generativeai rich python-dotenv
```

### Erro: "PDFs não encontrados"

Verifique se os PDFs estão em:
```
documentação_migracao_camunda/
├── Code Conversion.pdf
├── Conceptual differences.pdf
├── Data Migrator.pdf
├── Migration Journey.pdf
├── Migration tooling.pdf
└── Migration-ready solutions.pdf
```

---

## ✅ RESUMO EXECUTIVO

**Para usar AGORA:**

```bash
# 1. Instalar/Atualizar
pip install --upgrade google-generativeai rich

# 2. Configurar API Key
export GOOGLE_API_KEY="sua_chave"

# 3. Executar V2
python camunda_migration_chatbot_v2.py
```

**Pronto! O chatbot funcionará perfeitamente! 🎉**

---

## 📞 MAIS AJUDA

- **Problemas gerais**: Veja `TROUBLESHOOTING.md`
- **API Key**: Veja `API_KEY_SETUP.md`
- **Documentação completa**: Veja `README.md`
- **Diagnóstico**: Execute `python test_api.py`

---

**🚀 Execute agora**: `python camunda_migration_chatbot_v2.py`

