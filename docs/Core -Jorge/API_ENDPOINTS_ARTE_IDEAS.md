# 🔌 API Endpoints Completo - Arte Ideas Core App

## 🌐 Base URL
```
http://localhost:8000/  # Desarrollo local
```

## 📋 Estándar de URLs Unificado
Todas las APIs siguen el patrón: `/api/core/[modulo]/[accion]/`

---

## 🔐 Módulo 1: Autenticación (`/api/core/auth/`)

### Autenticación JWT
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| **POST** | `/api/core/auth/login/` | Login de usuario | No requerida |
| **POST** | `/api/core/auth/refresh/` | Refresh token | No requerida |
| **POST** | `/api/core/auth/logout/` | Logout de usuario | Requerida |

#### Ejemplos de Autenticación

**Login de Usuario:**
- **Método:** POST
- **URL:** `{{base_url}}/api/core/auth/login/`
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "username": "admin_a",
    "password": "admin123"
  }
  ```

**Respuesta Exitosa:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Posibles Errores:**
```json
{
  "detail": "No active account found with the given credentials"
}
```
```json
{
  "username": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "password": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "non_field_errors": [
    "Usuario inactivo. Contacte al administrador."
  ]
}
```
```json
{
  "detail": "Token inválido o expirado"
}
```

**Refresh Token:**
- **Método:** POST
- **URL:** `{{base_url}}/api/core/auth/refresh/`
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

**Respuesta Exitosa:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Logout de Usuario:**
- **Método:** POST
- **URL:** `{{base_url}}/api/core/auth/logout/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

**Respuesta Exitosa:**
```json
{
  "message": "Sesión cerrada exitosamente"
}
```

**Posibles Errores de Logout:**
```json
{
  "error": "Token inválido o ya expirado"
}
```
```json
{
  "refresh_token": [
    "El refresh token es requerido."
  ]
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```
```json
{
  "detail": "Token inválido."
}
```

**Posibles Errores de Refresh Token:**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```
```json
{
  "refresh": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "refresh": [
    "Token inválido o expirado."
  ]
}
```



---

## 👤 Módulo 2: Mi Perfil (`/api/core/profile/`)

### Gestión de Perfil Personal
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| **GET** | `/api/core/profile/view/` | Ver mi perfil | Requerida |
| **PUT** | `/api/core/profile/edit/` | Editar mi perfil | Requerida |
| **GET** | `/api/core/profile/statistics/` | Estadísticas mensuales | Requerida |
| **GET** | `/api/core/profile/activity/` | Actividad reciente | Requerida |
| **GET** | `/api/core/profile/completion/` | Porcentaje completitud | Requerida |
| **POST** | `/api/core/profile/change-password/` | Cambiar contraseña | Requerida |
| **POST** | `/api/core/profile/change-email/` | Cambiar email | Requerida |

#### Ejemplos de Mi Perfil

**Ver Mi Perfil:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/profile/view/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "admin_a",
  "email": "admin@tenant-a.com",
  "first_name": "Administrador",
  "last_name": "Tenant A",
  "full_name": "Administrador Tenant A",
  "phone": "987654321",
  "address": "Lima, Perú",
  "bio": "",
  "avatar": null,
  "role": "admin",
  "role_display": "Administrador",
  "tenant_name": "Estudio Fotográfico A",
  "email_verified": true,
  "is_active": true,
  "date_joined": "2025-10-31T22:01:05.123456Z",
  "last_login": "2025-10-31T22:30:15.654321Z",
  "profile": {
    "language": "es",
    "theme": "light",
    "email_notifications": true,
    "completion_percentage": 67
  }
}
```

**Editar Mi Perfil:**
- **Método:** PUT
- **URL:** `{{base_url}}/api/core/profile/edit/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "first_name": "Administrador",
    "last_name": "Actualizado",
    "phone": "999888777",
    "address": "Nueva dirección, Lima, Perú",
    "bio": "Administrador del estudio fotográfico con 5 años de experiencia"
  }
  ```

**Respuesta Exitosa:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "admin_a",
  "email": "admin@tenant-a.com",
  "first_name": "Administrador",
  "last_name": "Actualizado",
  "full_name": "Administrador Actualizado",
  "phone": "999888777",
  "address": "Nueva dirección, Lima, Perú",
  "bio": "Administrador del estudio fotográfico con 5 años de experiencia",
  "avatar": null,
  "role": "admin",
  "role_display": "Administrador",
  "tenant_name": "Estudio Fotográfico A",
  "email_verified": true,
  "is_active": true,
  "date_joined": "2025-10-31T22:01:05.123456Z",
  "last_login": "2025-10-31T22:30:15.654321Z",
  "profile": {
    "language": "es",
    "theme": "light",
    "email_notifications": true,
    "completion_percentage": 100
  }
}
```

**Posibles Errores de Edición de Perfil:**
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```
```json
{
  "first_name": [
    "Este campo no puede estar vacío."
  ]
}
```
```json
{
  "last_name": [
    "Este campo no puede estar vacío."
  ]
}
```
```json
{
  "phone": [
    "Ingrese un número de teléfono válido."
  ]
}
```
```json
{
  "bio": [
    "La biografía no puede superar los 500 caracteres."
  ]
}
```

**Estadísticas Mensuales:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/profile/statistics/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "orders_processed": 234,
  "clients_attended": 89,
  "sessions_completed": 45,
  "hours_worked": 180
}
```

**Actividad Reciente:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/profile/activity/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
[
  {
    "action": "update",
    "action_display": "Actualizar registro",
    "description": "Actualizó su perfil personal",
    "module": "profile",
    "created_at": "2025-10-31T22:45:30.123456Z",
    "time_ago": "Hace 5 minutos"
  },
  {
    "action": "login",
    "action_display": "Inicio de sesión",
    "description": "Inició sesión en el sistema",
    "module": "auth",
    "created_at": "2025-10-31T22:30:15.654321Z",
    "time_ago": "Hace 20 minutos"
  }
]
```

**Porcentaje de Completitud:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/profile/completion/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "completion_percentage": 100,
  "completed_fields": 6,
  "total_fields": 6
}
```

**Cambiar Contraseña:**
- **Método:** POST
- **URL:** `{{base_url}}/api/core/profile/change-password/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "current_password": "admin123",
    "new_password": "nuevaPassword123!",
    "confirm_password": "nuevaPassword123!"
  }
  ```

**Respuesta Exitosa:**
```json
{
  "message": "Contraseña actualizada correctamente"
}
```

**Posibles Errores:**
```json
{
  "current_password": [
    "La contraseña actual es incorrecta."
  ]
}
```
```json
{
  "non_field_errors": [
    "Las contraseñas no coinciden."
  ]
}
```
```json
{
  "current_password": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "new_password": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "new_password": [
    "La contraseña debe tener al menos 8 caracteres."
  ]
}
```
```json
{
  "new_password": [
    "Esta contraseña es demasiado común."
  ]
}
```
```json
{
  "confirm_password": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```

**Cambiar Email:**
- **Método:** POST
- **URL:** `{{base_url}}/api/core/profile/change-email/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "new_email": "nuevo.email@tenant-a.com",
    "password": "admin123"
  }
  ```

**Respuesta Exitosa:**
```json
{
  "message": "Email actualizado correctamente"
}
```

**Posibles Errores:**
```json
{
  "password": [
    "La contraseña es incorrecta."
  ]
}
```
```json
{
  "new_email": [
    "Este email ya está en uso."
  ]
}
```
```json
{
  "password": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "new_email": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "new_email": [
    "Ingrese una dirección de correo válida."
  ]
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```
```json
{
  "error": "Sin permisos para cambiar email"
}
```

---

## ⚙️ Módulo 3: Configuración (`/api/core/config/`)

### Configuración del Negocio
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| **GET** | `/api/core/config/business/view/` | Ver configuración del negocio | Admin |
| **PUT** | `/api/core/config/business/edit/` | Editar configuración del negocio | Admin |

### Gestión de Usuarios
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| **GET** | `/api/core/config/users/list/` | Lista de usuarios del tenant | Admin |
| **POST** | `/api/core/config/users/create/` | Crear nuevo usuario | Admin |
| **GET** | `/api/core/config/users/{id}/view/` | Ver usuario específico | Admin |
| **PUT** | `/api/core/config/users/{id}/edit/` | Editar usuario | Admin |
| **PATCH** | `/api/core/config/users/{id}/toggle/` | Activar/Desactivar usuario | Admin |
| **DELETE** | `/api/core/config/users/{id}/delete/` | Eliminar usuario | Admin |

### Roles y Permisos
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| **GET** | `/api/core/config/roles/list/` | Lista de roles disponibles | Admin |
| **GET** | `/api/core/config/permissions/{role}/view/` | Ver permisos de rol | Admin |
| **PUT** | `/api/core/config/permissions/{role}/edit/` | Editar permisos de rol | Admin |
| **POST** | `/api/core/config/permissions/{role}/reset/` | Restablecer permisos por defecto | Admin |

### Super Admin - Gestión de Tenants
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| **GET** | `/api/core/config/tenants/list/` | Lista de todos los tenants | Super Admin |
| **POST** | `/api/core/config/tenants/create/` | Crear nuevo tenant | Super Admin |
| **GET** | `/api/core/config/tenants/{id}/users/` | Usuarios de un tenant | Super Admin |

#### Ejemplos de Configuración del Negocio

**Ver Configuración del Negocio:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/config/business/view/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Estudio Fotográfico A",
  "slug": "tenant-a",
  "business_name": "Arte Ideas Diseño Gráfico A",
  "business_address": "Av. Lima 123, San Juan de Lurigancho",
  "business_phone": "987654321",
  "business_email": "info@tenant-a.com",
  "business_ruc": "20123456789",
  "currency": "PEN",
  "currency_display": "Soles (S/)",
  "location_type": "lima",
  "location_display": "Lima - Acceso Completo",
  "max_users": 20,
  "is_active": true
}
```

**Editar Configuración del Negocio:**
- **Método:** PUT
- **URL:** `{{base_url}}/api/core/config/business/edit/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "business_name": "Arte Ideas Diseño Gráfico A - Actualizado",
    "business_address": "Av. Lima 456, San Juan de Lurigancho, Lima",
    "business_phone": "987654322",
    "business_email": "contacto@tenant-a.com",
    "business_ruc": "20123456789",
    "currency": "PEN"
  }
  ```

**Respuesta Exitosa:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Estudio Fotográfico A",
  "slug": "tenant-a",
  "business_name": "Arte Ideas Diseño Gráfico A - Actualizado",
  "business_address": "Av. Lima 456, San Juan de Lurigancho, Lima",
  "business_phone": "987654322",
  "business_email": "contacto@tenant-a.com",
  "business_ruc": "20123456789",
  "currency": "PEN",
  "currency_display": "Soles (S/)",
  "location_type": "lima",
  "location_display": "Lima - Acceso Completo",
  "max_users": 20,
  "is_active": true
}
```

**Posibles Errores:**
```json
{
  "error": "Sin permisos para modificar configuración"
}
```
```json
{
  "business_email": [
    "Ingrese una dirección de correo válida."
  ]
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```
```json
{
  "error": "Usuario no pertenece a un tenant"
}
```
```json
{
  "business_name": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "business_phone": [
    "Ingrese un número de teléfono válido."
  ]
}
```
```json
{
  "business_ruc": [
    "El RUC debe tener 11 dígitos."
  ]
}
```
```json
{
  "business_ruc": [
    "Ya existe una empresa con este RUC."
  ]
}
```
```json
{
  "max_users": [
    "El número máximo de usuarios debe ser mayor a 0."
  ]
}
```
```json
{
  "currency": [
    "Seleccione una moneda válida."
  ]
}
```

#### Ejemplos de Gestión de Usuarios

**Lista de Usuarios del Tenant:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/config/users/list/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "username": "user_a",
    "email": "user@tenant-a.com",
    "first_name": "Usuario",
    "last_name": "Tenant A",
    "role": "employee",
    "role_display": "Empleado",
    "is_active": true,
    "status_display": "Activo",
    "phone": "987654323",
    "date_joined": "2025-10-31T22:01:05.123456Z"
  }
]
```

**Crear Nuevo Usuario:**
- **Método:** POST
- **URL:** `{{base_url}}/api/core/config/users/create/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "username": "fotografo_a",
    "email": "fotografo@tenant-a.com",
    "first_name": "Juan",
    "last_name": "Fotógrafo",
    "role": "photographer",
    "phone": "987654324",
    "password": "fotografo123",
    "confirm_password": "fotografo123"
  }
  ```

**Ejemplos Adicionales de Usuarios:**

**Ejemplo 2 - Manager:**
```json
{
  "username": "manager_a",
  "email": "manager@tenant-a.com",
  "first_name": "Gerente",
  "last_name": "Tenant A",
  "role": "manager",
  "phone": "987654325",
  "password": "manager123",
  "confirm_password": "manager123"
}
```

**Ejemplo 3 - Asistente:**
```json
{
  "username": "assistant_a",
  "email": "assistant@tenant-a.com",
  "first_name": "Asistente",
  "last_name": "Tenant A",
  "role": "assistant",
  "phone": "987654326",
  "password": "assistant123",
  "confirm_password": "assistant123"
}
```

**Respuesta Exitosa:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "username": "fotografo_a",
  "email": "fotografo@tenant-a.com",
  "first_name": "Juan",
  "last_name": "Fotógrafo",
  "role": "photographer",
  "role_display": "Fotógrafo",
  "is_active": true,
  "status_display": "Activo",
  "phone": "987654324",
  "date_joined": "2025-10-31T22:50:30.123456Z"
}
```

**Posibles Errores:**
```json
{
  "username": [
    "Ya existe un usuario con este nombre de usuario."
  ]
}
```
```json
{
  "email": [
    "Ya existe un usuario con este email."
  ]
}
```
```json
{
  "non_field_errors": [
    "Las contraseñas no coinciden."
  ]
}
```
```json
{
  "username": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "email": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "email": [
    "Ingrese una dirección de correo válida."
  ]
}
```
```json
{
  "first_name": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "last_name": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "role": [
    "Seleccione un rol válido."
  ]
}
```
```json
{
  "password": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "password": [
    "La contraseña debe tener al menos 8 caracteres."
  ]
}
```
```json
{
  "password": [
    "Esta contraseña es demasiado común."
  ]
}
```
```json
{
  "phone": [
    "Ingrese un número de teléfono válido."
  ]
}
```
```json
{
  "error": "Sin permisos para crear usuarios"
}
```
```json
{
  "error": "Usuario no pertenece a un tenant"
}
```
```json
{
  "error": "Se ha alcanzado el límite máximo de usuarios para este tenant"
}
```

**Ver Usuario Específico:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/config/users/3/view/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "username": "user_a",
  "email": "user@tenant-a.com",
  "first_name": "Usuario",
  "last_name": "Tenant A",
  "role": "employee",
  "role_display": "Empleado",
  "is_active": true,
  "status_display": "Activo",
  "phone": "987654323",
  "date_joined": "2025-10-31T22:01:05.123456Z"
}
```

**Editar Usuario:**
- **Método:** PUT
- **URL:** `{{base_url}}/api/core/config/users/3/edit/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "first_name": "Usuario",
    "last_name": "Actualizado",
    "email": "usuario.actualizado@tenant-a.com",
    "role": "manager",
    "phone": "999888777"
  }
  ```

**Respuesta Exitosa:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "username": "user_a",
  "email": "usuario.actualizado@tenant-a.com",
  "first_name": "Usuario",
  "last_name": "Actualizado",
  "role": "manager",
  "role_display": "Gerente",
  "is_active": true,
  "status_display": "Activo",
  "phone": "999888777",
  "date_joined": "2025-10-31T22:01:05.123456Z"
}
```

**Activar/Desactivar Usuario:**
- **Método:** PATCH
- **URL:** `{{base_url}}/api/core/config/users/3/toggle/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "message": "Usuario desactivado correctamente",
  "is_active": false
}
```

**Eliminar Usuario:**
- **Método:** DELETE
- **URL:** `{{base_url}}/api/core/config/users/3/delete/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "message": "Usuario user_a eliminado correctamente"
}
```

**Posibles Errores:**
```json
{
  "error": "No puedes eliminar tu propio usuario"
}
```
```json
{
  "error": "Usuario no encontrado"
}
```
```json
{
  "error": "Sin permisos para eliminar usuarios"
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```
```json
{
  "error": "Usuario no pertenece a un tenant"
}
```
```json
{
  "detail": "No se encontró el usuario especificado."
}
```

**Posibles Errores de Edición de Usuario:**
```json
{
  "email": [
    "Ya existe un usuario con este email."
  ]
}
```
```json
{
  "email": [
    "Ingrese una dirección de correo válida."
  ]
}
```
```json
{
  "role": [
    "Seleccione un rol válido."
  ]
}
```
```json
{
  "phone": [
    "Ingrese un número de teléfono válido."
  ]
}
```
```json
{
  "error": "Sin permisos para modificar usuarios"
}
```

**Posibles Errores de Activar/Desactivar Usuario:**
```json
{
  "error": "No puedes desactivar tu propio usuario"
}
```
```json
{
  "error": "Sin permisos para modificar usuarios"
}
```
```json
{
  "error": "Usuario no encontrado"
}
```

#### Ejemplos de Roles y Permisos

**Lista de Roles Disponibles:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/config/roles/list/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
[
  {
    "code": "admin",
    "name": "Administrador"
  },
  {
    "code": "manager",
    "name": "Gerente"
  },
  {
    "code": "employee",
    "name": "Empleado"
  },
  {
    "code": "photographer",
    "name": "Fotógrafo"
  },
  {
    "code": "assistant",
    "name": "Asistente"
  }
]
```

**Ver Permisos de un Rol:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/config/permissions/admin/view/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "role": "admin",
  "role_display": "Administrador",
  "modules_count": 10,
  "sensitive_actions_count": 7,
  "access_dashboard": true,
  "access_agenda": true,
  "access_pedidos": true,
  "access_clientes": true,
  "access_inventario": true,
  "access_activos": true,
  "access_gastos": true,
  "access_produccion": true,
  "access_contratos": true,
  "access_reportes": true,
  "view_costos": true,
  "view_precios": true,
  "view_margenes": true,
  "view_datos_clientes": true,
  "view_datos_financieros": true,
  "edit_precios": true,
  "delete_registros": true
}
```

**Editar Permisos de un Rol:**
- **Método:** PUT
- **URL:** `{{base_url}}/api/core/config/permissions/employee/edit/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "access_dashboard": true,
    "access_agenda": false,
    "access_pedidos": true,
    "access_clientes": true,
    "access_inventario": true,
    "access_activos": false,
    "access_gastos": false,
    "access_produccion": true,
    "access_contratos": false,
    "access_reportes": false,
    "view_costos": false,
    "view_precios": false,
    "view_margenes": false,
    "view_datos_clientes": true,
    "view_datos_financieros": false,
    "edit_precios": false,
    "delete_registros": false
  }
  ```

**Respuesta Exitosa:**
```json
{
  "role": "employee",
  "role_display": "Empleado",
  "modules_count": 5,
  "sensitive_actions_count": 1,
  "access_dashboard": true,
  "access_agenda": false,
  "access_pedidos": true,
  "access_clientes": true,
  "access_inventario": true,
  "access_activos": false,
  "access_gastos": false,
  "access_produccion": true,
  "access_contratos": false,
  "access_reportes": false,
  "view_costos": false,
  "view_precios": false,
  "view_margenes": false,
  "view_datos_clientes": true,
  "view_datos_financieros": false,
  "edit_precios": false,
  "delete_registros": false
}
```

**Posibles Errores de Edición de Permisos:**
```json
{
  "error": "Sin permisos para modificar permisos"
}
```
```json
{
  "error": "Permisos no encontrados"
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```
```json
{
  "error": "Usuario no pertenece a un tenant"
}
```
```json
{
  "error": "Rol no válido"
}
```
```json
{
  "access_dashboard": [
    "Este campo debe ser verdadero o falso."
  ]
}
```

**Restablecer Permisos por Defecto:**
- **Método:** POST
- **URL:** `{{base_url}}/api/core/config/permissions/employee/reset/`
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```

**Respuesta Exitosa:**
```json
{
  "role": "employee",
  "role_display": "Empleado",
  "modules_count": 3,
  "sensitive_actions_count": 0,
  "access_dashboard": true,
  "access_agenda": false,
  "access_pedidos": true,
  "access_clientes": true,
  "access_inventario": true,
  "access_activos": false,
  "access_gastos": false,
  "access_produccion": true,
  "access_contratos": false,
  "access_reportes": false,
  "view_costos": false,
  "view_precios": false,
  "view_margenes": false,
  "view_datos_clientes": false,
  "view_datos_financieros": false,
  "edit_precios": false,
  "delete_registros": false
}
```

#### Ejemplos de Super Admin - Gestión de Tenants

**Lista de Todos los Tenants (Solo Super Admin):**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/config/tenants/list/`
- **Headers:**
  ```
  Authorization: Bearer <superadmin_access_token>
  ```

**Respuesta Exitosa:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Estudio Fotográfico A",
    "slug": "tenant-a",
    "business_name": "Arte Ideas Diseño Gráfico A",
    "business_email": "info@tenant-a.com",
    "location_type": "lima",
    "currency": "PEN",
    "max_users": 20,
    "users_count": 2,
    "is_active": true,
    "created_at": "2025-10-31T22:01:05.123456Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "name": "Estudio Fotográfico B",
    "slug": "tenant-b",
    "business_name": "Arte Ideas Diseño Gráfico B",
    "business_email": "info@tenant-b.com",
    "location_type": "provincia",
    "currency": "PEN",
    "max_users": 10,
    "users_count": 2,
    "is_active": true,
    "created_at": "2025-10-31T22:01:05.123456Z"
  }
]
```

**Crear Nuevo Tenant (Solo Super Admin):**
- **Método:** POST
- **URL:** `{{base_url}}/api/core/config/tenants/create/`
- **Headers:**
  ```
  Authorization: Bearer <superadmin_access_token>
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "name": "Estudio Fotográfico C",
    "business_name": "Arte Ideas Diseño Gráfico C",
    "business_address": "Av. Arequipa 789, Arequipa",
    "business_phone": "987654326",
    "business_email": "info@tenant-c.com",
    "business_ruc": "20555666777",
    "currency": "PEN",
    "location_type": "provincia",
    "max_users": 15
  }
  ```

**Respuesta Exitosa:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "name": "Estudio Fotográfico C",
  "slug": "tenant-c",
  "business_name": "Arte Ideas Diseño Gráfico C",
  "business_email": "info@tenant-c.com",
  "location_type": "provincia",
  "currency": "PEN",
  "max_users": 15,
  "users_count": 0,
  "is_active": true,
  "created_at": "2025-10-31T23:00:00.123456Z"
}
```

**Posibles Errores de Creación de Tenant:**
```json
{
  "error": "Solo super admin puede crear tenants"
}
```
```json
{
  "name": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "business_name": [
    "Este campo es requerido."
  ]
}
```
```json
{
  "business_email": [
    "Ingrese una dirección de correo válida."
  ]
}
```
```json
{
  "business_email": [
    "Ya existe un tenant con este email."
  ]
}
```
```json
{
  "business_ruc": [
    "El RUC debe tener 11 dígitos."
  ]
}
```
```json
{
  "business_ruc": [
    "Ya existe un tenant con este RUC."
  ]
}
```
```json
{
  "max_users": [
    "El número máximo de usuarios debe ser mayor a 0."
  ]
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```

**Posibles Errores de Lista de Tenants:**
```json
{
  "error": "Solo super admin puede ver tenants"
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```

**Posibles Errores de Usuarios de Tenant:**
```json
{
  "error": "Solo super admin puede ver usuarios de tenants"
}
```
```json
{
  "error": "Tenant no encontrado"
}
```
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```

**Usuarios de un Tenant Específico (Solo Super Admin):**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/config/tenants/1/users/`
- **Headers:**
  ```
  Authorization: Bearer <superadmin_access_token>
  ```

**Respuesta Exitosa:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin_a",
    "email": "admin@tenant-a.com",
    "first_name": "Administrador",
    "last_name": "Tenant A",
    "role": "admin",
    "role_display": "Administrador",
    "is_active": true,
    "status_display": "Activo",
    "phone": "987654321",
    "date_joined": "2025-10-31T22:01:05.123456Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "username": "user_a",
    "email": "user@tenant-a.com",
    "first_name": "Usuario",
    "last_name": "Tenant A",
    "role": "employee",
    "role_display": "Empleado",
    "is_active": true,
    "status_display": "Activo",
    "phone": "987654323",
    "date_joined": "2025-10-31T22:01:05.123456Z"
  }
]
```

---

## 🏥 Módulo 4: Health Check (`/api/core/health/`)

### Sistema
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| **GET** | `/api/core/health/` | Health check del sistema | No requerida |

**Health Check del Sistema:**
- **Método:** GET
- **URL:** `{{base_url}}/api/core/health/`

**Respuesta Exitosa:**
```json
{
  "status": "ok",
  "message": "Arte Ideas Core App funcionando correctamente",
  "modules": {
    "profile": "Mi Perfil - Gestión personal del usuario",
    "configuration": "Configuración - Gestión de usuarios, negocio y permisos"
  }
}
```

---

## 🔐 Autenticación

### Credenciales de Prueba

**Super Admin (Acceso a todos los tenants):**
```
Username: superadmin
Password: admin123
```

**Admin Tenant A:**
```
Username: admin_a
Password: admin123
```

**Usuario Tenant A:**
```
Username: user_a
Password: user123
```

**Admin Tenant B:**
```
Username: admin_b
Password: admin123
```

**Usuario Tenant B:**
```
Username: user_b
Password: user123
```

### Métodos de Autenticación

1. **JWT Bearer Token** (Recomendado)
   - En Postman: Authorization tab → Bearer Token
   - Token: `<access_token_from_login>`

2. **Django Admin** (Para navegador)
   - Login en: `http://localhost:8000/admin/`

### Configuración en Postman

1. **Hacer Login** primero en `/api/core/auth/login/`
2. **Copiar access token** de la respuesta
3. **Authorization tab** → **Bearer Token**
4. **Token:** `<access_token>`

---

## 📊 Ejemplos de Respuestas

### Respuesta de Perfil Completo
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "admin_a",
  "email": "admin@tenant-a.com",
  "first_name": "Administrador",
  "last_name": "Tenant A",
  "full_name": "Administrador Tenant A",
  "phone": "987654321",
  "address": "Lima, Perú",
  "bio": "",
  "avatar": null,
  "role": "admin",
  "role_display": "Administrador",
  "tenant_name": "Estudio Fotográfico A",
  "email_verified": true,
  "is_active": true,
  "date_joined": "2025-10-31T22:01:05.123456Z",
  "last_login": "2025-10-31T22:30:15.654321Z",
  "profile": {
    "language": "es",
    "theme": "light",
    "email_notifications": true,
    "completion_percentage": 67
  }
}
```

### Error de Autenticación
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Error de Permisos
```json
{
  "error": "Sin permisos para modificar configuración"
}
```

### Error de Validación
```json
{
  "email": [
    "Ingrese una dirección de correo válida."
  ],
  "password": [
    "Este campo es requerido."
  ]
}
```

---

## 🔍 Filtros y Multi-Tenancy

### Aislamiento por Tenant
- Todos los endpoints filtran automáticamente por tenant del usuario autenticado
- Solo el super admin puede ver datos de múltiples tenants
- Los usuarios solo ven datos de su propio tenant

### Roles y Permisos
- **Super Admin**: Acceso completo a todos los tenants
- **Admin**: Gestión completa dentro de su tenant
- **Manager**: Acceso limitado según configuración de permisos
- **Employee/Photographer/Assistant**: Acceso básico según rol

### Ejemplos de Restricciones
```
Admin Tenant A → Solo ve usuarios de Tenant A
User Tenant B → Solo ve su propio perfil
Super Admin → Ve todos los tenants y usuarios
```

---

## 📝 Notas Importantes

1. **Multi-Tenancy**: Aislamiento automático de datos por tenant
2. **Autenticación JWT**: Tokens con expiración y refresh automático
3. **Permisos Granulares**: Control de acceso por rol y acción
4. **Validaciones**: Validaciones robustas en todos los endpoints
5. **Actividad**: Registro automático de todas las acciones
6. **UUIDs**: Uso de UUIDs para mayor seguridad
7. **Soft Delete**: Eliminación lógica para preservar datos

---

## 🚀 Uso en Desarrollo

### Iniciar Servidor
```bash
# Activar entorno virtual
venv\Scripts\Activate.ps1

# Iniciar servidor
python manage.py runserver
```

### Configuración en Postman
1. **Importar colección**: `Arte_Ideas_Core_API.postman_collection.json`
2. **Variables de entorno**:
   - `base_url`: `http://localhost:8000`
3. **Autenticación**: Configurar Bearer Token después del login

### Documentación Interactiva
- **Django Admin**: `http://localhost:8000/admin/`
- **Health Check**: `http://localhost:8000/api/core/health/`

### Herramientas Recomendadas
- **Postman**: Para pruebas de API
- **Django Admin**: Para gestión de datos
- **MySQL Workbench**: Para gestión de base de datos

---

## 🎯 Resumen de Endpoints

### Autenticación (3 endpoints)
- Login, refresh token y logout

### Mi Perfil (7 endpoints)
- Ver perfil, editar, estadísticas, actividad, completitud, cambiar contraseña/email

### Configuración del Negocio (2 endpoints)
- Ver y editar configuración del negocio

### Gestión de Usuarios (6 endpoints)
- CRUD completo de usuarios del tenant

### Roles y Permisos (4 endpoints)
- Gestión de roles y permisos granulares

### Super Admin (3 endpoints)
- Gestión de tenants (solo super admin)

### Health Check (1 endpoint)
- Verificación del estado del sistema

**Total: 26 endpoints documentados** ✅

---

## 📝 Notas Importantes sobre IDs

### **Uso de IDs Simples:**
- Reemplaza `{id}` con el número real del ID
- **Ejemplo correcto:** Para ver el usuario con ID 3, usa: `/api/core/config/users/3/view/`
- **Ejemplo correcto:** Para ver el tenant con ID 1, usa: `/api/core/config/tenants/1/users/`
- **❌ NO uses** `/api/core/config/users/{id}/view/` literalmente

### **IDs Disponibles en el Sistema:**
**Usuarios:**
- ID: 1 - superadmin (Super Admin Global)
- ID: 2 - admin_a (Admin Tenant 1)
- ID: 3 - user_a (Usuario Tenant 1)
- ID: 4 - admin_b (Admin Tenant 2)
- ID: 5 - user_b (Usuario Tenant 2)
- ID: 6 - fotografo_a (Fotógrafo Tenant 1)

**Tenants:**
- ID: 1 - Estudio Fotográfico A
- ID: 2 - Estudio Fotográfico B

### **Códigos de Respuesta HTTP:**
- **200** - OK (Operación exitosa)
- **201** - Created (Recurso creado exitosamente)
- **204** - No Content (Eliminación exitosa)
- **400** - Bad Request (Error de validación)
- **401** - Unauthorized (No autenticado)
- **403** - Forbidden (Sin permisos)
- **404** - Not Found (Recurso no encontrado)
- **409** - Conflict (Conflicto de datos únicos)
- **500** - Internal Server Error (Error del servidor)

---

## 🔍 Filtros y Búsquedas Avanzadas

### **Filtros Comunes:**
- `is_active=true/false` - Filtrar por estado activo
- `role=admin` - Filtrar por rol específico
- `search=texto` - Búsqueda por texto en múltiples campos
- `ordering=field` - Ordenar por campo específico

### **Ejemplos de Filtros:**
```
GET /api/core/config/users/list/?is_active=true
GET /api/core/config/users/list/?role=photographer
GET /api/core/config/users/list/?search=juan
GET /api/core/config/users/list/?ordering=-date_joined
```

### **Combinación de Filtros:**
```
GET /api/core/config/users/list/?is_active=true&role=admin&search=admin
```

---

## 🛡️ Seguridad y Mejores Prácticas

### **Autenticación:**
- Siempre incluir el token Bearer en headers
- Los tokens expiran en 8 horas
- Usar refresh token para renovar automáticamente
- Cerrar sesión al finalizar para invalidar tokens

### **Permisos:**
- Verificar permisos antes de cada operación
- Los usuarios solo ven datos de su tenant
- Super admin tiene acceso completo
- Roles granulares para control de acceso

### **Validaciones:**
- Todos los campos requeridos deben enviarse
- Validar formato de emails y teléfonos
- Contraseñas deben cumplir políticas de seguridad
- RUC debe tener formato válido (11 dígitos)

### **Multi-Tenancy:**
- Aislamiento automático de datos por tenant
- Usuarios no pueden ver datos de otros tenants
- Configuraciones independientes por tenant
- Límites de usuarios por tenant

---

## 🚨 Errores Comunes y Soluciones

### **Error 401 - No Autenticado:**
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```
**Solución:** Incluir header `Authorization: Bearer <token>`

### **Error 403 - Sin Permisos:**
```json
{
  "error": "Sin permisos para modificar usuarios"
}
```
**Solución:** Verificar que el usuario tenga el rol adecuado

### **Error 400 - Validación:**
```json
{
  "email": [
    "Ya existe un usuario con este email."
  ]
}
```
**Solución:** Corregir los datos según el mensaje de error

### **Error 404 - No Encontrado:**
```json
{
  "error": "Usuario no encontrado"
}
```
**Solución:** Verificar que el ID existe y pertenece al tenant

---

## 📱 Configuración Postman Actualizada

### **Variables de Entorno:**
```json
{
  "base_url": "http://localhost:8000",
  "user_id": "3",
  "tenant_id": "1",
  "access_token": "{{access_token_from_login}}"
}
```

### **Headers Globales:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

### **Scripts de Prueba:**
```javascript
// Guardar token automáticamente después del login
if (pm.response.code === 200) {
    const response = pm.response.json();
    if (response.access) {
        pm.environment.set("access_token", response.access);
    }
}
```

---

## 🎯 Ejemplos de Flujos Completos

### **Flujo 1: Crear Usuario Completo**
```
1. POST /api/core/auth/login/ (Obtener token de admin)
2. POST /api/core/config/users/create/ (Crear usuario)
3. GET /api/core/config/users/list/ (Verificar creación)
4. PUT /api/core/config/users/{id}/edit/ (Actualizar datos)
5. PATCH /api/core/config/users/{id}/toggle/ (Activar/Desactivar)
```

### **Flujo 2: Gestión de Permisos**
```
1. POST /api/core/auth/login/ (Login como admin)
2. GET /api/core/config/roles/list/ (Ver roles disponibles)
3. GET /api/core/config/permissions/{role}/view/ (Ver permisos actuales)
4. PUT /api/core/config/permissions/{role}/edit/ (Modificar permisos)
5. POST /api/core/config/permissions/{role}/reset/ (Restablecer si es necesario)
```

### **Flujo 3: Configuración de Negocio**
```
1. POST /api/core/auth/login/ (Login como admin)
2. GET /api/core/config/business/view/ (Ver configuración actual)
3. PUT /api/core/config/business/edit/ (Actualizar configuración)
4. GET /api/core/profile/view/ (Verificar cambios en perfil)
```

---

## 📋 Checklist de Testing

### **Autenticación:**
- [ ] Login con credenciales válidas
- [ ] Login con credenciales inválidas
- [ ] Refresh token válido
- [ ] Refresh token expirado
- [ ] Logout exitoso
- [ ] Acceso sin token

### **Gestión de Usuarios:**
- [ ] Crear usuario con datos válidos
- [ ] Crear usuario con email duplicado
- [ ] Crear usuario con username duplicado
- [ ] Editar usuario propio
- [ ] Editar usuario de otro tenant (debe fallar)
- [ ] Eliminar usuario propio (debe fallar)
- [ ] Activar/Desactivar usuario

### **Permisos y Roles:**
- [ ] Ver permisos como admin
- [ ] Ver permisos como usuario (debe fallar)
- [ ] Modificar permisos como admin
- [ ] Modificar permisos como usuario (debe fallar)
- [ ] Restablecer permisos por defecto

### **Multi-Tenancy:**
- [ ] Usuario Tenant A no ve datos de Tenant B
- [ ] Super admin ve todos los tenants
- [ ] Admin solo ve su tenant
- [ ] Filtrado automático por tenant

---

## 🔧 Troubleshooting

### **Problema: Token Expirado**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```
**Solución:** Usar refresh token o hacer login nuevamente

### **Problema: Usuario Inactivo**
```json
{
  "non_field_errors": [
    "Usuario inactivo. Contacte al administrador."
  ]
}
```
**Solución:** Activar usuario desde panel de administración

### **Problema: Límite de Usuarios**
```json
{
  "error": "Se ha alcanzado el límite máximo de usuarios para este tenant"
}
```
**Solución:** Aumentar max_users en configuración del tenant

### **Problema: Permisos Insuficientes**
```json
{
  "error": "Sin permisos para modificar usuarios"
}
```
**Solución:** Verificar rol del usuario y permisos asignados