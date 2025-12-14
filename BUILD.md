# Compilar el Proyecto

## Requisitos
```bash
pip install pyinstaller pillow
```

## Compilar el ejecutable

Desde la raíz del proyecto, ejecuta:

```bash
pyinstaller build.spec
```

El ejecutable se generará en la carpeta `dist/Configurador_PCs.exe`

## Iconos utilizados

- **Icono del ejecutable y barra de tareas**: `docs/icons/Logo-ServiciosInformaticos.ico`
- **Icono de la barra superior de la ventana**: `docs/icons/Logo-ServiciosInformaticos-2.ico`

## Estructura del ejecutable

El `.spec` incluye:
- Todos los archivos de `assets/` (fondos de pantalla y lockscreen por centros)
- Los iconos necesarios de `docs/icons/`
- No muestra consola (`console=False`)
- Icono principal para el .exe

## Notas importantes

1. El ejecutable buscará las carpetas `assets` relativas a su ubicación
2. Los iconos se incluyen en el ejecutable para que funcionen correctamente
3. El modo `onefile` empaqueta todo en un solo .exe
