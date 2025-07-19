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

# Configuración para usar exclusivamente la conexión remota a Postgres (Supabase)
DB_CONNECTION_STRING = os.environ.get('DATABASE_URL')

# Estas variables ya no se usarán, pero se mantienen para compatibilidad con código existente
DB_HOST = None
DB_PORT = None
DB_USER = None
DB_PASSWORD = None
DB_NAME = "postgres"  # Nombre de la base de datos en Supabase

def validate_environment():
    """Validar que todas las variables de entorno necesarias estén configuradas"""
    # Verificar si tenemos la cadena de conexión para Supabase
    if DB_CONNECTION_STRING:
        print("✅ Cadena de conexión para Supabase detectada")
        # Mostramos los primeros caracteres para verificar sin exponer credenciales
        masked_connection = DB_CONNECTION_STRING[:20] + "..." if len(DB_CONNECTION_STRING) > 20 else "..."
        print(f"   - Conexión: {masked_connection}")
        return True
    else:
        print("❌ Error: DATABASE_URL no está configurada en el archivo .env")
        print("💡 Agrega la línea: DATABASE_URL=postgresql://usuario:contraseña@host:puerto/basededatos")
        return False

def test_postgresql_connection():
    """Verificar si PostgreSQL está disponible usando variables de entorno"""
    print(f"string de conexión: {DB_CONNECTION_STRING if DB_CONNECTION_STRING else 'No disponible'}")
    try:
        if DB_CONNECTION_STRING:
            # Usar la cadena de conexión completa (como la de Supabase)
            print("ℹ️  Usando cadena de conexión completa")
            conn = psycopg2.connect(DB_CONNECTION_STRING)
            print("✅ Conexión a PostgreSQL (mediante URL) exitosa")
        else:
            # Usar parámetros individuales
            print("ℹ️  Usando conexión tradicional con parámetros individuales")
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("✅ Conexión a PostgreSQL exitosa")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL no está disponible: {e}")
        print("\n💡 Verifica que:")
        if DB_CONNECTION_STRING:
            print("   - La URL de conexión (DATABASE_URL) sea correcta")
            print("   - La base de datos remota esté disponible")
        else:
            print("   - PostgreSQL esté instalado y ejecutándose")
            print("   - Las credenciales en .env sean correctas")
            print("   - El puerto esté disponible")
        return False

def create_database_if_not_exists():
    """Crear la base de datos si no existe usando variables de entorno"""
    try:
        # Conectar a PostgreSQL (base de datos por defecto)
        if DB_CONNECTION_STRING:
            # En caso de usar Supabase u otro servicio gestionado, generalmente
            # no es necesario crear la base de datos ya que viene pre-configurada
            print("ℹ️  Usando base de datos gestionada mediante URL de conexión")
            # La base de datos ya debería existir en el servicio gestionado
            return True
            
        # Conexión tradicional para entornos locales
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
        
        # Mostrar la configuración de la base de datos
        print(f"🔍 URI de la base de datos: {app.config['SQLALCHEMY_DATABASE_URI'][:20]}...")
        print(f"🔍 Modo de Flask: {app.config['ENV']}")
        
        with app.app_context():
            print("🔄 Inicializando tablas de la aplicación...")
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
        
        # Información adicional de depuración
        try:
            from app import app
            print(f"🔍 Modo de Flask: {app.config.get('ENV', 'No configurado')}")
            print(f"� URI de la base de datos: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurada')[:20]}...")
            print(f"🔍 Variable de entorno DATABASE_URL: {os.environ.get('DATABASE_URL', 'No configurada')[:20]}...")
        except Exception as debug_error:
            print(f"🔍 Error al obtener información de depuración: {debug_error}")
            
        print("�💡 Verifica que:")
        print("   - La base de datos esté creada")
        print("   - Las credenciales sean correctas")
        print("   - La conexión a Supabase esté activa")
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
        print("\n❌ No se puede conectar a PostgreSQL en Supabase.")
        print("\n🔧 Pasos para solucionar:")
        print("   1. Verifica que la cadena de conexión en DATABASE_URL sea correcta")
        print("   2. Asegúrate de que la base de datos en Supabase esté activa")
        print("   3. Comprueba que la IP desde donde te conectas esté permitida")
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
    print("   - Usando base de datos remota en Supabase")
    print("   - Conexión mediante URL segura")
    print("\n📊 Para administrar la base de datos:")
    print("   - Accede al panel de control de Supabase")
    print("   - Ve a la sección 'Database' o 'SQL Editor'")
    print("   - Utiliza las herramientas de Supabase para gestionar tablas y datos")

if __name__ == "__main__":
    main()
