"""
Módulo de gestión de usuarios locales de Windows
Diseñado para centros de cómputo (CLA-WinConfig)
"""

import ctypes
import getpass
import subprocess
from pathlib import Path


class GestorUsuarios:
    """Gestor de creación y configuración de usuarios locales en Windows"""

    def __init__(self, callback=None):
        self.callback = callback
        self.es_admin = self.verificar_admin()

    # =========================
    # UTILIDADES
    # =========================

    def log(self, mensaje):
        if self.callback:
            self.callback(mensaje)

    def verificar_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    def usuario_existe(self, nombre_usuario):
        cmd = f'net user "{nombre_usuario}"'
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return r.returncode == 0

    # =========================
    # ADMINISTRADOR INTEGRADO
    # =========================

    def obtener_admin_integrado(self):
        """
        Obtiene el administrador integrado (SID termina en -500)
        """
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            """
            Get-LocalUser |
            Where-Object { $_.SID.Value.EndsWith('-500') } |
            Select-Object -ExpandProperty Name
            """
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        nombre = r.stdout.strip()
        return nombre if nombre else None

    def deshabilitar_admin_integrado(self):
        """
        Deshabilita el administrador integrado de Windows (SID-500)
        """
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            """
            $u = Get-LocalUser | Where-Object { $_.SID.Value.EndsWith('-500') }
            if ($u -and $u.Enabled) {
                Disable-LocalUser -Name $u.Name
                Write-Output "Administrador integrado deshabilitado"
            } else {
                Write-Output "Administrador integrado ya estaba deshabilitado"
            }
            """
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return True, r.stdout.strip()

    # =========================
    # CREACIÓN DE USUARIOS
    # =========================

    def crear_usuario(self, nombre_usuario, contraseña="", es_admin=False):
        if not self.es_admin:
            return False, "❌ Se requieren permisos de administrador"

        if self.usuario_existe(nombre_usuario):
            return True, f"✔ Usuario '{nombre_usuario}' ya existe"

        if contraseña:
            cmd = f'net user "{nombre_usuario}" "{contraseña}" /add'
        else:
            cmd = f'net user "{nombre_usuario}" /add /active:yes'

        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if r.returncode != 0:
            return False, r.stderr.strip()

        if es_admin:
            cmd_admin = f'net localgroup Administrators "{nombre_usuario}" /add'
            subprocess.run(cmd_admin, shell=True, capture_output=True)

            return True, f"✔ Administrador '{nombre_usuario}' creado"

        return True, f"✔ Usuario '{nombre_usuario}' creado"

    # =========================
    # UAC
    # =========================

    def configurar_uac(self):
        """
        Configura UAC para que usuarios estándar soliciten credenciales
        """
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            """
            Set-ItemProperty `
            -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' `
            -Name ConsentPromptBehaviorUser `
            -Value 1
            """
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)

        if r.returncode != 0:
            return False, "❌ Error al configurar UAC"

        return True, "✔ UAC configurado correctamente"

    # =========================
    # FLUJO PRINCIPAL
    # =========================
    
    def cambiar_nombre_visible(self, nombre_cuenta, nombre_visible):
        """
        Cambia solo el nombre visible (FullName) del usuario.
        NO cambia SID, NO carpeta, NO nombre real.
        """
        if not self.es_admin:
            return False, "❌ Se requieren permisos de administrador"

        if not self.usuario_existe(nombre_cuenta):
            return False, f"❌ El usuario '{nombre_cuenta}' no existe"

        if not nombre_visible or not nombre_visible.strip():
            return False, "❌ El nombre visible no puede estar vacío"

        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f'Set-LocalUser -Name "{nombre_cuenta}" -FullName "{nombre_visible}"'
        ]

        r = subprocess.run(cmd, capture_output=True, text=True)

        if r.returncode != 0:
            return False, r.stderr.strip() or "❌ Error al cambiar nombre visible"

        return True, f"✔ Nombre visible cambiado a '{nombre_visible}'"

    def cambiar_password(self, nombre_cuenta, nueva_password):
        """
        Cambia la contraseña del usuario indicado
        """
        if not self.es_admin:
            return False, "❌ Se requieren permisos de administrador"

        if not self.usuario_existe(nombre_cuenta):
            return False, f"❌ El usuario '{nombre_cuenta}' no existe"

        if not nueva_password:
            return False, "❌ La contraseña no puede estar vacía"

        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f'''
            $pwd = ConvertTo-SecureString "{nueva_password}" -AsPlainText -Force
            Set-LocalUser -Name "{nombre_cuenta}" -Password $pwd
            '''
        ]

        r = subprocess.run(cmd, capture_output=True, text=True)

        if r.returncode != 0:
            return False, r.stderr.strip() or "❌ Error al cambiar contraseña"

        return True, "✔ Contraseña del administrador actualizada"
    
    def configurar_centro_computo(
        self,
        nombre_visible_admin,
        password_admin,
        usuario_alumno,
        configurador_pc=None
    ):
        self.log("=== Iniciando Gestión de Usuarios ===")

        if not self.es_admin:
            return False, "❌ Ejecutar como administrador"

        import getpass
        usuario_actual = getpass.getuser()
        self.log(f"✓ Administrador actual detectado: '{usuario_actual}'")

        # 1. Crear usuario estándar
        self.log("\n--- Paso 1: Creando usuario estándar ---")
        ok, msg = self.crear_usuario(
            nombre_usuario=usuario_alumno,
            contraseña="",
            es_admin=False
        )
        self.log(msg)
        
        if not ok and "ya existe" not in msg.lower():
            return False, msg

        # 2. Cambiar nombre visible del admin actual
        self.log("\n--- Paso 2: Configurando administrador ---")
        ok, msg = self.cambiar_nombre_visible(
            nombre_cuenta=usuario_actual,
            nombre_visible=nombre_visible_admin
        )
        self.log(msg)
        if not ok:
            return False, msg

        # 3. Cambiar contraseña del admin actual
        self.log("✓ Actualizando credenciales del administrador actual")
        ok, msg = self.cambiar_password(
            nombre_cuenta=usuario_actual,
            nueva_password=password_admin
        )
        self.log(msg)
        if not ok:
            return False, msg

        # 4. Configurar UAC
        self.log("\n--- Paso 3: Configurando UAC ---")
        ok, msg = self.configurar_uac()
        self.log(msg)

        return True, "✔ Usuario estándar creado y administrador configurado"