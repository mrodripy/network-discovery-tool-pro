# network_discovery_tool/cli.py
import argparse
import sys
import os
from typing import Optional

# Importaciones diferidas para mejor performance
# Las importaciones reales se hacen dentro de main()

def parse_arguments():
    """Configura y parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Network Discovery Tool - Escanea hosts y puertos en tu red',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s 192.168.1.0/24                    # Escaneo básico de hosts
  %(prog)s 192.168.1.0/24 -p 22,80,443      # Escanea hosts + puertos comunes
  %(prog)s 192.168.1.0/24 -p 1-100          # Escanea primeros 100 puertos
  %(prog)s 192.168.1.0/24 -p all            # Escanea puertos 1-1000
  %(prog)s 192.168.1.0/24 --service-scan    # Detecta servicios en puertos
  %(prog)s 192.168.1.0/24 -o html           # Genera reporte HTML
  %(prog)s 192.168.1.0/24 --verbose         # Modo detallado
  %(prog)s 192.168.1.0/24 --log-level DEBUG # Logging detallado
        """
    )
    
    # Argumento obligatorio
    parser.add_argument(
        'network',
        help='Red a escanear en formato CIDR (ej. 192.168.1.0/24)'
    )
    
    # Opciones de escaneo de hosts
    scan_group = parser.add_argument_group('Opciones de escaneo de hosts')
    scan_group.add_argument(
        '-t', '--timeout',
        type=int,
        default=2,
        help='Timeout en segundos para ping (default: 2)'
    )
    scan_group.add_argument(
        '--threads',
        type=int,
        default=50,
        help='Número máximo de hilos concurrentes (default: 50)'
    )
    
    # Opciones de escaneo de puertos
    port_group = parser.add_argument_group('Opciones de escaneo de puertos')
    port_group.add_argument(
        '-p', '--ports',
        default='',
        help='Puertos a escanear (ej: 22,80,443 o 1-100 o "all" para 1-1000)'
    )
    port_group.add_argument(
        '--port-timeout',
        type=float,
        default=1.0,
        help='Timeout por puerto en segundos (default: 1.0)'
    )
    port_group.add_argument(
        '--service-scan',
        action='store_true',
        help='Muestra nombres de servicio para puertos abiertos'
    )
    
    # Opciones de salida
    output_group = parser.add_argument_group('Opciones de salida')
    output_group.add_argument(
        '-o', '--output',
        choices=['text', 'json', 'csv', 'html'],
        default='text',
        help='Formato de salida (default: text)'
    )
    
    # Opciones de logging/debug
    debug_group = parser.add_argument_group('Opciones de logging y debug')
    debug_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra información detallada durante el escaneo'
    )
    debug_group.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Nivel de logging (default: INFO)'
    )
    debug_group.add_argument(
        '--no-color',
        action='store_true',
        help='Deshabilita colores en la salida'
    )
    
    return parser.parse_args()


def setup_logging(args):
    """Configura el sistema de logging según los argumentos."""
    # Importación diferida para evitar errores si no está instalado colorlog
    try:
        from .logger import get_logger
    except ImportError as e:
        print(f"[ERROR] No se pudo importar el módulo logger: {e}")
        print("[INFO] Asegúrate de que logger.py existe en network_discovery_tool/")
        sys.exit(1)
    
    # Determinar nivel de verbosidad
    verbose = args.verbose or (args.log_level == 'DEBUG')
    
    # Obtener logger
    logger = get_logger(verbose)
    
    # Log inicial de configuración
    logger.debug(f"Argumentos recibidos: {args}")
    logger.debug(f"Directorio actual: {os.getcwd()}")
    
    return logger


def validate_network(network_str: str, logger) -> bool:
    """Valida el formato de la red."""
    try:
        from ipaddress import IPv4Network
        network = IPv4Network(network_str, strict=False)
        
        # Validaciones de seguridad/sentido común
        if network.prefixlen < 8:
            logger.warning(f"Prefijo muy amplio (/8 o menor). Esto escaneará {network.num_addresses:,} IPs")
            confirm = input("¿Continuar? (s/N): ")
            if confirm.lower() != 's':
                logger.info("Escaneo cancelado por el usuario")
                return False
        
        if network.num_addresses > 65536:  # Más de /16
            logger.warning(f"El escaneo incluirá {network.num_addresses:,} IPs. Esto puede tomar mucho tiempo.")
        
        return True
        
    except ValueError as e:
        logger.error(f"Formato de red inválido: {network_str}")
        logger.error(f"Error: {e}")
        logger.info("Formato correcto: 192.168.1.0/24 o 10.0.0.0/8")
        return False


def main():
    """Función principal ejecutada desde la línea de comandos."""
    args = None
    logger = None
    
    try:
        # 1. Parsear argumentos
        args = parse_arguments()
        
        # 2. Configurar logging
        logger = setup_logging(args)
        
        # 3. Validar red
        if not validate_network(args.network, logger):
            sys.exit(1)
        
        # 4. Log de inicio
        logger.scan_start(args.network, args.threads, args.timeout)
        
        # 5. Importar módulos necesarios (diferidos para mejor performance)
        logger.debug("Importando módulos de escaneo...")
        try:
            from .scanner import NetworkScanner, PortScanner
            from .output import generate_report
        except ImportError as e:
            logger.critical(f"Error importando módulos: {e}")
            logger.critical("Asegúrate de que scanner.py y output.py existen")
            sys.exit(1)
        
        # 6. FASE 1: Escaneo de hosts
        logger.info("Fase 1: Escaneo de hosts...")
        
        scanner = NetworkScanner(
            timeout=args.timeout, 
            max_threads=args.threads,
            verbose=args.verbose
        )
        
        hosts = scanner.scan_network(args.network)
        
        if not hosts:
            logger.warning("No se encontraron hosts activos en la red especificada")
            print("\n❌ No se encontraron hosts activos.")
            sys.exit(0)
        
        stats = scanner.get_scan_stats()
        logger.info(f"Hosts encontrados: {stats['total_hosts_found']}")
        
        # 7. FASE 2: Escaneo de puertos (si se especificó)
        port_results = {}
        if args.ports:
            logger.info("Fase 2: Escaneo de puertos...")
            
            # Parsear puertos
            if args.ports.lower() == 'all':
                ports_to_scan = set(range(1, 1001))
                logger.warning("Escaneando puertos 1-1000. Esto puede tomar tiempo.")
                
                # Confirmación para escaneo masivo
                if len(hosts) > 10 and len(ports_to_scan) > 100:
                    logger.warning(f"Se escanearán {len(ports_to_scan)} puertos en {len(hosts)} hosts")
                    confirm = input("¿Continuar? (s/N): ")
                    if confirm.lower() != 's':
                        logger.info("Escaneo de puertos cancelado por el usuario")
                        args.ports = ''  # Deshabilitar escaneo de puertos
            else:
                ports_to_scan = PortScanner.parse_port_range(args.ports)
                logger.debug(f"Puertos a escanear: {sorted(ports_to_scan)}")
            
            if args.ports:  # Si no fue cancelado
                logger.info(f"Escaneando {len(ports_to_scan)} puertos en {len(hosts)} hosts...")
                
                port_scanner = PortScanner(
                    timeout=args.port_timeout, 
                    max_threads=min(args.threads, 200),  # Límite por seguridad
                    verbose=args.verbose
                )
                
                port_results = port_scanner.scan_hosts_ports(hosts, ports_to_scan)
                
                # Añadir información de puertos a los hosts
                for host in hosts:
                    host['open_ports'] = port_results.get(host['ip'], [])
        
        # 8. Generar reporte
        logger.info("Generando reporte...")
        
        report = generate_report(
            hosts, 
            args.output, 
            port_info=port_results if args.ports else None,
            service_scan=args.service_scan
        )
        
        # 9. Mostrar/guardar resultados
        if args.output == 'text':
            print("\n" + "="*60)
            print(report)
        else:
            filename = f"scan_results_{args.network.replace('/', '_')}.{args.output}"
            
            # Evitar sobreescribir archivos existentes
            counter = 1
            while os.path.exists(filename):
                filename = f"scan_results_{args.network.replace('/', '_')}_{counter}.{args.output}"
                counter += 1
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                logger.info(f"Resultados guardados en: {filename}")
                print(f"\n✅ Reporte guardado como: {filename}")
                
                # Sugerencia para HTML
                if args.output == 'html':
                    print(f"💡 Ábrelo en tu navegador: firefox {filename} 2>/dev/null || xdg-open {filename}")
                    
            except (IOError, PermissionError) as e:
                logger.error(f"No se pudo guardar el archivo {filename}: {e}")
                print("\n❌ Error guardando archivo. Mostrando resultado en consola:")
                print(report)
        
        # 10. Log de finalización
        open_ports_count = sum(len(ports) for ports in port_results.values()) if args.ports else 0
        logger.scan_complete(len(hosts), stats['scan_duration'], open_ports_count)
        
        # 11. Mostrar resumen rápido en consola
        if args.output != 'text':  # Si ya mostramos texto, no repetir
            print(f"\n📊 RESUMEN: {len(hosts)} hosts, {open_ports_count} puertos abiertos")
            if open_ports_count > 0:
                print("🌐 Hosts con puertos abiertos:")
                for host in hosts:
                    if host.get('open_ports'):
                        ports = [str(p['port']) for p in host['open_ports']]
                        print(f"   • {host['ip']}: {', '.join(ports)}")
        
        logger.debug("Proceso completado exitosamente")
        sys.exit(0)
            
    except KeyboardInterrupt:
        if logger:
            logger.warning("Escaneo interrumpido por el usuario (Ctrl+C)")
        else:
            print("\n⚠️  Escaneo interrumpido por el usuario")
        print("\n🛑 Operación cancelada")
        sys.exit(130)  # Código estándar para Ctrl+C
    
    except ValueError as e:
        if logger:
            logger.error(f"Error de validación: {e}")
        else:
            print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    except Exception as e:
        if logger:
            logger.critical(f"Error crítico no manejado: {e}", exc_info=True)
        else:
            print(f"\n💥 ERROR CRÍTICO: {e}")
            print("💡 Ejecuta con --verbose para más detalles")
        
        # Información de debugging útil
        if args and args.verbose:
            print("\n🔧 INFORMACIÓN DE DEBUGGING:")
            print(f"   Python: {sys.version}")
            print(f"   Directorio: {os.getcwd()}")
            print(f"   Args: {args}")
        
        sys.exit(1)


# Punto de entrada cuando se ejecuta directamente
if __name__ == "__main__":
    main()
