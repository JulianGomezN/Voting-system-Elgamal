#!/usr/bin/env python3
"""
Script para crear datos de prueba en la base de datos
"""

from datetime import datetime, timedelta
import sys
import os

# Agregar el directorio actual al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Election, Candidate, Vote
from werkzeug.security import generate_password_hash
import json

def create_test_data():
    """Crear datos de prueba para demostrar la funcionalidad de limpieza"""
    
    with app.app_context():
        print("=== Creando datos de prueba ===")
        
        # Crear usuarios de prueba
        test_users = [
            {'username': 'usuario1', 'email': 'usuario1@test.com', 'password': '123456'},
            {'username': 'usuario2', 'email': 'usuario2@test.com', 'password': '123456'},
            {'username': 'usuario3', 'email': 'usuario3@test.com', 'password': '123456'},
        ]
        
        created_users = []
        for user_data in test_users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password'])
            )
            db.session.add(user)
            created_users.append(user)
        
        # Crear elecciones de prueba
        test_elections = [
            {
                'title': 'Elección de Prueba 1',
                'description': 'Esta es una elección de prueba para demostrar la funcionalidad',
                'start_date': datetime.now() - timedelta(hours=1),
                'end_date': datetime.now() + timedelta(hours=1)
            },
            {
                'title': 'Elección de Prueba 2',
                'description': 'Otra elección de prueba',
                'start_date': datetime.now() + timedelta(hours=1),
                'end_date': datetime.now() + timedelta(hours=3)
            }
        ]
        
        created_elections = []
        for election_data in test_elections:
            # Generar claves ficticias para la elección
            public_key = {'p': 123, 'g': 456, 'public_key': 789}
            private_key = {'p': 123, 'private_key': 101112}
            
            election = Election(
                title=election_data['title'],
                description=election_data['description'],
                start_date=election_data['start_date'],
                end_date=election_data['end_date'],
                public_key=json.dumps(public_key),
                private_key=json.dumps(private_key)
            )
            db.session.add(election)
            created_elections.append(election)
        
        db.session.commit()
        
        # Crear candidatos de prueba
        test_candidates = [
            {'name': 'Candidato A', 'description': 'Propuesta A', 'election_id': 1},
            {'name': 'Candidato B', 'description': 'Propuesta B', 'election_id': 1},
            {'name': 'Candidato C', 'description': 'Propuesta C', 'election_id': 2},
            {'name': 'Candidato D', 'description': 'Propuesta D', 'election_id': 2},
        ]
        
        for candidate_data in test_candidates:
            candidate = Candidate(
                name=candidate_data['name'],
                description=candidate_data['description'],
                election_id=candidate_data['election_id'],
                encrypted_votes=json.dumps([])
            )
            db.session.add(candidate)
        
        db.session.commit()
        
        print(f"✓ Creados {len(created_users)} usuarios de prueba")
        print(f"✓ Creadas {len(created_elections)} elecciones de prueba")
        print(f"✓ Creados {len(test_candidates)} candidatos de prueba")
        
        # Mostrar estadísticas actuales
        print("\n=== Estadísticas actuales ===")
        print(f"Total usuarios: {User.query.count()}")
        print(f"Total elecciones: {Election.query.count()}")
        print(f"Total candidatos: {Candidate.query.count()}")
        print(f"Total votos: {Vote.query.count()}")
        print(f"Usuarios admin: {User.query.filter_by(is_admin=True).count()}")
        print(f"Usuarios normales: {User.query.filter_by(is_admin=False).count()}")

def show_database_stats():
    """Mostrar estadísticas de la base de datos"""
    
    with app.app_context():
        print("\n=== Estadísticas de Base de Datos ===")
        print(f"Total usuarios: {User.query.count()}")
        print(f"Total elecciones: {Election.query.count()}")
        print(f"Total candidatos: {Candidate.query.count()}")
        print(f"Total votos: {Vote.query.count()}")
        print(f"Usuarios admin: {User.query.filter_by(is_admin=True).count()}")
        print(f"Usuarios normales: {User.query.filter_by(is_admin=False).count()}")
        print(f"Elecciones activas: {Election.query.filter_by(is_active=True).count()}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        create_test_data()
    else:
        show_database_stats()
        print("\nPara crear datos de prueba, ejecuta: python test_cleanup.py create")
        print("Para limpiar la base de datos, usa el botón 'Limpiar BD' en el dashboard de administrador")
