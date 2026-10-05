# Informe de Uso Crítico de Inteligencia Artificial - NutriPet

## 1. Declaración de Uso
En el desarrollo del proyecto **NutriPet**, se utilizó Inteligencia Artificial (Gemini / ChatGPT) como asistente técnico para la estructuración de la lógica de negocio, refactorización de código en Python, diseño de componentes en Django y la implementación de la API RESTful con Django REST Framework (DRF).

---

## 2. Auditoría de Interacciones y Correcciones Aplicadas

### Interacción 1: Seguridad y Protección de Vistas HTML (ES2)
* **Consulta (Prompt):**
  > "¿Cómo proteger las vistas en Django usando un decorador personalizado que valide grupos de usuarios en el servidor y cómo ocultar los botones de Editar/Eliminar en la plantilla HTML?"
* **Respuesta de la IA:**
  Sugirió validar únicamente en la plantilla HTML con directivas `{% if request.user.is_staff %}` para ocultar las opciones de edición y eliminación según el perfil.
* **Corrección y Justificación Técnica:**
  Se rechazó la validación exclusiva en la plantilla porque un usuario no autorizado podía eludirla ingresando directamente la URL `/editar/1/`. Se implementó el decorador personalizado `@requiere_rol("admin")` en `views.py` para forzar la validación estricta a nivel de servidor.

---

### Interacción 2: Modelo de Usuarios y Gestión de Roles (ES2)
* **Consulta (Prompt):**
  > "¿Cómo estructurar el modelo Django para manejar roles de usuario y permisos sin complicar la arquitectura?"
* **Respuesta de la IA:**
  Sugirió crear un modelo de roles personalizado extendiendo `AbstractUser` o con una relación `OneToOneField`.
* **Corrección y Justificación Técnica:**
  Se simplificó la arquitectura rechazando el modelo personalizado e implementando la solución nativa de Django mediante `django.contrib.auth.models.Group` ("admin" y "normal"), garantizando mantenibilidad y menor sobrecarga.

---

### Interacción 3: Normalización de Datos en Migración (`cargar_datos.py`)
* **Consulta (Prompt):**
  > "¿Cómo migrar el historial previo de `datos.json` al modelo Django usando un script de carga automatizado?"
* **Respuesta de la IA:**
  Entregó un script que insertaba directamente las cadenas del JSON a la base de datos sin transformación previa.
* **Corrección y Justificación Técnica:**
  El script inicial fallaba al convertir enteros cuando encontraba valores `'N/A'` o textos inconsistentes como `"Otra especie"`, impidiendo que los registros se pudieran editar en `/admin/`. Se agregaron las funciones `mapear_especie()` y `mapear_alergeno()` con manejo de excepciones `try/except` para limpiar los campos y sincronizarlos con los `choices` del modelo Django.

---

### Interacción 4: Estructura del Formulario y Campo Alérgeno
* **Consulta (Prompt):**
  > "¿Cómo capturar el alérgeno en `form.html` sin usar ModelForm pero asegurando que coincida con el motor de reglas?"
* **Respuesta de la IA:**
  Sugirió un campo `<input type="text" name="alergeno">` de texto libre.
* **Corrección y Justificación Técnica:**
  Se reemplazó el `input` por un menú desplegable `<select>` con las opciones normalizadas para evitar que diferencias tipográficas o de capitalización corrompieran la evaluación en `solucion.py`.

---

### Interacción 5: Autenticación de API REST y Manejo de Errores 403 (ES3)
* **Consulta (Prompt):**
  > "¿Cómo solucionar un error `403 Forbidden` al probar los endpoints de la API con clientes como `curl` o Postman sin complicar la configuración de seguridad?"
* **Respuesta de la IA:**
  Sugirió utilizar `permission_classes = [AllowAny]` o el decorador `@csrf_exempt` en los `ViewSet` para omitir la verificación de autorización durante el desarrollo, o enviar el token mediante un parámetro GET en la URL (`?token=...`).
* **Corrección y Justificación Técnica:**
  * **Descarte de `AllowAny` / `@csrf_exempt`:** Se descartó completamente. Desactivar la autenticación deja la API totalmente expuesta e insegura. Apagar las verificaciones no soluciona el problema de fondo; la solución técnica correcta fue configurar la cabecera HTTP estándar `Authorization: Token <key>` en las peticiones.
  * **Descarte de Token en la URL:** El envío de tokens en la Query String expone credenciales sensibles en logs de servidores proxies e historial de navegadores.

---

### Interacción 6: Serialización y Protección de Reglas de Negocio (ES3)
* **Consulta (Prompt):**
  > "¿Cómo declarar el `Serializer` para la API REST sin tener que listar todos los campos manualmente?"
* **Respuesta de la IA:**
  Sugirió declarar `fields = '__all__'` en la clase Meta de `RecomendacionSerializer`.
* **Corrección y Justificación Técnica:**
  Se rechazó el uso de `fields = '__all__'`. Exponer todos los campos sin restricciones permitía que un cliente malintencionado enviara un JSON con el campo `recomendacion` modificado arbitrariamente, eludiendo la lógica del motor `solucion.py`. Se especificaron explícitamente los campos requeridos y se configuró `read_only_fields = ['recomendacion', 'creado']` para forzar que el backend calcule siempre la recomendación.

---

### Interacción 7: Permisos Granulares y Operaciones Críticas (ES3)
* **Consulta (Prompt):**
  > "¿Cómo permitir que los usuarios puedan consultar y crear registros mediante la API, pero restringir el borrado solo a administradores?"
* **Respuesta de la IA:**
  Sugirió dividir la vista en dos `ViewSet` separados en URLs distintas: uno de solo lectura y otro de administración.
* **Corrección y Justificación Técnica:**
  Se rechazó la duplicación de endpoints por violar las buenas prácticas de arquitectura RESTful. Se creó una clase de permiso personalizada `SoloStaffBorra` en `permissions.py` integrada en un único `ModelViewSet`. Esta clase valida `is_authenticated` para peticiones generales y evalúa `is_staff` exclusivamente cuando el método HTTP es `DELETE`.

---

## 3. Conclusión sobre la Integración de IA
El uso de la Inteligencia Artificial funcionó como una herramienta de aceleración para el diseño de arquitectura y escritura de código base. Sin embargo, **la supervisión humana y la validación técnica fueron indispensables** para:
1. Garantizar la seguridad de la aplicación en los endpoints RESTful evitando soluciones inseguras como `AllowAny`.
2. Proteger la integridad de la regla de negocio mediante la correcta declaración de campos `read_only` en los serializers.
3. Mantener una arquitectura RESTful limpia centralizando permisos (`SoloStaffBorra`) dentro del router y `ViewSet` nativo de DRF.