#!/usr/bin/env python3
"""
Script de inicio rápido para TUNRAG
Verifica la configuración y lanza la aplicación automáticamente.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Verifica que el archivo .env exista y tenga la API key"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        print("💡 Ejecuta 'python setup.py' para configurar el entorno")
        return False
    
    # Cargar variables de entorno
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'tu_api_key_de_openai_aqui':
        print("❌ OPENAI_API_KEY no está configurada correctamente")
        print("💡 Edita el archivo .env y configura tu API key de OpenAI")
        return False
    
    print("✅ Configuración de entorno verificada")
    return True

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import flask
        import openai
        import pandas
        print("✅ Dependencias verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Ejecuta 'pip install -r requirements.txt'")
        return False

def check_files():
    """Verifica que los archivos necesarios existan"""
    required_files = [
        'app.py',
        'src/config/config.py',
        'src/utils/logger.py',
        'templates/index.html',
        'static/js/script.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✅ Archivos del sistema verificados")
    return True

def start_application():
    """Inicia la aplicación Flask"""
    try:
        print("\n🚀 Iniciando TUNRAG...")
        print("📱 La aplicación estará disponible en: http://localhost:5000")
        print("⏹️  Presiona Ctrl+C para detener\n")
        
        # Ejecutar la aplicación
        subprocess.run([sys.executable, 'app.py'])
        
    except KeyboardInterrupt:
        print("\n\n👋 TUNRAG detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")

def main():
    """Función principal"""
    print("🎯 TUNRAG - Sistema de PQRS con Inteligencia Artificial")
    print("=" * 60)
    
    # Verificaciones
    checks = [
        ("Archivo de entorno", check_env_file),
        ("Dependencias", check_dependencies),
        ("Archivos del sistema", check_files)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 Verificando {check_name}...")
        if not check_func():
            all_passed = False
    
    if not all_passed:
        print("\n❌ Algunas verificaciones fallaron")
        print("💡 Ejecuta 'python setup.py' para configurar el sistema")
        return False
    
    print("\n✅ Todas las verificaciones pasaron")
    
    # Preguntar si quiere iniciar la aplicación
    try:
        response = input("\n¿Deseas iniciar TUNRAG ahora? (s/n): ").lower().strip()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            start_application()
        else:
            print("\n💡 Para iniciar manualmente, ejecuta: python app.py")
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
