$apps = @(
    @{ name="WinRAR";       file="winrar.exe";        args="/S" },
    @{ name="Visor Simple"; file="visor_simple.exe";  args="/S" },
    @{ name="VLC";          file="vlc.exe";           args="/S" },
    @{ name="XAMPP";        file="xampp.exe";         args="--mode unattended" },
    @{ name="JDK 8";        file="jdk8.exe";          args="/s" },
    @{ name="NetBeans 8";   file="netbeans8.exe";     args="--silent" },
    @{ name="Arduino";      file="arduino.exe";       args="/S" },
    @{ name="PSeInt";       file="pseint.exe";        args="/S" },
    @{ name="SQLyog";       file="sqlyog.exe";        args="/VERYSILENT" },
    @{ name="VirtualBox";   file="virtualbox.exe";   args="--silent" }
)

$folder = "C:\Instaladores"

foreach ($app in $apps) {
    $path = Join-Path $folder $app.file

    if (Test-Path $path) {
        Write-Host "Instalando $($app.name)..."
        Start-Process $path -ArgumentList $app.args -Wait
        Write-Host "$($app.name) instalado."
    }
    else {
        Write-Host "No se encontró $($app.file)"
    }
}

Write-Host "Todas las instalaciones finalizadas."
