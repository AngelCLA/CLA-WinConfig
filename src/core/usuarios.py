"""Módulo de gestión de usuarios locales de Windows"""
import ctypes
import subprocess
import json
from pathlib import Path


class GestorUsuarios:
    """Gestor de creación y configuración de usuarios locales en Windows"""
    
    def __init__(self, callback=None):
        """
        Inicializa el gestor de usuarios.
        
        Args:
            callback: Función para registrar mensajes (opcional)
        """
        self.callback = callback
        self.es_admin = self.verificar_admin()
    
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
    
    def validar_entrada(self, usuario, contraseña=None):
        """
        Valida que los campos no estén vacíos.
        
        Args:
            usuario: Nombre de usuario
            contraseña: Contraseña (opcional, puede ser None para validación sin contraseña)
        
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        if not usuario or not usuario.strip():
            return False, "El nombre de usuario no puede estar vacío"
        
        if contraseña is not None and not contraseña:
            return False, "La contraseña no puede estar vacía"
        
        # Validar caracteres no permitidos en Windows
        caracteres_invalidos = r'<>:"/\|?*'
        for char in caracteres_invalidos:
            if char in usuario:
                return False, f"El nombre de usuario contiene caracteres no válidos: {char}"
        
        # Limitar longitud
        if len(usuario) > 20:
            return False, "El nombre de usuario no puede exceder 20 caracteres"
        
        return True, ""
    
    def usuario_existe(self, nombre_usuario):
        """
        Verifica si un usuario ya existe en el sistema.
        
        Args:
            nombre_usuario: Nombre del usuario a verificar
        
        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            comando = f'net user "{nombre_usuario}"'
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return resultado.returncode == 0
        except Exception as e:
            self.log(f"⚠️ Error al verificar si el usuario existe: {e}")
            return False
    
    def renombrar_usuario(self, nombre_actual, nombre_nuevo):
        """
        Renombra un usuario existente.
        
        Args:
            nombre_actual: Nombre actual del usuario
            nombre_nuevo: Nuevo nombre del usuario
        
        Returns:
            tuple: (éxito, mensaje)
        """
        # Validar entrada
        es_válido, mensaje_error = self.validar_entrada(nombre_nuevo)
        if not es_válido:
            return False, f"❌ {mensaje_error}"
        
        # Verificar permisos de administrador
        if not self.es_admin:
            return False, "❌ Se requieren permisos de administrador para renombrar usuarios"
        
        # Verificar si el usuario actual existe
        if not self.usuario_existe(nombre_actual):
            return False, f"❌ El usuario '{nombre_actual}' no existe en el sistema"
        
        # Verificar si el nuevo nombre ya existe
        if self.usuario_existe(nombre_nuevo):
            return False, f"❌ El usuario '{nombre_nuevo}' ya existe en el sistema"
        
        try:
            # Usar 'wmic useraccount' que es más confiable para renombrar usuarios
            # Primero intentar con wmic
            comando = f'wmic useraccount where name="{nombre_actual}" rename "{nombre_nuevo}"'
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if resultado.returncode != 0:
                # Si wmic falla, intentar con PowerShell (sintaxis correcta sin espacios)
                script_ps = f'''
$usuario = [ADSI]"WinNT://./{nombre_actual}"
$usuario.psbase.Rename("{nombre_nuevo}")
$usuario.CommitChanges()
'''
                comando_ps = 'powershell -NoProfile -Command "' + script_ps + '"'
                resultado = subprocess.run(
                    comando_ps,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if resultado.returncode != 0:
                    error_msg = resultado.stderr.strip() or "No se pudo renombrar"
                    self.log(f"⚠️ Error al renombrar: {error_msg}")
                    return False, f"❌ Error al renombrar usuario: {error_msg}"
            
            return True, f"✔ Usuario renombrado de '{nombre_actual}' a '{nombre_nuevo}'"
        
        except subprocess.TimeoutExpired:
            return False, "❌ Timeout al renombrar usuario (operación tardó demasiado)"
        except Exception as e:
            return False, f"❌ Error al renombrar usuario: {str(e)}"
    
    def cambiar_contraseña_usuario(self, nombre_usuario, contraseña_nueva):
        """
        Cambia la contraseña de un usuario existente.
        
        Args:
            nombre_usuario: Nombre del usuario existente
            contraseña_nueva: Nueva contraseña (puede ser vacía para sin contraseña)
        
        Returns:
            tuple: (éxito, mensaje)
        """
        # Validar nombre de usuario
        es_válido, mensaje_error = self.validar_entrada(nombre_usuario, "dummy")
        if not es_válido:
            return False, f"❌ {mensaje_error}"
        
        # Verificar permisos de administrador
        if not self.es_admin:
            return False, "❌ Se requieren permisos de administrador para cambiar contraseñas"
        
        # Verificar si el usuario existe
        if not self.usuario_existe(nombre_usuario):
            return False, f"❌ El usuario '{nombre_usuario}' no existe en el sistema"
        
        try:
            if contraseña_nueva == "":
                # Sin contraseña - usar net user directamente
                comando = f'net user "{nombre_usuario}" /active:yes'
                resultado = subprocess.run(
                    comando,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if resultado.returncode != 0:
                    error_msg = resultado.stderr.strip() or "Error desconocido"
                    return False, f"❌ Error al cambiar contraseña: {error_msg}"
                
                return True, f"✔ Usuario '{nombre_usuario}' sin contraseña"
            else:
                # Con contraseña - usar net user (sintaxis correcta)
                comando = f'net user "{nombre_usuario}" "{contraseña_nueva}"'
                resultado = subprocess.run(
                    comando,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if resultado.returncode != 0:
                    error_msg = resultado.stderr.strip() or "Error desconocido"
                    return False, f"❌ Error al cambiar contraseña: {error_msg}"
                
                return True, f"✔ Contraseña de '{nombre_usuario}' actualizada exitosamente"
        
        except subprocess.TimeoutExpired:
            return False, "❌ Timeout al cambiar contraseña (operación tardó demasiado)"
        except Exception as e:
            return False, f"❌ Error al cambiar contraseña: {str(e)}"
    
    def crear_usuario(self, nombre_usuario, contraseña="", es_admin=False):
        """
        Crea un nuevo usuario local en Windows.
        
        Args:
            nombre_usuario: Nombre del usuario
            contraseña: Contraseña del usuario (vacía para sin contraseña)
            es_admin: Si True, agrega el usuario al grupo de administradores
        
        Returns:
            tuple: (éxito, mensaje)
        """
        # Validar nombre de usuario
        es_válido, mensaje_error = self.validar_entrada(nombre_usuario, "dummy")
        if not es_válido:
            return False, f"❌ {mensaje_error}"
        
        # Verificar permisos de administrador
        if not self.es_admin:
            return False, "❌ Se requieren permisos de administrador para crear usuarios"
        
        # Verificar si el usuario ya existe
        if self.usuario_existe(nombre_usuario):
            return False, f"⚠️ El usuario '{nombre_usuario}' ya existe en el sistema"
        
        try:
            if contraseña == "":
                # Crear usuario sin contraseña
                comando = f'net user "{nombre_usuario}" /add /active:yes'
            else:
                # Crear usuario con contraseña
                comando = f'net user "{nombre_usuario}" "{contraseña}" /add'
            
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if resultado.returncode != 0:
                error_msg = resultado.stderr.strip() or "Error desconocido"
                return False, f"❌ Error al crear usuario: {error_msg}"
            
            # Si es admin, agregarlo al grupo de administradores
            if es_admin:
                comando_admin = f'net localgroup Administrators "{nombre_usuario}" /add'
                resultado_admin = subprocess.run(
                    comando_admin,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if resultado_admin.returncode != 0:
                    error_msg = resultado_admin.stderr.strip() or "Error desconocido"
                    self.log(f"⚠️ Usuario creado pero no se agregó a administradores: {error_msg}")
                    return True, f"✔ Usuario '{nombre_usuario}' creado (pero no como admin)"
                
                return True, f"✔ Usuario administrador '{nombre_usuario}' creado exitosamente"
            else:
                if contraseña == "":
                    return True, f"✔ Usuario estándar '{nombre_usuario}' creado sin contraseña"
                else:
                    return True, f"✔ Usuario estándar '{nombre_usuario}' creado exitosamente"
        
        except subprocess.TimeoutExpired:
            return False, "❌ Timeout al crear el usuario (operación tardó demasiado)"
        except Exception as e:
            return False, f"❌ Error al crear usuario: {str(e)}"
    
    def configurar_uac(self):
        """
        Configura UAC para solicitar credenciales de administrador al instalar software.
        Establece ConsentPromptBehaviorUser = 1 en el registro.
        
        Returns:
            tuple: (éxito, mensaje)
        """
        if not self.es_admin:
            return False, "❌ Se requieren permisos de administrador para configurar UAC"
        
        try:
            import winreg
            
            # Ruta del registro para UAC
            ruta_registro = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
            
            try:
                # Abrir la clave del registro
                clave = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    ruta_registro,
                    0,
                    winreg.KEY_SET_VALUE
                )
                
                # Establecer ConsentPromptBehaviorUser a 1
                # 0 = No preguntar (solo elevación silenciosa)
                # 1 = Preguntar credenciales para cambios de PC
                # 2 = Preguntar (solo consentimiento) - predeterminado
                winreg.SetValueEx(
                    clave,
                    "ConsentPromptBehaviorUser",
                    0,
                    winreg.REG_DWORD,
                    1
                )
                
                winreg.CloseKey(clave)
                return True, "✔ UAC configurado correctamente"
            
            except FileNotFoundError:
                # Si la clave no existe, crearla
                clave = winreg.CreateKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    ruta_registro
                )
                winreg.SetValueEx(
                    clave,
                    "ConsentPromptBehaviorUser",
                    0,
                    winreg.REG_DWORD,
                    1
                )
                winreg.CloseKey(clave)
                return True, "✔ UAC configurado correctamente (clave creada)"
        
        except PermissionError:
            return False, "❌ Permiso denegado al configurar UAC"
        except Exception as e:
            return False, f"❌ Error al configurar UAC: {str(e)}"
    
    def obtener_usuario_admin(self):
        """
        Obtiene el nombre del primer usuario administrador del sistema.
        
        Returns:
            str: Nombre del usuario admin, o None si no se encuentra
        """
        try:
            # Método 1: Usar net localgroup Administrators
            comando = 'net localgroup Administrators'
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if resultado.returncode == 0:
                líneas = resultado.stdout.strip().split('\n')
                # Procesar líneas después del header
                en_miembros = False
                for línea in líneas:
                    línea = línea.strip()
                    # Saltar líneas vacías y separadores
                    if not línea or '---' in línea or 'Members' in línea or 'Miembros' in línea:
                        en_miembros = True
                        continue
                    # Saltar líneas de comando completado
                    if 'comando se completó' in línea or 'command completed' in línea:
                        break
                    # Si estamos en la sección de miembros y hay contenido
                    if en_miembros and línea:
                        # Ignorar SIDs (empiezan con S-)
                        if not línea.startswith('S-'):
                            # Retornar el usuario (ignorar dominio si existe)
                            usuario = línea.split('\\')[-1] if '\\' in línea else línea
                            if usuario and usuario != 'Administrator':
                                return usuario
            
            # Método 2: Si no encontró, intentar con usuarios comunes
            usuarios_comunes = ['Administrador', 'Administrator', 'admin', 'Admin']
            for usuario in usuarios_comunes:
                if self.usuario_existe(usuario):
                    return usuario
            
            return None
            
        except Exception as e:
            self.log(f"⚠️ Error al obtener usuario admin: {e}")
            return None
