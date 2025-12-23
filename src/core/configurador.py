"""Lógica de configuración del PC"""
import os
import sys
import winreg
import ctypes
import shutil
import subprocess
import getpass
from pathlib import Path

# Detectar si está empaquetado en .exe
if getattr(sys, 'frozen', False):
    # Ruta cuando está en .exe
    BASE_PATH = Path(sys.executable).parent
else:
    # Ruta cuando se ejecuta como script
    BASE_PATH = Path(__file__).parent.parent


class ConfiguradorPC:
    def __init__(self, numero_pc, carpeta_centro='CID-Centro_Computo', usuario_objetivo=None, callback=None):
        self.numero_pc = numero_pc
        self.carpeta_centro = carpeta_centro
        carpeta_base = BASE_PATH.parent / "assets" / carpeta_centro
        self.ruta_wallpapers = carpeta_base / "wallpapers"
        self.ruta_lockscreen = carpeta_base / "lockscreen"
        self.es_admin = self.verificar_admin()
        self.callback = callback
        
        # Carpeta para almacenar fondos de pantalla
        self.ruta_pictures = Path.home() / "Fondos"
        self.ruta_pictures.mkdir(parents=True, exist_ok=True)

        # Usuario objetivo y su SID
        self.usuario_objetivo = usuario_objetivo or getpass.getuser()
        self.sid_objetivo = self.obtener_sid_usuario(self.usuario_objetivo)

    def obtener_sid_usuario(self, nombre_usuario):
        """Obtiene el SID de un usuario local con reintentos"""
        max_intentos = 5
        
        for intento in range(1, max_intentos + 1):
            try:
                # Método 1: Usar PowerShell con Get-LocalUser
                cmd = [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f"(Get-LocalUser -Name '{nombre_usuario}').SID.Value"
                ]
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                sid = r.stdout.strip()
                
                if sid and sid.startswith('S-1-5-'):
                    self.log(f"✓ SID obtenido para '{nombre_usuario}': {sid}")
                    return sid
                
                # Método 2: Usar WMIC como alternativa
                cmd_wmic = f'wmic useraccount where name="{nombre_usuario}" get sid'
                r_wmic = subprocess.run(cmd_wmic, shell=True, capture_output=True, text=True, timeout=10)
                
                lines = r_wmic.stdout.strip().split('\n')
                if len(lines) > 1:
                    sid = lines[1].strip()
                    if sid and sid.startswith('S-1-5-'):
                        self.log(f"✓ SID obtenido para '{nombre_usuario}' (WMIC): {sid}")
                        return sid
                
                # Si no se obtuvo, esperar y reintentar
                if intento < max_intentos:
                    self.log(f"⏳ Reintentando obtener SID... (intento {intento}/{max_intentos})")
                    import time
                    time.sleep(2)
                
            except Exception as e:
                if intento < max_intentos:
                    self.log(f"⚠️  Error obteniendo SID (intento {intento}): {e}")
                    import time
                    time.sleep(2)
                else:
                    self.log(f"✗ Error obteniendo SID después de {max_intentos} intentos: {e}")
        
        self.log(f"✗ No se pudo obtener el SID para '{nombre_usuario}' después de {max_intentos} intentos")
        return None
    
    def limpiar_cache_fondos(self):
        """Limpia el caché de fondos de pantalla de Windows para el usuario"""
        try:
            # Determinar el usuario correcto
            if self.soy_usuario_objetivo:
                usuario = self.usuario_actual
            else:
                usuario = self.usuario_objetivo
            
            # Ruta del caché de imágenes transcodificadas
            cache_path = Path(f"C:/Users/{usuario}/AppData/Roaming/Microsoft/Windows/Themes/TranscodedWallpaper")
            cached_files_path = Path(f"C:/Users/{usuario}/AppData/Roaming/Microsoft/Windows/Themes/CachedFiles")
            
            # Eliminar archivo de caché principal
            if cache_path.exists():
                try:
                    cache_path.unlink()
                    self.log(f"✓ Caché eliminado: TranscodedWallpaper")
                except Exception as e:
                    self.log(f"⚠️  No se pudo eliminar caché: {e}")
            
            # Eliminar carpeta de archivos cacheados
            if cached_files_path.exists():
                try:
                    import shutil
                    shutil.rmtree(cached_files_path)
                    self.log(f"✓ Caché eliminado: CachedFiles")
                except Exception as e:
                    self.log(f"⚠️  No se pudo eliminar CachedFiles: {e}")
            
            return True
        except Exception as e:
            self.log(f"⚠️  Error al limpiar caché: {e}")
            return False
    
    def crear_script_aplicar_fondo(self, ruta_imagen):
        """Crea un script VBS que se ejecuta al iniciar sesión para aplicar el fondo"""
        try:
            if not self.es_admin:
                return False
            
            # Crear script VBS que aplica el fondo Y hace diagnóstico
            script_vbs = f'''Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Log de diagnóstico
Set logFile = objFSO.CreateTextFile("C:\\Users\\Public\\fondo_debug.log", True)
logFile.WriteLine "=== Diagnóstico de Fondo ==="
logFile.WriteLine "Fecha: " & Now()

' Leer valor actual del registro
On Error Resume Next
wallpaperActual = objShell.RegRead("HKCU\\Control Panel\\Desktop\\Wallpaper")
wallpaperPolicy = objShell.RegRead("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\Wallpaper")
logFile.WriteLine "Fondo actual (Desktop): " & wallpaperActual
logFile.WriteLine "Fondo política (Policies): " & wallpaperPolicy
On Error Goto 0

' Aplicar fondo de pantalla
objShell.RegWrite "HKCU\\Control Panel\\Desktop\\Wallpaper", "{ruta_imagen}", "REG_SZ"
objShell.RegWrite "HKCU\\Control Panel\\Desktop\\WallpaperStyle", "10", "REG_SZ"
objShell.RegWrite "HKCU\\Control Panel\\Desktop\\TileWallpaper", "0", "REG_SZ"

logFile.WriteLine "Aplicando: {ruta_imagen}"

' Refrescar el escritorio
Const SPI_SETDESKWALLPAPER = 20
Const SPIF_UPDATEINIFILE = 1
Const SPIF_SENDCHANGE = 2

Set objSystemInfo = CreateObject("WScript.Shell")
objSystemInfo.Run "rundll32.exe user32.dll,UpdatePerUserSystemParameters ,1 ,True", 0, False

logFile.WriteLine "Script ejecutado correctamente"
logFile.Close
'''
            
            # Guardar script con nombre único por usuario en carpeta pública
            script_path = Path(f"C:/Users/Public/aplicar_fondo_{self.usuario_objetivo}.vbs")
            with open(script_path, 'w') as f:
                f.write(script_vbs)
            
            # Asegurar que el hive esté cargado
            if not self.asegurar_hive_cargado():
                self.log("⚠️  No se pudo cargar el registro para crear script de inicio")
                return False
            
            # Crear la clave Run si no existe y agregar el script
            try:
                key = winreg.CreateKeyEx(
                    winreg.HKEY_USERS,
                    f"{self.sid_objetivo}\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                    0, 
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(key, "AplicarFondo", 0, winreg.REG_SZ, f'wscript.exe "{script_path}"')
                winreg.CloseKey(key)
                
                self.log("✓ Script de inicio creado para aplicar fondo al iniciar sesión")
                return True
            except Exception as e:
                self.log(f"⚠️  No se pudo crear script de inicio: {e}")
                return False
                
        except Exception as e:
            self.log(f"⚠️  Error al crear script de aplicación: {e}")
            return False
        
    def log(self, mensaje):
        """Envía mensaje al callback si existe"""
        if self.callback:
            self.callback(mensaje)
    
    def copiar_imagen_a_pictures(self, ruta_origen, nombre_destino, publico=False):
        """
        [DEPRECADO] Esta función ya no se usa. 
        Ahora las imágenes se aplican directamente desde la USB sin copiar.
        """
        try:
            if not ruta_origen.exists():
                return None
            
            # Si es público, usar carpeta accesible por todos
            if publico:
                ruta_destino = Path("C:/Users/Public/Pictures") / nombre_destino
                ruta_destino.parent.mkdir(parents=True, exist_ok=True)
            else:
                ruta_destino = self.ruta_pictures / nombre_destino
            
            shutil.copy2(str(ruta_origen), str(ruta_destino))
            return ruta_destino
        except Exception as e:
            self.log(f"✗ Error al copiar imagen a Fondos: {e}")
            return None
        
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
    
    def asegurar_hive_cargado(self):
        """Asegura que el hive del usuario objetivo esté cargado en HKEY_USERS"""
        if not self.sid_objetivo:
            return False
        
        try:
            # Intentar abrir la clave para verificar si está cargada
            test_key = winreg.OpenKey(
                winreg.HKEY_USERS,
                f"{self.sid_objetivo}",
                0,
                winreg.KEY_READ
            )
            winreg.CloseKey(test_key)
            return True  # Ya está cargado
        except FileNotFoundError:
            # No está cargado, intentar cargarlo
            self.log(f"⏳ Cargando registro de '{self.usuario_objetivo}'...")
            
            # Obtener ruta del perfil
            profile_path = Path(f"C:/Users/{self.usuario_objetivo}")
            ntuser_path = profile_path / "NTUSER.DAT"
            
            if not ntuser_path.exists():
                self.log(f"✗ No se encuentra NTUSER.DAT en {profile_path}")
                return False
            
            # Cargar el hive usando reg load
            cmd = f'reg load "HKU\\{self.sid_objetivo}" "{ntuser_path}"'
            resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if resultado.returncode == 0:
                self.log(f"✓ Registro cargado correctamente")
                return True
            else:
                self.log(f"✗ Error al cargar registro: {resultado.stderr}")
                return False
        except Exception as e:
            self.log(f"✗ Error verificando hive: {e}")
            return False
    
    def descargar_hive(self):
        """Descarga el hive del usuario del registro si fue cargado manualmente"""
        if not self.sid_objetivo:
            return
        
        try:
            # Intentar descargar el hive
            self.log(f"⏳ Descargando registro de '{self.usuario_objetivo}'...")
            cmd = f'reg unload "HKU\\{self.sid_objetivo}"'
            resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # No mostrar error si ya está descargado
            if resultado.returncode == 0:
                self.log(f"✓ Registro descargado correctamente")
            # Error 2 significa que no estaba cargado (es normal)
            elif "no se puede encontrar" not in resultado.stderr.lower():
                self.log(f"⚠️  Nota: {resultado.stderr.strip()}")
        except Exception as e:
            self.log(f"⚠️  Error al descargar hive: {e}")
        
    def establecer_tema_oscuro(self):
        """Activa el tema oscuro de Windows"""
        try:
            # ⭐ Si somos el usuario objetivo, usar HKEY_CURRENT_USER
            if self.soy_usuario_objetivo:
                key = winreg.CreateKeyEx(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
                self.log("✓ Tema oscuro activado (usuario actual)")
                return True
            
            # Si no somos el usuario objetivo, usar el método anterior con SID
            if not self.sid_objetivo:
                self.log("✗ No se pudo obtener el SID del usuario objetivo")
                return False
            
            # Asegurar que el hive esté cargado
            if not self.asegurar_hive_cargado():
                self.log("✗ No se pudo cargar el registro del usuario")
                return False
            
            # Crear la clave si no existe
            key = winreg.CreateKeyEx(
                winreg.HKEY_USERS,
                f"{self.sid_objetivo}\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
                0,
                winreg.KEY_SET_VALUE
            )
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
            
            # Usar ruta directa desde assets (sin copiar)
            ruta_absoluta = str(archivo_fondo.absolute())
            
            self.log(f"📁 Aplicando fondo desde: {archivo_fondo.name}")
            
            # ⭐ Si somos el usuario objetivo, usar HKEY_CURRENT_USER y SystemParametersInfo
            if self.soy_usuario_objetivo:
                try:
                    # Método 1: Usar SystemParametersInfo (más efectivo)
                    import ctypes
                    SPI_SETDESKWALLPAPER = 20
                    SPIF_UPDATEINIFILE = 0x01
                    SPIF_SENDCHANGE = 0x02
                    
                    # Aplicar el fondo de pantalla
                    resultado = ctypes.windll.user32.SystemParametersInfoW(
                        SPI_SETDESKWALLPAPER,
                        0,
                        ruta_absoluta,
                        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
                    )
                    
                    if resultado:
                        self.log(f"✓ Fondo de pantalla aplicado (usuario actual)")
                        self.log(f"   Ruta: {ruta_absoluta}")
                        
                        # También actualizar en registro para persistencia
                        key = winreg.CreateKeyEx(
                            winreg.HKEY_CURRENT_USER,
                            r"Control Panel\Desktop",
                            0, 
                            winreg.KEY_SET_VALUE
                        )
                        winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, ruta_absoluta)
                        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
                        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
                        winreg.CloseKey(key)
                        
                        # Limpiar caché
                        self.limpiar_cache_fondos()
                        
                        return True
                    else:
                        self.log(f"⚠️  SystemParametersInfo falló, intentando método alternativo...")
                        
                except Exception as e:
                    self.log(f"⚠️  Error con SystemParametersInfo: {e}")
                
                # Método 2 (fallback): Solo registro + script VBS
                try:
                    key = winreg.CreateKeyEx(
                        winreg.HKEY_CURRENT_USER,
                        r"Control Panel\Desktop",
                        0, 
                        winreg.KEY_SET_VALUE
                    )
                    winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, ruta_absoluta)
                    winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
                    winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
                    winreg.CloseKey(key)
                    
                    self.limpiar_cache_fondos()
                    
                    # Refrescar escritorio con rundll32
                    os.system("rundll32.exe user32.dll,UpdatePerUserSystemParameters ,1 ,True")
                    
                    self.log(f"✓ Fondo configurado en registro (usuario actual)")
                    self.log(f"   Ruta: {ruta_absoluta}")
                    self.log(f"   ℹ️  Si no se ve, cierre sesión y vuelva a entrar")
                    
                    return True
                except Exception as e:
                    self.log(f"✗ Error aplicando fondo: {e}")
                    return False
            
            # Si no somos el usuario objetivo, usar el método con SID
            if not self.sid_objetivo:
                self.log(f"✗ No se pudo obtener el SID del usuario '{self.usuario_objetivo}'")
                return False
            
            # Asegurar que el hive esté cargado
            if not self.asegurar_hive_cargado():
                self.log("✗ No se pudo cargar el registro del usuario")
                return False
            
            # Limpiar caché de fondos antiguos
            self.limpiar_cache_fondos()
            
            try:
                # Crear/abrir la clave Control Panel\Desktop del usuario objetivo
                key = winreg.CreateKeyEx(
                    winreg.HKEY_USERS,
                    f"{self.sid_objetivo}\\Control Panel\\Desktop",
                    0, 
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, ruta_absoluta)
                winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
                winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
                winreg.CloseKey(key)
                
                self.log(f"✓ Fondo configurado para '{self.usuario_objetivo}'")
                self.log(f"   Ruta: {ruta_absoluta}")
                
                # Crear script de inicio
                if self.es_admin:
                    self.crear_script_aplicar_fondo(ruta_absoluta)
                
                return True
            except Exception as e:
                self.log(f"✗ Error al escribir en registro: {e}")
                return False
                
        except Exception as e:
            self.log(f"✗ Error al establecer fondo de pantalla: {e}")
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
                self.log(f"✗ No se puede bloquear personalización sin archivo de fondo")
                return False
            
            ruta_absoluta = str(archivo_fondo.absolute())
            
            # ⭐ Si somos el usuario objetivo, usar HKEY_CURRENT_USER
            if self.soy_usuario_objetivo:
                # Crear clave de políticas del sistema
                key = winreg.CreateKeyEx(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                    0, 
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, ruta_absoluta)
                winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
                winreg.CloseKey(key)
                
                # Crear clave de políticas del explorador
                key2 = winreg.CreateKeyEx(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                    0, 
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(key2, "NoThemesTab", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key2, "NoControlPanel", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key2)
                
                self.log("✓ Personalización bloqueada (usuario actual)")
                return True
            
            # Si no somos el usuario objetivo, usar el método con SID
            if not self.sid_objetivo:
                self.log("✗ No se pudo obtener el SID del usuario objetivo")
                return False
            
            # Asegurar que el hive esté cargado
            if not self.asegurar_hive_cargado():
                self.log("✗ No se pudo cargar el registro del usuario")
                return False
                
            # Crear clave de políticas del sistema
            key = winreg.CreateKeyEx(
                winreg.HKEY_USERS,
                f"{self.sid_objetivo}\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
                0, 
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, ruta_absoluta)
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
            winreg.CloseKey(key)
            
            # Crear clave de políticas del explorador
            key2 = winreg.CreateKeyEx(
                winreg.HKEY_USERS,
                f"{self.sid_objetivo}\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer",
                0, 
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key2, "NoThemesTab", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key2, "NoControlPanel", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key2)
            
            self.log("✓ Personalización bloqueada para usuario objetivo")
            return True
        except Exception as e:
            self.log(f"✗ Error al bloquear personalización: {e}")
            return False
    
    def bloquear_personalizacion(self):
        """Bloquea las opciones de personalización para el usuario"""
        try:
            # ⭐ Buscar archivo directamente en assets
            archivo_fondo = None
            
            self.log(f"🔍 Buscando fondo en: {self.ruta_wallpapers}")
            
            for ext in ['.jpg', '.png', '.jpeg']:
                ruta = self.ruta_wallpapers / f"PC-{self.numero_pc}{ext}"
                if ruta.exists():
                    archivo_fondo = ruta
                    self.log(f"✓ Fondo encontrado para bloqueo: {archivo_fondo.name}")
                    break
            
            if not archivo_fondo:
                self.log(f"✗ No se puede bloquear personalización sin archivo de fondo")
                return False
                
            if not self.sid_objetivo:
                self.log("✗ No se pudo obtener el SID del usuario objetivo")
                return False
            
            # Asegurar que el hive esté cargado
            if not self.asegurar_hive_cargado():
                self.log("✗ No se pudo cargar el registro del usuario")
                return False
                
            # Crear clave de políticas del sistema
            key = winreg.CreateKeyEx(
                winreg.HKEY_USERS,
                f"{self.sid_objetivo}\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
                0, 
                winreg.KEY_SET_VALUE
            )
            ruta_absoluta = str(archivo_fondo.absolute())
            self.log(f"📋 Aplicando política de fondo: {ruta_absoluta}")
            winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, ruta_absoluta)
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")  # 10 = Fill
            winreg.CloseKey(key)
            
            # Crear clave de políticas del explorador
            key2 = winreg.CreateKeyEx(
                winreg.HKEY_USERS,
                f"{self.sid_objetivo}\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer",
                0, 
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key2, "NoThemesTab", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key2, "NoControlPanel", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key2)
            
            self.log("✓ Personalización bloqueada para usuario objetivo")
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
    
    def cambiar_zona_horaria(self):
        """Cambia la zona horaria a UTC-07:00 (Chihuahua, La Paz, Mazatlán)"""
        if not self.es_admin:
            self.log("⚠️  Zona horaria omitida (requiere permisos de administrador)")
            return False
        
        try:
            import subprocess
            # Mountain Standard Time es UTC-07:00 (Chihuahua, La Paz, Mazatlán)
            comando = 'powershell -Command "Set-TimeZone -Id \'Mountain Standard Time\'"'
            resultado = os.system(comando)
            if resultado == 0:
                self.log("✓ Zona horaria configurada (UTC-07:00)")
                return True
            else:
                self.log("✗ Error al cambiar zona horaria")
                return False
        except Exception as e:
            self.log(f"✗ Error al cambiar zona horaria: {e}")
            return False
    
    def activar_windows(self):
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
        
        # Cambiar zona horaria automáticamente (sin opción de selección)
        self.cambiar_zona_horaria()
        
        exitosos = 0
        total = 0
        
        # Contar solo las tareas de configuración real (excluir mostrar_keys y reiniciar_explorer)
        tareas_configuracion = ['activar_windows', 'tema_oscuro', 'fondo_pantalla', 
                                'fondo_bloqueo', 'bloquear_personalizacion', 'optimizar_arranque']
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

        if opciones.get('optimizar_arranque', False):
            if self.optimizar_arranque(): exitosos += 1

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
    
    def optimizar_arranque(self):
        """Deshabilita programas comunes de inicio para mejorar el arranque"""
        if not self.es_admin:
            self.log("⚠️ Optimización de arranque omitida (requiere permisos de administrador)")
            return False

        self.log("⏳ Optimizando programas de arranque...")

        claves_run = [
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]

        claves_startup_approved = [
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run")
        ]

        patrones_bloqueados = [
            "onedrive",
            "teams",
            "msedge",
            "edge",
            "adobe",
            "google",
            "java",
            "spotify",
            "zoom",
            "updater"
            "CCXProcess",
            "discord",
            "steam",
            "epicgameslauncher",
            "battlenet",
            "spotify",
            "apple",
            "itunes",
            "quicktime",
            "dropbox",
            "skype",
            "microsoft 365 Copilot",
            "mobile device",
            "jusched"
        ]

        patrones_protegidos = [
            "defender",
            "security",
            "intel",
            "realtek",
            "synaptics",
            "audio",
            "graphics",
            "nvidia",
            "amd"
        ]

        eliminados = 0

        # 🔹 LIMPIAR Run
        for hive, ruta in claves_run:
            try:
                key = winreg.OpenKey(hive, ruta, 0, winreg.KEY_ALL_ACCESS)
                valores = []
                i = 0
                while True:
                    try:
                        valores.append(winreg.EnumValue(key, i))
                        i += 1
                    except OSError:
                        break

                for nombre, valor, _ in valores:
                    texto = f"{nombre} {valor}".lower()

                    if (
                        any(p in texto for p in patrones_bloqueados)
                        and not any(p in texto for p in patrones_protegidos)
                    ):
                        winreg.DeleteValue(key, nombre)
                        self.log(f"   ⛔ Inicio deshabilitado: {nombre}")
                        eliminados += 1

                winreg.CloseKey(key)
            except FileNotFoundError:
                continue
            except Exception as e:
                self.log(f"✗ Error optimizando Run: {e}")

        # 🔹 DESHABILITAR StartupApproved (Windows 10/11)
        for hive, ruta in claves_startup_approved:
            try:
                key = winreg.OpenKey(hive, ruta, 0, winreg.KEY_ALL_ACCESS)
                valores = []
                i = 0
                while True:
                    try:
                        valores.append(winreg.EnumValue(key, i)[0])
                        i += 1
                    except OSError:
                        break

                for nombre in valores:
                    nombre_l = nombre.lower()

                    if (
                        any(p in nombre_l for p in patrones_bloqueados)
                        and not any(p in nombre_l for p in patrones_protegidos)
                    ):
                        # 03 00 00 00 = deshabilitado
                        winreg.SetValueEx(
                            key,
                            nombre,
                            0,
                            winreg.REG_BINARY,
                            b"\x03\x00\x00\x00\x00\x00\x00\x00"
                        )
                        self.log(f"   🚫 Startup deshabilitado: {nombre}")
                        eliminados += 1

                winreg.CloseKey(key)
            except FileNotFoundError:
                continue
            except Exception as e:
                self.log(f"✗ Error optimizando StartupApproved: {e}")

        self.log(f"✓ Optimización completada ({eliminados} entradas deshabilitadas)")
        return True

    
    def __init__(self, numero_pc, carpeta_centro='CID-Centro_Computo', usuario_objetivo=None, callback=None):
        self.numero_pc = numero_pc
        self.carpeta_centro = carpeta_centro
        carpeta_base = BASE_PATH.parent / "assets" / carpeta_centro
        self.ruta_wallpapers = carpeta_base / "wallpapers"
        self.ruta_lockscreen = carpeta_base / "lockscreen"
        self.es_admin = self.verificar_admin()
        self.callback = callback
        
        # Variables para manejo de hive
        self.hive_cargado = False
        self.sid_temporal = None
        self.sid_objetivo_original = None
        
        # Carpeta para almacenar fondos de pantalla
        self.ruta_pictures = Path.home() / "Fondos"
        self.ruta_pictures.mkdir(parents=True, exist_ok=True)

        # Usuario objetivo y su SID
        self.usuario_objetivo = usuario_objetivo or getpass.getuser()
        
        # ⭐ NUEVO: Detectar si somos el usuario objetivo
        self.usuario_actual = getpass.getuser()
        self.soy_usuario_objetivo = (self.usuario_actual.lower() == self.usuario_objetivo.lower())
        
        if self.soy_usuario_objetivo:
            self.log(f"✓ Ejecutando como usuario objetivo: '{self.usuario_objetivo}'")
            self.log(f"   Se aplicarán cambios directamente (sin cargar hive)")
            # Para el usuario actual, usar HKEY_CURRENT_USER directamente
            self.sid_objetivo = None  # No necesitamos SID
        else:
            self.log(f"🔍 Obteniendo SID para usuario: '{self.usuario_objetivo}'")
            self.sid_objetivo = self.obtener_sid_usuario(self.usuario_objetivo)
            
            if not self.sid_objetivo:
                self.log(f"⚠️  ADVERTENCIA: No se pudo obtener el SID de '{self.usuario_objetivo}'")

    def cargar_registro_usuario(self, nombre_usuario):
        """Carga el hive de registro del usuario si no está cargado"""
        try:
            # Obtener la ruta del perfil del usuario
            cmd = [
                "powershell",
                "-NoProfile",
                "-Command",
                f"(Get-LocalUser -Name '{nombre_usuario}').SID.Value"
            ]
            r = subprocess.run(cmd, capture_output=True, text=True)
            sid = r.stdout.strip()
            
            if not sid or not sid.startswith('S-1-5-'):
                return False
            
            # Verificar si ya está cargado en HKEY_USERS
            try:
                test_key = winreg.OpenKey(
                    winreg.HKEY_USERS,
                    f"{sid}",
                    0,
                    winreg.KEY_READ
                )
                winreg.CloseKey(test_key)
                self.log(f"✓ Registro del usuario '{nombre_usuario}' ya está cargado")
                return True
            except FileNotFoundError:
                # El registro no está cargado, intentar cargarlo
                self.log(f"⏳ Cargando registro del usuario '{nombre_usuario}'...")
                
                # Obtener ruta del perfil
                cmd_profile = [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f"(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\{sid}').ProfileImagePath"
                ]
                r = subprocess.run(cmd_profile, capture_output=True, text=True)
                profile_path = r.stdout.strip()
                
                if profile_path:
                    ntuser_path = f"{profile_path}\\NTUSER.DAT"
                    # Cargar el hive
                    os.system(f'reg load "HKU\\{sid}" "{ntuser_path}"')
                    self.log(f"✓ Registro cargado para '{nombre_usuario}'")
                    return True
            
            return False
            
        except Exception as e:
            self.log(f"✗ Error cargando registro: {e}")
            return False
        
    def cargar_hive_usuario(self, nombre_usuario, sid):
        """Carga el hive de registro del usuario si no está cargado"""
        try:
            # Verificar si ya está cargado
            try:
                test_key = winreg.OpenKey(
                    winreg.HKEY_USERS,
                    f"{sid}",
                    0,
                    winreg.KEY_READ
                )
                winreg.CloseKey(test_key)
                self.log(f"✓ Registro de '{nombre_usuario}' ya está cargado")
                return True
            except FileNotFoundError:
                pass  # No está cargado, continuar
            
            self.log(f"⏳ Cargando registro de '{nombre_usuario}'...")
            
            # Intentar varias rutas posibles para el perfil
            posibles_rutas = [
                f"C:\\Users\\{nombre_usuario}",
                f"C:\\Users\\{nombre_usuario}.{os.environ.get('COMPUTERNAME', '')}",
            ]
            
            # También intentar obtener desde el registro
            try:
                cmd_profile = [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f"(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\{sid}' -ErrorAction SilentlyContinue).ProfileImagePath"
                ]
                r = subprocess.run(cmd_profile, capture_output=True, text=True)
                if r.stdout.strip():
                    posibles_rutas.insert(0, r.stdout.strip())
            except:
                pass
            
            ntuser_path = None
            for ruta in posibles_rutas:
                test_path = Path(ruta) / "NTUSER.DAT"
                if test_path.exists():
                    ntuser_path = str(test_path)
                    self.log(f"✓ Encontrado NTUSER.DAT en: {ntuser_path}")
                    break
            
            if not ntuser_path:
                self.log(f"✗ No se encontró NTUSER.DAT en ninguna ubicación")
                self.log(f"  Rutas buscadas: {posibles_rutas}")
                return False
            
            # Cargar el hive con reg load
            temp_key = f"TempUser_{sid.split('-')[-1]}"  # Usar último segmento del SID
            cmd_load = f'reg load "HKU\\{temp_key}" "{ntuser_path}"'
            
            self.log(f"⏳ Ejecutando: {cmd_load}")
            resultado = os.system(cmd_load + " >nul 2>&1")
            
            if resultado == 0:
                self.log(f"✓ Registro cargado temporalmente como '{temp_key}'")
                self.sid_temporal = temp_key
                self.sid_objetivo_original = self.sid_objetivo
                self.sid_objetivo = temp_key
                self.hive_cargado = True
                return True
            else:
                self.log(f"✗ Error al cargar registro (código {resultado})")
                return False
                
        except Exception as e:
            self.log(f"✗ Error al cargar hive: {e}")
            import traceback
            self.log(traceback.format_exc())
            return False

    def descargar_hive_usuario(self):
        """Descarga el hive temporal del registro"""
        if not hasattr(self, 'hive_cargado') or not self.hive_cargado:
            return
        
        try:
            self.log(f"⏳ Descargando registro temporal...")
            cmd_unload = f'reg unload "HKU\\{self.sid_temporal}"'
            resultado = os.system(cmd_unload)
            
            if resultado == 0:
                self.log(f"✓ Registro descargado correctamente")
                # Restaurar SID original
                self.sid_objetivo = self.sid_objetivo_original
                self.hive_cargado = False
            else:
                self.log(f"⚠️  Error al descargar registro (código {resultado})")
                
        except Exception as e:
            self.log(f"⚠️  Error al descargar hive: {e}")

    def limpiar_fondos_anteriores(self):
        """
        [DEPRECADO] Esta función ya no se usa.
        Ahora las imágenes se aplican directamente desde la USB sin copiar.
        """
        try:
            carpeta_publica = Path("C:/Users/Public/Pictures")
            if not carpeta_publica.exists():
                return
            
            # Buscar y eliminar fondos antiguos
            patrones = ["Wallpaper-PC-*.png", "Wallpaper-PC-*.jpg", "Wallpaper-PC-*.jpeg"]
            eliminados = 0
            
            for patron in patrones:
                for archivo in carpeta_publica.glob(patron):
                    try:
                        archivo.unlink()
                        eliminados += 1
                    except Exception as e:
                        self.log(f"⚠️  No se pudo eliminar {archivo.name}: {e}")
            
            if eliminados > 0:
                self.log(f"✓ {eliminados} fondo(s) anterior(es) eliminado(s)")
            
        except Exception as e:
            self.log(f"⚠️  Error al limpiar fondos anteriores: {e}")