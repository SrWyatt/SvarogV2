# UNIVERSIDAD GERARDO BARRIOS

**Facultad:** Ciencia y Tecnología  
**Asignatura:** Programación III  
**Docente:** William Alexander Montes Girón  
**Actividad:** Evaluación Parcial II  
**Estudiante:** Josué Esaú Batres Guardado – SMIS058820  
**Fecha de entrega:** 24 / 10 / 2025

---

## Introducción

En el mundo de la programación, la presentación visual del contenido en la consola suele pasarse por alto, pero es clave para mejorar la comprensión y la experiencia del usuario.

La librería **Rich** ofrece una manera moderna, elegante y funcional de imprimir texto, tablas, paneles, barras de progreso y trazas de errores en la terminal con colores y formato avanzado, sin necesidad de usar interfaces gráficas.

Este documento explora qué es **Rich**, sus principales funciones y cómo se ha utilizado en proyectos reales para mejorar la interacción visual en la línea de comandos.

---

## ¿Qué es la librería Rich y para qué se usa?

**Rich** es una librería de Python desarrollada por **Will McGugan** que permite mejorar la salida visual en la terminal agregando colores, estilos, tablas, paneles y barras de progreso, todo con un formato limpio y atractivo.

Su objetivo principal es hacer que las aplicaciones de consola sean más legibles y profesionales, sin requerir un entorno gráfico ni dependencias pesadas.

Se utiliza en proyectos de depuración, monitoreo de procesos, herramientas de línea de comandos (CLI) y dashboards ligeros.

---

## Instalación de la librería Rich

Para instalar **Rich**, se puede usar `pip`, el gestor de paquetes de Python:
```bash
pip install rich
```

También puede instalarse desde el código fuente disponible en GitHub:
```bash
git clone https://github.com/Textualize/rich.git
cd rich
python setup.py install
```

---

## Funciones más relevantes y utilizadas

### 1. print() personalizada de Rich

Permite imprimir texto con colores, estilos y formato enriquecido:
```python
from rich import print

print("[bold magenta]¡Hola desde Rich![/bold magenta]")
```

### 2. Console

Objeto principal que gestiona la salida formateada:
```python
from rich.console import Console

console = Console()
console.print("Texto con color [green]verde[/green]")
```

### 3. Table

Crea tablas con bordes, colores y alineaciones:
```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Usuarios Conectados")

table.add_column("Nombre", justify="left")
table.add_column("Estado", justify="center")

table.add_row("Alice", "[green]Activo[/green]")
table.add_row("Bob", "[red]Desconectado[/red]")

console.print(table)
```

### 4. Progress

Muestra barras de progreso animadas en la terminal:
```python
from rich.progress import track
import time

for paso in track(range(10), description="Cargando..."):
    time.sleep(0.2)
```

### 5. Traceback

Muestra errores y excepciones con formato colorido y organizado:
```python
from rich.traceback import install

install()

# Ejemplo que genera una excepción
1 / 0
```

---

## Casos de uso en la vida real

### Proyectos CLI populares

- **Poetry**, el gestor de dependencias de Python, utiliza Rich para mostrar información con formato agradable.
- **Textual**, un framework para crear interfaces de texto interactivas (también creado por el autor de Rich), se basa completamente en esta librería.

### Scripts internos y herramientas de DevOps

Ingenieros la usan para mostrar logs en tiempo real con colores que facilitan distinguir errores, advertencias y eventos importantes.

### Educación y documentación

Muchos instructores la usan para mostrar ejemplos más claros en terminales educativas o entornos interactivos.

---

## Bibliografía

- McGugan, W. (2020). *Rich: Rich text and beautiful formatting in the terminal*. Disponible en: https://github.com/Textualize/rich
- Documentación oficial de Rich: https://rich.readthedocs.io
- Python Package Index (PyPI): https://pypi.org/project/rich/
- Ejemplos de uso en proyectos reales: https://github.com/python-poetry/poetry
