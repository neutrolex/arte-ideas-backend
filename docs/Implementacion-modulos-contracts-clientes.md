# Implementación de módulos CRM: Clientes y Contratos

Este documento describe la integración de los módulos **Clientes** y **Contratos** en el proyecto actual, su uso de multi-tenancy, endpoints disponibles y requisitos.

## Resumen de Cambios
- Se creó `apps/crm/clientes` con modelos, serializers, vistas, admin y urls.
- Se creó `apps/crm/contracts` con modelos, serializers, vistas, urls, servicios y señales.
- Se actualizó `config/settings.py` para registrar `apps.crm.clientes` y `apps.crm.contracts` en `INSTALLED_APPS`.
- Se actualizó `apps/crm/urls.py` para incluir subrutas: `clients/` y `contracts/`.
- Se añadió la plantilla `templates/exports/contract.html` para generación de PDF (opcional con WeasyPrint).

## Multi-tenancy y Seguridad
- Todos los listados filtran por el `tenant` del usuario autenticado (excepto superadmin que ve todo).
- En creación (`POST`), se asigna automáticamente `tenant = request.user.tenant`.
- La unicidad de `dni` y `ruc` se valida por `tenant` tanto en constraints como en `clean()` del modelo.

## Endpoints

Base: `/api/crm/`

### Clientes (`/api/crm/clients/`)
- `GET /` — Lista de clientes del tenant
- `POST /` — Crear cliente (asigna tenant automáticamente)
- `GET /{id}/` — Ver cliente
- `PUT/PATCH /{id}/` — Editar cliente
- `DELETE /{id}/` — Eliminar cliente

Notas de validación:
- `tipo_cliente = particular` requiere `dni` (8 dígitos). Limpia `ruc`.
- `tipo_cliente = empresa/colegio` requiere `ruc` (11 dígitos). Limpia `dni`.
- `colegio` requiere `institucion_educativa`.

### Contratos (`/api/crm/contracts/`)
- `GET /` — Lista de contratos del tenant
- `POST /` — Crear contrato (asigna tenant automáticamente)
- `GET /{id}/` — Ver contrato
- `PUT/PATCH /{id}/` — Editar contrato
- `DELETE /{id}/` — Eliminar contrato
- `POST /{id}/download/` — Generar y guardar PDF del contrato

Notas de validación:
- `end_date >= start_date` (si existe)
- `amount >= 0`
- Debe existir al menos `client` (FK) o `client_name`.

## Dependencias
- PDF opcional: `weasyprint` (no instalada por defecto). La acción `download` retorna `501` si no está disponible.

Para habilitar generación de PDF:
```
pip install weasyprint
```
En Windows puede requerir dependencias del sistema (GTK / Cairo). Considerar entorno Linux para facilidad.

## Plantillas
- `templates/exports/contract.html` — plantilla HTML básica utilizada por el servicio de PDF.

## Admin
- `apps/crm/clientes/admin.py` — Admin listo con formulario dinámico y mensajes de éxito.
- `apps/crm/contracts` — puede añadirse admin si se requiere gestión desde el panel.

## Migraciones y Pruebas
Ejecutar:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Probar endpoints con un usuario autenticado. Superadmin accede a todos los registros.

## Consideraciones Futuras
- Añadir permisos finos por rol para acceso a módulos (`access_clientes`, `access_contratos`).
- Extender auditoría con señales en `contracts/signals.py`.
- Mejorar plantilla del contrato y agregar branding del tenant.