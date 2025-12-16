# Correcciones Realizadas - Gestión de Usuarios

## Problemas Identificados

1. **Función `renombrar_usuario()`**: El comando WMIC tenía una sintaxis incorrecta
   - Problema: Faltaba la palabra clave `call` en el comando WMIC
   - Comandoincorrecto: `wmic useraccount where name="usuario" rename "nuevo_nombre"`
   - Comando correcto: `wmic useraccount where name="usuario" call rename "nuevo_nombre"`

2. **Función `cambiar_contraseña_usuario()`**: No manejaba correctamente el cambio de contraseña
   - Mejorado con mejor manejo de errores
   - Se agregó soporte PowerShell como alternativa

3. **Función `obtener_usuario_admin()`**: Saltaba el usuario "Administrator" cuando debería detectarlo
   - Ahora detecta correctamente usuarios como "Administrador" y "Administrator"
   - Tiene orden de preferencia: Administrador > Administrator > otros

## Cambios Realizados

### 1. Función `renombrar_usuario()` [Línea ~114]
- Se agregó `call` en el comando WMIC: `wmic useraccount where name="{nombre_actual}" call rename "{nombre_nuevo}"`
- Mejorado el script PowerShell alternativo
- Se agregó escapado correcto de caracteres

**Antes:**
```python
comando = f'wmic useraccount where name="{nombre_actual}" rename "{nombre_nuevo}"'
```

**Después:**
```python
comando = f'wmic useraccount where name="{nombre_actual}" call rename "{nombre_nuevo}"'
```

### 2. Función `cambiar_contraseña_usuario()` [Línea ~195]
- Se mejoró el manejo del caso sin contraseña usando PowerShell
- Se agregó fallback a `net user` si PowerShell falla
- Se agregó mejor registro de errores

**Cambios clave:**
- Para sin contraseña: Ahora usa PowerShell primero, luego fallback a `net user`
- Se agregó `$user.Put("PasswordExpired", 1)` para forzar cambio de contraseña
- Se mejoró manejo de errores con logs adicionales

### 3. Función `obtener_usuario_admin()` [Línea ~396]
- Se corrigió la lógica para no saltar el usuario "Administrator"
- Se agregó recolección de todos los usuarios administradores
- Se agregó preferencia por usuarios comunes (Administrador, Administrator)

**Cambios clave:**
- Ahora retorna "Administrador" si existe (preferencia por español)
- Fallback a "Administrator" si existe
- Luego retorna el primer usuario administrador encontrado

## Archivos Modificados

- `src/core/usuarios.py`: Correcciones en 3 funciones principales

## Cómo Probar

Ejecutar el script de prueba:
```bash
cd c:\dev\Python\CLA-WinConfig
python test_usuarios.py
```

Este script hará:
1. Verificar permisos de administrador
2. Detectar el usuario administrador actual
3. Cambiar la contraseña (NOTA: cambiar la contraseña de prueba)
4. Verificar los cambios

## Notas Importantes

- ⚠️ El script **requiere permisos de administrador** para funcionar
- La aplicación debe ejecutarse como administrador para cambiar nombre y contraseña del admin
- Los cambios en usuarios locales requieren ejecutar la aplicación con `Run as Administrator`

## Próximos Pasos

Si aún hay problemas:
1. Ejecutar el aplicación en modo administrador
2. Revisar los mensajes de error en el log
3. Verificar que el usuario "Administrator" existe en el sistema
