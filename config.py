import os

class Config:
    """Configurações base da aplicação"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Banco de dados SQLite (desenvolvimento)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de aplicação
    ITEMS_PER_PAGE = 10
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    TESTING = False
    # Em produção, configure SQLALCHEMY_DATABASE_URI para PostgreSQL ou Firebase
    # Exemplo: SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/farmacia_audit'

class TestingConfig(Config):
    """Configurações para testes"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Seletor de configuração
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# ============================================
# INSTRUÇÕES PARA MIGRAÇÃO FIREBASE FIRESTORE
# ============================================
# 
# 1. Instale o Firebase Admin SDK:
#    pip install firebase-admin
#
# 2. Baixe a chave de serviço JSON do Firebase Console
#
# 3. Configure a variável de ambiente:
#    export FIREBASE_KEY_PATH="/caminho/para/serviceAccountKey.json"
#
# 4. Adapte o app.py para usar Firestore em vez de SQLAlchemy:
#    - Crie um módulo firebase_db.py com métodos CRUD
#    - Substitua db.session por operações Firestore
#    - Migre os modelos SQLAlchemy para estruturas Firestore
#
# 5. Estrutura Firestore equivalente:
#    /documentos/{docId}
#    /tickets/{ticketId}
#    /historico/{histId}
#    /estrutura/{estruturaId}
#
# Para mais detalhes, veja: https://firebase.google.com/docs/firestore
