#!/usr/bin/env python3
"""
Script de configuración inicial para SIFGPT
Configura el entorno y las dependencias necesarias
"""

import os
import sys
import subprocess
from pathlib import Path
from shutil import copy2

def print_banner():
    """Muestra el banner de bienvenida"""
    print("=" * 60)
    print("🚀 SIFGPT - Sistema de PQRS con Inteligencia Artificial")
    print("=" * 60)
    print("Configuración inicial del sistema")
    print("=" * 60)

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python 3.11+ requerido. Versión actual: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Versión compatible")
    return True

def install_dependencies():
    """Instala las dependencias de Python"""
    try:
        print("\n📦 Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_directories():
    """Crea los directorios necesarios"""
    directories = [
        'logs',
        'input/audios',
        'input/historico',
        'input/prompts',
        'input/plantillas_solucion',
        'backups'
    ]
    
    print("\n📁 Creando directorios...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")
    
    return True

def setup_env_file():
    """Configura el archivo de variables de entorno"""
    env_example = Path('env.example')
    env_file = Path('.env')
    
    if env_file.exists():
        print("\n⚠️  Archivo .env ya existe")
        response = input("¿Deseas sobrescribirlo? (s/n): ").lower().strip()
        if response not in ['s', 'si', 'sí', 'y', 'yes']:
            print("✅ Archivo .env mantenido")
            return True
    
    if env_example.exists():
        try:
            copy2(env_example, env_file)
            print("✅ Archivo .env creado desde env.example")
            
            # Solicitar configuración de OpenAI API Key
            print("\n🔑 Configuración de OpenAI:")
            api_key = input("Ingresa tu OpenAI API Key (o presiona Enter para configurar después): ").strip()
            
            if api_key:
                # Actualizar el archivo .env con la API key
                with open(env_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content = content.replace('your-openai-api-key-here', api_key)
                
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ OpenAI API Key configurada")
            else:
                print("💡 Recuerda configurar tu OpenAI API Key en el archivo .env")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando archivo .env: {e}")
            return False
    else:
        print("❌ Archivo env.example no encontrado")
        return False

def verify_setup():
    """Verifica que la configuración sea correcta"""
    print("\n🔍 Verificando configuración...")
    
    checks = [
        ("Archivo .env", Path('.env').exists()),
        ("Directorio logs", Path('logs').exists()),
        ("Directorio input", Path('input').exists()),
        ("Directorio src", Path('src').exists()),
        ("Archivo app.py", Path('app.py').exists()),
    ]
    
    all_passed = True
    for check_name, check_result in checks:
        status = "✅" if check_result else "❌"
        print(f"{status} {check_name}")
        if not check_result:
            all_passed = False
    
    return all_passed

def show_next_steps():
    """Muestra los próximos pasos"""
    print("\n🎯 Próximos pasos:")
    print("1. Configura tu OpenAI API Key en el archivo .env")
    print("2. Ejecuta: python app.py")
    print("3. Accede a: http://localhost:5000")
    print("\n💡 Para más ayuda, ejecuta: python start.py")

def main():
    """Función principal"""
    print_banner()
    
    # Verificar versión de Python
    if not check_python_version():
        print("\n❌ Versión de Python incompatible")
        return False
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error instalando dependencias")
        return False
    
    # Crear directorios
    if not create_directories():
        print("\n❌ Error creando directorios")
        return False
    
    # Configurar archivo .env
    if not setup_env_file():
        print("\n❌ Error configurando archivo .env")
        return False
    
    # Verificar configuración
    if not verify_setup():
        print("\n❌ Algunas verificaciones fallaron")
        return False
    
    print("\n🎉 ¡SIFGPT está configurado correctamente!")
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 ¡SIFGPT está listo para usar!")
        else:
            print("\n❌ Configuración incompleta")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
