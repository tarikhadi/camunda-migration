# 🚀 Quick Start - Camunda Migration Assistant

## Configuração em 3 Passos

### 1️⃣ Instalar Dependências

```bash
# Criar ambiente virtual (opcional mas recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar pacotes
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key

**Obter API Key:**
1. Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

**Configurar (escolha uma opção):**

**Opção A - Variável de ambiente:**
```bash
export GOOGLE_API_KEY="sua_api_key_aqui"
```

**Opção B - Arquivo .env:**
```bash
# Crie o arquivo
echo "GOOGLE_API_KEY=sua_api_key_aqui" > .env
```

### 3️⃣ Executar o Chatbot

```bash
python camunda_migration_chatbot.py
```

## ✅ Pronto!

Agora você pode fazer qualquer pergunta sobre migração Camunda 7 → 8.

## 💡 Exemplos de Perguntas

```
Quais são as diferenças entre Camunda 7 e 8?

Como migrar um processo BPMN?

O que é o Zeebe?

Como usar o Migration Tooling?

Quais conectores precisam ser migrados?

Como funciona o Data Migrator?
```

## 🆘 Problemas?

### Erro de API Key
```bash
# Verificar se está configurada
echo $GOOGLE_API_KEY

# Ou teste direto:
python -c "import os; print(os.environ.get('GOOGLE_API_KEY', 'NÃO CONFIGURADA'))"
```

### Erro de Módulos
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### PDFs não encontrados
Verifique se os arquivos estão em:
```
documentação_migracao_camunda/
├── Code Conversion.pdf
├── Conceptual differences.pdf
├── Data Migrator.pdf
├── Migration Journey.pdf
├── Migration tooling.pdf
└── Migration-ready solutions.pdf
```

## 📚 Documentação Completa

Consulte [README.md](README.md) para informações detalhadas.

---

**Happy Migrating! 🚀**

