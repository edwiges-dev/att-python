from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Configuração do Banco de Dados ---
# Define o caminho para o arquivo do banco de dados (site.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Boa prática para desativar avisos desnecessários
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

# --- Modelo do Banco de Dados ---
# Define a estrutura da tabela 'contato'
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Contato {self.nome}>'

# --- Rota Principal (Home Page) ---
@app.route('/', methods=['GET', 'POST'])
def index():
    # Se o formulário for enviado (método POST)
    if request.method == 'POST':
        # Captura os dados do formulário
        # Os 'names' (ex: 'nome') devem bater com o HTML
        nome_form = request.form['nome']
        email_form = request.form['email']
        mensagem_form = request.form['mensagem']
        
        # Cria um novo objeto Contato
        novo_contato = Contato(nome=nome_form, email=email_form, mensagem=mensagem_form)
        
        # Tenta salvar no banco de dados
        try:
            db.session.add(novo_contato)
            db.session.commit()
            # CORREÇÃO: Redireciona para a própria página (método GET)
            # Isso evita o reenvio do formulário se o usuário atualizar a página
            return redirect(url_for('index'))
        except Exception as e:
            # Em caso de erro (ex: email duplicado), informa o usuário
            db.session.rollback()
            return f"Ocorreu um erro ao salvar: {e}"

    # Se for um acesso normal (método GET), apenas renderiza a página
    return render_template('index.html')

# --- Execução da Aplicação ---
if __name__ == '__main__':
    # Garante que o app_context esteja ativo para criar o banco
    with app.app_context():
        # Cria as tabelas (se não existirem) antes de rodar
        db.create_all()
    # Roda a aplicação em modo de depuração (debug)
    app.run(debug=True)