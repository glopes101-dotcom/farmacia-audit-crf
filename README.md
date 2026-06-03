# 🏥 Farmácia Audit CRF - Sistema de Auditoria Pessoal

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Sistema de auditoria pessoal para farmácias com conformidade **RDC 44/2009** e **RDC 67/2007** da ANVISA, com gamificação otimizada para usuários com TDAH.

## 🎯 Objetivo

Auxiliar farmacêuticos na manutenção de conformidade regulatória através de:
- 📋 **Aba Documentação**: Controle de prazos de documentos e treinamentos
- 🏷️ **Aba Etiquetas e Controlados**: Auditoria rotativa de estoque (em desenvolvimento)
- 🏢 **Aba Estrutura**: Checklist de infraestrutura física (em desenvolvimento)

## 🚀 MVP - Fase 1: Aba Documentação

Nesta primeira versão, implementamos:
- ✅ Gestão de documentos com data de vencimento
- ✅ Alertas automáticos (vencido, vencimento próximo, regular)
- ✅ Barra "Escudo CRF" com indicador de conformidade
- ✅ Dashboard com status geral
- ✅ Gamificação visual (cores, animações, pontuação)

## 📋 Requisitos

- Python 3.9+
- pip ou conda
- SQLite (desenvolvimento) / PostgreSQL ou Firebase (produção)

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/glopes101-dotcom/farmacia-audit-crf.git
cd farmacia-audit-crf
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Inicialize o banco de dados
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     print("✅ Banco de dados criado!")
>>> exit()
```

### 5. Execute a aplicação
```bash
python app.py
```

Acesse: **http://localhost:5000**

## 📊 Estrutura do Projeto

```
farmacia-audit-crf/
├── app.py                    # Ponto de entrada Flask
├── config.py                 # Configurações (banco de dados, etc.)
├── models.py                 # Modelos SQLAlchemy
├── requirements.txt          # Dependências Python
├── services/
│   ├── __init__.py
│   └── audit_logic.py        # Lógica de alertas e pontuação
├── static/
│   ├── css/
│   │   └── style.css         # Estilos (tema dark/neon)
│   └── js/
│       └── main.js           # Lógica de interatividade
├── templates/
│   ├── base.html             # Layout base
│   ├── index.html            # Dashboard
│   └── docs.html             # Aba Documentação
├── database.db               # SQLite (gerado automaticamente)
├── .gitignore
└── README.md
```

## 🎮 Gamificação & Interface

### Escudo CRF (Barra de Conformidade)
- **100% (Verde/Neon)**: "CRF Blindado - Você está seguro!" ✅
- **80-99% (Amarelo)**: "Atenção: Brechas detectadas." ⚠️
- **< 80% (Vermelho)**: "Risco Sanitário Alto - Ação Necessária!" 🚨

### Micro-vitórias
- Sons de confirmação ao adicionar documentos
- Animações ao atingir 100% de conformidade
- Relatório visual de progresso

## 📚 Regulamentações

- **RDC 44/2009**: Boas Práticas Farmacêuticas para Farmácias e Drogarias
- **RDC 67/2007**: Boas Práticas de Manipulação de Preparações Magistrais

## 🔄 Migração para Firebase

O banco de dados foi estruturado para facilitar migração ao Firebase Firestore:
1. Cada tabela pode ser convertida em uma coleção Firestore
2. Relacionamentos via IDs são nativas do Firestore
3. Timestamps são preservados para sincronização

Veja `config.py` para instruções de configuração do Firebase.

## 📝 Próximas Fases

- [ ] Aba Etiquetas e Controlados (auditoria rotativa)
- [ ] Aba Estrutura (checklist de infraestrutura)
- [ ] Integração com Firebase Firestore
- [ ] Autenticação avançada
- [ ] Sincronização offline
- [ ] Relatórios em PDF

## 🤝 Contribuições

Este é um projeto pessoal, mas sugestões são bem-vindas! 

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Manus AI** | Junho de 2026

---

**Status**: 🚀 MVP em desenvolvimento | Fase 1: Documentação ✅
