from flask import Flask, send_from_directory, render_template,url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, static_folder='static', template_folder='templates')
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
   
@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        novo_contato = Contato(nome=nome, email=email, mensagem=mensagem)
        db.session.add(novo_contato)
        db.session.commit()
        return request(url_for('static', filename='index.html'))
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)