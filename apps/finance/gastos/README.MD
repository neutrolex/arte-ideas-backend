# 📖 APIS-DATAS-BACKEND: Documentación y Guía de Uso

Este documento detalla la arquitectura Multi-Tenant del proyecto y el uso del Módulo de Finanzas (`apps.finance`), confirmando la estabilidad del código base y la seguridad de los datos.

---

## 1. Configuración e Instalación

El proyecto utiliza una arquitectura de servicios robusta (JWT, Redis, Celery) y `django-tenants`.

### 1.1 Dependencias

* **Instalación** (con entorno virtual activo):
    ```bash
    pip install -r requirements.txt
    ```

### 1.2 Estructura Modular de Finanzas

La lógica de la aplicación se movió a una subcarpeta para mayor orden. Los archivos en la raíz (`finance/`) actúan como **ÍNDICES** que apuntan a la lógica en `finance/gastos/`.

| Archivo | Contenido (Código Índice) |
| :--- | :--- |
| `apps/finance/models.py` | `from .gastos.models import *` |
| `apps/finance/views.py` | `from .gastos.views import *` |
| `apps/finance/serializers.py` | `from .gastos.serializers import *` |
| `apps/finance/urls.py` | `path('', include('apps.finance.gastos.urls')),` |

### 1.3 Puesta en Marcha

1.  **Migraciones:**
    ```bash
    python manage.py migrate
    ```
2.  **Crear Superusuario:** (Obligatorio para Login)
    ```bash
    python manage.py createsuperuser
    ```
3.  **Iniciar Servidor:**
    ```bash
    python manage.py runserver
    ```

---

## 2. Arquitectura Multi-Tenant (CORE)

Esta arquitectura asegura que los datos del Tenant A (Empresa) nunca sean visibles para el Tenant B, incluso si acceden con un token válido.

### Componentes Clave

| Archivo | Clase | Función en Seguridad |
| :--- | :--- | :--- |
| `core/viewsets.py` | **TenantViewSet** | **Filtra Automáticamente** los listados (GET) por el `request.user.tenant`. |
| `core/middleware.py` | **TenantMiddleware** | Lee el Header `X-Tenant-ID` y asigna el Tenant al `request` para su verificación. |
| `core/permissions.py` | **TenantPermission** | Detiene peticiones (403 Forbidden) si el `X-Tenant-ID` no coincide con el Tenant del usuario logueado. |

---

## 3. Módulo: Gastos y Presupuestos (`/api/finance/`)

### 3.1 Endpoints y Lógica de Negocio

El módulo de finanzas se accede en `/api/finance/`. Los tests confirmaron la funcionalidad de los ViewSets y la lógica de negocio.

| Funcionalidad | Método | URL Completa | Lógica Probada con Éxito |
| :--- | :--- | :--- | :--- |
| **Login** | `POST` | `/api/core/auth/login/` | **Token Válido (200 OK)** y credenciales activas. |
| **Creación** | `POST` | `/api/finance/categories/` | **201 Created** al inyectar `tenant_id` y pasar la restricción `unique_together`. |
| **Lógica** | `POST` | `/api/finance/services/` | **201 Created**. Confirma que el Serializer acepta **`camelCase`** (`tipoServicio`, `fechaVencimiento`). |
| **Resumen** | `GET` | `/api/finance/summary/` | **200 OK**. Confirma que la vista agrega correctamente los montos (ej., `servicios_pendientes`). |
| **Edición** | `PATCH` | `/api/finance/services/{id}/` | **200 OK**. El cambio de monto se reflejó correctamente en la base de datos y en el resumen. |

### 3.2 Prueba Crítica de Aislamiento (Seguridad)

* **Test:** Intentar `GET /api/finance/summary/` con un `X-Tenant-ID` incorrecto (ej., `99`).
* **Resultado Verificado:** **`403 Forbidden`**.
* **Conclusión:** La seguridad Multi-Tenant es robusta.

---

##  4. Guía de Postman (Procedimiento Operativo)

Para usar cualquier endpoint de Finanzas, es obligatorio seguir esta secuencia:

### 4.1 Login

* **URL:** `http://127.0.0.1:8000/api/core/auth/login/`
* **Resultado:** Copiar el valor del token **`access`**.

### 4.2 Configuración de Headers (¡Esenciales!)

Estos dos headers deben acompañar **TODAS** las peticiones de Finanzas (CRUD):

| Header | Valor | Propósito |
| :--- | :--- | :--- |
| **`Authorization`** | `Bearer <Token_Access_JWT>` | Autenticación de la sesión. |
| **`X-Tenant-ID`** | `<ID del Tenant>` | Acceso a los datos de la empresa correcta. |

### 4.3 Ejemplo de Creación (Formato JSON)

```json
{
  "codigo": "SRV-ALQ-01",
  "tipoServicio": "Alquiler",
  "proveedor": "Inmobiliaria XYZ",
  "monto": "850.00",
  "fechaVencimiento": "2025-12-01",
  "periodo": "Noviembre 2025",
  "estado": "Pendiente",
  "categoria": 1
}
```