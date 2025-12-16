#!/usr/bin/env python3
"""
Camunda 7 to 8 Migration Assistant Chatbot - Versão 2
=======================================================
Versão alternativa que usa Google Files API + Caching
(Para quando File Search API não está disponível)
"""

import os
import time
from pathlib import Path
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

# Importa configurações
try:
    from config import GOOGLE_API_KEY, MODEL_NAME, GENERATION_CONFIG
except ImportError:
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    MODEL_NAME = "gemini-2.5-pro"
    GENERATION_CONFIG = {
        'temperature': 0.2,
        'top_p': 0.95,
        'top_k': 40,
        'max_output_tokens': 8192,
    }

# Inicializa o console Rich
console = Console()

class CamundaMigrationChatbot:
    """Chatbot especializado em migração Camunda 7 para 8"""
    
    def __init__(self, api_key: str = None):
        """Inicializa o chatbot com a API key do Google"""
        self.api_key = api_key or GOOGLE_API_KEY  # Agora vem do config.py
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY não configurada no config.py ou variável de ambiente")
        
        genai.configure(api_key=self.api_key)
        self.uploaded_files = []
        self.docs_path = Path(__file__).parent / "documentação_migracao_camunda"
        self.model = None
        
    def upload_documentation(self):
        """Faz upload de todos os PDFs de documentação"""
        pdf_files = list(self.docs_path.glob("*.pdf"))
        
        if not pdf_files:
            console.print(f"[bold red]❌ Nenhum PDF encontrado em {self.docs_path}[/bold red]")
            return False
        
        console.print(f"\n[bold cyan]📚 Fazendo upload de {len(pdf_files)} documentos...[/bold cyan]\n")
        
        for pdf_file in pdf_files:
            try:
                console.print(f"  [yellow]⏳[/yellow] Processando: {pdf_file.name}...")
                
                # Upload do arquivo
                uploaded_file = genai.upload_file(
                    path=str(pdf_file),
                    display_name=pdf_file.stem
                )
                
                # Aguarda processamento
                while uploaded_file.state.name == 'PROCESSING':
                    time.sleep(2)
                    uploaded_file = genai.get_file(uploaded_file.name)
                
                if uploaded_file.state.name == 'FAILED':
                    console.print(f"  [red]✗[/red] Falha ao processar {pdf_file.name}")
                    continue
                
                self.uploaded_files.append(uploaded_file)
                console.print(f"  [green]✓[/green] {pdf_file.name} importado")
                
            except Exception as e:
                console.print(f"  [red]✗[/red] Erro ao processar {pdf_file.name}: {str(e)}")
        
        console.print(f"\n[bold green]✓ {len(self.uploaded_files)} documentos carregados![/bold green]\n")
        return len(self.uploaded_files) > 0
    
    def get_system_prompt(self):
        """Retorna o prompt de sistema otimizado"""
        return """Você é um assistente especializado em migração do Camunda 7 para o Camunda 8.

SUAS RESPONSABILIDADES:
1. Fornecer respostas EXTREMAMENTE DETALHADAS, PRECISAS e DIDÁTICAS sobre migração
2. Ser paciente e explicativo, adaptando-se ao nível do desenvolvedor
3. Usar exemplos práticos sempre que possível
4. Citar as fontes da documentação oficial

DIRETRIZES:
- Seja COMPLETO: forneça todos os detalhes relevantes
- Seja DIDÁTICO: explique conceitos de forma clara e progressiva
- Seja PRÁTICO: inclua exemplos de código e comandos quando aplicável
- Seja ESTRUTURADO: organize as informações claramente
- Mencione quando houver diagramas ou imagens relevantes na documentação

ESTRUTURA DE RESPOSTA:
1. **Contexto**: Explique brevemente o tópico
2. **Resposta Detalhada**: Informação completa e precisa
3. **Exemplos Práticos**: Código ou comandos quando aplicável
4. **Considerações**: Avisos, boas práticas, limitações
5. **Referências**: Cite os documentos utilizados

IMPORTANTE:
- NUNCA invente informações
- Se não souber, seja honesto
- Priorize precisão técnica
- Mantenha tom profissional mas acessível"""

    def ask(self, question: str):
        """Faz uma pergunta ao chatbot"""
        if not self.uploaded_files:
            console.print("[bold red]❌ Nenhum documento carregado. Execute setup() primeiro.[/bold red]")
            return None
        
        try:
            # Cria modelo com os arquivos
            if not self.model:
                self.model = genai.GenerativeModel(
                    model_name=MODEL_NAME,
                    generation_config=GENERATION_CONFIG
                )
            
            # Monta prompt com contexto
            prompt_parts = [
                self.get_system_prompt(),
                "\nDOCUMENTAÇÃO DISPONÍVEL:",
            ]
            
            # Adiciona referência aos arquivos
            for file in self.uploaded_files:
                prompt_parts.append(f"- {file.display_name}")
            
            prompt_parts.extend([
                f"\nPERGUNTA DO DESENVOLVEDOR:\n{question}",
                "\nBase sua resposta EXCLUSIVAMENTE na documentação fornecida nos arquivos acima."
            ])
            
            # Adiciona arquivos ao contexto
            prompt_parts.extend(self.uploaded_files)
            
            # Gera resposta
            response = self.model.generate_content(prompt_parts)
            
            # Exibe resposta formatada
            if response.text:
                console.print(Panel(
                    Markdown(response.text),
                    title="[bold cyan]💡 Resposta do Assistente Camunda[/bold cyan]",
                    border_style="cyan",
                    padding=(1, 2)
                ))
            
            return response
            
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao processar pergunta: {str(e)}[/bold red]")
            return None
    
    def setup(self):
        """Configura o chatbot: upload da documentação"""
        try:
            console.print("\n[bold cyan]🔧 Configurando chatbot...[/bold cyan]")
            return self.upload_documentation()
        except Exception as e:
            console.print(f"[bold red]❌ Erro durante setup: {str(e)}[/bold red]")
            return False
    
    def interactive_mode(self):
        """Inicia o modo interativo do chatbot"""
        console.print(Panel.fit(
            "[bold cyan]🤖 Assistente de Migração Camunda 7 → 8[/bold cyan]\n\n"
            "Faça perguntas sobre qualquer aspecto da migração!\n"
            "Digite 'sair' ou 'exit' para encerrar.\n"
            "Digite 'limpar' ou 'clear' para limpar o histórico.",
            border_style="cyan"
        ))
        
        while True:
            try:
                question = Prompt.ask("\n[bold green]Sua pergunta[/bold green]")
                
                if question.lower() in ['sair', 'exit', 'quit']:
                    console.print("\n[bold cyan]👋 Até logo! Boa sorte com sua migração![/bold cyan]\n")
                    break
                
                if question.lower() in ['limpar', 'clear']:
                    console.clear()
                    continue
                
                if not question.strip():
                    continue
                
                console.print()
                self.ask(question)
                
            except KeyboardInterrupt:
                console.print("\n\n[bold cyan]👋 Até logo![/bold cyan]\n")
                break
            except Exception as e:
                console.print(f"\n[bold red]❌ Erro: {str(e)}[/bold red]\n")


def main():
    """Função principal"""
    console.print("\n" + "="*70)
    console.print("[bold cyan]   🚀 Assistente de Migração Camunda 7 → 8 [V2][/bold cyan]")
    console.print("="*70 + "\n")
    console.print("[dim]Versão alternativa usando Google Files API[/dim]\n")
    
    # Verifica API key (agora vem do config.py)
    api_key = GOOGLE_API_KEY
    if not api_key:
        console.print("[bold red]❌ GOOGLE_API_KEY não encontrada![/bold red]")
        console.print("Configure no arquivo config.py ou variável de ambiente")
        api_key = Prompt.ask("Ou digite sua Google API Key", password=True)
        if not api_key:
            console.print("[bold red]API Key é obrigatória.[/bold red]")
            return
    
    # Inicializa chatbot
    try:
        chatbot = CamundaMigrationChatbot(api_key=api_key)
        
        # Setup
        console.print("[bold yellow]⚙️  Inicializando...[/bold yellow]")
        if not chatbot.setup():
            console.print("[bold red]❌ Falha na inicialização.[/bold red]")
            return
        
        # Modo interativo
        chatbot.interactive_mode()
        
    except Exception as e:
        console.print(f"[bold red]❌ Erro: {str(e)}[/bold red]")


if __name__ == "__main__":
    main()

