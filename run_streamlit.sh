#!/bin/bash
# Script para executar o Streamlit com configurações otimizadas

echo "🚀 Iniciando Assistente de Migração Camunda (Streamlit)..."
echo ""

# Verifica se API key está configurada
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  GOOGLE_API_KEY não configurada!"
    echo ""
    read -sp "Digite sua Google API Key: " GOOGLE_API_KEY
    export GOOGLE_API_KEY
    echo ""
fi

echo "✅ API Key configurada"
echo ""
echo "🌐 Abrindo navegador..."
echo "   URL: http://localhost:8501"
echo ""
echo "💡 Para encerrar: Ctrl+C"
echo ""

# Executa Streamlit
streamlit run chatbot_streamlit.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false \
    --theme.primaryColor "#FF6B35" \
    --theme.backgroundColor "#FFFFFF" \
    --theme.secondaryBackgroundColor "#F0F2F6"

