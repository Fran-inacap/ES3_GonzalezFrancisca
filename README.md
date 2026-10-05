# NutriPet - Sistema Recomendador de Alimentos

NutriPet es una aplicación web desarrollada en **Django** que evalúa las características de una mascota (especie, edad y alérgeno) y aplica un motor de reglas para sugerir el alimento adecuado de la línea **Josera**.

---

## 🚀 Requisitos Previos

* **Python 3.10+**
* **Git**

---

## 🛠️ Instrucciones de Instalación y Ejecución

Sigue estos pasos para clonar y ejecutar la aplicación localmente:

### Clonar el repositorio y entrar al proyecto
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd NutriPet

## API RESTful NutriPet

### Configuración DRF e Decisiones de Arquitectura
- **Autenticación por Token:** Se optó por `TokenAuthentication` dado que el cliente consumirá los datos como un servicio decoupled en formato JSON, donde las cookies de sesión HTML tradicionales no aplican.
- **Permisos Globales:** Se estableció `IsAuthenticated` como la política por defecto en `REST_FRAMEWORK` para asegurar todos los endpoints frente a accesos anónimos.
- **Paginación:** Se configuró `PageNumberPagination` con un `PAGE_SIZE` de 10 elementos por página para optimizar la transferencia de datos y evitar la sobrecarga de ancho de banda.

### Tabla de Endpoints

| Método HTTP | Endpoint | Descripción | Permisos | Código Exito |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/token/` | Obtener token de autenticación | Público | `200 OK` |
| **GET** | `/api/recomendaciones/` | Listar recomendaciones (paginado) | Autenticado | `200 OK` |
| **POST** | `/api/recomendaciones/` | Crear recomendación (ejecuta regla) | Autenticado | `201 Created` |
| **GET** | `/api/recomendaciones/{id}/` | Detalle de recomendación | Autenticado | `200 OK` |
| **PUT/PATCH**| `/api/recomendaciones/{id}/` | Actualizar recomendación | Autenticado | `200 OK` |
| **DELETE** | `/api/recomendaciones/{id}/` | Eliminar recomendación | **Solo Staff** | `204 No Content` |
| **GET** | `/api/docs/` | Documentación interactiva Swagger | Público | `200 OK` |