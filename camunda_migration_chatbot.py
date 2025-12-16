#!/usr/bin/env python3
"""
Camunda 7 to 8 Migration Assistant Chatbot
=============================================
Um assistente RAG para ajudar desenvolvedores na migração do Camunda 7 para o Camunda 8.
Utiliza Google File Search API e Gemini para fornecer respostas contextualizadas e didáticas.
"""

import os
import time
from pathlib import Path
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

# Inicializa o console Rich para output formatado
console = Console()

class CamundaMigrationChatbot:
    """Chatbot especializado em migração Camunda 7 para 8"""
    
    def __init__(self, api_key: str = None):
        """
        Inicializa o chatbot com a API key do Google.
        
        Args:
            api_key: Google API Key. Se não fornecida, busca da variável de ambiente GOOGLE_API_KEY
        """
        # Configura API key
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY')
        if self.api_key:
            os.environ['GOOGLE_API_KEY'] = self.api_key
        
        self.client = genai.Client(api_key=self.api_key)
        self.file_search_store = None
        self.docs_path = Path(__file__).parent / "documentação_migracao_camunda"
        
    def create_file_search_store(self):
        """Cria um novo File Search store para documentos Camunda"""
        console.print("\n[bold cyan]🔧 Criando File Search Store...[/bold cyan]")
        
        try:
            # Cria o File Search store conforme documentação
            self.file_search_store = self.client.file_search_stores.create(
                config={'display_name': 'camunda-7-to-8-migration-docs'}
            )
            
            console.print(f"[green]✓[/green] File Search Store criado: {self.file_search_store.name}")
            return self.file_search_store
        except AttributeError as e:
            console.print(f"[bold red]❌ Erro: A API File Search não está disponível nesta versão.[/bold red]")
            console.print(f"[yellow]Atualize o pacote: pip install --upgrade google-genai[/yellow]\n")
            raise
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao criar File Search store: {e}[/bold red]")
            raise
    
    def upload_documentation(self):
        """
        Faz upload de todos os PDFs de documentação para o File Search store.
        Utiliza chunking otimizado para preservar contexto.
        """
        if not self.file_search_store:
            self.create_file_search_store()
        
        pdf_files = list(self.docs_path.glob("*.pdf"))
        
        if not pdf_files:
            console.print(f"[bold red]❌ Nenhum PDF encontrado em {self.docs_path}[/bold red]")
            return False
        
        console.print(f"\n[bold cyan]📚 Fazendo upload de {len(pdf_files)} documentos...[/bold cyan]\n")
        
        for pdf_file in pdf_files:
            try:
                console.print(f"  [yellow]⏳[/yellow] Processando: {pdf_file.name}...")
                
                # Upload e importação conforme documentação fornecida
                operation = self.client.file_search_stores.upload_to_file_search_store(
                    file=str(pdf_file),
                    file_search_store_name=self.file_search_store.name,
                    config={
                        'display_name': pdf_file.stem,
                        'chunking_config': {
                            'white_space_config': {
                                'max_tokens_per_chunk': 500,  # Chunks maiores para preservar contexto
                                'max_overlap_tokens': 100      # Overlap significativo para não perder contexto
                            }
                        }
                    }
                )
                
                # Aguarda conclusão da importação
                while not operation.done:
                    time.sleep(2)
                    operation = self.client.operations.get(operation)
                
                console.print(f"  [green]✓[/green] {pdf_file.name} importado com sucesso")
                
            except Exception as e:
                console.print(f"  [red]✗[/red] Erro ao processar {pdf_file.name}: {str(e)}")
        
        console.print(f"\n[bold green]✓ Documentação carregada com sucesso![/bold green]\n")
        return True
    
    def get_system_prompt(self):
        """
        Retorna o prompt de sistema otimizado para respostas didáticas e completas.
        """
        return """Você é um assistente especializado em migração do Camunda 7 para o Camunda 8, criado para ajudar desenvolvedores neste processo de transição.

SUAS RESPONSABILIDADES:
1. Fornecer respostas EXTREMAMENTE DETALHADAS, PRECISAS e DIDÁTICAS sobre qualquer aspecto da migração
2. Ser paciente e explicativo, adaptando-se ao nível de conhecimento do desenvolvedor
3. Usar exemplos práticos sempre que possível
4. Citar as fontes da documentação oficial usadas em suas respostas

DIRETRIZES DE RESPOSTA:
- Seja COMPLETO: não resuma demais, forneça todos os detalhes relevantes
- Seja DIDÁTICO: explique conceitos complexos de forma clara e progressiva
- Seja PRÁTICO: inclua exemplos de código, comandos e passos concretos quando aplicável
- Seja ESTRUTURADO: organize as informações em seções claras (contexto, solução, exemplos, considerações)
- Seja VISUAL: quando a documentação incluir diagramas, fluxogramas ou imagens importantes que ajudem na compreensão, MENCIONE explicitamente que existem recursos visuais disponíveis e descreva o que eles ilustram

SOBRE IMAGENS E DIAGRAMAS:
- A documentação contém imagens, diagramas e fluxogramas importantes
- Quando sua resposta se basear em chunks que contenham imagens, você deve:
  * IDENTIFICAR que há uma imagem relevante
  * DESCREVER o que a imagem ilustra
  * EXPLICAR como ela se relaciona com a resposta
  * MENCIONAR em qual documento ela se encontra

ESTRUTURA DE RESPOSTA IDEAL:
1. **Contexto**: Explique brevemente o tópico
2. **Resposta Detalhada**: Forneça a informação completa e precisa
3. **Exemplos Práticos**: Quando aplicável, mostre código ou comandos
4. **Recursos Visuais**: Se houver diagramas ou imagens relevantes, mencione e descreva
5. **Considerações Adicionais**: Avisos, boas práticas, limitações
6. **Referências**: Cite os documentos da documentação oficial utilizados

IMPORTANTE:
- NUNCA invente informações que não estejam na documentação fornecida
- Se não souber algo ou não encontrar na documentação, seja honesto
- Priorize sempre a precisão técnica
- Mantenha um tom profissional mas acessível e amigável

Agora, responda à pergunta do desenvolvedor com excelência e atenção aos detalhes."""

    def ask(self, question: str, show_citations: bool = True):
        """
        Faz uma pergunta ao chatbot e retorna a resposta com citações.
        
        Args:
            question: A pergunta do usuário
            show_citations: Se deve exibir as citações da resposta
            
        Returns:
            Resposta formatada do modelo
        """
        if not self.file_search_store:
            console.print("[bold red]❌ File Search Store não inicializado. Execute setup() primeiro.[/bold red]")
            return None
        
        try:
            # Monta o prompt completo com contexto do sistema
            full_prompt = f"""{self.get_system_prompt()}

PERGUNTA DO DESENVOLVEDOR:
{question}"""
            
            # Gera resposta usando File Search conforme documentação
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    tools=[
                        types.Tool(
                            file_search=types.FileSearch(
                                file_search_store_names=[self.file_search_store.name]
                            )
                        )
                    ],
                    temperature=0.2,
                )
            )
            
            # Exibe a resposta formatada
            if response.text:
                console.print(Panel(
                    Markdown(response.text),
                    title="[bold cyan]💡 Resposta do Assistente Camunda[/bold cyan]",
                    border_style="cyan",
                    padding=(1, 2)
                ))
            
            # Exibe citações se disponíveis
            if show_citations and hasattr(response.candidates[0], 'grounding_metadata'):
                self._display_citations(response.candidates[0].grounding_metadata)
            
            return response
            
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao processar pergunta: {str(e)}[/bold red]")
            return None
    
    def _display_citations(self, grounding_metadata):
        """
        Exibe as citações da resposta de forma formatada.
        
        Args:
            grounding_metadata: Metadados de grounding da resposta
        """
        if not grounding_metadata:
            return
        
        console.print("\n[bold yellow]📚 Referências da Documentação Oficial:[/bold yellow]")
        
        # Extrai e exibe chunks relevantes
        if hasattr(grounding_metadata, 'grounding_chunks'):
            for i, chunk in enumerate(grounding_metadata.grounding_chunks, 1):
                if hasattr(chunk, 'web') and chunk.web:
                    console.print(f"  [{i}] {chunk.web.uri} - {chunk.web.title}")
                elif hasattr(chunk, 'retrieved_context'):
                    # Para File Search, mostra informações do documento
                    console.print(f"  [{i}] Documento: {getattr(chunk.retrieved_context, 'title', 'N/A')}")
        
        console.print()
    
    def setup(self):
        """
        Configura o chatbot: cria store e faz upload da documentação.
        Retorna True se bem-sucedido.
        """
        try:
            self.create_file_search_store()
            return self.upload_documentation()
        except Exception as e:
            console.print(f"[bold red]❌ Erro durante setup: {str(e)}[/bold red]")
            return False
    
    def interactive_mode(self):
        """
        Inicia o modo interativo do chatbot no terminal.
        """
        console.print(Panel.fit(
            "[bold cyan]🤖 Assistente de Migração Camunda 7 → 8[/bold cyan]\n\n"
            "Faça perguntas sobre qualquer aspecto da migração!\n"
            "Digite 'sair' ou 'exit' para encerrar.\n"
            "Digite 'limpar' ou 'clear' para limpar o histórico.",
            border_style="cyan"
        ))
        
        while True:
            try:
                # Recebe pergunta do usuário
                question = Prompt.ask("\n[bold green]Sua pergunta[/bold green]")
                
                # Comandos especiais
                if question.lower() in ['sair', 'exit', 'quit']:
                    console.print("\n[bold cyan]👋 Até logo! Boa sorte com sua migração![/bold cyan]\n")
                    break
                
                if question.lower() in ['limpar', 'clear']:
                    console.clear()
                    continue
                
                if not question.strip():
                    continue
                
                # Processa pergunta
                console.print()
                self.ask(question)
                
            except KeyboardInterrupt:
                console.print("\n\n[bold cyan]👋 Até logo! Boa sorte com sua migração![/bold cyan]\n")
                break
            except Exception as e:
                console.print(f"\n[bold red]❌ Erro: {str(e)}[/bold red]\n")


def main():
    """Função principal para executar o chatbot"""
    
    # Banner de boas-vindas
    console.print("\n" + "="*70)
    console.print("[bold cyan]   🚀 Assistente de Migração Camunda 7 para Camunda 8 🚀[/bold cyan]")
    console.print("="*70 + "\n")
    
    # Verifica API key
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        console.print("[bold red]❌ GOOGLE_API_KEY não encontrada![/bold red]")
        console.print("Configure a variável de ambiente ou crie um arquivo .env\n")
        api_key = Prompt.ask("Digite sua Google API Key", password=True)
        if not api_key:
            console.print("[bold red]API Key é obrigatória. Encerrando.[/bold red]")
            return
    
    # Inicializa chatbot
    chatbot = CamundaMigrationChatbot(api_key=api_key)
    
    # Setup inicial
    console.print("[bold yellow]⚙️  Inicializando assistente...[/bold yellow]")
    if not chatbot.setup():
        console.print("[bold red]❌ Falha na inicialização. Encerrando.[/bold red]")
        return
    
    # Inicia modo interativo
    chatbot.interactive_mode()


if __name__ == "__main__":
    main()
