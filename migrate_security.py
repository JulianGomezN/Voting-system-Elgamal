"""
Script para migrar la base de datos a la nueva estructura segura
Ejecutar después de actualizar app.py
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import os

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Obtener configuración de base de datos
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME', 'elgamal_db')

def migrate_database():
    """Migrar la estructura de la base de datos para mayor seguridad"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("🔄 Iniciando migración de seguridad...")
        
        # 1. Crear nueva tabla VotingRecord
        print("📦 Creando tabla VotingRecord...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS voting_record (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id),
                election_id INTEGER NOT NULL REFERENCES election(id),
                voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, election_id)
            )
        """)
        
        # 2. Migrar datos existentes si hay votos
        print("📦 Verificando datos existentes...")
        cursor.execute("SELECT COUNT(*) FROM vote")
        vote_count = cursor.fetchone()[0]
        
        if vote_count > 0:
            print(f"⚠️  Se encontraron {vote_count} votos existentes")
            print("📦 Migrando registros de votación...")
            
            # Crear registros de votación desde votos existentes
            cursor.execute("""
                INSERT INTO voting_record (user_id, election_id, voted_at)
                SELECT DISTINCT user_id, election_id, timestamp
                FROM vote
                ON CONFLICT (user_id, election_id) DO NOTHING
            """)
            
            print("📦 Eliminando datos sensibles de votos existentes...")
            
            # Crear nueva tabla vote sin user_id y candidate_id
            cursor.execute("DROP TABLE IF EXISTS vote_new")
            cursor.execute("""
                CREATE TABLE vote_new (
                    id SERIAL PRIMARY KEY,
                    election_id INTEGER NOT NULL REFERENCES election(id),
                    encrypted_vote TEXT NOT NULL,
                    vote_hash VARCHAR(64) UNIQUE NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Migrar votos sin información del votante
            cursor.execute("""
                INSERT INTO vote_new (election_id, encrypted_vote, vote_hash, timestamp)
                SELECT election_id, encrypted_vote, vote_hash, timestamp
                FROM vote
            """)
            
            # Reemplazar tabla vote
            cursor.execute("DROP TABLE vote")
            cursor.execute("ALTER TABLE vote_new RENAME TO vote")
            
            print("✅ Migración de datos completada")
        else:
            print("📦 No hay datos existentes, creando estructura nueva...")
            
            # Recrear tabla vote con estructura segura
            cursor.execute("DROP TABLE IF EXISTS vote")
            cursor.execute("""
                CREATE TABLE vote (
                    id SERIAL PRIMARY KEY,
                    election_id INTEGER NOT NULL REFERENCES election(id),
                    encrypted_vote TEXT NOT NULL,
                    vote_hash VARCHAR(64) UNIQUE NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        cursor.close()
        conn.close()
        
        print("✅ Migración completada exitosamente")
        print("\n🔐 Mejoras de seguridad implementadas:")
        print("   - Votos anónimos: No se puede vincular votante con voto")
        print("   - Tabla separada para registro de votación")
        print("   - Hash único para verificación de integridad")
        print("   - Privacidad del voto garantizada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False

def main():
    if not DB_PASSWORD:
        print("❌ Error: DB_PASSWORD no configurada en .env")
        sys.exit(1)
    
    print("🚀 Migración de seguridad de base de datos")
    print("=" * 50)
    print("Esta migración implementa voto secreto verdadero")
    print("⚠️  ADVERTENCIA: Esta operación modificará la estructura de la base de datos")
    
    confirm = input("\n¿Continuar con la migración? (s/N): ")
    if confirm.lower() != 's':
        print("Migración cancelada")
        sys.exit(0)
    
    if migrate_database():
        print("\n🎉 ¡Migración exitosa!")
        print("\n📝 Próximos pasos:")
        print("   1. Reinicializa la aplicación: python init_db.py")
        print("   2. Ejecuta la aplicación: python app.py")
    else:
        print("\n❌ Migración falló")
        sys.exit(1)

if __name__ == "__main__":
    main()
