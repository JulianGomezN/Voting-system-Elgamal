# Instrucciones de Uso - Sistema de Votación Seguro ElGamal

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar aplicación (Windows)
start.bat

# Iniciar aplicación (Linux/Mac)
./start.sh

# O manualmente
python app.py
```

### 2. Acceso a la Aplicación
- **URL:** http://localhost:5000
- **Puerto:** 5000

## 👨‍💼 Configuración Inicial (Administrador)

### Paso 1: Crear Cuenta de Administrador
1. Ir a: http://localhost:5000/admin/create_admin
2. Completar formulario con:
   - Nombre de usuario
   - Email
   - Contraseña segura
3. Hacer clic en "Crear Administrador"

### Paso 2: Crear Primera Elección
1. Iniciar sesión como administrador
2. Hacer clic en "Nueva Elección"
3. Completar:
   - **Título:** Nombre de la elección
   - **Descripción:** Detalles de la elección
   - **Fecha inicio:** Cuándo empezar a aceptar votos
   - **Fecha fin:** Cuándo terminar la votación
4. Hacer clic en "Crear Elección"

### Paso 3: Agregar Candidatos
1. Ir a la elección creada
2. Hacer clic en "Agregar Candidato"
3. Completar:
   - **Nombre:** Nombre del candidato
   - **Descripción:** Propuestas y información
4. Repetir para todos los candidatos

## 👥 Uso para Votantes

### Paso 1: Registrarse
1. Ir a: http://localhost:5000/register
2. Completar formulario con:
   - Nombre de usuario único
   - Email válido
   - Contraseña segura
3. Hacer clic en "Registrarse"

### Paso 2: Votar
1. Iniciar sesión
2. Ir al Dashboard de Usuario
3. Seleccionar elección activa
4. Revisar candidatos
5. Hacer clic en "Votar por [Candidato]"
6. Confirmar votación

### Paso 3: Confirmación
- El sistema confirmará que el voto fue registrado
- Tu voto está cifrado con ElGamal
- No podrás votar nuevamente en la misma elección

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

## 🔒 Características de Seguridad

### Cifrado ElGamal
- **Claves únicas:** Cada elección tiene claves ElGamal propias
- **Cifrado de votos:** Los votos se cifran antes de almacenarse
- **Descifrado seguro:** Solo el administrador puede descifrar

### Integridad
- **Hash SHA-256:** Cada voto incluye verificación de integridad
- **Prevención de doble votación:** Un usuario = un voto por elección
- **Timestamps:** Registro temporal de cada voto

### Privacidad
- **Anonimato:** Tu identidad no se asocia con tu voto
- **Separación de datos:** Solo se registra que votaste, no por quién

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

### La aplicación no inicia
1. Verificar que Python está instalado
2. Instalar dependencias: `pip install -r requirements.txt`
3. Verificar que el puerto 5000 está libre

### Error al crear administrador
1. Asegurarse de que es la primera cuenta
2. Verificar que no existen otros administradores
3. Reiniciar la aplicación si es necesario

### Problemas con votos
1. Verificar que la elección esté activa
2. Comprobar fechas de inicio/fin
3. Asegurarse de no haber votado antes

### Error de cifrado
1. Ejecutar `python test_crypto.py` para verificar
2. Reinstalar pycryptodome si es necesario
3. Verificar que la clave secreta de Flask está configurada

## 📋 Checklist de Despliegue

### Antes de Usar
- [ ] Python 3.7+ instalado
- [ ] Dependencias instaladas
- [ ] Puerto 5000 disponible
- [ ] Pruebas de cifrado pasadas

### Configuración Inicial
- [ ] Administrador creado
- [ ] Primera elección configurada
- [ ] Candidatos agregados
- [ ] Fechas de elección configuradas

### Pruebas
- [ ] Registro de usuario funciona
- [ ] Votación funciona
- [ ] Resultados se muestran correctamente
- [ ] Seguridad verificada

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
