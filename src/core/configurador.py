"""Lógica de configuración del PC"""
import os
import sys
import winreg
import ctypes
from pathlib import Path

# Detectar si está empaquetado en .exe
if getattr(sys, 'frozen', False):
    # Ruta cuando está en .exe
    BASE_PATH = Path(sys.executable).parent
else:
    # Ruta cuando se ejecuta como script
    BASE_PATH = Path(__file__).parent.parent


class ConfiguradorPC:
    def __init__(self, numero_pc, carpeta_centro='CID-Centro_Computo', callback=None):
        self.numero_pc = numero_pc
        self.carpeta_centro = carpeta_centro
        carpeta_base = BASE_PATH.parent / "assets" / carpeta_centro
        self.ruta_wallpapers = carpeta_base / "wallpapers"
        self.ruta_lockscreen = carpeta_base / "lockscreen"
        self.es_admin = self.verificar_admin()
        self.callback = callback
        
    def log(self, mensaje):
        """Envía mensaje al callback si existe"""
        if self.callback:
            self.callback(mensaje)
        
    def verificar_admin(self):
        """Verifica si el script se está ejecutando con permisos de administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def solicitar_admin(self):
        """Re-ejecuta el script con permisos de administrador"""
        if not self.es_admin:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit()
        
    def establecer_tema_oscuro(self):
        """Activa el tema oscuro de Windows"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            self.log("✓ Tema oscuro activado")
            return True
        except Exception as e:
            self.log(f"✗ Error al activar tema oscuro: {e}")
            return False
    
    def establecer_fondo_pantalla(self):
        """Establece el fondo de pantalla según el número de PC"""
        try:
            archivo_fondo = None
            for ext in ['.jpg', '.png', '.jpeg']:
                ruta = self.ruta_wallpapers / f"PC-{self.numero_pc}{ext}"
                if ruta.exists():
                    archivo_fondo = ruta
                    break
            
            if not archivo_fondo:
                self.log(f"✗ No se encontró PC-{self.numero_pc}.jpg o PC-{self.numero_pc}.png")
                return False
            
            ruta_absoluta = str(archivo_fondo.absolute())
            SPI_SETDESKWALLPAPER = 0x0014
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, ruta_absoluta, 3)
            self.log(f"✓ Fondo de pantalla establecido: {archivo_fondo.name}")
            return True
        except Exception as e:
            self.log(f"✗ Error al establecer fondo de pantalla: {e}")
            return False
    
    def establecer_fondo_bloqueo(self):
        """Establece el fondo de pantalla de bloqueo"""
        if not self.es_admin:
            self.log("⚠️  Fondo de bloqueo omitido (requiere permisos de administrador)")
            return False
            
        try:
            archivo_bloqueo = None
            for ext in ['.jpg', '.png', '.jpeg']:
                ruta = self.ruta_lockscreen / f"PC-Bloqueo{ext}"
                if ruta.exists():
                    archivo_bloqueo = ruta
                    break
            
            if not archivo_bloqueo:
                self.log("✗ No se encontró PC-Bloqueo.jpg o PC-Bloqueo.png")
                return False
            
            try:
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\Policies\Microsoft\Windows\Personalization",
                                        0, winreg.KEY_SET_VALUE)
            except:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"SOFTWARE\Policies\Microsoft\Windows\Personalization",
                                   0, winreg.KEY_SET_VALUE)
            
            ruta_absoluta = str(archivo_bloqueo.absolute())
            winreg.SetValueEx(key, "LockScreenImage", 0, winreg.REG_SZ, ruta_absoluta)
            winreg.CloseKey(key)
            self.log("✓ Fondo de bloqueo establecido")
            return True
        except Exception as e:
            self.log(f"✗ Error al establecer fondo de bloqueo: {e}")
            return False
    
    def bloquear_personalizacion(self):
        """Bloquea las opciones de personalización para el usuario"""
        try:
            archivo_fondo = None
            for ext in ['.jpg', '.png', '.jpeg']:
                ruta = self.ruta_wallpapers / f"PC-{self.numero_pc}{ext}"
                if ruta.exists():
                    archivo_fondo = ruta
                    break
            
            if not archivo_fondo:
                self.log("✗ No se puede bloquear personalización sin archivo de fondo")
                return False
            
            try:
                key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 
                                        r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                                        0, winreg.KEY_SET_VALUE)
            except:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                   r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                                   0, winreg.KEY_SET_VALUE)
            
            winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, str(archivo_fondo.absolute()))
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "2")
            winreg.CloseKey(key)
            
            try:
                key2 = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,
                                         r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                                         0, winreg.KEY_SET_VALUE)
            except:
                key2 = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                    r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                                    0, winreg.KEY_SET_VALUE)
            
            winreg.SetValueEx(key2, "NoThemesTab", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key2, "NoControlPanel", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key2)
            
            self.log("✓ Personalización bloqueada")
            return True
        except Exception as e:
            self.log(f"✗ Error al bloquear personalización: {e}")
            return False
    
    def reiniciar_explorer(self):
        """Reinicia el explorador de Windows para aplicar cambios"""
        try:
            os.system("taskkill /f /im explorer.exe >nul 2>&1")
            os.system("start /B explorer.exe")
            self.log("✓ Explorador reiniciado")
            return True
        except Exception as e:
            self.log(f"✗ Error al reiniciar explorador: {e}")
            return False
    
    def obtener_clave_windows(self):
        """Obtiene la clave de producto de Windows"""
        try:
            import subprocess
            resultado = subprocess.run(
                ['powershell', '-Command', 
                 '(Get-WmiObject -query "select * from SoftwareLicensingService").OA3xOriginalProductKey'],
                capture_output=True, text=True, timeout=10
            )
            clave = resultado.stdout.strip()
            if clave and len(clave) > 10:
                return clave
            return None
        except:
            return None
    
    def obtener_clave_office(self):
        """Obtiene la última clave de Office instalada"""
        try:
            import subprocess
            
            # Intentar buscar Office en diferentes versiones
            rutas_office = [
                r"C:\Program Files\Microsoft Office\Office16",
                r"C:\Program Files (x86)\Microsoft Office\Office16",
                r"C:\Program Files\Microsoft Office\Office15",
                r"C:\Program Files (x86)\Microsoft Office\Office15"
            ]
            
            for ruta in rutas_office:
                if not os.path.exists(ruta):
                    continue
                    
                try:
                    # Ejecutar ospp.vbs con cscript
                    resultado = subprocess.run(
                        ['cscript', f'{ruta}\\ospp.vbs', '/dstatus'],
                        capture_output=True, text=True, timeout=15, 
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    
                    # Buscar la línea con "Last 5 characters"
                    for linea in resultado.stdout.split('\n'):
                        if "Last 5 characters" in linea:
                            import re
                            match = re.search(r'Last 5 characters[^\:]*:\s*(\w+)', linea)
                            if match:
                                return f"*****-*****-*****-*****-{match.group(1)}"
                except:
                    continue
                    
            return None
        except Exception as e:
            return None
    
    def activar_windows(self):
        """Activa Windows y Office ejecutando el script de activación"""
        if not self.es_admin:
            self.log("⚠️  Activación omitida (requiere permisos de administrador)")
            return False
        
        try:
            self.log("⏳ Iniciando activación (Windows + Office)...")
            comando = 'powershell -Command "irm https://get.activated.win | iex"'
            resultado = os.system(comando)
            if resultado == 0:
                self.log("✓ Windows y Office activados correctamente")
                return True
            else:
                self.log("✗ Error durante la activación")
                return False
        except Exception as e:
            self.log(f"✗ Error al activar: {e}")
            return False
    
    def aplicar_configuracion_completa(self, opciones):
        """Aplica las configuraciones seleccionadas"""
        self.log(f"\n{'='*50}")
        self.log(f"Configurando PC-{self.numero_pc}")
        self.log(f"{'='*50}\n")
        
        if not self.es_admin:
            self.log("⚠️  NOTA: Ejecutando sin permisos de administrador")
            self.log("   Algunas funciones estarán limitadas\n")
        
        exitosos = 0
        total = 0
        
        # Contar solo las tareas de configuración real (excluir mostrar_keys y reiniciar_explorer)
        tareas_configuracion = ['activar_windows', 'tema_oscuro', 'fondo_pantalla', 
                                'fondo_bloqueo', 'bloquear_personalizacion']
        total = sum(1 for key in tareas_configuracion if opciones.get(key, False))
        
        if opciones.get('activar_windows', False):
            if self.activar_windows(): exitosos += 1
        
        if opciones.get('tema_oscuro', False):
            if self.establecer_tema_oscuro(): exitosos += 1
            
        if opciones.get('fondo_pantalla', False):
            if self.establecer_fondo_pantalla(): exitosos += 1
            
        if opciones.get('fondo_bloqueo', False):
            if self.establecer_fondo_bloqueo(): exitosos += 1
            
        if opciones.get('bloquear_personalizacion', False):
            if self.bloquear_personalizacion(): exitosos += 1
        
        self.log(f"\n{'='*50}")
        self.log(f"Completado: {exitosos}/{total} tareas exitosas")
        self.log(f"{'='*50}\n")
        
        if opciones.get('reiniciar_explorer', False):
            self.reiniciar_explorer()
        
        # Mostrar claves de producto al final si está habilitado
        if opciones.get('mostrar_keys', False):
            self.log("\n📋 Claves de Producto:")
            clave_windows = self.obtener_clave_windows()
            if clave_windows:
                self.log(f"   Windows Key: {clave_windows}")
            else:
                self.log("   Windows Key: No disponible o no activado")
            
            clave_office = self.obtener_clave_office()
            if clave_office:
                self.log(f"   Office Key: {clave_office}")
            else:
                self.log("   Office Key: No disponible o no activado")
        
        return exitosos, total
