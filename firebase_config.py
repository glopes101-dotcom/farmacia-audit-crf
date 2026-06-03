"""
Configuração e inicialização do Firebase Admin SDK
Conecta a aplicação Flask com o Firebase Firestore
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# ============================================
# INICIALIZAR FIREBASE
# ============================================

def inicializar_firebase():
    """
    Inicializa o Firebase Admin SDK usando serviceAccountKey.json
    
    Returns:
        firestore.Client: Cliente Firestore pronto para uso
    """
    
    # Caminho da chave de serviço (na raiz do projeto)
    chave_path = Path(__file__).parent / 'serviceAccountKey.json'
    
    # Verificar se o arquivo existe
    if not chave_path.exists():
        raise FileNotFoundError(
            f"❌ Arquivo serviceAccountKey.json não encontrado em: {chave_path}\n"
            f"📍 Certifique-se de:\n"
            f"   1. Copiar serviceAccountKey.json para a raiz do projeto\n"
            f"   2. O arquivo está em: farmacia-audit-crf/serviceAccountKey.json"
        )
    
    try:
        # Inicializar credencial
        cred = credentials.Certificate(str(chave_path))
        
        # Inicializar app Firebase (se não estiver inicializado)
        if not firebase_admin.get_app():
            firebase_admin.initialize_app(cred)
        
        # Obter cliente Firestore
        db = firestore.client()
        
        print("✅ Firebase inicializado com sucesso!")
        return db
    
    except Exception as e:
        print(f"❌ Erro ao inicializar Firebase: {str(e)}")
        raise

# ============================================
# INICIALIZAR AO IMPORTAR
# ============================================

try:
    db = inicializar_firebase()
except FileNotFoundError as e:
    print(e)
    db = None
except Exception as e:
    print(f"⚠️ Aviso: Firebase não inicializado: {str(e)}")
    db = None
