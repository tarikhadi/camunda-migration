#!/usr/bin/env python3
"""
Script de setup automatizado para o Camunda Migration Assistant
================================================================
Este script ajuda a configurar o ambiente e testar a instalação.
"""

import os
import sys
from pathlib import Path


def check_python_version():
    """Verifica se a versão do Python é adequada"""
    print("🔍 Verificando versão do Python...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("\n🔍 Verificando dependências...")
    
    required = {
        'google.genai': 'google-genai',
        'rich': 'rich',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} não encontrado")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Instale as dependências faltantes:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True


def check_documentation():
    """Verifica se os PDFs de documentação existem"""
    print("\n🔍 Verificando documentação...")
    
    docs_path = Path(__file__).parent / "documentação_migracao_camunda"
    
    if not docs_path.exists():
        print(f"❌ Pasta de documentação não encontrada: {docs_path}")
        return False
    
    pdf_files = list(docs_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ Nenhum PDF encontrado em {docs_path}")
        return False
    
    print(f"✅ {len(pdf_files)} documentos PDF encontrados:")
    for pdf in pdf_files:
        print(f"   • {pdf.name}")
    
    return True


def check_api_key():
    """Verifica se a API key está configurada"""
    print("\n🔍 Verificando Google API Key...")
    
    # Tenta carregar do .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    if not api_key:
        print("⚠️  GOOGLE_API_KEY não configurada")
        print("\n   Configure de uma das seguintes formas:")
        print("   1. Variável de ambiente:")
        print("      export GOOGLE_API_KEY='sua_chave_aqui'")
        print("\n   2. Arquivo .env:")
        print("      echo 'GOOGLE_API_KEY=sua_chave_aqui' > .env")
        print("\n   3. Obtenha sua chave em:")
        print("      https://aistudio.google.com/app/apikey")
        return False
    
    # Não exibe a chave completa por segurança
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    print(f"✅ API Key configurada: {masked_key}")
    return True


def test_import():
    """Testa se o chatbot pode ser importado"""
    print("\n🔍 Testando importação do chatbot...")
    
    try:
        from camunda_migration_chatbot import CamundaMigrationChatbot
        print("✅ Chatbot importado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar chatbot: {e}")
        return False


def create_env_file():
    """Ajuda a criar arquivo .env"""
    env_path = Path(__file__).parent / ".env"
    
    if env_path.exists():
        response = input("\n.env já existe. Sobrescrever? (s/N): ").lower()
        if response != 's':
            print("Mantendo .env existente")
            return
    
    print("\n📝 Criar arquivo .env")
    api_key = input("Digite sua Google API Key (ou deixe vazio para pular): ").strip()
    
    if api_key:
        with open(env_path, 'w') as f:
            f.write(f"GOOGLE_API_KEY={api_key}\n")
        print(f"✅ Arquivo .env criado em {env_path}")
    else:
        print("⏭️  Pulado - configure manualmente depois")


def main():
    """Executa todos os checks"""
    print("\n" + "=" * 70)
    print("🚀 Setup - Camunda Migration Assistant")
    print("=" * 70 + "\n")
    
    checks = [
        ("Versão do Python", check_python_version),
        ("Dependências", check_dependencies),
        ("Documentação", check_documentation),
        ("API Key", check_api_key),
        ("Importação", test_import),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ Erro durante verificação: {e}")
            results[name] = False
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO")
    print("=" * 70 + "\n")
    
    all_passed = True
    for name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("✅ Tudo pronto! Execute: python camunda_migration_chatbot.py")
    else:
        print("⚠️  Alguns checks falharam. Corrija os problemas acima.")
        
        # Oferece criar .env se necessário
        if not results["API Key"]:
            response = input("\nDeseja criar arquivo .env agora? (s/N): ").lower()
            if response == 's':
                create_env_file()
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

