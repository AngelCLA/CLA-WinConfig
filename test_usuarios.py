#!/usr/bin/env python3
"""Script de prueba para la gestión de usuarios"""
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core import GestorUsuarios

def main():
    """Función principal de prueba"""
    print("=== Test de Gestión de Usuarios ===\n")
    
    # Crear gestor
    gestor = GestorUsuarios(callback=print)
    
    # Verificar permisos
    print(f"✓ Permisos de administrador: {gestor.es_admin}")
    
    if not gestor.es_admin:
        print("⚠️  Se requieren permisos de administrador para hacer pruebas")
        return
    
    print("\n--- Test 1: Obtener usuario administrador actual ---")
    admin_actual = gestor.obtener_usuario_admin()
    print(f"Usuario admin detectado: {admin_actual}")
    
    if admin_actual:
        print(f"\n--- Test 2: Verificar si {admin_actual} existe ---")
        existe = gestor.usuario_existe(admin_actual)
        print(f"Usuario {admin_actual} existe: {existe}")
        
        print(f"\n--- Test 3: Cambiar contraseña de {admin_actual} ---")
        # NOTA: Cambiar a una contraseña de prueba
        exito, msg = gestor.cambiar_contraseña_usuario(admin_actual, "Test@123456")
        print(f"Resultado: {msg}")
        
        if exito:
            print(f"\n--- Test 4: Cambiar contraseña nuevamente ---")
            exito2, msg2 = gestor.cambiar_contraseña_usuario(admin_actual, "Test@654321")
            print(f"Resultado: {msg2}")
    
    print("\n=== Fin de pruebas ===")

if __name__ == "__main__":
    main()
