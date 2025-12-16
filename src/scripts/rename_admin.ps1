param(
    [string]$OldName,
    [string]$NewName,
    [string]$NewPassword
)

function Log($msg) {
    Write-Output $msg
}

# Verificar privilegios
$principal = New-Object Security.Principal.WindowsPrincipal `
    ([Security.Principal.WindowsIdentity]::GetCurrent())

if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Log "❌ Ejecutar como administrador"
    exit 1
}

# Obtener usuario
$user = Get-LocalUser -Name $OldName -ErrorAction SilentlyContinue
if (-not $user) {
    Log "❌ Usuario '$OldName' no existe"
    exit 1
}

# Bloquear cuenta integrada (-500)
if ($user.SID.Value.EndsWith("-500")) {
    Log "❌ No se permite modificar la cuenta integrada del sistema"
    exit 1
}

# Renombrar si aplica
if ($OldName -ne $NewName) {
    Rename-LocalUser -Name $OldName -NewName $NewName
    Log "✔ Usuario renombrado: $OldName → $NewName"
}

# Cambiar contraseña
if ($NewPassword) {
    $Secure = ConvertTo-SecureString $NewPassword -AsPlainText -Force
    Set-LocalUser -Name $NewName -Password $Secure
    Log "✔ Contraseña actualizada"
}

exit 0
