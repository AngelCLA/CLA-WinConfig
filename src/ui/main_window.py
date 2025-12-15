"""Ventana principal del Configurador de PCs"""
import os
import sys
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from pathlib import Path
import time

# Importar estilos
from .styles import (configurar_estilos, COLOR_LIGHT, COLOR_TEXT, COLOR_BOLD_BLUE, 
                     COLOR_BLUE, COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_ACCENT, COLOR_DARK_BLUE)

# Importar módulo de usuarios
from core import GestorUsuarios

# Detectar BASE_PATH
if getattr(sys, 'frozen', False):
    BASE_PATH = Path(sys.executable).parent
else:
    BASE_PATH = Path(__file__).parent.parent


class InterfazConfiguradorPC:
    # Mapeo de centros a carpetas
    CENTROS_CARPETAS = {
        'CID-Centro de Cómputo': 'CID-Centro_Computo',
        'UD2-Laboratorio de Software': 'UD2-Laboratorio_Software',
        'UD2-Laboratorio de Redes': 'UD2-Laboratorio_Redes',
        'UD1-Centro de Cómputo': 'UD1-Centro_Computo',
        'UD1-Aula de Cómputo': 'UD1-Aula_Computo'
    }
    
    def __init__(self, root, ConfiguradorPC):
        self.root = root
        self.ConfiguradorPC = ConfiguradorPC
        self.root.title("Servicios Informaticos - Configurador de PCs")
        self.root.geometry("920x720")
        self.root.resizable(False, False)
        self.root.minsize(920, 720)
        
        # Establecer icono - usar BASE_PATH
        try:
            icono_path = BASE_PATH.parent / "docs" / "icons" / "Logo-ServiciosInformaticos-2.ico"
            if icono_path.exists():
                self.root.iconbitmap(str(icono_path.absolute()))
        except:
            pass
        
        # Centrar la ventana en la pantalla
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        # Configurar estilo con colores institucionales
        self.COLOR_LIGHT, self.COLOR_TEXT = configurar_estilos()
        
        # Verificar permisos de admin
        try:
            self.es_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            self.es_admin = False
        
        self.crear_interfaz()
    
    def crear_bento_card(self, parent, title, subtitle="", bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, extra_widget=None):
        """Crea una tarjeta estilo Bento con bordes redondeados"""
        # Container frame con bordes y sombra
        card_container = tk.Frame(parent, bg=border_color, highlightthickness=1, 
                                 highlightbackground=border_color, highlightcolor=border_color)
        
        # Frame interior con padding
        card_frame = tk.Frame(card_container, bg=bg_color)
        card_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Header de la tarjeta
        if title:
            header_frame = tk.Frame(card_frame, bg=bg_color)
            header_frame.pack(fill='x', padx=14, pady=(11, 6))
            
            title_label = tk.Label(header_frame, text=title, bg=bg_color, 
                                  fg=COLOR_BOLD_BLUE, font=('Segoe UI', 11, 'bold'))
            title_label.pack(side='left', anchor='w')
            
            # Widget extra (como checkbox) al lado derecho del título
            if extra_widget:
                extra_widget(header_frame).pack(side='right', anchor='e', padx=(10, 0))
            
            if subtitle:
                subtitle_label = tk.Label(header_frame, text=subtitle, bg=bg_color, 
                                         fg=COLOR_TEXT, font=('Segoe UI', 8))
                subtitle_label.pack(anchor='w', pady=(2, 0))
        
        # Content frame
        content_frame = tk.Frame(card_frame, bg=bg_color)
        content_frame.pack(fill='both', expand=True, padx=14, pady=(0, 11))
        
        return card_container, content_frame
        
    def crear_interfaz(self):
        # Configurar ventana principal
        self.root.configure(bg=self.COLOR_LIGHT)
        
        # ===== HEADER SECTION (Blue bar with logo) =====
        header_bar = tk.Frame(self.root, bg=COLOR_BOLD_BLUE, height=65)
        header_bar.pack(fill='x', side='top')
        header_bar.pack_propagate(False)
        
        # Logo y título en el header
        header_content = tk.Frame(header_bar, bg=COLOR_BOLD_BLUE)
        header_content.pack(side='left', padx=20, pady=10)
        
        # Logo (cargando imagen real)
        try:
            from PIL import Image, ImageTk
            logo_path = BASE_PATH.parent / "docs" / "icons" / "Logo-ServiciosInformaticos.png"
            if logo_path.exists():
                logo_img = Image.open(logo_path)
                # Redimensionar a 45px de alto manteniendo proporción
                aspect_ratio = logo_img.width / logo_img.height
                new_height = 45
                new_width = int(new_height * aspect_ratio)
                logo_img = logo_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(header_content, image=logo_photo, bg=COLOR_BOLD_BLUE)
                logo_label.image = logo_photo  # Mantener referencia
                logo_label.pack(side='left', padx=(0, 15))
            else:
                # Fallback al logo de texto
                logo = tk.Label(header_content, text="SI", bg=COLOR_BOLD_BLUE, fg='white',
                               font=('Segoe UI', 24, 'bold'), width=3, relief='solid', bd=2)
                logo.pack(side='left', padx=(0, 15))
        except:
            # Fallback al logo de texto si PIL no está disponible
            logo = tk.Label(header_content, text="SI", bg=COLOR_BOLD_BLUE, fg='white',
                           font=('Segoe UI', 24, 'bold'), width=3, relief='solid', bd=2)
            logo.pack(side='left', padx=(0, 15))
        
        # Títulos
        title_frame = tk.Frame(header_content, bg=COLOR_BOLD_BLUE)
        title_frame.pack(side='left')
        
        titulo = tk.Label(title_frame, text="Servicios Informáticos", 
                         font=('Segoe UI', 14, 'bold'), fg='white', bg=COLOR_BOLD_BLUE)
        titulo.pack(anchor='w')
        
        subtitulo = tk.Label(title_frame, text="Configurador de PCs", 
                            font=('Segoe UI', 10), fg='white', bg=COLOR_BOLD_BLUE)
        subtitulo.pack(anchor='w')
        
        # Estado de admin en la derecha
        if self.es_admin:
            admin_label = tk.Label(header_bar, text="● Administrador", 
                                  fg='#4CAF50', bg=COLOR_BOLD_BLUE, 
                                  font=('Segoe UI', 10, 'bold'))
            admin_label.pack(side='right', padx=20)
        
        # ===== MAIN CONTAINER =====
        main_container = tk.Frame(self.root, bg=self.COLOR_LIGHT)
        main_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        # ===== BENTO GRID LAYOUT - 2 columnas asimétricas =====
        # Columna izquierda: sidebar pequeña (215px fija)
        # Columna derecha: área de contenido grande (expandible)
        main_container.columnconfigure(0, weight=0, minsize=215)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=1)
        
        # ===== LEFT SIDEBAR (Columna 0) =====
        sidebar = tk.Frame(main_container, bg=self.COLOR_LIGHT)
        sidebar.grid(row=0, column=0, sticky='nsew', padx=(12, 6), pady=12)
        
        # Configurar grid de la sidebar (2 filas iguales)
        sidebar.rowconfigure(0, weight=1, uniform='row')
        sidebar.rowconfigure(1, weight=1, uniform='row')
        
        # Contenedor para Centro + Número de PC (mismo alto que Opciones de Configuración)
        top_cards_container = tk.Frame(sidebar, bg=self.COLOR_LIGHT)
        top_cards_container.grid(row=0, column=0, sticky='nsew', pady=(0, 6))
        
        # CARD: Centro/Identificador
        centro_card, centro_content = self.crear_bento_card(top_cards_container, "Centro", 
                                                            "Identificador del Centro de Cómputo")
        centro_card.pack(fill='both', expand=True, pady=(0, 12))
        
        # Dropdown del centro
        self.centro_var = tk.StringVar(value="CID-Centro de Cómputo")
        centro_combo = ttk.Combobox(centro_content, textvariable=self.centro_var, 
                                   state='readonly', font=('Segoe UI', 9))
        centro_combo['values'] = tuple(self.CENTROS_CARPETAS.keys())
        centro_combo.pack(fill='x', pady=12)
        
        # CARD: Número de PC
        pc_card, pc_content = self.crear_bento_card(top_cards_container, "Número de PC", 
                                                    "Identificador del equipo")
        pc_card.pack(fill='both', expand=True, pady=(0, 0))
        
        self.numero_pc_var = tk.StringVar(value="1")
        pc_input_frame = tk.Frame(pc_content, bg=COLOR_CARD_BG)
        pc_input_frame.pack(fill='x', pady=12)
        
        tk.Label(pc_input_frame, text="PC #", bg=COLOR_CARD_BG, fg=COLOR_TEXT, 
                font=('Segoe UI', 10)).pack(side='left', padx=(0, 8))
        numero_spin = ttk.Spinbox(pc_input_frame, from_=1, to=100, 
                                 textvariable=self.numero_pc_var, width=8, 
                                 font=('Segoe UI', 11, 'bold'))
        numero_spin.pack(side='left', fill='x', expand=True)
        
        # Contenedor para Botones + Progressbar (mismo alto que Registro de Actividad)
        bottom_cards_container = tk.Frame(sidebar, bg=self.COLOR_LIGHT)
        bottom_cards_container.grid(row=1, column=0, sticky='nsew', pady=(6, 0))
        
        # CARD: Botón Aplicar Configuración (sin fondo blanco)
        self.btn_aplicar = tk.Button(bottom_cards_container, text="Aplicar\nConfiguración", 
                                     command=self.aplicar_configuracion,
                                     font=('Segoe UI', 11, 'bold'), bg=COLOR_ACCENT, fg='white',
                                     relief='flat', cursor='hand2', bd=0, pady=20,
                                     highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
        self.btn_aplicar.pack(fill='x', pady=(0, 12))
        self.btn_aplicar.bind("<Enter>", lambda e: self.btn_aplicar.config(bg=COLOR_BLUE))
        self.btn_aplicar.bind("<Leave>", lambda e: self.btn_aplicar.config(bg=COLOR_ACCENT))
        
        # CARD: Botón Abrir Carpeta Assets (sin fondo blanco)
        btn_carpeta = tk.Button(bottom_cards_container, text="Abrir\nCarpeta Assets", 
                               command=self.abrir_carpeta_fondos,
                               font=('Segoe UI', 10, 'bold'), bg=COLOR_BOLD_BLUE, fg='white',
                               relief='flat', cursor='hand2', bd=0, pady=20,
                               highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
        btn_carpeta.pack(fill='x', pady=(0, 12))
        btn_carpeta.bind("<Enter>", lambda e: btn_carpeta.config(bg=COLOR_DARK_BLUE))
        btn_carpeta.bind("<Leave>", lambda e: btn_carpeta.config(bg=COLOR_BOLD_BLUE))
        
        # Barra de progreso (sin fondo blanco)
        self.progress = ttk.Progressbar(bottom_cards_container, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 12))
        
        # Footer card
        footer_card, footer_content = self.crear_bento_card(bottom_cards_container, "", "")
        footer_card.pack(fill='x', pady=(0, 0))
        
        # Primera línea
        line1 = tk.Frame(footer_content, bg=COLOR_CARD_BG)
        line1.pack(pady=2)
        
        tk.Label(line1, text="Desarrollado por ", bg=COLOR_CARD_BG, 
                fg=COLOR_TEXT, font=('Segoe UI', 8)).pack(side='left')
        
        github_link = tk.Label(line1, text="CLAAngel", bg=COLOR_CARD_BG, 
                              fg=COLOR_BLUE, font=('Segoe UI', 8, 'underline'), 
                              cursor="hand2")
        github_link.pack(side='left')
        github_link.bind("<Button-1>", lambda e: self.abrir_github())
        
        # Segunda línea
        tk.Label(footer_content, text="Departamento de Servicios Informáticos", 
                bg=COLOR_CARD_BG, fg=COLOR_TEXT, 
                font=('Segoe UI', 8)).pack(pady=2)
        
        # Tercera línea
        tk.Label(footer_content, text="Universidad Politécnica del Mar y la Sierra", 
                bg=COLOR_CARD_BG, fg=COLOR_TEXT, 
                font=('Segoe UI', 8)).pack(pady=2)
        
        # ===== RIGHT CONTENT AREA (Columna 1) =====
        content_area = tk.Frame(main_container, bg=self.COLOR_LIGHT)
        content_area.grid(row=0, column=1, sticky='nsew', padx=(6, 12), pady=12)
        
        # Configurar grid para el área de contenido (3 filas: opciones, usuarios, log)
        content_area.rowconfigure(0, weight=0, minsize=180)  # Opciones de Configuración
        content_area.rowconfigure(1, weight=0, minsize=200)  # Gestión de Usuarios
        content_area.rowconfigure(2, weight=1)               # Registro de Actividad (expandible)
        content_area.columnconfigure(0, weight=1)
        
        # Variables de configuración
        self.tema_oscuro_var = tk.BooleanVar(value=True)
        self.fondo_pantalla_var = tk.BooleanVar(value=True)
        self.fondo_bloqueo_var = tk.BooleanVar(value=True)
        self.bloquear_personalizacion_var = tk.BooleanVar(value=True)
        self.reiniciar_explorer_var = tk.BooleanVar(value=True)
        self.activar_windows_var = tk.BooleanVar(value=True)
        self.mostrar_keys_var = tk.BooleanVar(value=True)
        self.todas_var = tk.BooleanVar(value=True)
        
        # Función para crear el checkbox "Todas"
        def crear_checkbox_todas(parent):
            chk = ttk.Checkbutton(parent, text="Todas", variable=self.todas_var, 
                                 command=self.toggle_todas_opciones)
            return chk
        
        # CARD: Opciones de Configuración (arriba)
        opciones_card, opciones_content = self.crear_bento_card(content_area, 
                                                                 "Opciones de Configuración",
                                                                 "",
                                                                 extra_widget=crear_checkbox_todas)
        opciones_card.grid(row=0, column=0, sticky='nsew', pady=(0, 6))
        
        # Grid de checkboxes
        opciones_grid = tk.Frame(opciones_content, bg=COLOR_CARD_BG)
        opciones_grid.pack(fill='both', expand=True, pady=12)
        opciones_grid.columnconfigure(0, weight=1)
        opciones_grid.columnconfigure(1, weight=1)
        
        # Organizar en 2 columnas
        ttk.Checkbutton(opciones_grid, text="Activador (Windows + Office)", 
                       variable=self.activar_windows_var).grid(row=0, column=0, sticky='w', pady=6, padx=12)
        ttk.Checkbutton(opciones_grid, text="Activar tema oscuro", 
                       variable=self.tema_oscuro_var).grid(row=1, column=0, sticky='w', pady=6, padx=12)
        ttk.Checkbutton(opciones_grid, text="Establecer fondo de pantalla", 
                       variable=self.fondo_pantalla_var).grid(row=2, column=0, sticky='w', pady=6, padx=12)
        ttk.Checkbutton(opciones_grid, text="Mostrar claves de producto", 
                       variable=self.mostrar_keys_var).grid(row=3, column=0, sticky='w', pady=6, padx=12)
        ttk.Checkbutton(opciones_grid, text="Bloquear personalización", 
                       variable=self.bloquear_personalizacion_var).grid(row=0, column=1, sticky='w', pady=6, padx=12)
        ttk.Checkbutton(opciones_grid, text="Establecer fondo de bloqueo", 
                       variable=self.fondo_bloqueo_var).grid(row=1, column=1, sticky='w', pady=6, padx=12)
        ttk.Checkbutton(opciones_grid, text="Reiniciar explorador al finalizar", 
                       variable=self.reiniciar_explorer_var).grid(row=2, column=1, sticky='w', pady=6, padx=12)
        
        # ===== CARD: Gestión de Usuarios (nueva sección) =====
        usuarios_card, usuarios_content = self.crear_bento_card(content_area, 
                                                                "Gestión de Usuarios",
                                                                "Configurar administrador y crear usuario estándar")
        usuarios_card.grid(row=1, column=0, sticky='nsew', pady=(6, 6))
        
        # Grid para inputs de usuarios
        usuarios_grid = tk.Frame(usuarios_content, bg=COLOR_CARD_BG)
        usuarios_grid.pack(fill='both', expand=True, padx=0, pady=0)
        usuarios_grid.columnconfigure(0, weight=0, minsize=130)
        usuarios_grid.columnconfigure(1, weight=1)
        
        # Nuevo nombre administrador
        tk.Label(usuarios_grid, text="Nuevo Nombre Admin:", bg=COLOR_CARD_BG, 
                fg=COLOR_TEXT, font=('Segoe UI', 9)).grid(row=0, column=0, sticky='w', padx=12, pady=(8, 4))
        self.admin_user_var = tk.StringVar(value="Administrador")
        admin_input = tk.Entry(usuarios_grid, textvariable=self.admin_user_var, 
                              font=('Segoe UI', 9), width=15)
        admin_input.grid(row=0, column=1, sticky='ew', padx=(0, 12), pady=(8, 4))
        
        # Contraseña administrador
        tk.Label(usuarios_grid, text="Contraseña Admin:", bg=COLOR_CARD_BG, 
                fg=COLOR_TEXT, font=('Segoe UI', 9)).grid(row=1, column=0, sticky='w', padx=12, pady=4)
        self.admin_pass_var = tk.StringVar()
        admin_pass = tk.Entry(usuarios_grid, textvariable=self.admin_pass_var, 
                             font=('Segoe UI', 9), show='●', width=15)
        admin_pass.grid(row=1, column=1, sticky='ew', padx=(0, 12), pady=4)
        
        # Usuario estándar
        tk.Label(usuarios_grid, text="Usuario Estándar:", bg=COLOR_CARD_BG, 
                fg=COLOR_TEXT, font=('Segoe UI', 9)).grid(row=2, column=0, sticky='w', padx=12, pady=4)
        self.std_user_var = tk.StringVar(value="alumno")
        std_input = tk.Entry(usuarios_grid, textvariable=self.std_user_var, 
                            font=('Segoe UI', 9), width=15)
        std_input.grid(row=2, column=1, sticky='ew', padx=(0, 12), pady=(4, 8))
        
        # Botón para aplicar configuración de usuarios
        btn_usuarios_frame = tk.Frame(usuarios_content, bg=COLOR_CARD_BG)
        btn_usuarios_frame.pack(fill='x', padx=12, pady=(4, 8))
        btn_usuarios_frame.columnconfigure(0, weight=1)
        
        self.btn_usuarios = tk.Button(btn_usuarios_frame, text="Aplicar Configuración de Usuarios", 
                                      command=self.aplicar_configuracion_usuarios,
                                      font=('Segoe UI', 9, 'bold'), bg='#0078D4', fg='white',
                                      relief='flat', cursor='hand2', bd=0, pady=8,
                                      highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
        self.btn_usuarios.grid(row=0, column=0, sticky='ew')
        self.btn_usuarios.bind("<Enter>", lambda e: self.btn_usuarios.config(bg=COLOR_BLUE))
        self.btn_usuarios.bind("<Leave>", lambda e: self.btn_usuarios.config(bg='#0078D4'))
        
        # CARD: Registro de Actividad (abajo, expandible)
        log_card, log_content = self.crear_bento_card(content_area, "Registro de Actividad", "")
        log_card.grid(row=2, column=0, sticky='nsew', pady=(6, 0))
        
        # Text widget para el log
        log_frame = tk.Frame(log_content, bg=COLOR_CARD_BG)
        log_frame.pack(fill='both', expand=True)
        
        self.log_text = tk.Text(log_frame, state='disabled', 
                               font=('Consolas', 9), bg='#F8F9FA', fg=COLOR_TEXT,
                               relief='flat', padx=12, pady=10, wrap='word')
        self.log_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # Mensaje inicial
        self.log_mensaje("✓ Sistema listo. Seleccione las opciones y presione 'Aplicar Configuración'")
        self.log_mensaje("ℹ️ Las carpetas de assets se organizan por centro de cómputo")
    
    def log_mensaje(self, mensaje):
        """Agrega un mensaje al log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, mensaje + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
    
    def abrir_carpeta_fondos(self):
        """Abre la carpeta de assets del centro seleccionado o la crea si no existe"""
        centro_seleccionado = self.centro_var.get()
        carpeta_centro = self.CENTROS_CARPETAS.get(centro_seleccionado, 'CID-Centro_Computo')
        
        carpeta_assets = BASE_PATH.parent / "assets" / carpeta_centro
        carpeta_wallpapers = carpeta_assets / "wallpapers"
        carpeta_lockscreen = carpeta_assets / "lockscreen"
        
        if not carpeta_assets.exists():
            carpeta_assets.mkdir(parents=True)
            self.log_mensaje(f"✓ Carpeta '{carpeta_centro}' creada")
        if not carpeta_wallpapers.exists():
            carpeta_wallpapers.mkdir()
            self.log_mensaje(f"✓ Carpeta '{carpeta_centro}/wallpapers' creada")
        if not carpeta_lockscreen.exists():
            carpeta_lockscreen.mkdir()
            self.log_mensaje(f"✓ Carpeta '{carpeta_centro}/lockscreen' creada")
        
        os.startfile(carpeta_assets)
    
    def abrir_github(self):
        """Abre el enlace de GitHub en el navegador"""
        webbrowser.open("https://github.com/AngelCLA")
    
    def aplicar_configuracion(self):
        """Aplica la configuración en un hilo separado"""
        # Validar número de PC
        try:
            numero_pc = int(self.numero_pc_var.get())
            if numero_pc < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número de PC válido")
            return
        
        # Obtener carpeta del centro seleccionado
        centro_seleccionado = self.centro_var.get()
        carpeta_centro = self.CENTROS_CARPETAS.get(centro_seleccionado, 'CID-Centro_Computo')
        carpeta_centro_path = BASE_PATH.parent / "assets" / carpeta_centro
        
        # Verificar que existen las carpetas assets del centro
        if not (carpeta_centro_path / "wallpapers").exists() or not (carpeta_centro_path / "lockscreen").exists():
            messagebox.showerror("Error", f"No se encontraron las carpetas del centro '{centro_seleccionado}'.\n" +
                               "Use el botón 'Abrir Carpeta Assets' para crearlas.")
            return
        
        # Verificar que al menos una opción de configuración está seleccionada
        tareas_configuracion = [
            self.activar_windows_var.get(),
            self.tema_oscuro_var.get(),
            self.fondo_pantalla_var.get(),
            self.fondo_bloqueo_var.get(),
            self.bloquear_personalizacion_var.get()
        ]
        
        if not any(tareas_configuracion):
            messagebox.showwarning("Sin opciones seleccionadas", 
                                  "Por favor seleccione al menos una opción de configuración para continuar.")
            return
        
        # Deshabilitar botón
        self.btn_aplicar.config(state='disabled')
        self.progress.start()
        
        # Limpiar log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Crear opciones
        opciones = {
            'activar_windows': self.activar_windows_var.get(),
            'tema_oscuro': self.tema_oscuro_var.get(),
            'fondo_pantalla': self.fondo_pantalla_var.get(),
            'fondo_bloqueo': self.fondo_bloqueo_var.get(),
            'bloquear_personalizacion': self.bloquear_personalizacion_var.get(),
            'reiniciar_explorer': self.reiniciar_explorer_var.get(),
            'mostrar_keys': self.mostrar_keys_var.get()
        }
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.ejecutar_configuracion, 
                                 args=(numero_pc, opciones, carpeta_centro))
        thread.daemon = True
        thread.start()
    
    def ejecutar_configuracion(self, numero_pc, opciones, carpeta_centro):
        """Ejecuta la configuración"""
        try:
            configurador = self.ConfiguradorPC(numero_pc, carpeta_centro=carpeta_centro, callback=self.log_mensaje)
            exitosos, total = configurador.aplicar_configuracion_completa(opciones)
            
            self.root.after(100, lambda: self.finalizar_configuracion(exitosos, total))
        except Exception as e:
            self.log_mensaje(f"\n❌ Error inesperado: {e}")
            self.root.after(100, self.habilitar_boton)
    
    def finalizar_configuracion(self, exitosos, total):
        """Finaliza el proceso de configuración"""
        self.progress.stop()
        self.btn_aplicar.config(state='normal')
        
        # Crear un diálogo personalizado con Toplevel para garantizar el foco
        dialog = tk.Toplevel(self.root)
        dialog.title("Configuración Completada")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='white')
        
        # Contenido del diálogo
        if exitosos == total:
            icono_text = "✓"
            icono_color = '#4CAF50'
            titulo = "Éxito"
            mensaje = f"Configuración completada exitosamente\nPC{self.numero_pc_var.get()} configurada correctamente"
        else:
            icono_text = "⚠"
            icono_color = '#FF9800'
            titulo = "Completado con advertencias"
            mensaje = f"Configuración completada: {exitosos}/{total} tareas\nRevise el registro para más detalles"
        
        # Frame contenedor con padding
        content_frame = tk.Frame(dialog, bg='white', padx=30, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Icono
        icono_label = tk.Label(content_frame, text=icono_text, font=('Segoe UI', 48), 
                              fg=icono_color, bg='white')
        icono_label.pack(pady=(10, 10))
        
        # Mensaje
        mensaje_label = tk.Label(content_frame, text=mensaje, font=('Segoe UI', 11), 
                                justify='center', bg='white', wraplength=400)
        mensaje_label.pack(pady=10, padx=20)
        
        def cerrar_dialog():
            dialog.attributes('-topmost', False)
            dialog.destroy()
        
        btn_ok = tk.Button(content_frame, text="Aceptar", command=cerrar_dialog,
                          font=('Segoe UI', 11, 'bold'), bg='#0054A2', fg='white',
                          relief='flat', cursor='hand2', padx=40, pady=12)
        btn_ok.pack(pady=(15, 10))
        btn_ok.focus_set()
        
        # Permitir cerrar con Enter o Escape
        dialog.bind('<Return>', lambda e: cerrar_dialog())
        dialog.bind('<Escape>', lambda e: cerrar_dialog())
        
        # Actualizar para calcular el tamaño necesario
        dialog.update_idletasks()
        
        # Centrar el diálogo en la pantalla
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (dialog_width // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog_height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Forzar topmost y foco
        dialog.attributes('-topmost', True)
        dialog.lift()
        dialog.focus_force()
        
        # Esperar a que se cierre el diálogo
        dialog.wait_window()
    
    def habilitar_boton(self):
        """Habilita el botón de aplicar"""
        self.progress.stop()
        self.btn_aplicar.config(state='normal')
    
    def aplicar_configuracion_usuarios(self):
        """Aplica la configuración de usuarios en un hilo separado"""
        # Obtener valores
        admin_user_nuevo = self.admin_user_var.get().strip()
        admin_pass = self.admin_pass_var.get()
        std_user = self.std_user_var.get().strip()
        
        # Validaciones básicas
        if not admin_user_nuevo:
            messagebox.showwarning("Campo requerido", "Por favor ingrese el nuevo nombre del administrador")
            return
        
        if not admin_pass:
            messagebox.showwarning("Campo requerido", "Por favor ingrese la contraseña del administrador")
            return
        
        if not std_user:
            messagebox.showwarning("Campo requerido", "Por favor ingrese el nombre del usuario estándar")
            return
        
        # Deshabilitar botón
        self.btn_usuarios.config(state='disabled')
        self.progress.start()
        
        # Limpiar log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.ejecutar_configuracion_usuarios, 
                                 args=(admin_user_nuevo, admin_pass, std_user))
        thread.daemon = True
        thread.start()
    
    def ejecutar_configuracion_usuarios(self, admin_user_nuevo, admin_pass, std_user):
        """Ejecuta la configuración de usuarios"""
        try:
            self.log_mensaje("\n=== Iniciando Gestión de Usuarios ===")
            
            # Crear gestor de usuarios
            gestor = GestorUsuarios(callback=self.log_mensaje)
            
            # Verificar permisos de administrador
            if not gestor.es_admin:
                self.log_mensaje("❌ Se requieren permisos de administrador para cambiar configuración")
                self.root.after(100, self.habilitar_btn_usuarios)
                return
            
            self.log_mensaje("✓ Permisos de administrador verificados")
            
            # Detectar automáticamente el usuario administrador actual
            self.log_mensaje("\n→ Detectando usuario administrador actual...")
            admin_user_actual = gestor.obtener_usuario_admin()
            
            if admin_user_actual:
                self.log_mensaje(f"✓ Usuario administrador detectado: '{admin_user_actual}'")
            else:
                # Si no se puede detectar, usar el nombre nuevo proporcionado
                self.log_mensaje("⚠️  No se pudo detectar automáticamente, intentando con el nombre proporcionado...")
                # Verificar si el nombre nuevo existe
                if gestor.usuario_existe(admin_user_nuevo):
                    admin_user_actual = admin_user_nuevo
                    self.log_mensaje(f"✓ Usuario '{admin_user_nuevo}' encontrado")
                else:
                    self.log_mensaje(f"❌ No se encontró ningún usuario administrador en el sistema")
                    self.log_mensaje(f"   Asegúrese de que existe un usuario administrador")
                    self.root.after(100, self.habilitar_btn_usuarios)
                    return
            
            exitos = []
            
            # Renombrar usuario administrador al nombre deseado (solo si es diferente)
            if admin_user_actual != admin_user_nuevo:
                self.log_mensaje(f"\n→ Renombrando administrador: '{admin_user_actual}' → '{admin_user_nuevo}'...")
                exito_rename, msg_rename = gestor.renombrar_usuario(admin_user_actual, admin_user_nuevo)
                self.log_mensaje(msg_rename)
                exitos.append(exito_rename)
                # Usar el nuevo nombre para los siguientes comandos
                nombre_admin_final = admin_user_nuevo
            else:
                nombre_admin_final = admin_user_actual
                self.log_mensaje(f"\n→ Administrador ya tiene el nombre deseado: '{nombre_admin_final}'")
                exitos.append(True)
            
            # Cambiar contraseña del administrador
            self.log_mensaje(f"\n→ Asignando contraseña al administrador: '{nombre_admin_final}'...")
            exito_pass, msg_pass = gestor.cambiar_contraseña_usuario(nombre_admin_final, admin_pass)
            self.log_mensaje(msg_pass)
            exitos.append(exito_pass)
            
            # Crear usuario estándar sin contraseña
            self.log_mensaje(f"\n→ Creando usuario estándar: '{std_user}' (sin contraseña)...")
            exito_std, msg_std = gestor.crear_usuario(std_user, "", es_admin=False)
            self.log_mensaje(msg_std)
            exitos.append(exito_std)
            
            # Configurar UAC
            self.log_mensaje("\n→ Configurando UAC...")
            exito_uac, msg_uac = gestor.configurar_uac()
            self.log_mensaje(msg_uac)
            exitos.append(exito_uac)
            
            # Resumen
            self.log_mensaje("\n=== Resumen de Operaciones ===")
            
            if admin_user_actual != admin_user_nuevo:
                self.log_mensaje(f"{'✓' if exitos[0] else '✗'} Renombre de {admin_user_actual} a {admin_user_nuevo}")
                self.log_mensaje(f"{'✓' if exitos[1] else '✗'} Contraseña de {nombre_admin_final} asignada")
                self.log_mensaje(f"{'✓' if exitos[2] else '✗'} Usuario estándar {std_user} creado (sin contraseña)")
                self.log_mensaje(f"{'✓' if exitos[3] else '✗'} UAC configurado")
            else:
                self.log_mensaje(f"{'✓' if exitos[1] else '✗'} Contraseña de {nombre_admin_final} asignada")
                self.log_mensaje(f"{'✓' if exitos[2] else '✗'} Usuario estándar {std_user} creado (sin contraseña)")
                self.log_mensaje(f"{'✓' if exitos[3] else '✗'} UAC configurado")
            
            self.root.after(100, self.habilitar_btn_usuarios)
            
        except Exception as e:
            self.log_mensaje(f"\n❌ Error inesperado: {e}")
            self.root.after(100, self.habilitar_btn_usuarios)
    
    def habilitar_btn_usuarios(self):
        """Habilita el botón de usuarios"""
        self.progress.stop()
        self.btn_usuarios.config(state='normal')
    
    
    def toggle_todas_opciones(self):
        """Marca o desmarca todas las opciones de configuración"""
        estado = self.todas_var.get()
        
        # Lista de todas las variables de opciones
        self.activar_windows_var.set(estado)
        self.tema_oscuro_var.set(estado)
        self.fondo_pantalla_var.set(estado)
        self.fondo_bloqueo_var.set(estado)
        self.bloquear_personalizacion_var.set(estado)
        self.reiniciar_explorer_var.set(estado)
        self.mostrar_keys_var.set(estado)
