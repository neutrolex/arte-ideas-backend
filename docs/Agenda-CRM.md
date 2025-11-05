# Módulo Agenda (CRM)

Este módulo gestiona eventos, citas y recordatorios dentro del CRM con soporte para filtros avanzados y vistas de dashboard.

## Apps y configuración
- Registrar en `INSTALLED_APPS`: `apps.crm.agenda` y `django_filters`.
- Plantillas: `templates/agenda/proximos_eventos_demo.html`.

## Rutas (prefijo: `/api/crm/agenda/`)
- `GET /eventos/` — Lista de eventos (auth requerida)
- `POST /eventos/` — Crear evento (auth requerida)
- `POST /eventos/{id}/completar_evento/` — Completar evento
- `POST /eventos/{id}/cancelar_evento/` — Cancelar evento
- `GET /eventos/proximos_eventos/` — Próximos eventos del usuario
- `GET /eventos/eventos_hoy/` — Eventos del día
- `POST /eventos/verificar_disponibilidad/` — Chequea disponibilidad (serializador `Disponibilidad`)
- `GET /citas/` — Lista de citas (auth requerida)
- `POST /citas/{id}/confirmar_cita/` — Confirmar cita
- `POST /citas/{id}/completar_cita/` — Completar cita
- `GET /recordatorios/pendientes/` — Recordatorios pendientes
- `GET /dashboard/` — Datos agregados del dashboard
- `GET /proximos-eventos/` — Próximos eventos (API)
- `GET /eventos-hoy/` — Eventos del día (API)
- `GET /citas-pendientes/` — Citas pendientes (API)
- `GET /proximos-eventos-demo/` — Endpoint demo público (sin auth)
- `GET /demo/` — Página HTML demo que consume el endpoint anterior

## Señales
- Validación de fechas en `Evento` antes de guardar.
- Creación automática de `Recordatorio` según `recordatorio_minutos`.
- Actualización del estado del `Evento` al cambiar estado de `Cita`.
- Envío de recordatorios por email si corresponde.

## Filtros
- `EventoFilter` y `CitaFilter` soportan búsqueda por rango de fechas, estado, prioridad, tipo y banderas `vencidos`, `proximos`, `hoy`.

## Notas de multi-tenant
- Los querysets filtran por `request.user` (creado/asignado) sin alterar los modelos existentes.