import os
from datetime import timedelta

# Cargar variables de entorno desde .env si está disponible
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Si dotenv no está disponible, continuar sin él
    pass

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    
    # Configuración de PostgreSQL
    # Formato: postgresql://usuario:contraseña@host:puerto/nombre_base_datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    # Usar la conexión remota incluso en desarrollo
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:admin@localhost:5432/elgamal_db'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    # Asegurarse de que se use la conexión de Supabase
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    # Para pruebas, también usamos la base remota
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:admin@localhost:5432/elgamal_db'

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
