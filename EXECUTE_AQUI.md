# 🚀 EXECUTE AQUI - Guia Rápido

## ⚡ EXECUÇÃO RÁPIDA

### 🌐 **INTERFACE WEB (Streamlit) - RECOMENDADO** ⭐

```bash
cd /caminho/para/rag_migracao_camunda
export GOOGLE_API_KEY="sua_google_api_key_aqui"
streamlit run chatbot_streamlit.py
```

**OU use o script:**

```bash
./run_streamlit.sh
```

**Depois acesse**: http://localhost:8501

---

### 💻 **INTERFACE TERMINAL (CLI)**

```bash
cd /caminho/para/rag_migracao_camunda
export GOOGLE_API_KEY="sua_google_api_key_aqui"
python3 camunda_migration_chatbot_v2.py
```

---

## 🎯 O QUE CADA INTERFACE OFERECE

### **🌐 Streamlit (Web)**
- ✅ Interface visual moderna
- ✅ Chat estilo ChatGPT
- ✅ Botões de sugestão
- ✅ Histórico visual
- ✅ Fácil para não-técnicos
- ✅ Sidebar com informações
- ✅ Markdown renderizado lindamente

### **💻 Terminal (CLI)**
- ✅ Interface colorida (Rich)
- ✅ Rápida e leve
- ✅ Boa para desenvolvedores
- ✅ Markdown formatado
- ✅ Citações destacadas

---

## ⚠️ IMPORTANTE - SEGURANÇA

A API Key no comando acima foi **exposta publicamente**. 

**AÇÃO RECOMENDADA:**

1. **Regenere sua chave** AGORA:
   - Acesse: https://aistudio.google.com/app/apikey
   - Delete a chave atual
   - Crie uma nova

2. **Configure corretamente**:
   ```bash
   # Crie arquivo .env
   echo "GOOGLE_API_KEY=sua_nova_chave" > .env
   ```

3. **Execute sem expor**:
   ```bash
   # A aplicação lerá do .env
   streamlit run chatbot_streamlit.py
   ```

---

## 📊 COMPARAÇÃO

| Item | Terminal | Streamlit Web |
|------|----------|---------------|
| **Setup** | Imediato | 2-3 min upload |
| **UX** | Boa | Excelente |
| **Visual** | CLI colorido | Interface gráfica |
| **Para** | Desenvolvedores | Todos |
| **Compartilhar** | Difícil | Fácil |

---

## 🎨 INTERFACE STREAMLIT

Quando executar, você verá:

```
╔═══════════════════════════════════════════════╗
║  🤖 Assistente Migração Camunda 7 → 8        ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  [Sidebar]         [Chat]                     ║
║                                               ║
║  📊 Status         💬 Converse aqui           ║
║  ✅ 6 docs         👤 Usuário                 ║
║                    🤖 Assistente              ║
║  📚 Docs           [Digite pergunta...]       ║
║  💡 Exemplos                                  ║
║  🗑️ Limpar                                    ║
║  🔄 Reiniciar                                 ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

## 💡 PERGUNTAS QUE FUNCIONAM

```
Quais as principais diferenças entre Camunda 7 e 8?

Como migrar um processo BPMN?

O que é o Zeebe?

Como converter External Task Handlers?

Como funciona o Data Migrator?

Quais ferramentas disponíveis para migração?

Como adaptar conectores personalizados?

Quais as melhores práticas de migração?
```

**E QUALQUER outra pergunta sobre migração!**

---

## 🐛 PROBLEMAS?

### Erro: Porta em uso
```bash
streamlit run chatbot_streamlit.py --server.port 8502
```

### Erro: Streamlit não encontrado
```bash
pip install streamlit
```

### Erro: API Key inválida
- Regenere em: https://aistudio.google.com/app/apikey
- Configure: `export GOOGLE_API_KEY="nova_chave"`

---

## 📚 MAIS AJUDA

- **Guia Streamlit**: `STREAMLIT_GUIDE.md`
- **Como executar**: `COMO_EXECUTAR.md`
- **Leia primeiro**: `LEIA_PRIMEIRO.md`
- **README completo**: `README.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`

---

## ✅ STATUS ATUAL

✅ **Terminal funcionando** - Testado com sucesso!  
✅ **Streamlit criado** - Pronto para usar!  
✅ **6 PDFs carregados** - Documentação completa!  
✅ **Respostas didáticas** - Prompt otimizado!  

---

## 🚀 EXECUTE AGORA

**Recomendado (Web):**
```bash
streamlit run chatbot_streamlit.py
```

**Alternativa (Terminal):**
```bash
python3 camunda_migration_chatbot_v2.py
```

---

**🎉 Divirta-se migrando para Camunda 8!**

