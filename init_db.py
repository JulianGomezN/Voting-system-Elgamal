"""
Script to initialize the PostgreSQL database with secure environment variables
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
    print("⚠️ python-dotenv no está disponible")

# Obtener configuración de base de datos desde variables de entorno
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')

def validate_environment():
    """Validar que todas las variables de entorno necesarias estén configuradas"""
    if not DB_PASSWORD:
        print("❌ Error: DB_PASSWORD no está configurada en el archivo .env")
        print("💡 Agrega la línea: DB_PASSWORD=tu_password_real")
        return False
    
    print("✅ Variables de entorno cargadas correctamente")
    print(f"   - Host: {DB_HOST}")
    print(f"   - Puerto: {DB_PORT}")
    print(f"   - Usuario: {DB_USER}")
    print(f"   - Base de datos: {DB_NAME}")
    print(f"   - Contraseña: {'*' * len(DB_PASSWORD)}")
    return True

def test_postgresql_connection():
    """Verificar si PostgreSQL está disponible usando variables de entorno"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.close()
        print("✅ Conexión a PostgreSQL exitosa")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL no está disponible: {e}")
        print("\n💡 Verifica que:")
        print("   - PostgreSQL esté instalado y ejecutándose")
        print("   - Las credenciales en .env sean correctas")
        print("   - El puerto esté disponible")
        return False

def create_database_if_not_exists():
    """Crear la base de datos si no existe usando variables de entorno"""
    try:
        # Conectar a PostgreSQL (base de datos por defecto)
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            # Crear la base de datos
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"✅ Base de datos '{DB_NAME}' creada exitosamente")
        else:
            print(f"ℹ️  La base de datos '{DB_NAME}' ya existe")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error al crear la base de datos '{DB_NAME}': {e}")
        return False

def init_app_tables():
    """Inicializar las tablas de la aplicación"""
    try:
        # Importar la aplicación después de crear las bases de datos
        from app import app, db
        
        with app.app_context():
            # Verificar conexión
            with db.engine.connect() as conn:
                conn.execute(db.text('SELECT 1'))
            print("✅ Conexión Flask-SQLAlchemy establecida")
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas de la aplicación creadas exitosamente")
            
            # Verificar que las tablas se crearon
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            if tables:
                print(f"📋 Tablas creadas: {', '.join(tables)}")
            else:
                print("⚠️ No se detectaron tablas creadas")
            
        return True
        
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
        print("💡 Verifica que:")
        print("   - La base de datos esté creada")
        print("   - Las credenciales sean correctas")
        print("   - PostgreSQL esté ejecutándose")
        return False

def main():
    print("🚀 Inicializando base de datos PostgreSQL con configuración segura...")
    print("=" * 65)
    
    # Paso 1: Validar variables de entorno
    print("\n🔐 Paso 1: Validando configuración de seguridad...")
    if not validate_environment():
        sys.exit(1)
    
    # Paso 2: Verificar PostgreSQL
    print("\n📦 Paso 2: Verificando conexión a PostgreSQL...")
    if not test_postgresql_connection():
        print("\n❌ No se puede conectar a PostgreSQL.")
        print("\n🔧 Pasos para solucionar:")
        print("   1. Verifica que PostgreSQL esté instalado")
        print("   2. Inicia el servicio: net start postgresql-x64-17")
        print("   3. Confirma las credenciales en el archivo .env")
        print("   4. Ejecuta este script nuevamente")
        sys.exit(1)
    
    # Paso 3: Crear base de datos
    print(f"\n📦 Paso 3: Verificando base de datos '{DB_NAME}'...")
    if not create_database_if_not_exists():
        print("❌ No se pudo configurar la base de datos.")
        sys.exit(1)
    
    # Paso 4: Verificar dependencias Python
    print("\n📦 Paso 4: Verificando dependencias de Python...")
    try:
        import flask_sqlalchemy
        import psycopg2
        print("✅ Dependencias de Python verificadas")
    except ImportError as e:
        print(f"❌ Dependencias faltantes: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    
    # Paso 5: Crear tablas de la aplicación
    print("\n📦 Paso 5: Creando tablas de la aplicación...")
    if not init_app_tables():
        print("❌ No se pudieron crear las tablas.")
        sys.exit(1)
    
    print("\n" + "=" * 65)
    print("🎉 ¡Configuración completada exitosamente!")
    print("\n📝 Próximos pasos:")
    print("   1. Ejecuta la aplicación: python app.py")
    print("   2. Ve a http://localhost:5000")
    print("   3. Crea un usuario administrador en: /admin/create_admin")
    print(f"\n🔧 Información de conexión:")
    print(f"   - Host: {DB_HOST}")
    print(f"   - Puerto: {DB_PORT}") 
    print(f"   - Base de datos: {DB_NAME}")
    print(f"   - Usuario: {DB_USER}")
    print("\n📊 Para administrar la base de datos:")
    print("   - Abre pgAdmin 4")
    print(f"   - Conecta a {DB_HOST}:{DB_PORT}")
    print(f"   - Usuario: {DB_USER}")
    print(f"   - Busca la base de datos: {DB_NAME}")

if __name__ == "__main__":
    main()
