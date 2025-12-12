# network_discovery_tool/scanner.py
import concurrent.futures
import socket
import subprocess
import platform
from ipaddress import IPv4Network, AddressValueError
from typing import List, Dict, Optional, Set
import time

# Importar logger
from .logger import get_logger

# Diccionario de servicios comunes
SERVICE_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    445: 'SMB',
    3389: 'RDP',
    5900: 'VNC',
    8080: 'HTTP-Proxy',
    8443: 'HTTPS-Alt'
}

class NetworkScanner:
    def __init__(self, timeout: int = 2, max_threads: int = 50, verbose: bool = False):  # <-- VERBOSE AÑADIDO
        self.timeout = timeout
        self.max_threads = max_threads
        self.active_hosts = []
        self.scan_duration = 0
        self.logger = get_logger(verbose)  # <-- PASA VERBOSE
        
    def ping_host(self, ip: str) -> Optional[Dict]:
        """Realiza un ping a un host y retorna información si está activo."""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-W', str(self.timeout), ip]
        
        try:
            start_time = time.time()
            output = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout + 1,
                text=True
            )
            response_time = int((time.time() - start_time) * 1000)
            
            if output.returncode == 0:
                hostname = self.resolve_hostname(ip)
                return {
                    'ip': ip,
                    'hostname': hostname,
                    'status': 'active',
                    'response_time': response_time,
                    'open_ports': []  # Se llenará después si se escanean puertos
                }
        except Exception:
            pass
        
        return None
    
    def resolve_hostname(self, ip: str) -> str:
        """Resuelve el nombre de host para una IP."""
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except:
            return "N/A"
    
    def scan_network(self, network_cidr: str) -> List[Dict]:
        """Escanea un rango de red completo."""
        try:
            network = IPv4Network(network_cidr, strict=False)
        except AddressValueError:
            self.logger.error(f"Formato de red inválido: {network_cidr}")
            raise ValueError(f"Formato de red inválido: {network_cidr}")
        
        self.logger.info(f"Escaneando {network.num_addresses} direcciones IP...")
        start_time = time.time()
        hosts_data = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_ip = {
                executor.submit(self.ping_host, str(ip)): ip 
                for ip in network.hosts()
            }
            
            completed = 0
            total = network.num_addresses - 2
            
            for future in concurrent.futures.as_completed(future_to_ip):
                completed += 1
                if completed % 50 == 0:
                    self.logger.debug(f"Progreso: {completed}/{total}")
                
                result = future.result()
                if result:
                    hosts_data.append(result)
                    self.logger.debug(
                        f"Host activo: {result['ip']} ({result['hostname']})"
                    )
        
        self.scan_duration = time.time() - start_time
        self.active_hosts = hosts_data
        
        self.logger.info(
            f"Escaneo completado: {len(hosts_data)} hosts en "
            f"{self.scan_duration:.2f} segundos"
        )
        
        return hosts_data
    
    def get_scan_stats(self) -> Dict:
        """Retorna estadísticas del último escaneo."""
        return {
            'total_hosts_found': len(self.active_hosts),
            'scan_duration': round(self.scan_duration, 2),
            'hosts_per_second': round(len(self.active_hosts) / self.scan_duration, 2) 
            if self.scan_duration > 0 else 0
        }


class PortScanner:
    def __init__(self, timeout: int = 1, max_threads: int = 100, verbose: bool = False):  # <-- VERBOSE AÑADIDO
        self.timeout = timeout
        self.max_threads = max_threads
        self.logger = get_logger(verbose)  # <-- PASA VERBOSE
        
    @staticmethod
    def parse_port_range(port_spec: str) -> Set[int]:
        """Convierte una especificación de puertos a un conjunto."""
        ports = set()
        
        for part in port_spec.split(','):
            part = part.strip()
            if '-' in part:
                # Rango de puertos
                start_str, end_str = part.split('-')
                try:
                    start = int(start_str.strip())
                    end = int(end_str.strip())
                    if 1 <= start <= 65535 and 1 <= end <= 65535:
                        ports.update(range(min(start, end), max(start, end) + 1))
                except ValueError:
                    continue
            else:
                # Puerto individual
                try:
                    port = int(part)
                    if 1 <= port <= 65535:
                        ports.add(port)
                except ValueError:
                    continue
        
        return ports if ports else {22, 80, 443}  # Default si está vacío
    
    def scan_port(self, ip: str, port: int) -> Optional[int]:
        """Escanea un puerto TCP específico."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return port if result == 0 else None
        except (socket.timeout, socket.error, OSError):
            return None
    
    def scan_ports(self, ip: str, ports: Set[int]) -> List[Dict]:
        """Escanea múltiples puertos en un host y retorna información detallada."""
        open_ports = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_port = {
                executor.submit(self.scan_port, ip, port): port 
                for port in ports
            }
            
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                if future.result():
                    service = SERVICE_PORTS.get(port, 'Unknown')
                    open_ports.append({
                        'port': port,
                        'service': service,
                        'protocol': 'TCP'
                    })
        
        # Ordenar por número de puerto
        return sorted(open_ports, key=lambda x: x['port'])
    
    def scan_hosts_ports(self, hosts: List[Dict], ports: Set[int]) -> Dict[str, List[Dict]]:
        """Escanea puertos en múltiples hosts."""
        results = {}
        
        self.logger.info(f"Escaneando puertos en {len(hosts)} hosts activos...")
        self.logger.debug(f"Puertos a escanear: {sorted(ports)}")
        
        for i, host in enumerate(hosts, 1):
            ip = host['ip']
            self.logger.debug(f"Host {i}/{len(hosts)}: {ip}")
            
            open_ports = self.scan_ports(ip, ports)
            if open_ports:
                port_list = [p['port'] for p in open_ports]
                self.logger.info(f"{ip}: Puertos abiertos: {port_list}")
                results[ip] = open_ports
            else:
                self.logger.debug(f"{ip}: Sin puertos abiertos")
                results[ip] = []
        
        total_ports = sum(len(ports) for ports in results.values())
        self.logger.info(f"Escaneo de puertos completado: {total_ports} puertos abiertos")
        
        return results
