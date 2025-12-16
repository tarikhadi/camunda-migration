# 🤖 Assistente de Migração Camunda 7 → 8

Um chatbot RAG (Retrieval-Augmented Generation) especializado para auxiliar desenvolvedores na migração do Camunda 7 para o Camunda 8. Utiliza Google File Search API e Gemini para fornecer respostas contextualizadas, precisas e didáticas baseadas na documentação oficial.

## 🌟 Características

- **RAG com Google File Search**: Busca semântica inteligente na documentação oficial
- **Respostas Didáticas**: Prompt otimizado para explicações detalhadas e progressivas
- **Citações e Referências**: Sempre indica a fonte das informações
- **Consciente de Imagens**: Identifica e descreve diagramas e recursos visuais relevantes
- **Interface Amigável**: Terminal interativo com formatação rica usando Rich
- **Chunking Otimizado**: Configuração ajustada para preservar contexto e relações entre tópicos

## 📋 Pré-requisitos

- Python 3.8+
- Google API Key (obtenha em [Google AI Studio](https://aistudio.google.com/app/apikey))
- Documentação Camunda em PDF (já incluída na pasta `documentação_migracao_camunda/`)

## 🚀 Instalação

### 1. Clone ou navegue até o diretório do projeto

```bash
cd /Users/tarikhadi/Desktop/rag_migracao_camunda
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure sua API Key

**Opção A: Arquivo .env (recomendado)**

```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua API key
```

**Opção B: Variável de ambiente**

```bash
export GOOGLE_API_KEY="sua_api_key_aqui"
```

## 💻 Uso

### Modo Interativo (Principal)

Execute o chatbot em modo interativo:

```bash
python camunda_migration_chatbot.py
```

O chatbot irá:
1. Criar um File Search store
2. Fazer upload e indexar todos os PDFs da documentação
3. Iniciar uma sessão interativa onde você pode fazer perguntas

### Comandos Durante a Sessão

- Digite sua pergunta normalmente para receber uma resposta
- `sair` / `exit` / `quit` - Encerra o chatbot
- `limpar` / `clear` - Limpa o histórico do terminal
- `Ctrl+C` - Encerra o chatbot

## 📚 Exemplos de Perguntas

O chatbot pode responder QUALQUER pergunta sobre migração Camunda 7 → 8. Exemplos:

```
Quais são as principais diferenças conceituais entre Camunda 7 e 8?

Como migrar um processo BPMN do Camunda 7 para o 8?

O que é o Camunda 8 Migration Tooling e como usá-lo?

Como converter código Java de Camunda 7 para Camunda 8?

Existe uma ferramenta para migrar dados históricos?

Quais são as melhores práticas para migração de conectores?

Como funciona a arquitetura do Zeebe comparada ao Camunda 7?
```

## 🏗️ Arquitetura

```
┌─────────────────┐
│   Usuário       │
└────────┬────────┘
         │ Pergunta
         ▼
┌─────────────────────────────┐
│  Camunda Migration Chatbot  │
│  (camunda_migration_chatbot.py) │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Google File Search API     │
│  - Busca Semântica          │
│  - Embeddings (gemini-      │
│    embedding-001)           │
└────────┬────────────────────┘
         │ Chunks Relevantes
         ▼
┌─────────────────────────────┐
│  Gemini 2.5 Flash           │
│  - Geração de Resposta      │
│  - Prompt Didático          │
│  - Análise de Contexto      │
└────────┬────────────────────┘
         │ Resposta + Citações
         ▼
┌─────────────────────────────┐
│  Interface Rich (Terminal)  │
│  - Markdown Formatado       │
│  - Citações                 │
│  - Painéis Coloridos        │
└─────────────────────────────┘
```

## 📁 Estrutura do Projeto

```
rag_migracao_camunda/
├── camunda_migration_chatbot.py  # Script principal do chatbot
├── requirements.txt               # Dependências Python
├── .env.example                   # Exemplo de configuração
├── README.md                      # Este arquivo
└── documentação_migracao_camunda/ # Documentação oficial
    ├── Code Conversion.pdf
    ├── Conceptual differences.pdf
    ├── Data Migrator.pdf
    ├── Migration Journey.pdf
    ├── Migration tooling.pdf
    └── Migration-ready solutions.pdf
```

## 🎯 Funcionalidades Técnicas

### Chunking Inteligente

O chatbot usa uma configuração otimizada de chunking:
- **500 tokens por chunk**: Preserva contexto suficiente
- **100 tokens de overlap**: Garante que informações não sejam perdidas entre chunks

### Prompt Engineering

O sistema utiliza um prompt cuidadosamente desenvolvido que instrui o modelo a:
- Ser extremamente detalhado e didático
- Fornecer exemplos práticos
- Identificar e descrever recursos visuais
- Estruturar respostas de forma clara
- Sempre citar fontes

### Temperatura Otimizada

Usa `temperature=0.2` para respostas mais precisas e consistentes, essencial para documentação técnica.

## 🔧 Uso Programático

Você também pode usar o chatbot em seus próprios scripts:

```python
from camunda_migration_chatbot import CamundaMigrationChatbot

# Inicializa
chatbot = CamundaMigrationChatbot(api_key="sua_api_key")

# Setup (primeira vez)
chatbot.setup()

# Faz uma pergunta
response = chatbot.ask("Como migrar um processo BPMN?")

# Acessa o texto da resposta
print(response.text)
```

## 🛠️ Personalização

### Ajustar Chunking

Edite os parâmetros em `upload_documentation()`:

```python
'chunking_config': {
    'white_space_config': {
        'max_tokens_per_chunk': 500,  # Tamanho do chunk
        'max_overlap_tokens': 100      # Overlap entre chunks
    }
}
```

### Modificar o Prompt

Edite o método `get_system_prompt()` para customizar o comportamento do assistente.

### Usar Outro Modelo

Altere o modelo em `ask()`:

```python
response = self.client.models.generate_content(
    model="gemini-2.5-pro",  # Ou outro modelo suportado
    # ...
)
```

Modelos suportados pelo File Search:
- `gemini-2.5-pro`
- `gemini-2.5-flash` (padrão)
- `gemini-2.5-flash-lite`

## 📊 Limitações e Considerações

1. **Primeira execução**: O upload e indexação dos PDFs pode levar alguns minutos
2. **Custos**: Uso da API Google pode gerar custos. Monitore em [Google Cloud Console](https://console.cloud.google.com/)
3. **Imagens**: O modelo descreve imagens mas não as exibe no terminal. Para visualizar, consulte os PDFs originais
4. **File Search Store**: É criado um store persistente. Para limpar, use a API de deleção

## 🐛 Solução de Problemas

### Erro de API Key

```
❌ GOOGLE_API_KEY não encontrada!
```

**Solução**: Configure a variável de ambiente ou crie o arquivo `.env`

### Erro de Upload de Arquivos

```
❌ Nenhum PDF encontrado
```

**Solução**: Verifique se os PDFs estão na pasta `documentação_migracao_camunda/`

### Erro de Importação

```
ModuleNotFoundError: No module named 'google.genai'
```

**Solução**: Instale as dependências: `pip install -r requirements.txt`

## 📝 Licença

Este projeto é fornecido como está, para uso educacional e profissional.

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Este é um projeto focado em auxiliar a comunidade Camunda.

## 📞 Suporte

Para questões sobre:
- **Este chatbot**: Verifique os logs de erro e a documentação acima
- **Migração Camunda**: Use o próprio chatbot! Ele foi feito para isso 😊
- **Google AI API**: Consulte [Google AI Documentation](https://ai.google.dev/docs)

---

**Desenvolvido com ❤️ para a comunidade Camunda**

