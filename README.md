# CLA WinConfig

Herramienta profesional para la configuración automática de PCs con Windows en centros de cómputo

## ¿Qué es CLA WinConfig?

CLA WinConfig es una aplicación de escritorio diseñada específicamente para **centros de cómputo institucionales** que automatiza la configuración completa de equipos Windows. A diferencia de otras herramientas, incluye:

### ✨ Características Principales:
- ✅ **Tema oscuro del sistema** - Configuración automática
- 🖼️ **Fondos de pantalla personalizados por PC** - Cada equipo su imagen única
- 🔒 **Pantalla de bloqueo institucional** - Imagen unificada para todos los equipos
- 🚫 **Bloqueo de personalización** - Impide cambios no autorizados
- 🔄 **Reinicio automático del explorador** - Aplica cambios al instante
- 🔑 **Activación de Windows y Office** - Opcional, con scripts externos
- ⚡ **Optimización de arranque** - Deshabilita programas innecesarios en el inicio del sistema

### 🆕 Características Únicas:
- 👥 **Gestión completa de usuarios locales** - Crea administradores y usuarios estándar con un clic
- 🔐 **Configuración automática de UAC** - Control de cuentas de usuario optimizado
- 🏢 **Multi-centro de cómputo** - Soporte para múltiples laboratorios/centros con configuraciones independientes
- 📁 **Estructura de carpetas flexible** - Organización por centro de cómputo
- 🎯 **Aplicación de configuración a usuarios específicos** - Configurar fondos para cualquier usuario local
- 🔄 **Sistema de reintentos inteligente** - Obtención confiable de SIDs de usuario con tolerancia a errores
- 🧹 **Limpieza automática de caché** - Elimina cachés de Windows para garantizar aplicación de cambios

### 🎨 Interfaz Moderna:
- Diseño **Bento Card** con estilo institucional
- Colores corporativos azul/blanco
- Interfaz intuitiva y profesional
- Logs en tiempo real de todas las operaciones

Pensado para **técnicos de soporte**, **administradores de sistemas** y **centros educativos** donde se necesita configurar múltiples equipos de manera estandarizada, rápida y confiable.

## 📦 Descarga

👉 Descarga la última versión aquí:  [Releases](../../releases)

## 🖥️ Requisitos

- Windows 10 / 11
- Ejecutar como **Administrador** (requerido para algunas funciones)
- Python 3.8+ (solo para desarrollo)

## ▶️ Uso

### Para usuarios finales:
1. Descarga el archivo `.exe` desde [Releases](../../releases)
2. Coloca tus imágenes en las carpetas correspondientes (ver estructura de carpetas)
3. Ejecuta el archivo como administrador
4. Selecciona el número de PC y las opciones deseadas
5. Presiona "Aplicar Configuración"

### Estructura de carpetas requerida:

El programa espera encontrar las imágenes en la siguiente estructura:

```
CLA-WinConfig/
├── assets/
│   ├── Centro_Computo/
│       ├── wallpapers/          # Fondos de pantalla por PC
│       │   ├── PC-1.jpg         # Fondo para PC número 1
│       │   ├── PC-2.jpg         # Fondo para PC número 2
│       │   ├── PC-3.png         # También soporta .png y .jpeg
│       │   └── ...
│       └── lockscreen/          # Imágenes de pantalla de bloqueo
│           └── PC-Bloqueo.jpg   # Imagen única para todas las PCs
└── docs/
    └── icons/
        └── Logo-ServiciosInformaticos-2.ico  # Icono de la aplicación
```

**Formatos soportados:** `.jpg`, `.png`, `.jpeg`

### Nombrado de archivos:
- **Fondos de pantalla:** `PC-{numero}.jpg` (ejemplo: `PC-1.jpg`, `PC-25.png`)
- **Pantalla de bloqueo:** `PC-Bloqueo.jpg` (mismo para todas las PCs)

## 🗂️ Estructura del Proyecto

```
CLA WinConfig/
├── src/                      # Código fuente
│   ├── core/                 # Lógica de negocio
│   │   ├── __init__.py
│   │   └── usuarios.py       # Clase GestorUsuarios
│   │   └── configurador.py   # Clase ConfiguradorPC
│   ├── ui/                   # Interfaz gráfica
│   │   ├── __init__.py
│   │   ├── main_window.py    # Ventana principal
│   │   └── styles.py         # Estilos y colores
│   └── start.py              # Punto de entrada
├── assets/                   # Recursos (fondos e imágenes)
│   ├── Centro_Computo/       # Dividido por centros de Computo
│       ├── wallpapers/          # Fondos de pantalla
│       └── lockscreen/          # Pantallas de bloqueo
├── docs/                     # Documentación e iconos
│   ├── icons/               # Iconos de la aplicación
│   └── images/              # Imágenes de documentación
├── build.spec               # Especificaciones para la build
├── LICENSE                  # Licencia del proyecto
└── README.md                # Este archivo
```

## 🌟 Características Diferenciadoras

### 1️⃣ Multi-Centro de Cómputo
A diferencia de otras herramientas, CLA WinConfig permite gestionar **múltiples centros o laboratorios** desde una sola instalación:
- CID - Centro de Cómputo
- UD1 - Aula de Cómputo
- UD2 - Laboratorio de Software
- UD2 - Laboratorio de Redes
- Personalizable para agregar más centros

### 2️⃣ Gestión In - Lenguaje base
- **Tkinter** - Interfaz gráfica nativa de Windows
- **Threading** - Ejecución no bloqueantesuarios locales con:
- **Renombrado del administrador integrado** - Mayor seguridad al ocultar el usuario Admin
- **Creación de administrador personalizado** - Con nombre y contraseña institucional
- **Usuarios estándar configurables** - Sin permisos de instalación
- **Configuración UAC automática** - Siempre solicita credenciales para instalaciones
- **Obtención robusta de SIDs** - Sistema de reintentos con múltiples métodos (PowerShell + WMIC)

### 3️⃣ Aplicación Selectiva de Configuración
Característica única que permite:
- Aplicar fondos de pantalla a **usuarios específicos**
- Configurar equipos **antes de iniciar sesión** con el usuario final
- Modificación directa del registro del usuario por SID
- Limpieza automática de cachés para garantizar aplicación

### 4️⃣ Arquitectura Profesional
- **Código modular y mantenible** - Separación clara de responsabilidades
- **Sistema de callbacks** - Logs en tiempo real de todas las operaciones
- **Manejo robusto de errores** - Reintentos automáticos y mensajes claros
- **Detección automática de rutas** - Funciona tanto como script como ejecutable compilado

### 5️⃣ Experiencia de Usuario Superior
- **Interfaz Bento Card moderna** - Diseño limpio y profesional
- **Indicadores visuales claros** - Estado de cada operación en tiempo real
- **Colores institucionales** - Azul corporativo #003DA5
- **Respuesta inmediata** - Ejecución en hilos separados sin bloquear la interfaz

## 🔐 Seguridad

- El código es **100% abierto** y auditable en GitHub
- No se envía información a internet (excepto para activación opcional de Windows/Office)
- Los cambios se realizan localmente en el registro de Windows
- No se instala nada permanente en el sistema (ejecutable portable)
- **Scripts de PowerShell firmables** - Disponibles para auditoría
- **Operaciones reversibles** - Todos los cambios pueden deshacerse manualmente

## 🛠️ Desarrollo

### Tecnologías utilizadas:
- **Python 3.13+**
- **Tkinter** - Interfaz gráfirecta del registro de Windows
- **ctypes** - Interacción con APIs nativas de Windows
- **subprocess** - Ejecución de comandos PowerShell y cmd
- **pathlib** - Manejo moderno de rutas
- **PyInstaller** - Compilación a ejecutable único

### Arquitectura del Código:
-WinConfig
cd CLA-WinConfig

# Crear las carpetas necesarias para tu centro
mkdir assets\CID-Centro_Computo\wallpapers
mkdir assets\CID-Centro_Computo\lockscreen

# Ejecutar la aplicación
python src/start.py
```

### Compilar a ejecutable:

El proyecto incluye un archivo `build.spec` preconfigurado para PyInstaller:

```bash
# Instalar PyInstaller (solo primera vez)
pip install pyinstaller

# Compilar usando el spec file (recomendado)
pyinstaller build.spec
Técnicas Detalladas

### 1. Tema Oscuro del Sistema
Modifica las claves del registro:
- `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize`
- `AppsUseLightTheme` = 0
- `SystemUsesLightTheme` = 0

### 2. Fondo de Pantalla por PC
Sistema inteligente que:
- Busca archivos `PC-{numero}.jpg|png|jpeg`
- Copia a carpeta `~/Fondos` para persistencia
- Modifica registro del usuario específico por SID
- Limpia caché de Windows (`TranscodedWallpaper`, `CachedFiles`)
- Fuerza actualización con `SystemParametersInfoW`
- **Característica única**: Puede configurar fondos para **cualquier usuario local**, no solo el actual

### 3. Pantalla de Bloqueo Institucional
Configuración avanzada:
- Modifica `HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization`
- Establece `LockScreenImage` con permisos de administrador
- Bloquea cambios con políticas de grupo
- Requiere archivo `PC-Bloqueo.jpg` único para todo el centro

### 4. Bloqueo de Personalización
Implementa políticas de seguridad:
- `NoChangingWallpaper` = 1 (impide cambio de fondo)
- `NoDesktopBackgroundUI` = 1 (oculta opciones de personalización)
- Aplica a nivel de usuario mediante registro

### 5. Activación de Windows/Office
Ejecuta scripts externos con validaciones:
- Verifica conexión a internet antes de ejecutar
- Requiere permisos de administrador
- Ejecuta script PowerShell externo (no incluido)
- Captura y muestra errores de ejecución

### 6. Reinicio Inteligente del Explorador
Proceso seguro:
1. Mata todos los procesos `explorer.exe`
2. Espera 2 segundos para limpieza
3. Reinicia el explorador de Windows
4. Sincroniza cambios de registro

### 7. 👥 Gestión Avanzada de Usuarios
Sistema completo con múltiples métodos de respaldo:

**Renombrado de Administrador Integrado:**
- Detecta admin con SID terminado en `-500`
- Renombra usando PowerShell y WMIC como respaldo
- Configura descripción personalizada

**Creación de Usuarios:**
- Admin personalizado con contraseña fuerte
- Usuarios estándar limitados
- Validación de existencia previa
- Mensajes de error descriptivos

**Configuración UAC:**
- `ConsentPromptBehaviorAdmin` = 1 (solicitar credenciales)
- `ConsentPromptBehaviorUser` = 1 (solicitar credenciales)
- `EnableLUA` = 1 (activar UAC)

**Obtención Robusta de SID:**
- Método primario: `Get-LocalUser` (PowerShell)
- Método de respaldo: `WMIC useraccount`
- Sistema de reintentos: 5 intentos con espera de 2 segundos
- Timeout de 10 segundos por intento
- Validación de formato `S-1-5-*`

📖 **Documentación completa de usuarios**: Ver [CAMBIOS_USUARIOS.md](CAMBIOS_USUARIOS.md)

### 8. ⚡ Optimización de Arranque (Startup)
Sistema inteligente de optimización que mejora el tiempo de inicio del sistema:

**Funcionamiento:**
- Analiza programas de inicio en `HKLM` y `HKCU`
- Elimina entradas en `Run` de aplicaciones no esenciales
- Deshabilita programas en `StartupApproved` (Windows 10/11)
- Protege drivers y servicios críticos del sistema

**Programas deshabilitados:**
- Aplicaciones de nube: OneDrive, Dropbox
- Navegadores: Microsoft Edge, Chrome
- Mensajería: Teams, Discord, Skype, Zoom
- Actualizadores: Adobe, Java, Apple
- Launchers de juegos: Steam, Epic, Battle.net
- Reproductores: Spotify, iTunes

**Programas protegidos (nunca se deshabilitan):**
- Windows Defender / Security
- Drivers de audio (Realtek)
- Drivers gráficos (NVIDIA, AMD, Intel)
- Drivers de touchpad (Synaptics)
- Componentes críticos del sistema

**Resultado:** Mejora significativa en el tiempo de arranque del sistema sin afectar funcionalidad crítica.

## 👨‍💻 Autor

Desarrollado por **CLAAngel**  
Departamento de Sistemas Informáticos  
Universidad Politécnica del Mar y la Sierra

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la licencia [MIT](LICENSE).
