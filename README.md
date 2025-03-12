# Manual de Uso y Configuración de Cesium_5071A_V1

Este documento describe paso a paso la instalación, configuración y ejecución del software Cesium_5071A_V1 en distintos sistemas operativos, así como una explicación detallada de sus funcionalidades.

## 1. Introducción

Cesium_5071A_V1 es una aplicación diseñada para la caracterización y análisis de relojes atómicos, basada en la frecuencia del cesio. Utiliza una interfaz gráfica desarrollada en PyQt6 y maneja datos obtenidos de mediciones para su procesamiento y visualización. Su propósito es facilitar la interpretación de datos experimentales y mejorar la exactitud en el análisis de los relojes atómicos, permitiendo una gestión eficiente de las mediciones y resultados.

## 2. Requisitos Previos

Antes de instalar y ejecutar el programa, asegúrate de cumplir con los siguientes requisitos:

### 2.1. Dependencias Generales

- Python 3.8 o superior
- Qt6 y PyQt6
- SQLite3 para la base de datos
- Bibliotecas adicionales como `numpy`, `matplotlib`, `pandas`, entre otras.

### 2.2. Instalación de Dependencias por Sistema Operativo

#### **Windows**

1. Descarga e instala [Python](https://www.python.org/downloads/).
2. Abre una terminal (CMD o PowerShell) y ejecuta:
   ```sh
   pip install -r requirements.txt
   ```
3. Verifica la instalación con:
   ```sh
   python -m PyQt6.uic.pyuic
   ```

#### **Linux (Ubuntu/Debian)**

1. Instala Python y dependencias:
   ```sh
   sudo apt update
   sudo apt install python3 python3-pip python3-pyqt6 sqlite3
   ```
2. Instala los paquetes requeridos:
   ```sh
   pip install -r requirements.txt
   ```

#### **macOS**

1. Instala Python (se recomienda usar Homebrew):
   ```sh
   brew install python3
   ```
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

## 3. Clonación y Ejecución del Proyecto

Para obtener el código fuente desde GitHub, usa los siguientes comandos:

```sh
git clone https://github.com/Hodoal/Cesium_5071A_V1.git
cd Cesium_5071A_V1
```

Para ejecutar la aplicación:

```sh
python main.py
```

## 4. Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
Cesium_5071A_V1/
│── main.py                # Archivo principal de la aplicación, encargado de iniciar la interfaz gráfica.
│── ui/                    # Contiene los archivos de diseño de la interfaz de usuario en PyQt6.
│   │── main_window.ui      # Archivo principal de la interfaz gráfica.
│   │── resources.qrc       # Archivos de recursos como imágenes y estilos.
│── models/                # Contiene la lógica de base de datos y los modelos de datos.
│   │── database.py         # Manejo de la base de datos SQLite3.
│   │── data_processing.py  # Funciones para procesamiento de datos y cálculos.
│── controllers/           # Gestión de eventos y lógica de la aplicación.
│   │── main_controller.py  # Controlador principal que gestiona la interacción con la GUI.
│── database/              # Archivos relacionados con la base de datos SQLite3.
│   │── cesium_data.db      # Base de datos SQLite que almacena las mediciones.
│── assets/                # Contiene imágenes, íconos y otros recursos gráficos.
│── requirements.txt       # Lista de dependencias necesarias para ejecutar el proyecto.
│── README.md              # Documentación general del proyecto.
```

## 5. Funcionalidades

### 5.1. Interfaz Gráfica (GUI)

La aplicación cuenta con una interfaz desarrollada en PyQt6, permitiendo:

- Cargar datos de mediciones.
- Visualizar datos en gráficas interactivas.
- Exportar resultados en formatos CSV.
- Analizar desplazamientos de frecuencia.

### 5.2. Base de Datos

El sistema almacena información en una base de datos SQLite3, permitiendo consultas rápidas y eficientes.

### 5.3. Cálculo y Análisis de Datos

Se implementan funciones matemáticas para el análisis del desplazamiento de frecuencia debido a radiación de cuerpo negro, efecto Zeeman y otras correcciones.

## 6. Solución de Problemas

- **Error de PyQt6 no encontrado**: Asegúrate de instalarlo con `pip install PyQt6`.
- **Problemas con SQLite3**: Verifica que SQLite3 esté instalado correctamente (`sqlite3 --version`).
- **Problemas con Git**: Usa `git pull origin main` para actualizar tu versión.

## 7. Contribuciones y Contacto

Si deseas contribuir, abre un pull request en el repositorio oficial. Para soporte, contáctanos a través de [GitHub Issues](https://github.com/Hodoal/Cesium_5071A_V1/issues).

