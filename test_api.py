#!/usr/bin/env python3
"""
Script de teste para verificar a API Google Generative AI
"""

import os
import sys

def check_api_availability():
    """Verifica se a API está instalada e quais recursos estão disponíveis"""
    
    print("="*70)
    print("🔍 Verificando Google Generative AI API")
    print("="*70 + "\n")
    
    # 1. Verificar se o pacote está instalado
    try:
        from google import genai
        print("✅ Pacote google-genai instalado")
        
        # Verificar versão
        try:
            import google.genai
            if hasattr(google.genai, '__version__'):
                print(f"   Versão: {google.genai.__version__}")
        except:
            print("   Versão: não disponível")
    except ImportError as e:
        print(f"❌ Erro ao importar google-genai: {e}")
        print("\nInstale com: pip install google-genai")
        return False
    
    # 2. Verificar API Key
    api_key = os.environ.get('GOOGLE_API_KEY')
    if api_key:
        print(f"✅ GOOGLE_API_KEY configurada: {api_key[:8]}...{api_key[-4:]}")
    else:
        print("❌ GOOGLE_API_KEY não configurada")
        print("   Configure com: export GOOGLE_API_KEY='sua_chave'")
        return False
    
    # 3. Tentar criar cliente
    try:
        client = genai.Client(api_key=api_key)
        print("✅ Cliente criado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar cliente: {e}")
        return False
    
    # 4. Verificar recursos disponíveis
    print("\n" + "="*70)
    print("📦 Recursos disponíveis no cliente:")
    print("="*70 + "\n")
    
    resources = [
        'file_search_stores',
        'files',
        'models',
        'operations',
        'corpora',
        'documents'
    ]
    
    for resource in resources:
        if hasattr(client, resource):
            print(f"✅ client.{resource}")
        else:
            print(f"❌ client.{resource} (não disponível)")
    
    # 5. Listar todos os atributos
    print("\n" + "="*70)
    print("📋 Todos os atributos do cliente:")
    print("="*70 + "\n")
    
    all_attrs = [attr for attr in dir(client) if not attr.startswith('_')]
    for attr in all_attrs:
        print(f"  • {attr}")
    
    print("\n" + "="*70)
    
    # 6. Verificar File Search Store
    print("\n🔍 Testando File Search Store API...\n")
    
    if hasattr(client, 'file_search_stores'):
        print("✅ API file_search_stores está disponível!")
        print("   Você pode usar o chatbot normalmente.")
    else:
        print("❌ API file_search_stores NÃO está disponível.")
        print("\n📝 SOLUÇÕES:")
        print("   1. Atualize o pacote:")
        print("      pip install --upgrade google-genai")
        print("\n   2. Se ainda não funcionar, use uma versão específica:")
        print("      pip install google-genai>=0.8.0")
        print("\n   3. Verifique a documentação oficial:")
        print("      https://ai.google.dev/gemini-api/docs/file-search")
    
    return True


def main():
    """Executa os testes"""
    try:
        check_api_availability()
    except Exception as e:
        print(f"\n❌ Erro durante verificação: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

