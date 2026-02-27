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
        'UD2-Laboratorio de Finanzas': 'UD2-Laboratorio_Finanzas',
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
            admin_frame = tk.Frame(header_bar, bg=COLOR_BOLD_BLUE)
            admin_frame.pack(side='right', padx=20)
            # Círculo verde
            tk.Label(admin_frame, text="●", fg="#4CAF50", bg=COLOR_BOLD_BLUE, font=("Segoe UI", 10, "bold")).pack(side="left")
            # Texto claro
            tk.Label(admin_frame, text="Administrador", fg=COLOR_LIGHT, bg=COLOR_BOLD_BLUE, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(4,0))
        
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
        
        # Configurar grid de la sidebar (2 filas)
        sidebar.rowconfigure(0, weight=1, uniform='row')
        sidebar.rowconfigure(1, weight=1, uniform='row')
        
        # Contenedor para Centro + Número de PC (mismo alto que Opciones de Configuración)
        top_cards_container = tk.Frame(sidebar, bg=self.COLOR_LIGHT)
        top_cards_container.grid(row=0, column=0, sticky='nsew', pady=(0, 0))

        # CARD: Centro/Identificador (bento)
        centro_card, centro_content = self.crear_bento_card(top_cards_container, "Centro")
        centro_card.pack(fill='both', expand=True, pady=(0, 12))
        tk.Label(
            centro_content,
            text="Identificador del Centro de Cómputo",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT,
            font=('Segoe UI', 9)
        ).pack(anchor='w')
        self.centro_var = tk.StringVar(value="-- Seleccionar Centro --")
        centro_combo = ttk.Combobox(centro_content, textvariable=self.centro_var, cursor="hand2", 
                                   state='readonly', font=('Segoe UI', 9), style='White.TCombobox')
        centro_combo['values'] = tuple(self.CENTROS_CARPETAS.keys())
        centro_combo.pack(fill='x', pady=12)

        # CARD: Número de PC (bento)
        pc_card, pc_content = self.crear_bento_card(top_cards_container, "Número de PC")
        pc_card.pack(fill='both', expand=True, pady=(0, 12))
        tk.Label(
            pc_content,
            text="Identificador del equipo de cómputo",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT,
            font=('Segoe UI', 9)
        ).pack(anchor='w')
        self.numero_pc_var = tk.StringVar(value="1")
        pc_input_frame = tk.Frame(pc_content, bg=COLOR_CARD_BG)
        pc_input_frame.pack(fill='x',  pady=(6, 0))

        tk.Label(pc_input_frame, text="PC #", bg=COLOR_CARD_BG, fg=COLOR_TEXT, 
            font=('Segoe UI', 10)).pack(side='left', padx=(0, 8))

        def incrementar_pc():
            try:
                val = int(self.numero_pc_var.get())
                if val < 100:
                    self.numero_pc_var.set(str(val + 1))
            except ValueError:
                self.numero_pc_var.set("1")

        def decrementar_pc():
            try:
                val = int(self.numero_pc_var.get())
                if val > 1:
                    self.numero_pc_var.set(str(val - 1))
            except ValueError:
                self.numero_pc_var.set("1")

        btn_menos = tk.Button(
            pc_input_frame,
            text="-",
            width=3,
            font=('Segoe UI', 12, 'bold'),
            command=decrementar_pc,
            bg="#e3e7ef",  # color suave, puedes cambiarlo
            fg=COLOR_TEXT,
            relief='flat',
            activebackground="#d0d4db",
            activeforeground=COLOR_TEXT,
            borderwidth=0,
            cursor='hand2',
            highlightthickness=0
        )
        btn_menos.pack(side='left', padx=(0, 4))

        numero_entry = tk.Entry(
            pc_input_frame,
            textvariable=self.numero_pc_var,
            width=5,
            justify='center',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            highlightthickness=0,
            bd=0
        )
        numero_entry.pack(side='left', fill='x')

        btn_mas = tk.Button(
            pc_input_frame,
            text="+",
            width=3,
            font=('Segoe UI', 12, 'bold'),
            command=incrementar_pc,
            bg="#e3e7ef",  # color suave, puedes cambiarlo
            fg=COLOR_TEXT,
            relief='flat',
            activebackground="#d0d4db",
            activeforeground=COLOR_TEXT,
            borderwidth=0,
            cursor='hand2',
            highlightthickness=0
        )
        btn_mas.pack(side='left', padx=(4, 0))
        
        # CARD: Registro de Actividad (sidebar fila 2)
        log_card, log_content = self.crear_bento_card(sidebar, "Registro de Actividad", "")
        log_card.grid(row=1, column=0, sticky='nsew', pady=(0, 0))
        
        # Text widget para el log
        log_frame = tk.Frame(log_content, bg=COLOR_CARD_BG)
        log_frame.pack(fill='both', expand=True)
        log_frame.pack_propagate(False)

        
        self.log_text = tk.Text(log_frame, state='disabled', 
                               font=('Consolas', 8), bg='#F8F9FA', fg=COLOR_TEXT,
                               relief='flat', padx=12, pady=6, wrap='word')
        self.log_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # Mensaje inicial
        self.log_mensaje("✓ Sistema listo. Seleccione las opciones y presione 'Aplicar Configuración'")
        self.log_mensaje("ℹ️ Las carpetas de assets se organizan por centro de cómputo")
        
        # ===== RIGHT CONTENT AREA (Columna 1) =====
        content_area = tk.Frame(main_container, bg=self.COLOR_LIGHT)
        content_area.grid(row=0, column=1, sticky='nsew', padx=(6, 12), pady=12)
        
        # Configurar grid para el área de contenido
        # 2 columnas ocupando todo el espacio
        content_area.columnconfigure(0, weight=1, uniform="cards")
        content_area.columnconfigure(1, weight=1, uniform="cards")

        # Fila única: Opciones + Usuarios ocupan todo
        content_area.rowconfigure(0, weight=1)

        # Variables de configuración
        self.tema_oscuro_var = tk.BooleanVar(value=True)
        self.fondo_pantalla_var = tk.BooleanVar(value=True)
        self.fondo_bloqueo_var = tk.BooleanVar(value=True)
        self.optimizar_arranque_var = tk.BooleanVar(value=True)
        self.bloquear_personalizacion_var = tk.BooleanVar(value=True)
        self.reiniciar_explorer_var = tk.BooleanVar(value=True)
        self.activar_windows_var = tk.BooleanVar(value=True)
        self.mostrar_keys_var = tk.BooleanVar(value=True)
        self.todas_var = tk.BooleanVar(value=True)
        self.instalar_tareas_var = tk.BooleanVar(value=False)  # NUEVA VARIABLE
        
        # Variables de gestión de usuarios
        self.renombrar_admin_var = tk.BooleanVar(value=True)
        self.cambiar_pass_admin_var = tk.BooleanVar(value=True)
        self.crear_std_var = tk.BooleanVar(value=True)
        
        # Función para crear el checkbox "Todas"
        def crear_checkbox_todas(parent):
            chk = ttk.Checkbutton(parent, text="Todas", variable=self.todas_var, cursor="hand2", 
                                 command=self.toggle_todas_opciones)
            return chk
        
        # CARD: Opciones de Configuración (arriba)
        opciones_card, opciones_content = self.crear_bento_card(content_area, 
                                                                 "Opciones de Configuración",
                                                                 "",
                                                                 extra_widget=crear_checkbox_todas)
        # Descripción debajo del título
        tk.Label(
            opciones_content,
            text="Seleccione las opciones a aplicar",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT,
            font=('Segoe UI', 9)
        ).pack(anchor='w')
        opciones_card.grid(row=0, column=0, sticky='nsew', padx=(0, 6))
        
        # Grid de checkboxes y botones
        opciones_grid = tk.Frame(opciones_content, bg=COLOR_CARD_BG)
        opciones_grid.pack(fill='both', expand=True, pady=12)
        opciones_grid.columnconfigure(0, weight=1)

        ttk.Checkbutton(opciones_grid, text="Activador (Windows + Office)", 
               variable=self.activar_windows_var, cursor="hand2")\
            .grid(row=0, column=0, sticky='w', pady=6, padx=12)

        ttk.Checkbutton(opciones_grid, text="Activar tema oscuro", 
                    variable=self.tema_oscuro_var, cursor="hand2")\
            .grid(row=1, column=0, sticky='w', pady=6, padx=12)

        ttk.Checkbutton(opciones_grid, text="Establecer fondo de pantalla", 
                    variable=self.fondo_pantalla_var, cursor="hand2")\
            .grid(row=2, column=0, sticky='w', pady=6, padx=12)

        ttk.Checkbutton(opciones_grid, text="Mostrar claves de producto", 
                    variable=self.mostrar_keys_var, cursor="hand2")\
            .grid(row=3, column=0, sticky='w', pady=6, padx=12)

        ttk.Checkbutton(opciones_grid, text="Bloquear personalización", 
                    variable=self.bloquear_personalizacion_var, cursor="hand2")\
            .grid(row=4, column=0, sticky='w', pady=6, padx=12)

        ttk.Checkbutton(opciones_grid, text="Establecer fondo de bloqueo", 
                    variable=self.fondo_bloqueo_var, cursor="hand2")\
            .grid(row=5, column=0, sticky='w', pady=6, padx=12)
        
        ttk.Checkbutton(opciones_grid, text="Optimizar arranque (recomendado)", 
                    variable=self.optimizar_arranque_var, cursor="hand2")\
            .grid(row=6, column=0, sticky='w', pady=6, padx=12)
        
        # NUEVA OPCIÓN: Instalar tareas programadas
        ttk.Checkbutton(opciones_grid, text="Instalar tareas programadas", 
                    variable=self.instalar_tareas_var, cursor="hand2")\
            .grid(row=7, column=0, sticky='w', pady=6, padx=12)
        
        ttk.Checkbutton(opciones_grid, text="Reiniciar explorador al finalizar", 
                    variable=self.reiniciar_explorer_var, cursor="hand2")\
            .grid(row=8, column=0, sticky='w', pady=6, padx=12)
        
        # --- Botones dentro del panel de opciones ---
        botones_frame = tk.Frame(opciones_content, bg=COLOR_CARD_BG)
        botones_frame.pack(fill='x', pady=(8, 0))

        btn_carpeta = tk.Button(
            botones_frame,
            text="Ver carpeta de assets",
            command=self.abrir_carpeta_fondos,
            font=('Segoe UI', 9, 'bold'),
            bg='#134074',
            fg='white',
            relief='flat',
            cursor='hand2',
            bd=0,
            pady=8,
            highlightthickness=1,
            highlightbackground=COLOR_CARD_BORDER
        )
        btn_carpeta.pack(fill='x', expand=True, pady=(0, 8))
        btn_carpeta.bind("<Enter>", lambda e: btn_carpeta.config(bg=COLOR_BLUE))
        btn_carpeta.bind("<Leave>", lambda e: btn_carpeta.config(bg='#134074'))

        self.btn_aplicar = tk.Button(
            botones_frame,
            text="Aplicar configuración",
            command=self.aplicar_configuracion,
            font=('Segoe UI', 9, 'bold'),
            bg='#0078D4',
            fg='white',
            relief='flat',
            cursor='hand2',
            bd=0,
            pady=8,
            highlightthickness=1,
            highlightbackground=COLOR_CARD_BORDER
        )
        self.btn_aplicar.pack(fill='x', expand=True)
        self.btn_aplicar.bind("<Enter>", lambda e: self.btn_aplicar.config(bg=COLOR_DARK_BLUE))
        self.btn_aplicar.bind("<Leave>", lambda e: self.btn_aplicar.config(bg='#0078D4'))

        
        # ===== CARD: Gestión de Usuarios (nueva sección) =====
        usuarios_card, usuarios_content = self.crear_bento_card(content_area, 
                                                                "Gestión de Usuarios",)
        # Descripción debajo del título
        tk.Label(
            usuarios_content,
            text="Seleccione las tareas de usuarios a realizar",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT,
            font=('Segoe UI', 9)
        ).pack(anchor='w')

        usuarios_card.grid(row=0, column=1, sticky='nsew', padx=(6, 0))
        
        # Grid para inputs de usuarios
        usuarios_grid = tk.Frame(usuarios_content, bg=COLOR_CARD_BG)
        usuarios_grid.pack(fill='both', expand=True, padx=12, pady=8)
        usuarios_grid.columnconfigure(0, weight=1)

        # --- OPCIÓN 1: Renombrar Admin ---
        ttk.Checkbutton(usuarios_grid, text="Cambiar nombre de admin", 
                       variable=self.renombrar_admin_var, cursor="hand2")\
            .grid(row=0, column=0, sticky='w', pady=(5, 2))
        
        self.admin_user_var = tk.StringVar(value="Admin-SI")
        admin_input = tk.Entry(
            usuarios_grid,
            textvariable=self.admin_user_var,
            font=('Segoe UI', 9),
            relief='flat',
            highlightthickness=1,
            highlightbackground='#D1D5DB',
            bg='white'
        )
        admin_input.grid(row=1, column=0, sticky='ew', pady=(0, 10), padx=(20, 0))

        # --- OPCIÓN 2: Cambiar Contraseña Admin ---
        ttk.Checkbutton(usuarios_grid, text="Cambiar contraseña de admin", 
                       variable=self.cambiar_pass_admin_var, cursor="hand2")\
            .grid(row=2, column=0, sticky='w', pady=(5, 2))

        self.admin_pass_var = tk.StringVar(value="Servicios.Informaticos_UPMYS!")
        admin_pass_entry = tk.Entry(
            usuarios_grid,
            textvariable=self.admin_pass_var,
            font=('Segoe UI', 9),
            show='●',
            relief='flat',
            highlightthickness=1,
            highlightbackground='#D1D5DB',
            bg='white'
        )
        admin_pass_entry.grid(row=3, column=0, sticky='ew', pady=(0, 10), padx=(20, 0))

        # --- OPCIÓN 3: Crear Usuario Estándar ---
        ttk.Checkbutton(usuarios_grid, text="Crear usuario estándar", 
                       variable=self.crear_std_var, cursor="hand2")\
            .grid(row=4, column=0, sticky='w', pady=(5, 2))

        # Usuario estándar sincronizado con el número de PC
        self.std_user_var = tk.StringVar(value=f"Usuario-{self.numero_pc_var.get()}")
        std_input = tk.Entry(
            usuarios_grid,
            textvariable=self.std_user_var,
            font=('Segoe UI', 9),
            relief='flat',
            highlightthickness=1,
            highlightbackground='#D1D5DB',
            bg='white'
        )
        std_input.grid(row=5, column=0, sticky='ew', pady=(0, 12), padx=(20, 0))

        # Actualizar usuario estándar cuando cambie el número de PC
        def actualizar_usuario_estandar(*args):
            self.std_user_var.set(f"Usuario-{self.numero_pc_var.get()}")
        self.numero_pc_var.trace_add('write', actualizar_usuario_estandar)

        # Botón para aplicar configuración de usuarios
        btn_usuarios_frame = tk.Frame(usuarios_content, bg=COLOR_CARD_BG)
        btn_usuarios_frame.pack(fill='x', pady=(8, 0))

        self.btn_usuarios = tk.Button(
            btn_usuarios_frame,
            text="Aplicar Configuración de Usuarios",
            command=self.aplicar_configuracion_usuarios,
            font=('Segoe UI', 9, 'bold'),
            bg='#0078D4',
            fg='white',
            relief='flat',
            cursor='hand2',
            bd=0,
            pady=8,
            highlightthickness=1,
            highlightbackground=COLOR_CARD_BORDER
        )
        self.btn_usuarios.pack(fill='x', expand=True)
        self.btn_usuarios.bind("<Enter>", lambda e: self.btn_usuarios.config(bg=COLOR_DARK_BLUE))
        self.btn_usuarios.bind("<Leave>", lambda e: self.btn_usuarios.config(bg='#0078D4'))
        
        # ===== FOOTER SECTION (al pie de la ventana) =====
        footer_bar = tk.Frame(self.root, bg=COLOR_BOLD_BLUE, height=70)
        footer_bar.pack(fill='x', side='bottom')
        footer_bar.pack_propagate(False)
        
        # Barra de progreso integrada en el footer (como separador delgado)
        self.progress = ttk.Progressbar(footer_bar, mode='indeterminate', style='Footer.Horizontal.TProgressbar')
        self.progress.pack(fill='x', padx=0, pady=0)
        
        # Contenedor del footer con centrado
        footer_content_bar = tk.Frame(footer_bar, bg=COLOR_BOLD_BLUE)
        footer_content_bar.pack(fill='both', expand=True)
        
        # Primera línea: Desarrollado por CLAAngel (link) - Departamento...
        line1_footer_frame = tk.Frame(footer_content_bar, bg=COLOR_BOLD_BLUE)
        line1_footer_frame.pack(pady=(8, 2))
        
        tk.Label(line1_footer_frame, text="Desarrollado por ", bg=COLOR_BOLD_BLUE, fg='white', 
                font=('Segoe UI', 9)).pack(side='left')
        
        github_link_footer = tk.Label(line1_footer_frame, text="CLAAngel", bg=COLOR_BOLD_BLUE, fg='#5590FF', 
                                      font=('Segoe UI', 9, 'underline'), cursor="hand2")
        github_link_footer.pack(side='left')
        github_link_footer.bind("<Button-1>", lambda e: self.abrir_github())
        
        tk.Label(line1_footer_frame, text=" - Departamento de Servicios Informáticos", bg=COLOR_BOLD_BLUE, fg='white', 
                font=('Segoe UI', 9)).pack(side='left')
        
        # Segunda línea: Universidad...
        line2_footer = tk.Label(footer_content_bar,
                               text="Universidad Politécnica del Mar y la Sierra © 2025.",
                               bg=COLOR_BOLD_BLUE, fg='white',
                               font=('Segoe UI', 8))
        line2_footer.pack(pady=(2, 8))

    
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
        if centro_seleccionado not in self.CENTROS_CARPETAS:
            messagebox.showwarning("Centro no seleccionado", "Por favor, seleccione un centro de cómputo primero.")
            return

        carpeta_centro = self.CENTROS_CARPETAS.get(centro_seleccionado)
        
        carpeta_assets = BASE_PATH.parent / "assets" / carpeta_centro
        carpeta_wallpapers = carpeta_assets / "wallpapers"
        carpeta_lockscreen = carpeta_assets / "lockscreen"
        carpeta_tareas = carpeta_assets / "tareasprogramadas"  # NUEVA CARPETA
        
        if not carpeta_assets.exists():
            carpeta_assets.mkdir(parents=True)
            self.log_mensaje(f"✓ Carpeta '{carpeta_centro}' creada")
        if not carpeta_wallpapers.exists():
            carpeta_wallpapers.mkdir()
            self.log_mensaje(f"✓ Carpeta '{carpeta_centro}/wallpapers' creada")
        if not carpeta_lockscreen.exists():
            carpeta_lockscreen.mkdir()
            self.log_mensaje(f"✓ Carpeta '{carpeta_centro}/lockscreen' creada")
        if not carpeta_tareas.exists():  # CREAR CARPETA DE TAREAS
            carpeta_tareas.mkdir()
            self.log_mensaje(f"✓ Carpeta '{carpeta_centro}/tareasprogramadas' creada")
        
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
        
        # Validar centro seleccionado
        centro_seleccionado = self.centro_var.get()
        if centro_seleccionado not in self.CENTROS_CARPETAS:
            messagebox.showwarning("Centro no seleccionado", "Por favor seleccione un centro de cómputo para continuar.")
            return

        # Obtener carpeta del centro seleccionado
        carpeta_centro = self.CENTROS_CARPETAS.get(centro_seleccionado)
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
            self.bloquear_personalizacion_var.get(),
            self.optimizar_arranque_var.get(),
            self.instalar_tareas_var.get(),  # NUEVA TAREA
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
            'optimizar_arranque': self.optimizar_arranque_var.get(),
            'reiniciar_explorer': self.reiniciar_explorer_var.get(),
            'mostrar_keys': self.mostrar_keys_var.get(),
            'instalar_tareas': self.instalar_tareas_var.get()  # NUEVA OPCIÓN
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
        # Validar centro seleccionado (para evitar errores de contexto)
        if self.centro_var.get() not in self.CENTROS_CARPETAS:
            messagebox.showwarning("Centro no seleccionado", "Por favor seleccione un centro de cómputo antes de configurar usuarios.")
            return

        # Verificar que al menos una opción esté seleccionada
        if not (self.renombrar_admin_var.get() or self.cambiar_pass_admin_var.get() or self.crear_std_var.get()):
            messagebox.showwarning("Sin opciones", "Seleccione al menos una tarea de usuarios para realizar")
            return

        # Obtener valores
        admin_user_nuevo = self.admin_user_var.get().strip()
        admin_pass = self.admin_pass_var.get()
        std_user = self.std_user_var.get().strip()
        
        # Validaciones condicionales
        if self.renombrar_admin_var.get() and not admin_user_nuevo:
            messagebox.showwarning("Campo requerido", "Por favor ingrese el nuevo nombre del administrador")
            return
        
        if self.cambiar_pass_admin_var.get() and not admin_pass:
            messagebox.showwarning("Campo requerido", "Por favor ingrese la contraseña del administrador")
            return
        
        if self.crear_std_var.get() and not std_user:
            messagebox.showwarning("Campo requerido", "Por favor ingrese el nombre del usuario estándar")
            return
        
        # Deshabilitar botón
        self.btn_usuarios.config(state='disabled')
        self.progress.start()
        
        # Opciones
        opciones_usuarios = {
            'renombrar_admin': self.renombrar_admin_var.get(),
            'cambiar_pass_admin': self.cambiar_pass_admin_var.get(),
            'crear_std': self.crear_std_var.get(),
            'admin_nombre': admin_user_nuevo,
            'admin_pass': admin_pass,
            'std_nombre': std_user
        }

        # Limpiar log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.ejecutar_configuracion_usuarios, 
                                 args=(opciones_usuarios,))
        thread.daemon = True
        thread.start()

    def ejecutar_configuracion_usuarios(self, opciones):
        """Ejecuta la configuración de usuarios"""
        try:
            self.log_mensaje("\n" + "="*50)
            self.log_mensaje("GESTIÓN DE USUARIOS")
            self.log_mensaje("="*50)

            gestor = GestorUsuarios(callback=self.log_mensaje)

            if not gestor.es_admin:
                self.log_mensaje("❌ Se requieren permisos de administrador")
                self.root.after(100, self.habilitar_btn_usuarios)
                return

            self.log_mensaje("✓ Permisos de administrador verificados")

            centro_seleccionado = self.centro_var.get()
            self.log_mensaje(f"📍 Centro seleccionado: {centro_seleccionado}")

            import getpass
            usuario_actual = getpass.getuser()
            
            # --- TAREA 1: Renombrar Admin ---
            if opciones['renombrar_admin']:
                self.log_mensaje(f"\n--- Cambiando nombre visible de '{usuario_actual}' ---")
                ok, msg = gestor.cambiar_nombre_visible(usuario_actual, opciones['admin_nombre'])
                self.log_mensaje(msg)
                if not ok:
                    self.root.after(100, self.habilitar_btn_usuarios)
                    return

            # --- TAREA 2: Cambiar Contraseña ---
            if opciones['cambiar_pass_admin']:
                self.log_mensaje(f"\n--- Cambiando contraseña de '{usuario_actual}' ---")
                ok, msg = gestor.cambiar_password(usuario_actual, opciones['admin_pass'])
                self.log_mensaje(msg)
                if not ok:
                    self.root.after(100, self.habilitar_btn_usuarios)
                    return

            # --- TAREA 3: Crear Usuario Estándar ---
            if opciones['crear_std']:
                self.log_mensaje(f"\n--- Creando usuario estándar '{opciones['std_nombre']}' ---")
                ok, msg = gestor.crear_usuario(opciones['std_nombre'], "", es_admin=False)
                self.log_mensaje(msg)
                if not ok and "ya existe" not in msg.lower():
                    self.log_mensaje(f"❌ Error al crear usuario: {msg}")
                    self.root.after(100, self.habilitar_btn_usuarios)
                    return

            # --- TAREA 4: Configurar UAC (Siempre se hace si se toca algo de esto, o opcional?) ---
            # Por ahora lo mantenemos como parte de la configuración base si se creó un usuario estándar
            if opciones['crear_std']:
                self.log_mensaje("\n--- Configurando UAC ---")
                ok, msg = gestor.configurar_uac()
                self.log_mensaje(msg)

            self.log_mensaje("\n" + "="*50)
            self.log_mensaje("✔ GESTIÓN DE USUARIOS FINALIZADA")
            self.log_mensaje("="*50)

            self.root.after(100, self.habilitar_btn_usuarios)

        except Exception as e:
            self.log_mensaje(f"\n❌ Error inesperado: {e}")
            import traceback
            self.log_mensaje(traceback.format_exc())
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
        self.optimizar_arranque_var.set(estado)
        self.instalar_tareas_var.set(estado)  # NUEVA LÍNEA