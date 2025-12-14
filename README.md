# CLA WinConfig

Herramienta para la configuración automática de PCs con Windows en centros de cómputo

## ¿Qué es CLA WinConfig?

CLA WinConfig es una aplicación de escritorio que automatiza tareas repetitivas al preparar equipos Windows, como:
- ✅ Aplicar tema oscuro del sistema
- 🖼️ Establecer fondos de pantalla personalizados por PC
- 🔒 Configurar pantalla de bloqueo institucional
- 🚫 Bloquear opciones de personalización para usuarios
- 🔄 Reiniciar el explorador de Windows
- 🔑 Activar Windows y Office (opcional)

Pensado para uso institucional, técnico y en centros de cómputo donde se necesita configurar múltiples equipos de manera estandarizada.

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

## 🔐 Seguridad

- El código es **100% abierto** y auditable
- No se envía información a internet (excepto para activación opcional)
- Los cambios se realizan localmente en el registro de Windows
- No se instala nada permanente en el sistema

## 🛠️ Desarrollo

### Tecnologías utilizadas:
- **Python 3.13+**
- **Tkinter** - Interfaz gráfica
- **winreg** - Modificación del registro de Windows
- **ctypes** - Interacción con APIs de Windows

### Instalación para desarrollo:

```bash
# Clonar el repositorio
git clone https://github.com/AngelCLA/CLA WinConfig
cd Config_PCs

# Crear las carpetas necesarias
mkdir assets\Centro_Computo\wallpapers
mkdir assets\Centro_Computo\lockscreen

# Ejecutar la aplicación
python src/start.py
```

### Compilar a ejecutable:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable
pyinstaller --onefile --windowed --icon=docs/icons/Logo-ServiciosInformaticos-2.ico src/start.py
```

## 📝 Funcionalidades detalladas

### 1. Tema Oscuro
Activa el modo oscuro del sistema operativo modificando las claves del registro de Windows.

### 2. Fondo de Pantalla
Establece un fondo de pantalla específico según el número de PC. Cada PC puede tener su propio fondo personalizado.

### 3. Pantalla de Bloqueo
Configura la imagen que aparece cuando el equipo está bloqueado (requiere permisos de administrador).

### 4. Bloquear Personalización
Impide que los usuarios cambien el fondo de pantalla mediante políticas del registro de Windows.

### 5. Activación de Windows/Office
Ejecuta un script de activación externo (requiere permisos de administrador y conexión a internet).

### 6. Reiniciar Explorador
Reinicia el proceso `explorer.exe` para aplicar los cambios visuales inmediatamente.

## 👨‍💻 Autor

Desarrollado por **CLAAngel**  
Departamento de Sistemas Informáticos  
Universidad Politécnica del Mar y la Sierra

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la licencia [MIT](LICENSE).