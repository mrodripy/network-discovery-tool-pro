# Changelog

Todos los cambios notables en Network Discovery Tool PRO serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.0] - 2025-12-11
### 🎉 Lanzamiento Inicial PRO

**¡Primera versión pública de Network Discovery Tool PRO!**

### Added
- **Escaneo completo de puertos TCP** con detección de servicios comunes
- **Sistema de logging profesional** con colores y rotación de archivos
- **Reportes HTML** con diseño visual y estadísticas
- **Múltiples formatos de salida**: HTML, JSON, CSV, Texto
- **CLI avanzada** con argumentos complejos y validación
- **Arquitectura modular** separada por funcionalidades
- **Escaneo paralelo** configurable con hilos
- **Manejo robusto de errores** y excepciones
- **Documentación completa** en README.md

### Changed
- **Reescritura completa** desde la versión básica
- **Nuevo comando principal**: `ndiscover-pro`
- **Nueva estructura de paquetes** profesional
- **setup.py** configurado para publicación en PyPI

### Technical
- **Python 3.6+** requerido
- **Dependencia principal**: `colorlog` para logging con colores
- **Arquitectura**: Separación clara de responsabilidades
- **Código**: Comentado y siguiendo PEP 8

### Breaking Changes
- No compatible con la versión básica anterior
- Nuevos nombres de comandos y argumentos
- Requiere instalación via `pip install -e .`

---

*Este proyecto sigue Semantic Versioning. Los cambios en versiones mayores (2.x.x) pueden incluir breaking changes.*
