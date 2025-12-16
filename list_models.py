#!/usr/bin/env python3
"""
Lista todos os modelos disponíveis na Google Generative AI API
"""

from config import GOOGLE_API_KEY
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)

print("🔍 Listando modelos disponíveis na Google Generative AI API:\n")
print("="*70)

try:
    models = genai.list_models()
    
    print("\n📋 MODELOS QUE SUPORTAM generateContent:\n")
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display: {model.display_name}")
            print(f"   Descrição: {model.description[:80]}...")
            print()
    
    print("="*70)
    print("\n💡 Use o nome do modelo (ex: 'gemini-1.5-pro-latest') no config.py")
    
except Exception as e:
    print(f"❌ Erro ao listar modelos: {e}")

