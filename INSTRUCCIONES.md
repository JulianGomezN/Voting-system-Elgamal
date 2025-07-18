# 🚀 Instrucciones de Uso - Sistema de Votación Seguro ElGamal

## � Instalación y Configuración Inicial

### 1. **Requisitos del Sistema**
```bash
# Componentes necesarios
- Python 3.7+ (Recomendado: 3.11+)
- PostgreSQL 17+ (Mínimo: PostgreSQL 12)
- pip (Gestor de paquetes Python)
- Git (Opcional)

# Verificar instalaciones
python --version
psql --version
pip --version
```

### 2. **Configuración de PostgreSQL**
```bash
# 1. Instalar PostgreSQL (si no está instalado)
# Windows: Descargar desde postgresql.org
# Ubuntu: sudo apt install postgresql postgresql-contrib
# macOS: brew install postgresql

# 2. Iniciar servicio PostgreSQL
# Windows:
net start postgresql-x64-17

# Linux:
sudo systemctl start postgresql
sudo systemctl enable postgresql

# macOS:
brew services start postgresql

# 3. Crear base de datos y usuario
sudo -u postgres psql
CREATE DATABASE elgamal_db;
CREATE USER postgres WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE elgamal_db TO postgres;
\q
```

### 3. **Instalación del Proyecto**
```bash
# 1. Clonar o descargar proyecto
git clone [URL_REPOSITORIO]
cd proyecto-cripto

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar archivo .env (ya configurado)
# Debe contener:
# DATABASE_URL=postgresql://postgres:admin@localhost:5432/elgamal_db
# DB_PASSWORD=admin
# DB_NAME=elgamal_db

# 5. Inicializar base de datos
python init_db.py

# 6. Ejecutar aplicación
python app.py
```

### 4. **Acceso al Sistema**
- **URL Principal:** http://localhost:5000
- **Puerto:** 5000
- **Base de Datos:** PostgreSQL (localhost:5432)

## 👨‍💼 Configuración Inicial (Administrador)

### Paso 1: **Crear Cuenta de Administrador**
1. **Acceder a:** http://localhost:5000/admin/create_admin
2. **Completar formulario:**
   - **Usuario:** Nombre único para administrador
   - **Email:** Correo electrónico válido
   - **Contraseña:** Mínimo 8 caracteres, incluir mayúsculas y números
3. **Confirmar:** Hacer clic en "Crear Administrador"
4. **Resultado:** Primera cuenta de administrador creada

### Paso 2: **Crear Primera Elección**
1. **Autenticarse:** Iniciar sesión con cuenta de administrador
2. **Navegación:** Hacer clic en "Nueva Elección" en dashboard
3. **Información requerida:**
   - **Título:** Nombre descriptivo de la elección
   - **Descripción:** Detalles, propósito y contexto
   - **Fecha inicio:** Cuando empezar a aceptar votos (formato: AAAA-MM-DD HH:MM)
   - **Fecha fin:** Cuando terminar votación (formato: AAAA-MM-DD HH:MM)
4. **Validación:** Sistema verifica fechas y genera claves ElGamal únicas
5. **Confirmar:** Hacer clic en "Crear Elección"

### Paso 3: **Agregar Candidatos**
1. **Seleccionar elección:** Ir a la elección recién creada
2. **Agregar candidato:** Hacer clic en "Agregar Candidato"
3. **Información del candidato:**
   - **Nombre completo:** Nombre oficial del candidato
   - **Descripción:** Propuestas, experiencia, información relevante
   - **Orden en boleta:** (Automático)
4. **Repetir:** Agregar todos los candidatos necesarios
5. **Activación:** La elección estará lista cuando llegue la fecha de inicio

## 👥 Proceso para Usuarios (Votantes)

### Paso 1: **Registro de Usuario**
1. **Acceso:** http://localhost:5000/register
2. **Crear cuenta:**
   - **Nombre de usuario:** Único en el sistema
   - **Email:** Para identificación (no se usa para comunicación)
   - **Contraseña segura:** Mínimo 8 caracteres
3. **Validación:** Sistema verifica unicidad de datos
4. **Confirmación:** Cuenta lista para votar

### Paso 2: **Proceso de Votación Segura**
1. **Autenticación:** Iniciar sesión en http://localhost:5000/login
2. **Seleccionar elección:** Solo elecciones activas aparecen disponibles
3. **Revisar candidatos:** Leer propuestas y información
4. **Votar:**
   - **Seleccionar candidato:** Un solo candidato por elección
   - **Confirmar voto:** Verificar selección antes de confirmar
   - **Cifrado automático:** Sistema cifra voto con ElGamal antes de guardar
5. **Confirmación:** Mensaje confirma que voto fue registrado
6. **Anonimato:** Tu identidad ya no está asociada con tu voto

### Paso 3: **Verificación Post-Votación**
1. **Estado de votación:** Dashboard muestra "Has votado" para elecciones completadas
2. **No re-votación:** Sistema previene múltiples votos automáticamente
3. **Privacidad:** Tu voto específico es matemáticamente imposible de determinar

## 📊 Ver Resultados (Solo Administradores)

### Acceso a Resultados
1. Iniciar sesión como administrador
2. Ir al Dashboard de Administrador
3. Hacer clic en "Resultados" para la elección deseada
4. Ver resultados descifrados automáticamente

### Información Mostrada
- **Tabla de resultados:** Candidatos y votos recibidos
- **Porcentajes:** Distribución de votos
- **Gráfico circular:** Visualización de resultados
- **Ganador:** Candidato con más votos

## � Características de Seguridad Avanzadas

### **Modelo de Anonimato Absoluto**

#### **Separación de Tablas de Seguridad:**
- **Tabla Vote:** Almacena votos cifrados SIN identidad del votante
- **Tabla VotingRecord:** Registra participación SIN contenido del voto
- **Imposibilidad de correlación:** Matemáticamente imposible unir ambas tablas

#### **Cifrado ElGamal 2048-bit**
- **Claves únicas:** Cada elección genera claves criptográficas independientes
- **Cifrado en servidor:** Los votos se cifran antes de almacenarse en BD
- **Descifrado controlado:** Solo administradores pueden acceder a totales
- **Resistencia:** 2^1024 operaciones requeridas para quebrar = imposible

#### **Verificación de Integridad**
- **Hash SHA-256:** Cada voto incluye huella digital única
- **Detección de manipulación:** Cualquier cambio invalida el hash
- **Timestamps seguros:** Registro temporal inmutable
- **Validación automática:** Sistema verifica integridad constantemente

### **Garantías Criptográficas**

#### **Confidencialidad Total:**
- Tu voto individual es **matemáticamente imposible** de descifrar
- Solo los totales pueden ser calculados por administradores
- Ni siquiera la base de datos contiene votos en texto plano

#### **Anonimato Garantizado:**
- **Antes de votar:** Tu identidad está registrada como "elegible"
- **Durante el voto:** Tu selección se cifra instantáneamente
- **Después de votar:** Tu identidad se separa completamente del voto
- **Resultado:** Imposible determinar por quién votaste

#### **Integridad Verificable:**
- Cada voto incluye **prueba criptográfica** de autenticidad
- **Detección automática** de intentos de manipulación
- **Registro inmutable** de participación
- **Auditoría completa** sin comprometer privacidad

### **Proceso de Seguridad en Tiempo Real**

```
[Usuario selecciona candidato] 
           ↓
[Sistema cifra con ElGamal]
           ↓
[Voto anónimo → Tabla Vote]
           ↓
[Registro participación → Tabla VotingRecord]
           ↓
[Separación irreversible]
           ↓
[Anonimato absoluto garantizado]
```

### **Protección Contra Ataques**

#### **Ataques de Base de Datos:**
- **Hacker obtiene BD completa:** Solo ve números cifrados inútiles
- **Administrador corrupto:** No puede asociar votos con votantes
- **Inyección SQL:** Protegido por SQLAlchemy ORM

#### **Ataques Criptográficos:**
- **Fuerza bruta:** Requiere más tiempo que edad del universo
- **Ataques de canal lateral:** Cifrado en servidor, no en cliente
- **Análisis de patrones:** Cada voto usa números aleatorios únicos

#### **Ataques de Red:**
- **HTTPS obligatorio:** Toda comunicación cifrada en tránsito
- **Tokens de sesión seguros:** Previene secuestro de sesión
- **Validación de entrada:** Protección contra XSS y CSRF

## 🛠️ Funciones Administrativas

### Gestión de Elecciones
- **Crear elecciones:** Con fechas de inicio/fin
- **Activar/desactivar:** Control de estado de elecciones
- **Agregar candidatos:** Múltiples candidatos por elección

### Monitoreo
- **Dashboard:** Resumen de actividad
- **Resultados en tiempo real:** Una vez finalizada la elección
- **Estadísticas:** Participación y resultados

## 🎯 Casos de Uso

### Elecciones Estudiantiles
- Presidencia estudiantil
- Representantes de clase
- Actividades extracurriculares

### Votaciones Corporativas
- Elección de representantes
- Decisiones organizacionales
- Feedback interno

### Investigación Académica
- Estudios sobre sistemas de votación
- Pruebas de conceptos criptográficos
- Demostraciones educativas

## 🔧 Solución de Problemas

### **Problemas de Configuración Inicial**

#### **Error: PostgreSQL no se conecta**
```bash
# Síntomas: "could not connect to server" o "connection refused"
# Soluciones:

# 1. Verificar que PostgreSQL está ejecutándose
# Windows:
net start postgresql-x64-17

# Linux:
sudo systemctl status postgresql
sudo systemctl start postgresql

# macOS:
brew services list | grep postgresql
brew services start postgresql

# 2. Verificar puerto y credenciales
psql -h localhost -p 5432 -U postgres -d elgamal_db

# 3. Revisar archivo .env
cat .env | grep DB_
```

#### **Error: Base de datos no existe**
```bash
# Síntomas: "database does not exist"
# Solución:
sudo -u postgres psql
CREATE DATABASE elgamal_db;
GRANT ALL PRIVILEGES ON DATABASE elgamal_db TO postgres;
\q

# Luego ejecutar:
python init_db.py
```

#### **Error: Dependencias Python**
```bash
# Síntomas: "ModuleNotFoundError" o "ImportError"
# Solución:
pip install --upgrade pip
pip install -r requirements.txt

# Si persiste:
pip install --force-reinstall -r requirements.txt

# Verificar instalación específica:
pip freeze | grep -E "(psycopg2|Flask|cryptography)"
```

### **Problemas Durante el Uso**

#### **La aplicación no inicia**
```bash
# 1. Verificar Python y puerto
python --version  # Debe ser 3.7+
netstat -an | grep 5000  # Puerto debe estar libre

# 2. Probar conexión a BD
python -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://postgres:admin@localhost:5432/elgamal_db')
    print('✅ PostgreSQL OK')
    conn.close()
except Exception as e:
    print('❌ Error:', e)
"

# 3. Inicializar base de datos
python init_db.py

# 4. Ejecutar aplicación
python app.py
```

#### **Error al crear administrador**
```bash
# Síntomas: "Admin already exists" o error en formulario
# Causas y soluciones:

# 1. Ya existe un administrador
# Solución: Usar cuenta existente o limpiar BD

# 2. Error de base de datos
python init_db.py  # Reinicializar tablas

# 3. Verificar conectividad
python -c "from app import app, db; app.app_context().push(); print(db.engine)"
```

#### **Problemas con votos o cifrado**
```bash
# Síntomas: Error al votar, cifrado falla, resultados incorrectos

# 1. Probar sistema criptográfico
python test_crypto.py

# Salida esperada:
# ✅ Prueba de cifrado/descifrado: EXITOSA
# ✅ Prueba de integridad: EXITOSA
# ✅ Prueba de múltiples votos: EXITOSA

# 2. Verificar que la elección esté activa
python -c "
from app import app, Election
from datetime import datetime
app.app_context().push()
elections = Election.query.all()
for e in elections:
    now = datetime.now()
    active = e.start_date <= now <= e.end_date
    print(f'Elección: {e.title}, Activa: {active}')
"

# 3. Comprobar que usuario no ha votado
# En la interfaz web, revisar dashboard de usuario
```

#### **Error de migración**
```bash
# Síntomas: Estructura de BD antigua, errores de compatibilidad
# Solución: Ejecutar migración de seguridad

# 1. Backup de datos (opcional)
pg_dump elgamal_db > backup_$(date +%Y%m%d).sql

# 2. Ejecutar migración
python migrate_security.py

# 3. Reinicializar si es necesario
python init_db.py

# 4. Verificar nueva estructura
python -c "
from app import app, db, Vote, VotingRecord
app.app_context().push()
print('Tablas Vote:', Vote.query.count())
print('Tablas VotingRecord:', VotingRecord.query.count())
"
```

### **Diagnóstico Avanzado**

#### **Verificación completa del sistema**
```bash
# Script de diagnóstico automático
python -c "
import sys
print('=== DIAGNÓSTICO DEL SISTEMA ===')

# 1. Versión Python
print(f'Python: {sys.version}')

# 2. Dependencias críticas
try:
    import flask, psycopg2, cryptography
    print('✅ Dependencias críticas: OK')
except ImportError as e:
    print(f'❌ Dependencias: {e}')

# 3. Conexión PostgreSQL
try:
    import psycopg2
    conn = psycopg2.connect('postgresql://postgres:admin@localhost:5432/elgamal_db')
    print('✅ PostgreSQL: OK')
    conn.close()
except Exception as e:
    print(f'❌ PostgreSQL: {e}')

# 4. Cifrado ElGamal
try:
    from elgamal_crypto import ElGamalCrypto
    crypto = ElGamalCrypto()
    keys = crypto.generate_keys()
    encrypted = crypto.encrypt_vote(1, keys)
    decrypted = crypto.decrypt_vote(encrypted, keys)
    assert decrypted == 1
    print('✅ Cifrado ElGamal: OK')
except Exception as e:
    print(f'❌ Cifrado: {e}')

# 5. Variables de entorno
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        print('✅ Variables de entorno: OK')
    else:
        print('❌ Variables de entorno: .env no configurado')
except Exception as e:
    print(f'❌ Variables: {e}')

print('=== FIN DIAGNÓSTICO ===')
"
```

### **Logs y Depuración**

#### **Habilitar modo debug**
```bash
# Ejecutar aplicación en modo debug
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows

python app.py --debug
```

#### **Revisar logs de PostgreSQL**
```bash
# Ubuntu/Debian:
sudo tail -f /var/log/postgresql/postgresql-*.log

# Windows:
# Buscar en: C:\Program Files\PostgreSQL\17\data\log\

# macOS:
tail -f /opt/homebrew/var/log/postgresql*.log
```

### **Contacto para Soporte**

Si los problemas persisten:

1. **Ejecutar diagnóstico completo** (script arriba)
2. **Revisar archivos de log** de aplicación y PostgreSQL
3. **Verificar documentación** en README.md y SEGURIDAD_ELGAMAL.md
4. **Comprobar configuración** de .env y requirements.txt

**Información útil para reportar problemas:**
- Salida del script de diagnóstico
- Mensajes de error exactos
- Sistema operativo y versiones
- Pasos para reproducir el problema

## 📋 Checklist de Despliegue

### **Requisitos Previos**
- [ ] **Python 3.7+** instalado y funcionando
- [ ] **PostgreSQL 17+** instalado y servicio ejecutándose  
- [ ] **Puerto 5432** disponible para PostgreSQL
- [ ] **Puerto 5000** disponible para Flask
- [ ] **Dependencias Python** instaladas correctamente
- [ ] **Archivo .env** configurado con credenciales correctas

### **Configuración de Base de Datos**
- [ ] **PostgreSQL iniciado** (`net start postgresql-x64-17` o equivalente)
- [ ] **Base de datos creada** (`elgamal_db` existe)
- [ ] **Usuario configurado** (postgres con contraseña admin)
- [ ] **Conexión verificada** (`psql -h localhost -p 5432 -U postgres -d elgamal_db`)
- [ ] **Tablas inicializadas** (`python init_db.py` ejecutado exitosamente)

### **Pruebas de Sistema**
- [ ] **Cifrado funcional** (`python test_crypto.py` pasa todas las pruebas)
- [ ] **Aplicación inicia** (`python app.py` sin errores)
- [ ] **URL accesible** (http://localhost:5000 responde)
- [ ] **Variables de entorno** cargadas correctamente

### **Configuración Inicial de Aplicación**
- [ ] **Administrador creado** (primera cuenta de admin configurada)
- [ ] **Elección de prueba** creada con fechas válidas
- [ ] **Candidatos agregados** (al menos 2 para pruebas)
- [ ] **Fechas configuradas** (inicio y fin de elección apropiados)

### **Pruebas de Funcionalidad**
- [ ] **Registro de usuario** funciona correctamente
- [ ] **Login/logout** operativo para usuarios y administradores  
- [ ] **Proceso de votación** completo sin errores
- [ ] **Votos cifrados** se almacenan en tabla Vote sin user_id
- [ ] **Registro de participación** se guarda en tabla VotingRecord
- [ ] **Conteo de resultados** funciona para administradores
- [ ] **Prevención de doble voto** activa y funcional

### **Verificación de Seguridad**
- [ ] **Anonimato verificado** (imposible correlacionar voto con votante)
- [ ] **Cifrado ElGamal** operativo con claves de 2048 bits
- [ ] **Separación de tablas** implementada correctamente
- [ ] **Hashes de integridad** generados para cada voto
- [ ] **Validación de fechas** previene votos fuera de período
- [ ] **Contraseñas hasheadas** con Werkzeug
- [ ] **Sesiones seguras** con tokens apropiados

### **Configuración de Producción (Opcional)**
- [ ] **HTTPS configurado** para conexiones seguras
- [ ] **Variables de entorno** robustas (no usar credenciales de desarrollo)
- [ ] **Base de datos backup** configurado
- [ ] **Logs de seguridad** habilitados  
- [ ] **Rate limiting** implementado
- [ ] **Monitoreo de sistema** activo

### **Documentación y Soporte**
- [ ] **README.md** revisado y actualizado
- [ ] **INSTRUCCIONES.md** accesible para usuarios
- [ ] **SEGURIDAD_ELGAMAL.md** disponible para análisis técnico
- [ ] **Scripts de diagnóstico** probados y funcionales

## 🌟 Mejoras Futuras

### Funcionalidades Adicionales
- [ ] Múltiples elecciones simultáneas
- [ ] Notificaciones por email
- [ ] Exportación de resultados
- [ ] Auditoría de votos

### Seguridad Avanzada
- [ ] Autenticación de dos factores
- [ ] Certificados digitales
- [ ] Logging de seguridad
- [ ] Rate limiting

### Experiencia de Usuario
- [ ] Aplicación móvil
- [ ] Temas personalizables
- [ ] Multiidioma
- [ ] Accesibilidad mejorada

## 📞 Soporte

Para problemas o preguntas:
1. Revisar este archivo de instrucciones
2. Ejecutar pruebas: `python test_crypto.py`
3. Verificar logs en la consola
4. Comprobar documentación en README.md

---

**¡Disfruta votando de forma segura con ElGamal!** 🗳️🔐
