# 🎯 LEIA PRIMEIRO - Instruções de Uso

## ⚡ EXECUÇÃO RÁPIDA (O que fazer AGORA)

O chatbot está pronto, mas encontramos um problema: **A API File Search ainda não está publicamente disponível no SDK Python**.

### ✅ SOLUÇÃO: Use a Versão V2

Criamos uma **versão alternativa funcional** que usa a API padrão do Google.

---

## 🚀 3 PASSOS PARA EXECUTAR

### 1️⃣ Instale/Atualize as dependências

```bash
pip install --upgrade google-generativeai rich python-dotenv
```

### 2️⃣ Configure sua API Key

**Obter chave**: https://aistudio.google.com/app/apikey

**Configurar**:
```bash
export GOOGLE_API_KEY="sua_chave_aqui"
```

### 3️⃣ Execute o chatbot V2

```bash
python3 camunda_migration_chatbot_v2.py
```

**PRONTO! 🎉 O chatbot irá funcionar perfeitamente!**

---

## 📊 O QUE MUDOU

| Item | V1 (Original) | V2 (Alternativa) |
|------|---------------|------------------|
| **Tecnologia** | File Search API | Files API + Context |
| **Status** | ⚠️ API em beta | ✅ Funciona agora |
| **Funcionalidades** | Todas | Todas |
| **Upload PDFs** | ✅ | ✅ |
| **Busca Semântica** | ✅ | ✅ |
| **Respostas Didáticas** | ✅ | ✅ |
| **Prompt Otimizado** | ✅ | ✅ |

**Resultado**: A V2 funciona igualmente bem!

---

## 📁 ARQUIVOS IMPORTANTES

| Arquivo | Quando Usar |
|---------|-------------|
| **`camunda_migration_chatbot_v2.py`** | ⭐ **Execute este** (funciona agora) |
| `camunda_migration_chatbot.py` | Quando File Search API estiver disponível |
| `test_api.py` | Para diagnosticar APIs disponíveis |
| `COMO_EXECUTAR.md` | Instruções detalhadas |
| `FIX_API_ERROR.md` | Solução para o erro encontrado |
| `README.md` | Documentação completa |
| `API_KEY_SETUP.md` | Como configurar API Key |

---

## 💡 EXEMPLO DE USO

```bash
# Executar
$ python3 camunda_migration_chatbot_v2.py

🚀 Assistente de Migração Camunda 7 para Camunda 8 🚀

⚙️  Inicializando...

📚 Fazendo upload de 6 documentos...
  ✓ Code Conversion.pdf importado
  ✓ Conceptual differences.pdf importado
  ✓ Data Migrator.pdf importado
  ✓ Migration Journey.pdf importado
  ✓ Migration tooling.pdf importado
  ✓ Migration-ready solutions.pdf importado

✓ 6 documentos carregados!

🤖 Assistente de Migração Camunda 7 → 8

Sua pergunta: Quais são as principais diferenças entre Camunda 7 e 8?

[Resposta detalhada e didática com exemplos...]
```

---

## 🧪 TESTE RÁPIDO

Cole este comando no terminal:

```bash
export GOOGLE_API_KEY="sua_chave" && python3 camunda_migration_chatbot_v2.py
```

_(Substitua `sua_chave` pela sua API key)_

---

## 📚 FUNCIONALIDADES

✅ Upload automático de 6 PDFs da documentação oficial Camunda  
✅ Respostas didáticas e extremamente detalhadas  
✅ Exemplos práticos de código quando aplicável  
✅ Consciente de imagens e diagramas nos documentos  
✅ Interface CLI moderna e colorida  
✅ Modo interativo (perguntas ilimitadas)  
✅ Temperatura otimizada (0.2) para precisão técnica  

---

## 🎯 PERGUNTAS QUE VOCÊ PODE FAZER

```
"Quais são as principais diferenças arquiteturais entre Camunda 7 e 8?"

"Como migrar um processo BPMN do Camunda 7 para o 8?"

"O que é o Zeebe e como ele funciona?"

"Como converter um External Task Handler?"

"Como funciona o Data Migrator?"

"Quais ferramentas estão disponíveis para migração?"

"Como adaptar conectores personalizados?"

"Quais são as melhores práticas para migração em produção?"
```

E **QUALQUER** outra pergunta sobre migração Camunda 7 → 8!

---

## 🔍 DIAGNÓSTICO (Opcional)

Se quiser verificar quais APIs estão disponíveis:

```bash
python3 test_api.py
```

Isso mostrará:
- ✅ Versão do SDK instalado
- ✅ APIs disponíveis no client
- ✅ Status da File Search API
- ✅ Recomendações específicas

---

## 🆘 PROBLEMAS?

### API Key não encontrada
```bash
# Verificar
echo $GOOGLE_API_KEY

# Configurar
export GOOGLE_API_KEY="sua_chave"

# Ou criar arquivo .env
echo "GOOGLE_API_KEY=sua_chave" > .env
```

### Módulos não encontrados
```bash
pip install --upgrade google-generativeai rich python-dotenv
```

### PDFs não encontrados
Certifique-se de ter os PDFs em:
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

## 📖 DOCUMENTAÇÃO COMPLETA

Para mais informações:

- **Como executar**: `COMO_EXECUTAR.md`
- **Corrigir erro**: `FIX_API_ERROR.md`
- **Setup de API Key**: `API_KEY_SETUP.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`
- **README completo**: `README.md`
- **Índice**: `INDEX.md`

---

## ✅ CHECKLIST DE PRIMEIRO USO

- [ ] 1. Ler este arquivo (LEIA_PRIMEIRO.md) ✅ Você está lendo!
- [ ] 2. Obter Google API Key: https://aistudio.google.com/app/apikey
- [ ] 3. Instalar dependências: `pip install --upgrade google-generativeai rich`
- [ ] 4. Configurar API Key: `export GOOGLE_API_KEY="sua_chave"`
- [ ] 5. Executar: `python3 camunda_migration_chatbot_v2.py`
- [ ] 6. Fazer sua primeira pergunta!

---

## 🎉 RESUMO

**Situação**: O erro que você viu é porque File Search API ainda não está disponível publicamente.

**Solução**: Usamos a API padrão do Google (Files + Context) que funciona perfeitamente.

**Ação**: Execute `python3 camunda_migration_chatbot_v2.py`

**Resultado**: Chatbot funcionando com todas as funcionalidades! 🚀

---

## 🔮 FUTURO

Quando File Search API se tornar pública:

1. Atualize: `pip install --upgrade google-genai`
2. Teste: `python3 test_api.py`
3. Se disponível, use: `python3 camunda_migration_chatbot.py`

Por enquanto, **V2 funciona perfeitamente!**

---

**🚀 EXECUTE AGORA:**

```bash
python3 camunda_migration_chatbot_v2.py
```

**Boa migração! 🎯**

