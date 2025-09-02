#!/usr/bin/env python3
"""
Script de configuración inicial para TUNRAG
Este script ayuda a configurar el entorno y verificar que todo esté funcionando correctamente.
"""

import os
import sys
from pathlib import Path
import subprocess

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    required_packages = [
        'flask', 'flask-cors', 'python-dotenv', 'openai', 
        'requests', 'pandas', 'numpy', 'python-multipart'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} instalado")
        except ImportError:
            print(f"❌ {package} no encontrado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Instalando paquetes faltantes: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Paquetes instalados exitosamente")
        except subprocess.CalledProcessError:
            print("❌ Error al instalar paquetes")
            return False
    
    return True

def create_env_file():
    """Crea el archivo .env si no existe"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    
    print("📝 Creando archivo .env...")
    
    env_content = """# Configuración de OpenAI
OPENAI_API_KEY=tu_api_key_de_openai_aqui

# Configuración opcional de OpenAI
OPENAI_BASE_URL=
OPENAI_MODEL=gpt-4o
WHISPER_MODEL=whisper-1

# Configuración de la aplicación
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
PORT=5000
HOST=0.0.0.0

# Configuración de logging
LOG_LEVEL=INFO

# Configuración de seguridad
CORS_ORIGINS=*

# Configuración de archivos
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=input/audios

# Configuración de caché
CACHE_TIMEOUT=3600
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env creado exitosamente")
        print("⚠️  IMPORTANTE: Edita el archivo .env y configura tu OPENAI_API_KEY")
        return True
    except Exception as e:
        print(f"❌ Error al crear archivo .env: {e}")
        return False

def check_directories():
    """Verifica que los directorios necesarios existan"""
    required_dirs = [
        'input/audios',
        'input/historico', 
        'input/prompts',
        'input/plantillas_solucion',
        'logs',
        'static/css',
        'static/js',
        'static/images',
        'templates'
    ]
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio {dir_path} verificado")
    
    return True

def check_files():
    """Verifica que los archivos necesarios existan"""
    required_files = [
        'input/historico/historico.csv',
        'input/tabla.csv',
        'input/prompts/sys_prompt.txt',
        'input/prompts/estructura_json.txt',
        'input/prompts/categorias.txt',
        'input/prompts/entidades.txt',
        'input/prompts/faqs.txt',
        'input/prompts/respuestas_faqs.txt',
        'input/prompts/sys_prompt_faqs.txt',
        'input/prompts/sys_prompt_solucion.txt',
        'input/plantillas_solucion/plantilla.txt',
        'input/plantillas_solucion/plantilla_hist.txt'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} encontrado")
        else:
            print(f"❌ {file_path} no encontrado")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Archivos faltantes: {len(missing_files)}")
        print("   Algunos archivos de prompts pueden estar faltando")
        print("   El sistema puede no funcionar correctamente sin ellos")
    
    return len(missing_files) == 0

def run_tests():
    """Ejecuta tests básicos del sistema"""
    print("\n🧪 Ejecutando tests básicos...")
    
    try:
        # Test de importación
        sys.path.append('src/')
        from src.config.config import config
        from src.utils.logger import logger
        print("✅ Importaciones básicas funcionando")
        
        # Test de configuración
        config.validate_config()
        print("✅ Configuración válida")
        
        # Test de logger
        logger.info("Test de logger")
        print("✅ Logger funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en tests: {e}")
        return False

def main():
    """Función principal del script de setup"""
    print("🚀 Configurando TUNRAG...\n")
    
    checks = [
        ("Versión de Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Archivo .env", create_env_file),
        ("Directorios", check_directories),
        ("Archivos", check_files),
        ("Tests básicos", run_tests)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n🔍 Verificando {check_name}...")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error en verificación de {check_name}: {e}")
            results.append((check_name, False))
    
    # Resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DE CONFIGURACIÓN")
    print("="*50)
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for check_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} {check_name}")
    
    print(f"\n🎯 Resultado: {success_count}/{total_count} verificaciones pasaron")
    
    if success_count == total_count:
        print("\n🎉 ¡TUNRAG está configurado correctamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Edita el archivo .env y configura tu OPENAI_API_KEY")
        print("   2. Ejecuta: python app.py")
        print("   3. Abre http://localhost:5000 en tu navegador")
    else:
        print("\n⚠️  Algunas verificaciones fallaron")
        print("   Revisa los errores anteriores y corrige los problemas")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
