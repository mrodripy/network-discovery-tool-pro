# Network Discovery Tool PRO 🔍⚡

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/mrodripy/network-discovery-tool-pro)](https://github.com/mrodripy/network-discovery-tool-pro/releases)
[![GitHub Actions Status](https://github.com/mrodripy/network-discovery-tool-pro/actions/workflows/main.yml/badge.svg)](https://github.com/mrodripy/network-discovery-tool-pro/actions)
[![GitHub issues](https://img.shields.io/github/issues/mrodripy/network-discovery-tool-pro)](https://github.com/mrodripy/network-discovery-tool-pro/issues)

**Herramienta profesional de escaneo de redes** con detección de puertos, reportes HTML y sistema de logging avanzado.

> 🚀 **Versión PRO** - Evolución del [Network-Discovery-Tool básico](https://github.com/mrodripy/Network-Discovery-Tool) con características empresariales

## ✨ Características PRO

| Característica | Descripción |
|----------------|-------------|
| 🔍 **Escaneo de hosts** | Descubrimiento rápido mediante ping paralelo |
| 🚪 **Escaneo de puertos TCP** | Detección de puertos abiertos con servicios |
| 📊 **Múltiples formatos** | HTML, JSON, CSV, Texto |
| 🎨 **Reportes HTML** | Visualización profesional con estadísticas |
| 📝 **Logging avanzado** | Sistema con colores y rotación de archivos |
| ⚡ **Paralelización** | Hilos configurables para máximo rendimiento |
| 🛡️ **Validación robusta** | Manejo de errores y entrada segura |
| 🔧 **CLI profesional** | Argumentos avanzados y ayuda detallada |

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/mrodripy/network-discovery-tool-pro.git
cd network-discovery-tool-pro

# Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar en modo desarrollo
pip install -e .

# Verificar instalación
ndiscover-pro --help

📖 Uso Básico
```bash

# Escaneo básico de red
ndiscover-pro 192.168.1.0/24

# Escaneo con puertos comunes
ndiscover-pro 192.168.1.0/24 -p 22,80,443

# Reporte HTML profesional
ndiscover-pro 192.168.1.0/24 -p 1-100 -o html

# Escaneo detallado con logging
ndiscover-pro 192.168.1.0/24 --verbose --log-level DEBUG

# Detección de servicios
ndiscover-pro 192.168.1.0/24 -p 22,80,443,3389 --service-scan

# Escaneo rápido con más hilos
ndiscover-pro 192.168.1.0/24 --threads 100 --timeout 1

🖥️ Ejemplo de Salida
```bash

$ ndiscover-pro 192.168.1.0/24 -p 22,80,443 --verbose
14:30:25 - INFO - 🔍 INICIANDO ESCANEO PRO
14:30:25 - INFO - Red: 192.168.1.0/24, Hilos: 50, Timeout: 2s
14:30:25 - INFO - Fase 1: Escaneo de hosts...
14:30:29 - INFO - ✅ 9 hosts encontrados en 4.23 segundos
14:30:29 - INFO - Fase 2: Escaneo de puertos...
14:30:35 - INFO - 📡 192.168.1.1: Puertos abiertos: [80, 443]
14:30:35 - INFO - 📡 192.168.1.100: Puertos abiertos: [22]

============================================================
         NETWORK DISCOVERY TOOL PRO - REPORT
============================================================
Fecha: 2025-12-11 19:30:35
Hosts encontrados: 9
Puertos abiertos: 3
------------------------------------------------------------
IP                   HOSTNAME                       TIME (ms) 
------------------------------------------------------------
192.168.1.1          router.local                   5         
192.168.1.100        server.local                   12        
============================================================

🌐 Reporte HTML Profesional

La opción -o html genera un reporte visual completo que incluye:

    📊 Estadísticas de escaneo

    🎯 Tabla de hosts con colores

    🔢 Badges para puertos abiertos

    📈 Resumen visual de servicios

    📱 Diseño responsive

Para ver el reporte HTML:
```bash

ndiscover-pro 192.168.1.0/24 -p 22,80,443,3389,8080 -o html
firefox scan_results_192.168.1.0_24.html  # O tu navegador preferido

🛠️ Comandos Avanzados
Especificación de puertos flexible:
bash

# Puertos individuales
ndiscover-pro 192.168.1.0/24 -p 22,80,443

# Rangos de puertos
ndiscover-pro 192.168.1.0/24 -p 1-100

# Combinación
ndiscover-pro 192.168.1.0/24 -p 20-25,80,443-450

# Todos los puertos comunes (1-1000)
ndiscover-pro 192.168.1.0/24 -p all

Opciones de salida:
bash

# JSON para procesamiento automático
ndiscover-pro 192.168.1.0/24 -o json

# CSV para hojas de cálculo
ndiscover-pro 192.168.1.0/24 -o csv

# Texto simple para terminal
ndiscover-pro 192.168.1.0/24 -o text

Configuración de rendimiento:
bash

# Más hilos para escaneo rápido
ndiscover-pro 192.168.1.0/24 --threads 200

# Timeout reducido para redes rápidas
ndiscover-pro 192.168.1.0/24 --timeout 1

# Timeout específico para puertos
ndiscover-pro 192.168.1.0/24 --port-timeout 0.5

🏗️ Arquitectura del Proyecto
text

network-discovery-tool-pro/
├── network_discovery_tool/     # Paquete principal
│   ├── __init__.py            # Configuración del paquete
│   ├── cli.py                 # Interfaz de línea de comandos
│   ├── scanner.py             # Motores de escaneo
│   ├── output.py              # Generador de reportes
│   └── logger.py              # Sistema de logging
├── main.py                    # Punto de entrada
├── setup.py                   # Configuración para pip
├── requirements.txt           # Dependencias
├── README.md                  # Esta documentación
├── CHANGELOG.md              # Historial de cambios
└── LICENSE                    # Licencia MIT

📦 Módulos Principales
scanner.py

    NetworkScanner: Escaneo de hosts mediante ping paralelo

    PortScanner: Escaneo de puertos TCP con detección de servicios

    Escaneo paralelo con concurrent.futures

output.py

    Generación de reportes en múltiples formatos

    HTML con CSS integrado para visualización profesional

    JSON estructurado para integraciones

    CSV para análisis en hojas de cálculo

logger.py

    Sistema de logging con niveles (DEBUG, INFO, WARNING, ERROR)

    Salida coloreada a consola

    Logs rotativos a archivo

    Métodos especializados para eventos de escaneo

cli.py

    Parsing de argumentos con argparse

    Validación de entrada y manejo de errores

    Mensajes de ayuda detallados

    Soporte para redirección de salida

⚠️ Uso Responsable y Legal

IMPORTANTE: Solo usa esta herramienta en redes propias o con permiso explícito.
✅ Usos permitidos:

    Redes locales de tu propiedad

    Laboratorios de testing y práctica

    Máquinas virtuales bajo tu control

    Auditorías con autorización escrita

❌ Usos prohibidos:

    Redes públicas o ajenas sin permiso

    Sitios web o servicios de terceros

    Redes corporativas o educativas sin autorización

    Cualquier actividad ilegal o maliciosa

El autor no se responsabiliza del uso indebido de esta herramienta.
🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

    Haz fork del repositorio

    Crea una rama para tu feature (git checkout -b feature/nueva-funcionalidad)

    Commit tus cambios (git commit -m 'Añadir nueva funcionalidad')

    Push a la rama (git push origin feature/nueva-funcionalidad)

    Abre un Pull Request

Guía de estilo:

    Sigue PEP 8 para código Python

    Añade comentarios para código complejo

    Incluye ejemplos de uso para nuevas features

    Actualiza la documentación correspondiente

🐛 Reportar Problemas

Si encuentras un bug o tienes una sugerencia:

    Busca si el problema ya fue reportado

    Crea un nuevo issue con:

        Descripción clara del problema

        Pasos para reproducirlo

        Comportamiento esperado vs actual

        Capturas de pantalla si aplica

        Versión de Python y del sistema

📈 Roadmap
Próximas versiones:

    v2.1: Base de datos SQLite para historial de escaneos

    v2.2: Comando --compare para detectar cambios en la red

    v2.3: Dashboard web con Flask/FastAPI

    v2.4: Escaneo UDP y detección de OS básica

Características planeadas:

    Exportación a formato Nmap XML

    Integración con APIs de monitoreo

    Scripting y automatización avanzada

    Plugin system para escaneos personalizados

📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.
👨‍💻 Autor

Miguel Rodríguez - @mrodripy
🙏 Agradecimientos

    Inspirado por herramientas como nmap, masscan

    Comunidad de Python por las increíbles bibliotecas estándar

    Todos los contribuidores y usuarios que prueban y mejoran este proyecto

🔗 Enlaces Relacionados

    Versión básica - Versión simple solo para escaneo de hosts

    Reportar un issue

    Ver releases

    Changelog

<p align="center"> <strong>¿Te gusta este proyecto?</strong><br> ¡Dale una ⭐ en GitHub y compártelo con otros profesionales! </p><p align="center"> <sub>Creado con ❤️ para la comunidad de networking y seguridad</sub> </p> ```
