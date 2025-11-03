from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funcionarios.db'
db = SQLAlchemy(app)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    tefefone = db.Column(db.String(20), nullable=False)
    nome-copleto = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    idade = db.Column(db.Integer, nullable=False)
    curso = db.Column(db.String(120), nullable=False)
    naturalidade = db.Column(db.String(120), nullable=False)
    nivel = db.Column(db.String(50), nullable=False)
    instituição = db.Column(db.String(120), nullable=False)
    status_academico = db.Column(db.String(50), nullable=False)

