# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="network-discovery-tool",
    version="2.0.0",
    author="mrodripy",
    author_email="",  # Opcional
    description="Herramienta profesional para descubrir hosts y puertos en redes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrodripy/Network-Discovery-Tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: Security",
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorlog>=6.7.0",  # Para logging con colores
    ],
    entry_points={
        "console_scripts": [
            "ndiscover=network_discovery_tool.cli:main",
        ],
    },
    include_package_data=True,
    keywords="network, scanner, security, discovery, portscan",
)
