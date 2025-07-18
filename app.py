from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os
from elgamal_crypto import ElGamalCrypto
from config import config

app = Flask(__name__)

# Configurar la aplicación
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize ElGamal crypto
crypto = ElGamalCrypto()

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    has_voted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    public_key = db.Column(db.Text)  # Store as JSON string
    private_key = db.Column(db.Text)  # Store as JSON string (only for admin)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    encrypted_votes = db.Column(db.Text)  # Store encrypted votes as JSON
    vote_count = db.Column(db.Integer, default=0)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    encrypted_vote = db.Column(db.Text, nullable=False)  # Solo el voto encriptado
    vote_hash = db.Column(db.String(64), unique=True, nullable=False)  # Hash único para verificación
    timestamp = db.Column(db.DateTime, default=datetime.now)
    # ❌ NO almacenar user_id ni candidate_id por seguridad

class VotingRecord(db.Model):
    """Tabla separada solo para registrar quién ya votó (sin vincular al voto específico)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.now)
    # Constraint para evitar votos duplicados
    __table_args__ = (db.UniqueConstraint('user_id', 'election_id', name='one_vote_per_user_per_election'),)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def check_election_status(election):
    """Helper function to check election status and provide debug info"""
    now = datetime.now()
    
    status = {
        'is_active': election.is_active,
        'is_started': now >= election.start_date,
        'is_ended': now > election.end_date,
        'current_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'start_time': election.start_date.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': election.end_date.strftime('%Y-%m-%d %H:%M:%S'),
        'can_vote': election.is_active and now >= election.start_date and now <= election.end_date
    }
    
    return status

def update_election_status():
    """Update election status based on current time"""
    now = datetime.now()
    
    # Close elections that have ended
    expired_elections = Election.query.filter(
        Election.is_active == True,
        Election.end_date < now
    ).all()
    
    for election in expired_elections:
        election.is_active = False
        print(f"Elección '{election.title}' cerrada automáticamente - terminó el {election.end_date}")
    
    if expired_elections:
        db.session.commit()
        print(f"Se cerraron {len(expired_elections)} elecciones automáticamente")
    
    return len(expired_elections)

# Routes
@app.route('/')
def index():
    update_election_status()  # Update election status before showing
    elections = Election.query.filter_by(is_active=True).all()
    return render_template('index.html', elections=elections)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Usuario ya existe')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email ya está registrado')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registro exitoso')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales inválidas')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    update_election_status()  # Update election status before showing
    if current_user.is_admin:
        elections = Election.query.all()
        # Get database statistics for admin
        db_stats = {
            'total_elections': Election.query.count(),
            'active_elections': Election.query.filter_by(is_active=True).count(),
            'total_candidates': Candidate.query.count(),
            'total_votes': Vote.query.count(),
            'total_voting_records': VotingRecord.query.count(),
            'total_users': User.query.filter_by(is_admin=False).count(),
            'admin_users': User.query.filter_by(is_admin=True).count()
        }
        return render_template('admin_dashboard.html', elections=elections, db_stats=db_stats)
    else:
        active_elections = Election.query.filter_by(is_active=True).all()
        return render_template('user_dashboard.html', elections=active_elections)

@app.route('/create_election', methods=['GET', 'POST'])
@login_required
def create_election():
    if not current_user.is_admin:
        flash('Solo los administradores pueden crear elecciones')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        
        # Generate ElGamal keys for this election
        keys = crypto.generate_keys()
        public_key = {
            'p': keys['p'],
            'g': keys['g'],
            'public_key': keys['public_key']
        }
        private_key = {
            'p': keys['p'],
            'private_key': keys['private_key']
        }
        
        election = Election(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            public_key=json.dumps(public_key),
            private_key=json.dumps(private_key)
        )
        db.session.add(election)
        db.session.commit()
        
        flash('Elección creada exitosamente')
        return redirect(url_for('dashboard'))
    
    return render_template('create_election.html')

@app.route('/election/<int:election_id>')
@login_required
def view_election(election_id):
    update_election_status()  # Update election status before showing
    election = Election.query.get_or_404(election_id)
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    
    # Check if user has already voted
    user_vote = VotingRecord.query.filter_by(user_id=current_user.id, election_id=election_id).first()
    
    return render_template('election.html', election=election, candidates=candidates, user_vote=user_vote)

@app.route('/vote', methods=['POST'])
@login_required
def vote():
    election_id = request.form['election_id']
    candidate_id = request.form['candidate_id']
    
    update_election_status()  # Update election status before processing vote
    
    election = Election.query.get_or_404(election_id)
    candidate = Candidate.query.get_or_404(candidate_id)
    
    # Check if user has already voted
    existing_vote = VotingRecord.query.filter_by(user_id=current_user.id, election_id=election_id).first()
    if existing_vote:
        flash('Ya has votado en esta elección')
        return redirect(url_for('view_election', election_id=election_id))
    
    # Check if election is active and within time bounds
    now = datetime.now()
    if not election.is_active:
        flash('La elección está cerrada')
        return redirect(url_for('view_election', election_id=election_id))
    
    if now < election.start_date:
        flash(f'La elección aún no ha comenzado. Inicia el {election.start_date.strftime("%Y-%m-%d %H:%M:%S")}')
        return redirect(url_for('view_election', election_id=election_id))
    
    if now > election.end_date:
        flash(f'La elección ha terminado. Terminó el {election.end_date.strftime("%Y-%m-%d %H:%M:%S")}')
        return redirect(url_for('view_election', election_id=election_id))
    
    # Encrypt the vote using ElGamal - Include candidate_id in encrypted data
    public_key_data = json.loads(election.public_key)
    vote_data = {
        'candidate_id': int(candidate_id),
        'value': 1,  # 1 vote for this candidate
        'election_id': int(election_id)
    }
    encrypted_vote = crypto.encrypt_vote(vote_data, public_key_data)
    
    # Create vote hash for integrity (without revealing voter identity)
    hash_data = {
        'encrypted_vote': encrypted_vote,
        'election_id': election_id,
        'timestamp': now.isoformat()
    }
    vote_hash = crypto.hash_vote(hash_data)
    
    # Store the encrypted vote (anonymously)
    vote = Vote(
        election_id=election_id,
        encrypted_vote=json.dumps(encrypted_vote),
        vote_hash=vote_hash
    )
    db.session.add(vote)
    
    # Record that user voted (without linking to specific vote)
    voting_record = VotingRecord(
        user_id=current_user.id,
        election_id=election_id
    )
    db.session.add(voting_record)
    
    # Update user's voting status
    current_user.has_voted = True
    db.session.commit()
    
    flash('Voto registrado exitosamente')
    return redirect(url_for('view_election', election_id=election_id))

@app.route('/add_candidate/<int:election_id>', methods=['GET', 'POST'])
@login_required
def add_candidate(election_id):
    if not current_user.is_admin:
        flash('Solo los administradores pueden agregar candidatos')
        return redirect(url_for('dashboard'))
    
    election = Election.query.get_or_404(election_id)
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        candidate = Candidate(
            name=name,
            description=description,
            election_id=election_id,
            encrypted_votes=json.dumps([])  # Initialize empty encrypted votes list
        )
        db.session.add(candidate)
        db.session.commit()
        
        flash('Candidato agregado exitosamente')
        return redirect(url_for('view_election', election_id=election_id))
    
    return render_template('add_candidate.html', election=election)

@app.route('/results/<int:election_id>')
@login_required
def view_results(election_id):
    if not current_user.is_admin:
        flash('Solo los administradores pueden ver resultados')
        return redirect(url_for('dashboard'))
    
    election = Election.query.get_or_404(election_id)
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    
    # Decrypt votes and count them
    private_key_data = json.loads(election.private_key)
    results = {candidate.id: 0 for candidate in candidates}
    
    # Get all votes for this election
    votes = Vote.query.filter_by(election_id=election_id).all()
    
    for vote in votes:
        try:
            encrypted_vote = json.loads(vote.encrypted_vote)
            decrypted_data = crypto.decrypt_vote(encrypted_vote, private_key_data)
            
            # Extract candidate_id from decrypted data
            if isinstance(decrypted_data, dict):
                candidate_id = decrypted_data.get('candidate_id')
                vote_value = decrypted_data.get('value', 1)
            else:
                # Backward compatibility
                candidate_id = decrypted_data
                vote_value = 1
            
            if candidate_id in results:
                results[candidate_id] += vote_value
                
        except Exception as e:
            print(f"Error decrypting vote: {e}")
    
    # Prepare results for template
    final_results = []
    for candidate in candidates:
        final_results.append({
            'candidate': candidate,
            'votes': results[candidate.id]
        })
    
    return render_template('results.html', election=election, results=final_results)

@app.route('/admin/close_election/<int:election_id>', methods=['POST'])
@login_required
def close_election(election_id):
    if not current_user.is_admin:
        flash('Solo los administradores pueden cerrar elecciones')
        return redirect(url_for('dashboard'))
    
    election = Election.query.get_or_404(election_id)
    election.is_active = False
    db.session.commit()
    
    flash(f'Elección "{election.title}" cerrada exitosamente')
    return redirect(url_for('dashboard'))

@app.route('/admin/reopen_election/<int:election_id>', methods=['POST'])
@login_required
def reopen_election(election_id):
    if not current_user.is_admin:
        flash('Solo los administradores pueden reabrir elecciones')
        return redirect(url_for('dashboard'))
    
    election = Election.query.get_or_404(election_id)
    now = datetime.now()
    
    # Solo permitir reabrir si no ha pasado la fecha de fin
    if now <= election.end_date:
        election.is_active = True
        db.session.commit()
        flash(f'Elección "{election.title}" reabierta exitosamente')
    else:
        flash('No se puede reabrir una elección cuya fecha de fin ya pasó')
    
    return redirect(url_for('dashboard'))

@app.route('/admin/update_elections_status')
@login_required
def update_elections_status():
    if not current_user.is_admin:
        flash('Solo los administradores pueden actualizar el estado de las elecciones')
        return redirect(url_for('dashboard'))
    
    closed_count = update_election_status()
    if closed_count > 0:
        flash(f'Se cerraron {closed_count} elecciones automáticamente')
    else:
        flash('No hay elecciones que cerrar')
    
    return redirect(url_for('dashboard'))

@app.route('/admin/create_admin', methods=['GET', 'POST'])
def create_admin():
    # Check if any admin exists
    admin_exists = User.query.filter_by(is_admin=True).first()
    if admin_exists:
        flash('Ya existe un administrador')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        flash('Administrador creado exitosamente')
        return redirect(url_for('login'))
    
    return render_template('create_admin.html')

@app.route('/admin/delete_election/<int:election_id>', methods=['POST'])
@login_required
def delete_election(election_id):
    if not current_user.is_admin:
        flash('Solo los administradores pueden eliminar elecciones')
        return redirect(url_for('dashboard'))
    
    election = Election.query.get_or_404(election_id)
    election_title = election.title
    
    # Check if election has votes
    vote_count = Vote.query.filter_by(election_id=election_id).count()
    voting_record_count = VotingRecord.query.filter_by(election_id=election_id).count()
    
    if vote_count > 0 or voting_record_count > 0:
        flash(f'No se puede eliminar la elección "{election_title}" porque ya tiene {vote_count} votos registrados')
        return redirect(url_for('dashboard'))
    
    try:
        # Delete all voting records first
        VotingRecord.query.filter_by(election_id=election_id).delete()
        
        # Delete all votes for this election
        Vote.query.filter_by(election_id=election_id).delete()
        
        # Delete all candidates (after votes are deleted)
        Candidate.query.filter_by(election_id=election_id).delete()
        
        # Delete the election
        db.session.delete(election)
        db.session.commit()
        
        flash(f'Elección "{election_title}" eliminada exitosamente')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la elección: {str(e)}')
    
    return redirect(url_for('dashboard'))

@app.route('/admin/clear_database', methods=['POST'])
@login_required
def clear_database():
    if not current_user.is_admin:
        flash('Solo los administradores pueden limpiar la base de datos')
        return redirect(url_for('dashboard'))
    
    try:
        # Get counts before deletion for the message
        vote_count = Vote.query.count()
        voting_record_count = VotingRecord.query.count()
        candidate_count = Candidate.query.count()
        election_count = Election.query.count()
        user_count = User.query.filter_by(is_admin=False).count()  # Don't count admin users
        
        # Delete all voting records
        VotingRecord.query.delete()
        
        # Delete all votes
        Vote.query.delete()
        
        # Delete all candidates
        Candidate.query.delete()
        
        # Delete all elections
        Election.query.delete()
        
        # Delete all non-admin users
        User.query.filter_by(is_admin=False).delete()
        
        # Reset has_voted flag for admin users (in case they voted during testing)
        admin_users = User.query.filter_by(is_admin=True).all()
        for admin in admin_users:
            admin.has_voted = False
        
        db.session.commit()
        
        flash(f'Base de datos limpiada exitosamente. Se eliminaron: {election_count} elecciones, {candidate_count} candidatos, {vote_count} votos, {voting_record_count} registros de votación y {user_count} usuarios no administradores.')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al limpiar la base de datos: {str(e)}')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
