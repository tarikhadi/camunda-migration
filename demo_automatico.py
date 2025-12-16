#!/usr/bin/env python3
"""Demo automático do chatbot"""

import os
from camunda_migration_chatbot_v2 import CamundaMigrationChatbot
from rich.console import Console

console = Console()

def main():
    console.print("\n" + "="*70)
    console.print("[bold cyan]   🚀 DEMO - Assistente de Migração Camunda 7 → 8[/bold cyan]")
    console.print("="*70 + "\n")
    
    # Inicializa
    api_key = os.environ.get('GOOGLE_API_KEY')
    console.print(f"[dim]Usando API Key: {api_key[:10]}...{api_key[-4:]}[/dim]\n")
    
    chatbot = CamundaMigrationChatbot(api_key=api_key)
    
    # Setup
    console.print("[bold yellow]⚙️  Fazendo upload da documentação...[/bold yellow]")
    if not chatbot.setup():
        console.print("[red]❌ Falha no setup[/red]")
        return
    
    # Pergunta de teste
    console.print("\n" + "="*70)
    console.print("[bold green]🧪 TESTE: Fazendo uma pergunta automática[/bold green]")
    console.print("="*70 + "\n")
    
    pergunta = "Quais são as principais diferenças entre Camunda 7 e Camunda 8?"
    console.print(f"[yellow]Pergunta:[/yellow] {pergunta}\n")
    
    response = chatbot.ask(pergunta)
    
    console.print("\n" + "="*70)
    console.print("[bold green]✅ SUCESSO! O chatbot está funcionando![/bold green]")
    console.print("="*70 + "\n")
    console.print("Para usar o modo interativo, execute:")
    console.print("[cyan]python3 camunda_migration_chatbot_v2.py[/cyan]\n")

if __name__ == "__main__":
    main()

