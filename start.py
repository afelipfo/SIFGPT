#!/usr/bin/env python3
"""
Script de inicio rápido para SIFGPT
Permite iniciar la aplicación de forma rápida y sencilla
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import flask
        import openai
        import pandas
        import numpy
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def check_config():
    """Verifica la configuración básica"""
    config_files = ['.env', 'env.example']
    env_file = None
    
    for file in config_files:
        if Path(file).exists():
            env_file = file
            break
    
    if env_file:
        print(f"✅ Archivo de configuración encontrado: {env_file}")
        return True
    else:
        print("⚠️  No se encontró archivo de configuración")
        print("💡 Copia env.example como .env y configura tus valores")
        return False

def check_directories():
    """Verifica que existan los directorios necesarios"""
    required_dirs = ['src', 'templates', 'static', 'input', 'logs']
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Directorios faltantes: {', '.join(missing_dirs)}")
        return False
    else:
        print("✅ Todos los directorios necesarios existen")
        return True

def start_application():
    """Inicia la aplicación"""
    try:
        print("\n🚀 Iniciando SIFGPT...")
        
        # Verificar que app.py existe
        if not Path('app.py').exists():
            print("❌ app.py no encontrado")
            return False
        
        # Iniciar la aplicación
        process = subprocess.Popen([sys.executable, 'app.py'])
        
        print("✅ Aplicación iniciada")
        print("🌐 Accede a: http://localhost:5000")
        print("⏹️  Presiona Ctrl+C para detener")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n\n👋 SIFGPT detenido por el usuario")
            process.terminate()
            process.wait()
        
        return True
        
    except Exception as e:
        print(f"❌ Error iniciando la aplicación: {e}")
        return False

def show_menu():
    """Muestra el menú principal"""
    print("\n🎯 SIFGPT - Sistema de PQRS con Inteligencia Artificial")
    print("=" * 60)
    print("1. Verificar dependencias")
    print("2. Verificar configuración")
    print("3. Verificar directorios")
    print("4. Iniciar aplicación")
    print("5. Verificar todo y iniciar")
    print("6. Salir")
    print("=" * 60)

def main():
    """Función principal"""
    while True:
        show_menu()
        
        try:
            choice = input("\nSelecciona una opción (1-6): ").strip()
            
            if choice == '1':
                check_dependencies()
                
            elif choice == '2':
                check_config()
                
            elif choice == '3':
                check_directories()
                
            elif choice == '4':
                start_application()
                
            elif choice == '5':
                print("\n🔍 Verificando todo...")
                deps_ok = check_dependencies()
                config_ok = check_config()
                dirs_ok = check_directories()
                
                if all([deps_ok, config_ok, dirs_ok]):
                    print("\n✅ Todo está listo para iniciar")
                    response = input("\n¿Deseas iniciar SIFGPT ahora? (s/n): ").lower().strip()
                    if response in ['s', 'si', 'sí', 'y', 'yes']:
                        start_application()
                else:
                    print("\n❌ Hay problemas que resolver antes de iniciar")
                    
            elif choice == '6':
                print("\n👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida. Selecciona 1-6")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
