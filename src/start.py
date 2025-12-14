"""
Configurador de PCs - Aplicación principal
Punto de entrada para el configurador automático de PCs
"""
import os
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox

# Importar módulos de la aplicación
from core import ConfiguradorPC
from ui import InterfazConfiguradorPC


def solicitar_permisos_admin():
    """Solicita permisos de administrador al iniciar"""
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # Re-ejecutar el script con permisos de administrador
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 0
            )
            sys.exit()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener permisos de administrador:\n{e}")
        sys.exit()


def main():
    """Función principal de la aplicación"""
    # Solicitar permisos de administrador al inicio
    solicitar_permisos_admin()
    
    root = tk.Tk()
    app = InterfazConfiguradorPC(root, ConfiguradorPC)
    root.mainloop()


if __name__ == "__main__":
    main()
