from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Documento(db.Model):
    """Modelo para documentos, certificados e treinamentos da farmácia"""
    __tablename__ = 'documento'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # AFE, AE, Alvará, Treinamento, Outro
    data_emissao = db.Column(db.Date)
    data_vencimento = db.Column(db.Date, nullable=False)
    responsavel = db.Column(db.String(100))  # ANVISA, Vigilância Sanitária, etc.
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Documento {self.nome}>'
    
    @property
    def dias_para_vencer(self):
        """Calcula dias até o vencimento"""
        delta = self.data_vencimento - datetime.now().date()
        return delta.days
    
    @property
    def status_alerta(self):
        """Retorna status de alerta: 'vencido', 'proximo', 'regular'"""
        dias = self.dias_para_vencer
        if dias < 0:
            return 'vencido'
        elif dias <= 30:
            return 'proximo'
        else:
            return 'regular'
    
    @property
    def cor_status(self):
        """Retorna cor para exibição baseada no status"""
        status_map = {
            'vencido': '#FF4444',      # Vermelho
            'proximo': '#FFD700',      # Amarelo
            'regular': '#00FF00'       # Verde neon
        }
        return status_map.get(self.status_alerta, '#FFFFFF')
    
    @property
    def icon_status(self):
        """Retorna ícone para exibição"""
        icon_map = {
            'vencido': '❌',
            'proximo': '⚠️',
            'regular': '✅'
        }
        return icon_map.get(self.status_alerta, '❓')

class Secao(db.Model):
    """Modelo para seções de auditoria (etiquetas e controlados)"""
    __tablename__ = 'secao'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    ultima_auditoria = db.Column(db.DateTime)
    frequencia_dias = db.Column(db.Integer, default=7)  # padrão: semanal
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    itens_auditoria = db.relationship('ItemAuditoria', backref='secao', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Secao {self.nome}>'
    
    @property
    def proxima_auditoria(self):
        """Retorna a data da próxima auditoria recomendada"""
        if not self.ultima_auditoria:
            return datetime.now()
        return self.ultima_auditoria + timedelta(days=self.frequencia_dias)
    
    @property
    def dias_desde_ultima_auditoria(self):
        """Retorna dias desde a última auditoria"""
        if not self.ultima_auditoria:
            return float('inf')  # Nunca foi auditada
        delta = datetime.now() - self.ultima_auditoria
        return delta.days

class ItemAuditoria(db.Model):
    """Modelo para itens auditados (medicamentos, produtos)"""
    __tablename__ = 'item_auditoria'
    
    id = db.Column(db.Integer, primary_key=True)
    secao_id = db.Column(db.Integer, db.ForeignKey('secao.id'), nullable=False)
    nome_item = db.Column(db.String(100), nullable=False)
    lote = db.Column(db.String(50))
    validade_embalagem = db.Column(db.Date)
    validade_sistema = db.Column(db.Date)
    fisico_vs_sistema_ok = db.Column(db.Boolean)
    validade_ok = db.Column(db.Boolean)
    data_conferencia = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ItemAuditoria {self.nome_item}>'
    
    @property
    def status_item(self):
        """Retorna status geral do item"""
        if self.fisico_vs_sistema_ok and self.validade_ok:
            return 'conforme'
        elif self.fisico_vs_sistema_ok is False or self.validade_ok is False:
            return 'divergencia'
        else:
            return 'nao_auditado'

class HistoricoAuditoriaSecao(db.Model):
    """Modelo para histórico de auditorias de seção"""
    __tablename__ = 'historico_auditoria_secao'
    
    id = db.Column(db.Integer, primary_key=True)
    secao_id = db.Column(db.Integer, db.ForeignKey('secao.id'), nullable=False)
    data_auditoria = db.Column(db.DateTime, default=datetime.utcnow)
    status_geral = db.Column(db.String(20))  # Conforme, Divergência
    pontuacao_secao = db.Column(db.Integer)  # 0-100
    total_itens = db.Column(db.Integer)  # Total de itens auditados
    itens_conformes = db.Column(db.Integer)  # Itens sem divergências
    
    def __repr__(self):
        return f'<HistoricoAuditoriaSecao {self.id}>'

class TicketCorrecao(db.Model):
    """Modelo para tickets de correção de divergências"""
    __tablename__ = 'ticket_correcao'
    
    id = db.Column(db.Integer, primary_key=True)
    origem_tipo = db.Column(db.String(50), nullable=False)  # AuditoriaItem, ChecklistEstrutura, Documento
    origem_id = db.Column(db.Integer)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), default='Aberto')  # Aberto, Em Andamento, Fechado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_limite = db.Column(db.Date)
    data_fechamento = db.Column(db.DateTime)
    prioridade = db.Column(db.String(20), default='Normal')  # Baixa, Normal, Alta, Crítica
    
    def __repr__(self):
        return f'<TicketCorrecao {self.id}>'

class ChecklistEstrutura(db.Model):
    """Modelo para checklist de estrutura física da farmácia"""
    __tablename__ = 'checklist_estrutura'
    
    id = db.Column(db.Integer, primary_key=True)
    data_auditoria = db.Column(db.Date, default=datetime.utcnow)
    temperatura_ok = db.Column(db.Boolean)
    ralos_limpos = db.Column(db.Boolean)
    iluminacao_ok = db.Column(db.Boolean)
    higienizacao_ok = db.Column(db.Boolean)
    pontuacao = db.Column(db.Integer)  # 0-100
    observacoes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<ChecklistEstrutura {self.id}>'
