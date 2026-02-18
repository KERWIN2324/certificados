from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_curso = db.Column(db.String(255), nullable=False)

class UsuarioCurso(db.Model):
    __tablename__ = 'usuario_cursos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id', ondelete='CASCADE'))
    aprobado = db.Column(db.Boolean, default=False)
    fecha_aprobacion = db.Column(db.Date)

    usuario = db.relationship('User', backref=db.backref('cursos', lazy=True))
    curso = db.relationship('Curso')

class Certificado(db.Model):
    __tablename__ = 'certificados'
    id = db.Column(db.Integer, primary_key=True)
    nombre_certificado = db.Column(db.String(255), nullable=False)
    url_pdf = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    usuario = db.relationship('User', backref=db.backref('certificados', lazy=True))
    curso_id = db.Column(db.Integer, nullable=True)  # <-- agrega esto

