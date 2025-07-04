# Sistema de Votación Seguro con Cifrado ElGamal

## Descripción
Este es un sistema de votación web seguro desarrollado en Python con Flask que utiliza cifrado ElGamal para garantizar la privacidad e integridad de los votos.

## Características Principales

### 🔐 Seguridad
- **Cifrado ElGamal**: Todos los votos se cifran usando el algoritmo ElGamal
- **Verificación de Integridad**: Cada voto incluye un hash SHA-256 para verificar su integridad
- **Anonimato**: Los votantes permanecen completamente anónimos
- **Prevención de Doble Votación**: El sistema garantiza que cada usuario vote solo una vez

### 🎯 Funcionalidades
- **Autenticación Segura**: Sistema de login con contraseñas hasheadas
- **Gestión de Elecciones**: Crear y administrar elecciones con fechas de inicio y fin
- **Gestión de Candidatos**: Agregar candidatos a las elecciones
- **Votación Cifrada**: Los votos se cifran antes de almacenarse
- **Resultados Descifrados**: Solo los administradores pueden ver los resultados
- **Dashboard Intuitivo**: Interfaz moderna y fácil de usar

### 🏗️ Arquitectura
- **Backend**: Flask con SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript con Bootstrap 5
- **Base de Datos**: SQLite
- **Criptografía**: ElGamal personalizado con PyCryptodome
- **Autenticación**: Flask-Login

## Instalación

### Requisitos
- Python 3.7+
- pip

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd proyecto-cripto
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

4. **Acceder a la aplicación**
   - Abrir navegador en: `http://localhost:5000`

## Uso

### Configuración Inicial

1. **Crear Administrador**
   - Acceder a: `http://localhost:5000/admin/create_admin`
   - Crear la primera cuenta de administrador

2. **Crear Elección**
   - Iniciar sesión como administrador
   - Hacer clic en "Nueva Elección"
   - Completar título, descripción y fechas

3. **Agregar Candidatos**
   - Ir a la elección creada
   - Hacer clic en "Agregar Candidato"
   - Completar información del candidato

### Para Usuarios

1. **Registrarse**
   - Crear cuenta con usuario, email y contraseña

2. **Votar**
   - Iniciar sesión
   - Seleccionar elección activa
   - Elegir candidato y confirmar voto

3. **Verificar Voto**
   - El sistema confirmará que el voto fue registrado

### Para Administradores

1. **Ver Resultados**
   - Acceder al dashboard de administrador
   - Hacer clic en "Resultados" para cada elección
   - Los votos se descifran automáticamente

## Seguridad Técnica

### Cifrado ElGamal
```python
# Generación de claves
keys = crypto.generate_keys()
public_key = {'p': keys['p'], 'g': keys['g'], 'public_key': keys['public_key']}

# Cifrado de voto
encrypted_vote = crypto.encrypt_vote(1, public_key_data)

# Descifrado (solo administrador)
decrypted_vote = crypto.decrypt_vote(encrypted_vote, private_key_data)
```

### Verificación de Integridad
```python
# Cada voto incluye un hash para verificar integridad
vote_hash = crypto.hash_vote(vote_data)
```

### Flujo de Seguridad
1. **Generación de Claves**: Cada elección tiene claves ElGamal únicas
2. **Cifrado de Voto**: Los votos se cifran en el servidor antes de almacenarse
3. **Verificación**: Cada voto incluye hash de integridad
4. **Anonimato**: Solo se registra que el usuario votó, no por quién
5. **Descifrado Seguro**: Solo el administrador puede descifrar usando la clave privada

## Estructura del Proyecto

```
proyecto-cripto/
│
├── app.py                 # Aplicación principal Flask
├── elgamal_crypto.py      # Implementación del cifrado ElGamal
├── requirements.txt       # Dependencias Python
├── README.md             # Documentación
│
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── user_dashboard.html
│   ├── create_election.html
│   ├── election.html
│   ├── add_candidate.html
│   ├── results.html
│   └── create_admin.html
│
└── voting_system.db      # Base de datos SQLite (se crea automáticamente)
```

## Consideraciones de Seguridad

### ✅ Implementado
- Cifrado ElGamal de votos
- Verificación de integridad con hash
- Prevención de doble votación
- Anonimato de votantes
- Contraseñas hasheadas
- Validación de fechas de elección

### 🔄 Recomendaciones para Producción
- Usar HTTPS en producción
- Implementar rate limiting
- Usar base de datos más robusta (PostgreSQL)
- Implementar logging de seguridad
- Configurar claves secretas más seguras
- Implementar recuperación de contraseñas

## Ejemplo de Uso

### Crear una Elección
```python
# 1. Crear administrador
# 2. Crear elección con título y fechas
# 3. Agregar candidatos
# 4. Los usuarios pueden votar
# 5. Ver resultados descifrados
```

### Proceso de Votación
```python
# Usuario selecciona candidato
# Sistema cifra voto con ElGamal
# Almacena voto cifrado con hash de integridad
# Usuario recibe confirmación
# Administrador puede descifrar resultados
```

## Soporte

Para dudas o problemas:
1. Revisar logs de la aplicación
2. Verificar que todas las dependencias estén instaladas
3. Comprobar que el puerto 5000 esté disponible

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de investigación.
