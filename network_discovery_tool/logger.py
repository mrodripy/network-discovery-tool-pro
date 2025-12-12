# network_discovery_tool/logger.py
import logging
import sys
import os
from datetime import datetime
from typing import Optional

class NDLogger:
    """Logger profesional para Network Discovery Tool."""
    
    def __init__(self, name: str = "ndiscover", verbose: bool = False):
        self.logger = logging.getLogger(name)
        
        # Nivel base
        level = logging.DEBUG if verbose else logging.INFO
        self.logger.setLevel(level)
        
        # Evitar log duplicados si ya está configurado
        if not self.logger.handlers:
            self._setup_handlers(verbose)
    
    def _setup_handlers(self, verbose: bool):
        """Configura los handlers de logging."""
        
        # Formato profesional
        detailed_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # 1. Handler para CONSOLA (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        console_handler.setFormatter(simple_format)
        console_handler.addFilter(lambda record: record.levelno <= logging.WARNING)
        
        # 2. Handler para ERRORES (stderr)
        error_handler = logging.StreamHandler(sys.stderr)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(simple_format)
        
        # 3. Handler para ARCHIVO (log detallado)
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(
            log_dir, 
            f"ndiscover_{datetime.now().strftime('%Y%m%d')}.log"
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_format)
        
        # Añadir todos los handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(file_handler)
    
    # Métodos conveniencia
    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
    
    def scan_start(self, network: str, threads: int, timeout: int):
        """Log para inicio de escaneo."""
        self.info("=" * 50)
        self.info("INICIANDO ESCANEO DE RED")
        self.info("=" * 50)
        self.info(f"Red: {network}")
        self.info(f"Hilos: {threads}, Timeout: {timeout}s")
        self.info(f"Hora inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.debug("Configuración de escaneo cargada")
    
    def scan_complete(self, hosts_found: int, duration: float, open_ports: int = 0):
        """Log para finalización de escaneo."""
        self.info("=" * 50)
        self.info("ESCANEO COMPLETADO")
        self.info("=" * 50)
        self.info(f"Hosts encontrados: {hosts_found}")
        if open_ports > 0:
            self.info(f"Puertos abiertos: {open_ports}")
        self.info(f"Duración: {duration:.2f} segundos")
        self.info(f"Velocidad: {hosts_found/duration:.1f} hosts/seg" if duration > 0 else "N/A")
        self.info(f"Hora fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def host_discovered(self, ip: str, hostname: str, response_time: int):
        """Log para host descubierto."""
        self.debug(f"Host activo: {ip} ({hostname}) - {response_time}ms")
    
    def port_discovered(self, ip: str, port: int, service: str):
        """Log para puerto descubierto."""
        self.info(f"Puerto abierto: {ip}:{port} ({service})")

# Instancia global para fácil acceso
_logger_instance: Optional[NDLogger] = None

def get_logger(verbose: bool = False) -> NDLogger:
    """Obtiene o crea una instancia del logger."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = NDLogger(verbose=verbose)
    return _logger_instance
