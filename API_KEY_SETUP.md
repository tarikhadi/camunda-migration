# 🔑 Configuração da Google API Key

Guia detalhado para obter e configurar sua Google API Key para usar o Camunda Migration Assistant.

## 📝 Passo a Passo

### 1️⃣ Obter a API Key

1. **Acesse o Google AI Studio**
   - URL: https://aistudio.google.com/app/apikey
   - Faça login com sua conta Google

2. **Criar uma nova API Key**
   - Clique no botão **"Create API Key"**
   - Escolha um projeto Google Cloud existente ou crie um novo
   - A chave será gerada automaticamente

3. **Copiar a chave**
   - Clique no ícone de copiar 📋
   - **IMPORTANTE**: Guarde esta chave em local seguro
   - Você não poderá visualizá-la novamente depois

### 2️⃣ Configurar no Projeto

Existem **3 formas** de configurar a API Key. Escolha a que preferir:

---

## Opção A: Arquivo .env (Recomendado) ⭐

**Vantagens:**
- ✅ Seguro (não commita no Git)
- ✅ Fácil de gerenciar
- ✅ Funciona automaticamente

**Como fazer:**

1. Crie o arquivo `.env` na raiz do projeto:

```bash
cd /Users/tarikhadi/Desktop/rag_migracao_camunda
echo "GOOGLE_API_KEY=SUA_CHAVE_AQUI" > .env
```

2. Ou edite manualmente:

```bash
nano .env
```

E adicione:

```
GOOGLE_API_KEY=SUA_CHAVE_AQUI
```

3. Salve e pronto! O chatbot lerá automaticamente.

**Verificar:**

```bash
cat .env
```

---

## Opção B: Variável de Ambiente

**Vantagens:**
- ✅ Não precisa criar arquivo
- ✅ Funciona imediatamente
- ❌ Precisa configurar em cada sessão

**macOS / Linux:**

```bash
export GOOGLE_API_KEY="SUA_CHAVE_AQUI"
```

**Windows CMD:**

```cmd
set GOOGLE_API_KEY=SUA_CHAVE_AQUI
```

**Windows PowerShell:**

```powershell
$env:GOOGLE_API_KEY="SUA_CHAVE_AQUI"
```

**Tornar permanente:**

**macOS / Linux (Bash):**
```bash
echo 'export GOOGLE_API_KEY="SUA_CHAVE_AQUI"' >> ~/.bashrc
source ~/.bashrc
```

**macOS / Linux (Zsh):**
```bash
echo 'export GOOGLE_API_KEY="SUA_CHAVE_AQUI"' >> ~/.zshrc
source ~/.zshrc
```

**Windows:**
1. Painel de Controle → Sistema → Configurações avançadas do sistema
2. Variáveis de Ambiente
3. Nova variável do usuário:
   - Nome: `GOOGLE_API_KEY`
   - Valor: `SUA_CHAVE_AQUI`

**Verificar:**

```bash
echo $GOOGLE_API_KEY  # macOS/Linux
echo %GOOGLE_API_KEY%  # Windows CMD
echo $env:GOOGLE_API_KEY  # Windows PowerShell
```

---

## Opção C: Passar Direto no Código

**Vantagens:**
- ✅ Funciona imediatamente
- ❌ Menos seguro
- ❌ Não recomendado para produção

**Como fazer:**

Edite o código onde inicializa o chatbot:

```python
from camunda_migration_chatbot import CamundaMigrationChatbot

# Passe a API key diretamente
chatbot = CamundaMigrationChatbot(api_key="SUA_CHAVE_AQUI")
```

⚠️ **ATENÇÃO**: Nunca commite código com API keys hardcoded!

---

## ✅ Verificar Configuração

Execute o script de verificação:

```bash
python setup.py
```

Ou verifique manualmente:

```python
import os

api_key = os.environ.get('GOOGLE_API_KEY')

if api_key:
    masked = api_key[:8] + "..." + api_key[-4:]
    print(f"✅ API Key configurada: {masked}")
else:
    print("❌ API Key não encontrada")
```

---

## 🔒 Segurança da API Key

### ✅ Boas Práticas

1. **Nunca compartilhe sua API key**
   - Não poste em fóruns, issues, etc.
   - Não a inclua em screenshots

2. **Use .env para desenvolvimento**
   ```bash
   # .gitignore já inclui:
   .env
   ```

3. **Regenere se exposta**
   - Se você acidentalmente expor sua chave, regenere imediatamente
   - Google AI Studio → API Keys → Regenerate

4. **Monitore uso**
   - Acesse: https://console.cloud.google.com/apis/dashboard
   - Verifique cotas e uso

5. **Restrinja a chave (opcional)**
   - No Google Cloud Console, você pode restringir por:
     - IP
     - Aplicação
     - API específica

### ❌ Não Fazer

- ❌ Commitar .env no Git
- ❌ Compartilhar chave publicamente
- ❌ Hardcoded em código que vai para produção
- ❌ Usar a mesma chave em múltiplos projetos sem controle

---

## 💰 Cotas e Limites

### Free Tier (Gratuito)

A Google oferece uso gratuito com limites:

- **Requisições por minuto**: Varia por modelo
- **Tokens por dia**: Limite generoso
- **File Search**: Incluído

### Monitorar Uso

1. **Google Cloud Console**
   - URL: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
   - Veja uso em tempo real

2. **Alertas**
   - Configure alertas de cota
   - Receba email quando atingir X% do limite

### Aumentar Limites

Se precisar de mais:

1. Configure billing no Google Cloud
2. Limites aumentam automaticamente
3. Preços: https://ai.google.dev/pricing

---

## 🐛 Problemas Comuns

### Erro: "API key not valid"

```
Error 401: Invalid API key
```

**Soluções:**
1. Verifique se copiou a chave completa (sem espaços)
2. Certifique-se de que a API está ativada
3. Tente gerar nova chave

### Erro: "API not enabled"

```
Error 403: API not enabled
```

**Solução:**
1. Acesse: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
2. Clique em **"Enable"**
3. Aguarde alguns segundos e tente novamente

### Erro: "Quota exceeded"

```
Error 429: Rate limit exceeded
```

**Soluções:**
1. Aguarde alguns minutos
2. Verifique cotas em: https://console.cloud.google.com/apis/dashboard
3. Configure billing para limites maiores

### API Key não é reconhecida

```
❌ GOOGLE_API_KEY não encontrada!
```

**Soluções:**

1. **Verificar variável:**
   ```bash
   echo $GOOGLE_API_KEY
   ```

2. **Recarregar terminal:**
   ```bash
   source ~/.bashrc  # ou ~/.zshrc
   ```

3. **Verificar arquivo .env:**
   ```bash
   cat .env
   ls -la .env  # Verificar se existe
   ```

4. **Usar python-dotenv:**
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Carrega .env automaticamente
   ```

---

## 📚 Recursos Adicionais

- **Google AI Studio**: https://aistudio.google.com/
- **Documentação API**: https://ai.google.dev/docs
- **Pricing**: https://ai.google.dev/pricing
- **Cloud Console**: https://console.cloud.google.com/
- **Support**: https://support.google.com/

---

## 🎯 Checklist Final

Antes de executar o chatbot, verifique:

- [ ] API Key obtida no Google AI Studio
- [ ] API Key configurada (arquivo .env OU variável de ambiente)
- [ ] Arquivo `.env` no `.gitignore` (se usando .env)
- [ ] Comando `echo $GOOGLE_API_KEY` retorna sua chave
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Script `setup.py` executado com sucesso

Se todos itens estiverem marcados, você está pronto para usar o chatbot! 🚀

---

**Execute agora:**

```bash
python camunda_migration_chatbot.py
```

Ou teste com o demo:

```bash
python demo.py
```

---

**Em caso de dúvidas, consulte TROUBLESHOOTING.md**

