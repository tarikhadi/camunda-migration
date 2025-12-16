#!/usr/bin/env python3
"""
Exemplo de uso programático do Camunda Migration Chatbot
=========================================================
Este script demonstra como usar o chatbot em seus próprios programas.
"""

import os
from camunda_migration_chatbot import CamundaMigrationChatbot

def example_single_question():
    """Exemplo: fazer uma única pergunta"""
    print("=" * 70)
    print("EXEMPLO 1: Pergunta única")
    print("=" * 70 + "\n")
    
    # Inicializa o chatbot
    chatbot = CamundaMigrationChatbot()
    
    # Setup (necessário apenas na primeira vez)
    print("Configurando chatbot...")
    if not chatbot.setup():
        print("Erro no setup!")
        return
    
    # Faz uma pergunta
    response = chatbot.ask(
        "Quais são as principais diferenças arquiteturais entre Camunda 7 e Camunda 8?"
    )
    
    # Acessa informações da resposta
    if response:
        print("\n--- Texto da Resposta ---")
        print(response.text)


def example_multiple_questions():
    """Exemplo: fazer múltiplas perguntas em sequência"""
    print("\n\n" + "=" * 70)
    print("EXEMPLO 2: Múltiplas perguntas")
    print("=" * 70 + "\n")
    
    chatbot = CamundaMigrationChatbot()
    
    # Setup uma única vez
    print("Configurando chatbot...")
    if not chatbot.setup():
        print("Erro no setup!")
        return
    
    questions = [
        "O que é Zeebe?",
        "Como funciona o Data Migrator?",
        "Quais ferramentas estão disponíveis para migração?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n--- Pergunta {i}: {question} ---")
        response = chatbot.ask(question, show_citations=True)
        if response:
            print(f"Resposta recebida ({len(response.text)} caracteres)")


def example_with_custom_api_key():
    """Exemplo: usar com API key específica"""
    print("\n\n" + "=" * 70)
    print("EXEMPLO 3: Com API key customizada")
    print("=" * 70 + "\n")
    
    # Passa a API key diretamente (não recomendado hardcoded)
    api_key = os.environ.get('GOOGLE_API_KEY', 'sua_api_key_aqui')
    chatbot = CamundaMigrationChatbot(api_key=api_key)
    
    # Restante do código...
    print("Chatbot inicializado com API key customizada")


def example_accessing_metadata():
    """Exemplo: acessar metadados da resposta"""
    print("\n\n" + "=" * 70)
    print("EXEMPLO 4: Acessando metadados")
    print("=" * 70 + "\n")
    
    chatbot = CamundaMigrationChatbot()
    
    if not chatbot.setup():
        return
    
    response = chatbot.ask(
        "Como converter um External Task Handler de Camunda 7 para 8?",
        show_citations=False  # Não exibir automaticamente
    )
    
    if response and response.candidates:
        candidate = response.candidates[0]
        
        print("\n--- Metadados da Resposta ---")
        print(f"Finish Reason: {candidate.finish_reason}")
        
        # Acessa grounding metadata se disponível
        if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
            print("\nGrounding Metadata disponível:")
            print(candidate.grounding_metadata)


def example_error_handling():
    """Exemplo: tratamento de erros"""
    print("\n\n" + "=" * 70)
    print("EXEMPLO 5: Tratamento de erros")
    print("=" * 70 + "\n")
    
    try:
        chatbot = CamundaMigrationChatbot()
        
        # Tenta fazer uma pergunta sem setup (vai falhar graciosamente)
        print("Tentando perguntar sem fazer setup...")
        response = chatbot.ask("Teste")
        
        if response is None:
            print("Como esperado, retornou None sem setup")
        
        # Agora com setup
        print("\nFazendo setup...")
        if chatbot.setup():
            print("Setup bem-sucedido!")
            response = chatbot.ask("O que é BPMN?")
            if response:
                print("Pergunta processada com sucesso!")
        
    except Exception as e:
        print(f"Erro capturado: {e}")


def main():
    """Executa todos os exemplos"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "EXEMPLOS DE USO - CAMUNDA MIGRATION CHATBOT" + " " * 15 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Descomente o exemplo que deseja executar:
    
    # example_single_question()
    # example_multiple_questions()
    # example_with_custom_api_key()
    # example_accessing_metadata()
    # example_error_handling()
    
    print("\n" + "=" * 70)
    print("Para executar os exemplos, descomente a função desejada em main()")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

