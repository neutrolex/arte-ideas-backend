# CRM • Contratos

Este módulo implementa la gestión de contratos dentro de `apps/crm/contracts`, alineado con la arquitectura y convenciones del proyecto `arte-ideas-backend-2`.

## Estructura
- `apps.py`: configuración de la app.
- `models.py`: modelo `Contract` con aislamiento multi-tenant y compatibilidad opcional con `crm.Cliente`.
- `admin.py`: registro en el admin, autoasignación de `tenant`, filtrado por `tenant`, acción de generación de PDF.
- `services.py`: `ContractPDFService` con import perezoso de WeasyPrint.
- `signals.py`: placeholders para integraciones.
- `templates/exports/contract.html`: plantilla para render del PDF.
- `tests.py`: pruebas básicas de API.

## Endpoints (DRF)
- `GET/POST /api/crm/contracts/` — Listar/crear contratos.
- `GET/PUT/DELETE /api/crm/contracts/{id}/` — CRUD contrato específico.
- `GET /api/crm/contracts/{id}/download/` — Generar/descargar documento del contrato.

## Configuración
- Añadir en `INSTALLED_APPS`: `apps.crm.contracts` (ya incluido).
- Dependencia opcional: `weasyprint` para generación de PDF.

## Integración
- Filtrado y asignación de `tenant` basado en el usuario autenticado.
- Integración opcional con `apps.crm.clientes.Cliente` vía FK.