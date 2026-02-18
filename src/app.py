from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Curso, UsuarioCurso, Certificado
from utils import generar_certificado
from datetime import date

# Crear app
app = Flask(__name__)
app.secret_key = "mi_clave_secreta"

# Configuración MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:TU_PASSWORD@localhost/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# --- Rutas ---

@app.route('/')
def home():
    return redirect(url_for('login'))

# Registro
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Usuario registrado con éxito", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Email o contraseña incorrectos", "danger")
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    cursos = UsuarioCurso.query.filter_by(user_id=current_user.id).all()
    certificados = Certificado.query.filter_by(user_id=current_user.id).all()

    # 1️⃣ Generar PDF automáticamente si el curso está aprobado y no tiene certificado
    for uc in cursos:
        if uc.aprobado:
            # Verificar si ya tiene certificado
            existe = Certificado.query.filter_by(user_id=current_user.id, curso_id=uc.curso_id).first()
            if not existe:
                ruta_pdf = generar_certificado(uc.usuario, uc.curso)
                cert = Certificado(
                    nombre_certificado=f"Certificado {uc.curso.nombre_curso}",
                    url_pdf=ruta_pdf,
                    user_id=current_user.id,
                    curso_id=uc.curso_id
                )
                db.session.add(cert)
                db.session.commit()

    # Actualizamos la lista de certificados
    certificados = Certificado.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', name=current_user.username, certificados=certificados, cursos=cursos)


# Aprobar curso y generar certificado
@app.route('/aprobar_curso/<int:usuario_curso_id>')
@login_required
def aprobar_curso(usuario_curso_id):
    uc = UsuarioCurso.query.get(usuario_curso_id)
    if uc and uc.user_id == current_user.id:
        uc.aprobado = True
        uc.fecha_aprobacion = date.today()
        ruta_pdf = generar_certificado(uc.usuario, uc.curso)
        certificado = Certificado(
            nombre_certificado=f"Certificado {uc.curso.nombre_curso}",
            url_pdf=ruta_pdf,
            user_id=current_user.id
        )
        db.session.add(certificado)
        db.session.commit()
        flash("Certificado generado correctamente!", "success")
    else:
        flash("Curso no encontrado o no autorizado", "danger")
    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)
