# Documentación API de Pedidos - Arte Ideas

## 📋 Resumen

API REST para la gestión de pedidos en el sistema Arte Ideas. Permite crear, leer, actualizar y eliminar pedidos, así como gestionar sus items y productos asociados.

## 🔐 Autenticación

Todas las peticiones requieren autenticación JWT. Incluir el token en el header:

```
Authorization: Bearer <tu_token_jwt>
```

## 📍 Endpoints Principales

### 1. Listar Pedidos
**GET** `/api/orders/`

Obtiene la lista de todos los pedidos del tenant actual.

#### Parámetros de Consulta (Query Parameters)
- `cliente__nombre`: Filtrar por nombre del cliente
- `tipo_documento`: Filtrar por tipo de documento (proforma, nota_venta, contrato)
- `estado`: Filtrar por estado del pedido (pending, in_process, completed, delayed, cancelled)
- `fecha_entrega`: Filtrar por fecha de entrega (formato: YYYY-MM-DD)
- `search`: Búsqueda general (busca en número de pedido, nombre, email, teléfono, DNI del cliente)

#### Ejemplo de Request
```bash
curl -X GET "https://api.arteideas.com/api/orders/?cliente__nombre=Juan&estado=pending&search=2024" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Ejemplo de Response (200 OK)
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "order_number": "ORD-2024-001",
      "client": 1,
      "client_info": {
        "id": 1,
        "full_name": "Juan Pérez",
        "email": "juan@example.com",
        "phone": "+51999999999",
        "dni": "12345678",
        "address": "Calle Principal 123",
        "client_type": "particular",
        "school_level": null,
        "grade": null,
        "section": null,
        "company_name": null
      },
      "document_type": "proforma",
      "client_type": "particular",
      "school_level": null,
      "grade": null,
      "section": null,
      "start_date": "2024-01-15",
      "delivery_date": "2024-02-15",
      "scheduled_dates": {
        "sesiones_fotograficas": [
          {"fecha": "2024-01-20", "hora": "10:00"}
        ],
        "entregas": [
          {"fecha": "2024-02-15", "hora": "14:00"}
        ]
      },
      "scheduled_sessions": ["2024-01-20 10:00"],
      "scheduled_deliveries": ["2024-02-15 14:00"],
      "subtotal": 1000.00,
      "tax": 180.00,
      "total": 1180.00,
      "paid_amount": 500.00,
      "balance": 680.00,
      "extra_services": {},
      "status": "pending",
      "contract": null,
      "notes": "Cliente preferencial",
      "affects_inventory": true,
      "items": [
        {
          "id": 1,
          "product_name": "Sesión Fotográfica Escolar",
          "product_description": "Sesión individual con 10 fotos impresas",
          "quantity": 1,
          "unit_price": 800.00,
          "subtotal": 800.00,
          "affects_inventory": true
        }
      ],
      "created_at": "2024-01-10T10:00:00Z",
      "updated_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```

### 2. Obtener Pedido Específico
**GET** `/api/orders/{id}/`

Obtiene los detalles de un pedido específico.

#### Ejemplo de Request
```bash
curl -X GET "https://api.arteideas.com/api/orders/1/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Ejemplo de Response (200 OK)
```json
{
  "id": 1,
  "order_number": "ORD-2024-001",
  "client": 1,
  "client_info": {
    "id": 1,
    "full_name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+51999999999",
    "dni": "12345678",
    "address": "Calle Principal 123",
    "client_type": "particular",
    "school_level": null,
    "grade": null,
    "section": null,
    "company_name": null
  },
  "document_type": "proforma",
  "client_type": "particular",
  "school_level": null,
  "grade": null,
  "section": null,
  "start_date": "2024-01-15",
  "delivery_date": "2024-02-15",
  "scheduled_dates": {
    "sesiones_fotograficas": [
      {"fecha": "2024-01-20", "hora": "10:00"}
    ],
    "entregas": [
      {"fecha": "2024-02-15", "hora": "14:00"}
    ]
  },
  "scheduled_sessions": ["2024-01-20 10:00"],
  "scheduled_deliveries": ["2024-02-15 14:00"],
  "subtotal": 1000.00,
  "tax": 180.00,
  "total": 1180.00,
  "paid_amount": 500.00,
  "balance": 680.00,
  "extra_services": {},
  "status": "pending",
  "contract": null,
  "notes": "Cliente preferencial",
  "affects_inventory": true,
  "items": [
    {
      "id": 1,
      "product_name": "Sesión Fotográfica Escolar",
      "product_description": "Sesión individual con 10 fotos impresas",
      "quantity": 1,
      "unit_price": 800.00,
      "subtotal": 800.00,
      "affects_inventory": true
    }
  ],
  "created_at": "2024-01-10T10:00:00Z",
  "updated_at": "2024-01-10T10:00:00Z"
}
```

### 3. Crear Pedido
**POST** `/api/orders/`

Crea un nuevo pedido.

#### Body Parameters
```json
{
  "order_number": "ORD-2024-002",
  "client": 1,
  "document_type": "proforma",
  "client_type": "particular",
  "start_date": "2024-01-20",
  "delivery_date": "2024-02-20",
  "total": 1500.00,
  "paid_amount": 750.00,
  "status": "pending",
  "notes": "Nuevo pedido",
  "items": [
    {
      "product_name": "Sesión Fotográfica Familiar",
      "product_description": "Sesión familiar con 15 fotos impresas",
      "quantity": 1,
      "unit_price": 1200.00
    },
    {
      "product_name": "Álbum Digital",
      "product_description": "Álbum digital con 50 fotos",
      "quantity": 2,
      "unit_price": 150.00
    }
  ]
}
```

#### Ejemplo de Request
```bash
curl -X POST "https://api.arteideas.com/api/orders/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "ORD-2024-002",
    "client": 1,
    "document_type": "proforma",
    "client_type": "particular",
    "start_date": "2024-01-20",
    "delivery_date": "2024-02-20",
    "total": 1500.00,
    "paid_amount": 750.00,
    "status": "pending",
    "notes": "Nuevo pedido",
    "items": [
      {
        "product_name": "Sesión Fotográfica Familiar",
        "product_description": "Sesión familiar con 15 fotos impresas",
        "quantity": 1,
        "unit_price": 1200.00
      },
      {
        "product_name": "Álbum Digital",
        "product_description": "Álbum digital con 50 fotos",
        "quantity": 2,
        "unit_price": 150.00
      }
    ]
  }'
```

#### Ejemplo de Response (201 Created)
```json
{
  "id": 2,
  "order_number": "ORD-2024-002",
  "client": 1,
  "client_info": {
    "id": 1,
    "full_name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+51999999999",
    "dni": "12345678",
    "address": "Calle Principal 123",
    "client_type": "particular",
    "school_level": null,
    "grade": null,
    "section": null,
    "company_name": null
  },
  "document_type": "proforma",
  "client_type": "particular",
  "school_level": null,
  "grade": null,
  "section": null,
  "start_date": "2024-01-20",
  "delivery_date": "2024-02-20",
  "scheduled_dates": {},
  "scheduled_sessions": [],
  "scheduled_deliveries": [],
  "subtotal": 1500.00,
  "tax": 270.00,
  "total": 1770.00,
  "paid_amount": 750.00,
  "balance": 1020.00,
  "extra_services": {},
  "status": "pending",
  "contract": null,
  "notes": "Nuevo pedido",
  "affects_inventory": true,
  "items": [
    {
      "id": 3,
      "product_name": "Sesión Fotográfica Familiar",
      "product_description": "Sesión familiar con 15 fotos impresas",
      "quantity": 1,
      "unit_price": 1200.00,
      "subtotal": 1200.00,
      "affects_inventory": true
    },
    {
      "id": 4,
      "product_name": "Álbum Digital",
      "product_description": "Álbum digital con 50 fotos",
      "quantity": 2,
      "unit_price": 150.00,
      "subtotal": 300.00,
      "affects_inventory": true
    }
  ],
  "created_at": "2024-01-15T15:30:00Z",
  "updated_at": "2024-01-15T15:30:00Z"
}
```

### 4. Actualizar Pedido
**PUT** `/api/orders/{id}/`

Actualiza completamente un pedido existente.

#### Body Parameters
```json
{
  "order_number": "ORD-2024-002",
  "client": 1,
  "document_type": "proforma",
  "client_type": "particular",
  "start_date": "2024-01-20",
  "delivery_date": "2024-02-25",
  "total": 1600.00,
  "paid_amount": 800.00,
  "status": "in_process",
  "notes": "Pedido actualizado",
  "items": [
    {
      "product_name": "Sesión Fotográfica Familiar",
      "product_description": "Sesión familiar con 15 fotos impresas",
      "quantity": 1,
      "unit_price": 1200.00
    },
    {
      "product_name": "Álbum Digital Premium",
      "product_description": "Álbum digital con 100 fotos",
      "quantity": 2,
      "unit_price": 200.00
    }
  ]
}
```

### 5. Actualización Parcial
**PATCH** `/api/orders/{id}/`

Actualiza parcialmente un pedido.

#### Body Parameters
```json
{
  "status": "completed",
  "notes": "Pedido entregado exitosamente"
}
```

### 6. Eliminar Pedido
**DELETE** `/api/orders/{id}/`

Elimina un pedido (solo administradores).

#### Ejemplo de Request
```bash
curl -X DELETE "https://api.arteideas.com/api/orders/2/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Ejemplo de Response (204 No Content)
```
```

## 📊 Endpoints de Resumen y Estadísticas

### 7. Resumen de Pedidos
**GET** `/api/orders/summary/`

Obtiene un resumen completo de todos los pedidos.

#### Ejemplo de Request
```bash
curl -X GET "https://api.arteideas.com/api/orders/summary/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Ejemplo de Response (200 OK)
```json
{
  "total_orders": 45,
  "total_amount": 54000.50,
  "total_paid": 42000.25,
  "total_balance": 12000.25,
  "pending_orders": 15,
  "in_process_orders": 10,
  "completed_orders": 18,
  "delayed_orders": 2,
  "cancelled_orders": 0,
  "proforma_orders": 20,
  "sale_note_orders": 15,
  "contract_orders": 10
}
```

### 8. Resumen de Totales Absolutos
**GET** `/api/orders/totals_summary/`

Obtiene los totales absolutos de todos los pedidos.

#### Ejemplo de Request
```bash
curl -X GET "https://api.arteideas.com/api/orders/totals_summary/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Ejemplo de Response (200 OK)
```json
{
  "total_absoluto": 5400.50,
  "saldo_absoluto": 1200.00
}
```

### 9. Autocompletado de Clientes
**GET** `/api/orders/autocomplete_clients/`

Busca clientes para autocompletado en formularios.

#### Parámetros de Consulta
- `q`: Texto de búsqueda (mínimo 2 caracteres)
- `client_type`: Filtrar por tipo de cliente (opcional: particular, colegio, empresa)

#### Ejemplo de Request
```bash
curl -X GET "https://api.arteideas.com/api/orders/autocomplete_clients/?q=Juan&client_type=particular" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Ejemplo de Response (200 OK)
```json
{
  "results": [
    {
      "id": 1,
      "first_name": "Juan",
      "last_name": "Pérez García",
      "full_name": "Juan Pérez García",
      "email": "juan@example.com",
      "phone": "+51999999999",
      "dni": "12345678",
      "address": "Calle Principal 123",
      "client_type": "particular"
    },
    {
      "id": 5,
      "first_name": "Juan Carlos",
      "last_name": "Rodríguez",
      "full_name": "Juan Carlos Rodríguez",
      "email": "juancarlos@example.com",
      "phone": "+51888888888",
      "dni": "87654321",
      "address": "Avenida Secundaria 456",
      "client_type": "particular"
    }
  ]
}
```

### 10. Pedidos Atrasados
**GET** `/api/orders/overdue_orders/`

Obtiene pedidos con fecha de entrega vencida y estado pendiente o en proceso.

#### Ejemplo de Request
```bash
curl -X GET "https://api.arteideas.com/api/orders/overdue_orders/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 11. Pedidos por Estado
**GET** `/api/orders/by_status/`

Obtiene pedidos filtrados por estado o resumen por estado.

#### Parámetros de Consulta
- `status`: Filtrar por estado específico (opcional)

#### Ejemplo de Request
```bash
curl -X GET "https://api.arteideas.com/api/orders/by_status/?status=pending" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 12. Próximas Entregas
**GET** `/api/orders/upcoming_deliveries/`

Obtiene pedidos con entregas programadas para la próxima semana.

#### Ejemplo de Request
```bash
curl -X GET "https://api.arteideas.com/api/orders/upcoming_deliveries/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## ✅ Acciones sobre Pedidos

### 13. Marcar Pedido como Completado
**POST** `/api/orders/{id}/mark_as_completed/`

Marca un pedido como completado.

#### Ejemplo de Request
```bash
curl -X POST "https://api.arteideas.com/api/orders/1/mark_as_completed/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Ejemplo de Response (200 OK)
```json
{
  "detail": "Pedido marcado como completado"
}
```

### 14. Marcar Pedido como Cancelado
**POST** `/api/orders/{id}/mark_as_cancelled/`

Marca un pedido como cancelado.

#### Ejemplo de Request
```bash
curl -X POST "https://api.arteideas.com/api/orders/1/mark_as_cancelled/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Ejemplo de Response (200 OK)
```json
{
  "detail": "Pedido marcado como cancelado"
}
```

## 🔄 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Recurso eliminado exitosamente |
| 400 | Bad Request - Error en los datos enviados |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - Sin permisos suficientes |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

## ⚠️ Errores Comunes

### Error 400 - Datos Inválidos
```json
{
  "order_number": ["Ya existe un pedido con este número"],
  "delivery_date": ["La fecha de entrega debe ser posterior a la fecha de inicio"],
  "total": ["El total no puede ser negativo"],
  "paid_amount": ["El monto pagado no puede exceder el total"]
}
```

### Error 403 - Sin Permisos
```json
{
  "detail": "No tiene permisos para realizar esta acción"
}
```

### Error 404 - Recurso No Encontrado
```json
{
  "detail": "No encontrado"
}
```

## 📋 Campos de Filtrado y Búsqueda

### Filtros Disponibles (DjangoFilterBackend)
- `cliente__nombre`: Nombre del cliente (icontains)
- `tipo_documento`: Tipo de documento (exact)
- `estado`: Estado del pedido (exact)
- `fecha_entrega`: Fecha de entrega (date)

### Campos de Búsqueda (SearchFilter)
Busca en los siguientes campos:
- `order_number`: Número de pedido
- `client__first_name`: Nombre del cliente
- `client__last_name`: Apellido del cliente
- `client__email`: Email del cliente
- `client__phone`: Teléfono del cliente
- `client__dni`: DNI del cliente

### Ordenamiento (OrderingFilter)
- `order_number`: Por número de pedido
- `start_date`: Por fecha de inicio
- `delivery_date`: Por fecha de entrega
- `total`: Por monto total
- `status`: Por estado
- `client__first_name`: Por nombre del cliente
- `client__last_name`: Por apellido del cliente

## 🔧 Tipos de Datos

### Tipos de Documento
- `proforma`: Proforma
- `nota_venta`: Nota de Venta
- `contrato`: Contrato

### Tipos de Cliente
- `particular`: Cliente particular
- `colegio`: Institución educativa
- `empresa`: Empresa

### Niveles Escolares (para colegios)
- `inicial`: Educación inicial
- `primaria`: Educación primaria
- `secundaria`: Educación secundaria

### Estados de Pedido
- `pending`: Pendiente
- `in_process`: En proceso
- `completed`: Completado
- `delayed`: Atrasado
- `cancelled`: Cancelado

## 📞 Soporte

Para soporte técnico o consultas sobre la API, contactar al equipo de desarrollo.

---

**Última actualización**: Enero 2024
**Versión**: 1.0.0