#!/usr/bin/env python3
"""Teste rápido da API"""

import os
import google.generativeai as genai
from rich.console import Console

console = Console()

# Configura API
api_key = os.environ.get('GOOGLE_API_KEY')
console.print(f"[cyan]API Key configurada:[/cyan] {api_key[:10]}...{api_key[-4:]}")

genai.configure(api_key=api_key)

# Teste simples
console.print("\n[yellow]🧪 Testando API...[/yellow]")

try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Diga 'olá' em uma frase.")
    console.print(f"[green]✅ API funcionando![/green]")
    console.print(f"[dim]Resposta: {response.text}[/dim]")
except Exception as e:
    console.print(f"[red]❌ Erro: {e}[/red]")

