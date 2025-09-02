#!/usr/bin/env python3
"""
Script de mantenimiento para SIFGPT
"""

import os
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/maintenance.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def clean_logs(days_to_keep=30):
    """Limpia logs antiguos"""
    try:
        logs_dir = Path('logs')
        if not logs_dir.exists():
            logger.info("Directorio de logs no existe")
            return
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        for log_file in logs_dir.glob('*.log'):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink()
                deleted_count += 1
                logger.info(f"Log eliminado: {log_file}")
        
        logger.info(f"Limpieza de logs completada. {deleted_count} archivos eliminados")
        
    except Exception as e:
        logger.error(f"Error limpiando logs: {e}")

def clean_audio_files(days_to_keep=7):
    """Limpia archivos de audio antiguos"""
    try:
        audio_dir = Path('input/audios')
        if not audio_dir.exists():
            logger.info("Directorio de audio no existe")
            return
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        for audio_file in audio_dir.glob('*.wav'):
            if audio_file.stat().st_mtime < cutoff_date.timestamp():
                audio_file.unlink()
                deleted_count += 1
                logger.info(f"Audio eliminado: {audio_file}")
        
        logger.info(f"Limpieza de audio completada. {deleted_count} archivos eliminados")
        
    except Exception as e:
        logger.error(f"Error limpiando archivos de audio: {e}")

def create_backup():
    """Crea un backup del sistema"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"sifgpt_backup_{timestamp}"
        backup_dir = Path('backups') / backup_name
        
        # Crear directorio de backup
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivos y directorios a respaldar
        items_to_backup = [
            'src',
            'templates',
            'static',
            'input',
            'requirements.txt',
            'app.py',
            'README.md'
        ]
        
        for item in items_to_backup:
            if Path(item).exists():
                if Path(item).is_dir():
                    shutil.copytree(item, backup_dir / item)
                else:
                    shutil.copy2(item, backup_dir)
        
        logger.info(f"Backup creado exitosamente: {backup_dir}")
        return str(backup_dir)
        
    except Exception as e:
        logger.error(f"Error creando backup: {e}")
        return None

def optimize_system():
    """Optimiza el sistema"""
    try:
        logger.info("Iniciando optimización del sistema...")
        
        # Limpiar logs
        clean_logs()
        
        # Limpiar archivos de audio
        clean_audio_files()
        
        # Crear backup
        backup_path = create_backup()
        if backup_path:
            logger.info(f"Backup de seguridad creado en: {backup_path}")
        
        logger.info("Optimización del sistema completada")
        
    except Exception as e:
        logger.error(f"Error en optimización: {e}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Script de mantenimiento para SIFGPT')
    parser.add_argument('--clean-logs', action='store_true', help='Limpiar logs antiguos')
    parser.add_argument('--clean-audio', action='store_true', help='Limpiar archivos de audio antiguos')
    parser.add_argument('--backup', action='store_true', help='Crear backup del sistema')
    parser.add_argument('--optimize', action='store_true', help='Ejecutar optimización completa')
    parser.add_argument('--days', type=int, default=30, help='Días a mantener (por defecto: 30)')
    
    args = parser.parse_args()
    
    print("🔧 SIFGPT - Script de Mantenimiento")
    print("=" * 40)
    
    if args.clean_logs:
        print("🧹 Limpiando logs...")
        clean_logs(args.days)
    
    if args.clean_audio:
        print("🎵 Limpiando archivos de audio...")
        clean_audio_files(args.days)
    
    if args.backup:
        print("💾 Creando backup...")
        backup_path = create_backup()
        if backup_path:
            print(f"✅ Backup creado en: {backup_path}")
        else:
            print("❌ Error creando backup")
    
    if args.optimize:
        print("⚡ Ejecutando optimización completa...")
        optimize_system()
    
    if not any([args.clean_logs, args.clean_audio, args.backup, args.optimize]):
        print("📋 Uso del script:")
        print("  --clean-logs     Limpiar logs antiguos")
        print("  --clean-audio    Limpiar archivos de audio antiguos")
        print("  --backup         Crear backup del sistema")
        print("  --optimize       Ejecutar optimización completa")
        print("  --days N         Especificar días a mantener (por defecto: 30)")

if __name__ == "__main__":
    main()
