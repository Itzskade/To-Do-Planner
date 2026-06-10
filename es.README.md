<p align="right">
  <a href="README.md">
    <img src="https://img.shields.io/badge/🌐%20English-README-%2312bab9?style=for-the-badge" alt="README English" />
  </a>
</p>

# To-Do Planner 📝

**To-Do Planner** es una aplicación de productividad ligera y eficiente diseñada para ayudarte a organizar tus tareas y pendientes diarios. Desarrollada en Python, te permite gestionar tu tiempo fácilmente, hacer un seguimiento de tu progreso y mantener tu vida diaria perfectamente organizada de forma sencilla e intuitiva.

---

## 🌟 Características Principales

* **Gestión de Tareas:** Añade, lista y completa tus tareas diarias sin esfuerzo.
* **Ligero y Rápido:** Uso mínimo de recursos para una planificación rápida e instantánea.
* **Ejecutable Independiente:** Se puede compilar en un solo binario para que se ejecute de forma nativa sin necesidad de tener Python instalado.
* **Persistencia de Datos:** Mantiene tus listas de tareas guardadas de forma segura localmente.

---

## 🛠️ Comandos y Uso

Este proyecto incluye un flujo de trabajo automatizado simplificado. Puedes gestionarlo todo usando comandos sencillos en la terminal:

| Comando | Descripción |
| :--- | :--- |
| `make install` | Configura el entorno virtual e instala todas las dependencias necesarias. |
| `make run` | Ejecuta la aplicación To-Do Planner directamente. |
| `make build` | Compila la aplicación en un archivo ejecutable independiente. |
| `make clean` | Limpia los archivos de compilación, la caché y los archivos temporales. |
| `make fclean` | Realiza una limpieza profunda, incluyendo la eliminación del entorno virtual. |
| `make remove` | Elimina los datos y la base de datos local de la aplicación. |

---

## 🚀 Primeros Pasos

1. Clona o descarga el repositorio en tu máquina local.
2. Abre tu terminal en el directorio raíz del proyecto.
3. Ejecuta `make install` para preparar el entorno.
4. Ejecuta `make run` ¡para empezar a planificar tu día!

---

## 📝 Notas Técnicas

- **Compatibilidad del entorno:** Diseñado para entornos tipo Unix (Linux, macOS o WSL en Windows) debido a los comandos nativos utilizados en el `Makefile` (`rm`, `echo -e`, etc.).
- **Gestión de dependencias:** Si requieres nuevas librerías en el proyecto, recuerda agregarlas a `requirements.txt` y ejecutar `make install` para integrarlas limpiamente en el entorno aislado.
- **Ciclo de compilación:** Al usar `make build`, el sistema verificará e instalará automáticamente `PyInstaller` si aún no lo tienes en tu `venv` para generar el empaquetado portátil.
- **Directorio de datos:** La carpeta `data/` se genera de manera dinámica almacenando el estado de tus pendientes; ten cuidado al usar `make remove` ya que purgará dicho registro.

---
