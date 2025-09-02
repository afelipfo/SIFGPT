#!/usr/bin/env python3
"""
Script de mantenimiento para TUNRAG
Permite realizar tareas de mantenimiento del sistema.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta

def clean_logs(days_to_keep=30):
    """Limpia logs antiguos"""
    log_dir = Path('logs')
    if not log_dir.exists():
        print("❌ Directorio de logs no encontrado")
        return False
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    deleted_count = 0
    
    for log_file in log_dir.glob('*.log*'):
        if log_file.stat().st_mtime < cutoff_date.timestamp():
            try:
                log_file.unlink()
                deleted_count += 1
                print(f"🗑️  Eliminado: {log_file.name}")
            except Exception as e:
                print(f"❌ Error al eliminar {log_file.name}: {e}")
    
    print(f"✅ {deleted_count} archivos de log eliminados")
    return True

def clean_audio_files(days_to_keep=7):
    """Limpia archivos de audio antiguos"""
    audio_dir = Path('input/audios')
    if not audio_dir.exists():
        print("❌ Directorio de audio no encontrado")
        return False
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    deleted_count = 0
    
    for audio_file in audio_dir.glob('*'):
        if audio_file.is_file() and audio_file.stat().st_mtime < cutoff_date.timestamp():
            try:
                audio_file.unlink()
                deleted_count += 1
                print(f"🗑️  Eliminado: {audio_file.name}")
            except Exception as e:
                print(f"❌ Error al eliminar {audio_file.name}: {e}")
    
    print(f"✅ {deleted_count} archivos de audio eliminados")
    return True

def refresh_caches():
    """Refresca las cachés del sistema"""
    try:
        sys.path.append('src/')
        from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
        from src.config.config import config
        
        # Crear instancia temporal para refrescar cachés
        orchestrator = PQRSOrchestratorService("temp_key")
        orchestrator.refresh_all_caches()
        
        print("✅ Cachés refrescadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al refrescar cachés: {e}")
        return False

def backup_data():
    """Crea un backup de los datos importantes"""
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"tunrag_backup_{timestamp}"
    backup_path = backup_dir / backup_name
    
    try:
        # Crear backup de directorios importantes
        important_dirs = ['input', 'logs']
        
        for dir_name in important_dirs:
            if Path(dir_name).exists():
                shutil.copytree(dir_name, backup_path / dir_name)
        
        print(f"✅ Backup creado en: {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def check_disk_usage():
    """Verifica el uso de disco"""
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = Path(root) / file
            try:
                total_size += file_path.stat().st_size
                file_count += 1
            except:
                pass
    
    total_mb = total_size / (1024 * 1024)
    print(f"📊 Uso de disco: {total_mb:.2f} MB")
    print(f"📁 Total de archivos: {file_count}")
    
    return total_mb, file_count

def optimize_system():
    """Optimiza el sistema"""
    print("🔧 Optimizando sistema...")
    
    # Limpiar logs antiguos
    clean_logs(30)
    
    # Limpiar archivos de audio antiguos
    clean_audio_files(7)
    
    # Refrescar cachés
    refresh_caches()
    
    # Verificar uso de disco
    check_disk_usage()
    
    print("✅ Optimización completada")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Script de mantenimiento para TUNRAG')
    parser.add_argument('--clean-logs', type=int, metavar='DAYS', 
                       help='Limpiar logs más antiguos que N días')
    parser.add_argument('--clean-audio', type=int, metavar='DAYS',
                       help='Limpiar archivos de audio más antiguos que N días')
    parser.add_argument('--refresh-caches', action='store_true',
                       help='Refrescar todas las cachés del sistema')
    parser.add_argument('--backup', action='store_true',
                       help='Crear backup de los datos')
    parser.add_argument('--disk-usage', action='store_true',
                       help='Verificar uso de disco')
    parser.add_argument('--optimize', action='store_true',
                       help='Ejecutar optimización completa del sistema')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    print("🔧 TUNRAG - Script de Mantenimiento")
    print("=" * 50)
    
    if args.clean_logs:
        clean_logs(args.clean_logs)
    
    if args.clean_audio:
        clean_audio_files(args.clean_audio)
    
    if args.refresh_caches:
        refresh_caches()
    
    if args.backup:
        backup_data()
    
    if args.disk_usage:
        check_disk_usage()
    
    if args.optimize:
        optimize_system()
    
    print("\n✅ Mantenimiento completado")

if __name__ == "__main__":
    main()
