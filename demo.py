#!/usr/bin/env python3
"""
Script de Demonstração Rápida - Camunda Migration Assistant
============================================================
Execute este script para ver o chatbot em ação com perguntas pré-definidas.
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

console = Console()

def check_environment():
    """Verifica se o ambiente está configurado"""
    console.print("\n[bold cyan]🔍 Verificando ambiente...[/bold cyan]\n")
    
    # Verifica API key
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        console.print("[bold red]❌ GOOGLE_API_KEY não configurada![/bold red]")
        console.print("\nConfigure antes de continuar:")
        console.print("  export GOOGLE_API_KEY='sua_chave_aqui'\n")
        console.print("Obtenha sua chave em: [link]https://aistudio.google.com/app/apikey[/link]\n")
        return False
    
    console.print("[green]✅[/green] API Key configurada")
    
    # Verifica dependências
    try:
        import google.genai
        console.print("[green]✅[/green] google-genai instalado")
    except ImportError:
        console.print("[bold red]❌ google-genai não instalado[/bold red]")
        console.print("Execute: pip install -r requirements.txt\n")
        return False
    
    try:
        from camunda_migration_chatbot import CamundaMigrationChatbot
        console.print("[green]✅[/green] Chatbot disponível")
    except ImportError as e:
        console.print(f"[bold red]❌ Erro ao importar chatbot: {e}[/bold red]\n")
        return False
    
    console.print("\n[bold green]✓ Ambiente pronto![/bold green]\n")
    return True


def run_demo():
    """Executa demonstração com perguntas pré-definidas"""
    
    from camunda_migration_chatbot import CamundaMigrationChatbot
    
    # Banner
    console.print("\n" + "="*70)
    console.print("[bold cyan]   🚀 DEMO - Camunda Migration Assistant 🚀[/bold cyan]")
    console.print("="*70 + "\n")
    
    console.print("Este demo fará 3 perguntas ao chatbot para demonstrar suas capacidades.\n")
    
    # Perguntas de demonstração
    demo_questions = [
        {
            "titulo": "Pergunta 1: Conceitual",
            "pergunta": "Quais são as principais diferenças arquiteturais entre Camunda 7 e Camunda 8?",
            "descricao": "Teste de compreensão conceitual e arquitetural"
        },
        {
            "titulo": "Pergunta 2: Prática",
            "pergunta": "Como usar o Migration Tooling para converter processos BPMN?",
            "descricao": "Teste de instruções práticas e ferramentas"
        },
        {
            "titulo": "Pergunta 3: Técnica",
            "pergunta": "Como converter um External Task Handler de Camunda 7 para Job Worker no Camunda 8?",
            "descricao": "Teste de conversão de código e detalhes técnicos"
        }
    ]
    
    # Inicializa chatbot
    console.print("[bold yellow]⚙️  Inicializando chatbot...[/bold yellow]\n")
    chatbot = CamundaMigrationChatbot()
    
    # Setup
    console.print("[bold yellow]📚 Fazendo upload da documentação...[/bold yellow]")
    console.print("[dim]   (Isto pode levar alguns minutos na primeira vez)[/dim]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processando PDFs...", total=None)
        
        try:
            if not chatbot.setup():
                console.print("\n[bold red]❌ Falha no setup. Encerrando.[/bold red]\n")
                return
        except Exception as e:
            console.print(f"\n[bold red]❌ Erro durante setup: {e}[/bold red]\n")
            return
    
    console.print("\n[bold green]✓ Chatbot pronto![/bold green]\n")
    
    # Executa perguntas de demo
    for i, item in enumerate(demo_questions, 1):
        console.print("\n" + "="*70)
        console.print(f"[bold cyan]{item['titulo']}[/bold cyan]")
        console.print("="*70 + "\n")
        
        console.print(f"[dim]Objetivo: {item['descricao']}[/dim]\n")
        
        console.print(Panel(
            f"[bold]{item['pergunta']}[/bold]",
            title="[yellow]❓ Pergunta[/yellow]",
            border_style="yellow"
        ))
        
        console.print()
        
        try:
            response = chatbot.ask(item['pergunta'], show_citations=True)
            
            if not response:
                console.print("[bold red]❌ Sem resposta[/bold red]")
                continue
            
            # Estatísticas da resposta
            console.print(f"\n[dim]📊 Resposta: {len(response.text)} caracteres[/dim]")
            
            # Pausa entre perguntas (exceto na última)
            if i < len(demo_questions):
                console.print("\n[dim]Pressione Enter para continuar...[/dim]")
                input()
        
        except Exception as e:
            console.print(f"\n[bold red]❌ Erro: {e}[/bold red]")
            continue
    
    # Resumo final
    console.print("\n" + "="*70)
    console.print("[bold cyan]✨ DEMO CONCLUÍDA[/bold cyan]")
    console.print("="*70 + "\n")
    
    console.print(Panel.fit(
        "[bold green]✓[/bold green] O chatbot está funcionando perfeitamente!\n\n"
        "Para usar o modo interativo completo, execute:\n"
        "[bold cyan]python camunda_migration_chatbot.py[/bold cyan]\n\n"
        "Você poderá fazer [bold]qualquer pergunta[/bold] sobre migração Camunda 7 → 8!",
        border_style="green"
    ))
    
    console.print()


def main():
    """Função principal"""
    
    try:
        # Verifica ambiente
        if not check_environment():
            sys.exit(1)
        
        # Confirma execução
        console.print("[bold yellow]⚠️  Este demo fará upload dos PDFs e consumirá cotas da API.[/bold yellow]")
        resposta = console.input("\nDeseja continuar? [bold](S/n)[/bold]: ").lower()
        
        if resposta in ['n', 'nao', 'não', 'no']:
            console.print("\n[dim]Demo cancelado.[/dim]\n")
            return
        
        # Executa demo
        run_demo()
        
    except KeyboardInterrupt:
        console.print("\n\n[dim]Demo interrompido pelo usuário.[/dim]\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Erro inesperado: {e}[/bold red]\n")
        raise


if __name__ == "__main__":
    main()

