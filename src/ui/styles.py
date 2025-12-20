"""Configuración de estilos y colores para la interfaz"""
from tkinter import ttk

# Colores institucionales
COLOR_DARK_BLUE = "#061856"      # Azul oscuro
COLOR_BOLD_BLUE = "#134074"      # Azul audaz
COLOR_BLUE = "#0054A2"            # Azul
COLOR_LIGHT_BLUE = "#5590FF"      # Azul claro
COLOR_LIGHT = "#F2F9FF"           # Blanco/Neutral claro
COLOR_TEXT = "#1a1a1a"            # Texto oscuro
COLOR_CARD_BG = "#FFFFFF"         # Fondo de tarjetas
COLOR_CARD_BORDER = "#E0E0E0"     # Borde de tarjetas
COLOR_ACCENT = "#5590FF"          # Color de acento


def configurar_estilos():
    """Configura los estilos de la UI con colores institucionales"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Estilo para frames principales
    style.configure('TFrame', background=COLOR_LIGHT, bordercolor=COLOR_CARD_BORDER, lightcolor=COLOR_LIGHT_BLUE, darkcolor=COLOR_LIGHT_BLUE)
    style.configure('TLabelFrame', background=COLOR_LIGHT, foreground=COLOR_TEXT, relief='solid', borderwidth=.5, bordercolor=COLOR_CARD_BORDER, lightcolor=COLOR_LIGHT_BLUE, darkcolor=COLOR_LIGHT_BLUE)
    style.map('TLabelFrame', background=[('', COLOR_LIGHT)])
    style.configure('TLabelFrame.Label', background=COLOR_LIGHT, foreground=COLOR_BOLD_BLUE, font=('Segoe UI', 10, 'bold'))
    
    # Estilo para labels
    style.configure('TLabel', background=COLOR_LIGHT, foreground=COLOR_TEXT, font=('Segoe UI', 10))
    
    # Estilo para checkbuttons
    style.configure('TCheckbutton', background=COLOR_CARD_BG, foreground=COLOR_TEXT, font=('Segoe UI', 10), bordercolor=COLOR_CARD_BORDER, lightcolor=COLOR_LIGHT_BLUE, darkcolor=COLOR_LIGHT_BLUE)
    style.map('TCheckbutton', foreground=[('active', COLOR_BOLD_BLUE)])
    
    # Estilo para spinbox
    style.configure('TSpinbox', foreground=COLOR_TEXT, font=('Segoe UI', 10), bordercolor=COLOR_CARD_BORDER, lightcolor=COLOR_LIGHT_BLUE, darkcolor=COLOR_LIGHT_BLUE)
    
    # Estilo para botones
    style.configure('TButton', font=('Segoe UI', 10, 'bold'), bordercolor=COLOR_CARD_BORDER, lightcolor=COLOR_LIGHT_BLUE, darkcolor=COLOR_LIGHT_BLUE)
    style.map('TButton',
             background=[('', COLOR_BLUE), ('active', COLOR_BOLD_BLUE)],
             foreground=[('', 'white'), ('active', 'white')])
    
    # Estilo para progressbar
    # Estilo personalizado para Progressbar del footer
    style.configure(
        'Footer.Horizontal.TProgressbar',
        background=COLOR_LIGHT_BLUE,
        troughcolor=COLOR_BOLD_BLUE,
        bordercolor=COLOR_BOLD_BLUE,
        lightcolor=COLOR_LIGHT_BLUE,
        darkcolor=COLOR_LIGHT_BLUE,
        thickness=4 
    )

    # Estilos para tarjetas Bento
    style.configure('Card.TFrame', background=COLOR_CARD_BG, relief='flat')
    style.configure('CardTitle.TLabel', background=COLOR_CARD_BG, foreground=COLOR_BOLD_BLUE, 
                   font=('Segoe UI', 11, 'bold'))
    style.configure('CardSubtitle.TLabel', background=COLOR_CARD_BG, foreground=COLOR_TEXT, 
                   font=('Segoe UI', 9))
    
    return COLOR_LIGHT, COLOR_TEXT
