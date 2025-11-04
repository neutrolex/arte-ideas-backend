# CONFIGURACION
## 🧾 **HU01 – Creación y Gestión de Usuarios**

**Etiquetas:**  
⚙️ CONFIGURACIÓN (gris)  
👥 USUARIOS (celeste)  
🟡 PRIORIDAD ALTA (amarillo)

**Descripción:**  
Como **administrador del sistema**, quiero **crear, editar y eliminar usuarios**, para mantener actualizado el acceso del personal y asegurar que cada uno tenga el rol correcto dentro del sistema.

**Criterios de Aceptación:**

- El sistema debe permitir registrar un nuevo usuario con **Nombre Completo, Email y Rol**.
    
- Al crear una cuenta, se asignará automáticamente una **contraseña predeterminada (“12345678”)**.
    
- En el **primer inicio de sesión**, el usuario deberá **cambiar su contraseña obligatoriamente**.
    
- La tabla de usuarios debe mostrar **Nombre, Email, Rol, Estado y Acciones**.
    
- Debe ser posible **editar o eliminar** usuarios desde las acciones de la tabla.
    
- No se deben permitir usuarios con **emails duplicados**.
    

**Checklist de Tareas:**  
☑ Crear formulario de registro de usuario.  
☑ Implementar asignación automática de contraseña inicial.  
☑ Forzar cambio de contraseña al primer acceso.  
☑ Diseñar tabla con datos de usuarios y sus acciones CRUD.  
☑ Validar unicidad del correo electrónico.  
☑ Conectar las acciones de edición y eliminación con el listado.

**Campos del Formulario:**

- Nombre Completo
    
- Email
    
- Rol (Administrador / Ventas / Producción / Operario)
    

**Botones de Acción:**

- Guardar Usuario
    
- Cancelar
    
- Editar (en tabla)
    
- Eliminar (en tabla)
    

---

## 🧾 **HU02 – Configuración del Negocio**

**Etiquetas:**  
🏢 NEGOCIO (naranja)  
⚙️ CONFIGURACIÓN (gris)  
🟢 PRIORIDAD MEDIA (verde)

**Descripción:**  
Como **administrador**, quiero **actualizar los datos generales de la empresa**, para que la información utilizada en reportes y documentos esté siempre actualizada.

**Criterios de Aceptación:**

- Debe mostrarse un formulario con los datos básicos del negocio.
    
- Todos los cambios deben guardarse con un **botón único de “Actualizar”**.
    
- El sistema debe validar que **los campos obligatorios no estén vacíos**.
    
- Los datos actualizados deben reflejarse de inmediato en las secciones del sistema que los usen (ej. reportes, encabezados).
    

**Checklist de Tareas:**  
☑ Crear formulario de datos corporativos.  
☑ Implementar validaciones básicas (campos requeridos, formato de email, longitud del teléfono, etc.).  
☑ Añadir acción para guardar todos los cambios.  
☑ Mostrar mensaje de confirmación al actualizar correctamente.

**Campos del Formulario:**

- Nombre de Empresa
    
- Dirección
    
- Teléfono
    
- Email Corporativo
    
- RUC
    
- Tipo de Moneda (Soles / Dólar / Euro)
    

**Botones de Acción:**

- Actualizar
    
- Cancelar
    

---

## 🧾 **HU03 – Administración de Roles y Permisos**

**Etiquetas:**  
🔐 SEGURIDAD (rojo)  
👤 ROLES (morado)  
🟡 PRIORIDAD ALTA (amarillo)

**Descripción:**  
Como **administrador**, quiero **definir los permisos de acceso por cada rol**, para controlar qué módulos y acciones pueden realizar los usuarios según su función.

**Criterios de Aceptación:**

- Debe mostrarse la lista de **roles disponibles** (Administrador, Ventas, Producción, Operario).
    
- Al seleccionar un rol, se deben visualizar sus **módulos habilitados y acciones sensibles**.
    
- El administrador podrá **activar o desactivar permisos** por módulo y acción.
    
- Debe existir la opción de **guardar los cambios** y **restablecer los permisos por defecto**.
    
- Los cambios deben aplicarse de inmediato al sistema.
    

**Checklist de Tareas:**  
☑ Crear vista para gestión de roles y permisos.  
☑ Implementar selección de rol y carga de permisos asociados.  
☑ Habilitar opciones de activar/desactivar permisos.  
☑ Desarrollar botones de guardar y restablecer.  
☑ Validar que los cambios se guarden correctamente.

**Campos del Formulario:**

- Rol (Administrador / Ventas / Producción / Operario)
    
- Lista de módulos (Dashboard, Agenda, Pedidos, Clientes, Inventario, Activos, Gastos, Producción, Contratos, Reportes)
    
- Lista de acciones sensibles (Eliminar Pedido, Modificar Costo, etc.)
    

**Botones de Acción:**

- Guardar Permisos
    
- Restablecer por Defecto
# MI PERFIL
## 🧾 **HU01 – Visualización de Perfil y Rendimiento**

**Etiquetas:**  
👤 PERFIL (celeste)  
📊 ESTADÍSTICAS (verde)  
🟢 PRIORIDAD MEDIA (verde claro)

**Descripción:**  
Como **usuario del sistema**, quiero **ver mis datos personales, estado de cuenta y métricas de rendimiento**, para tener una visión clara de mi información y desempeño dentro del sistema.

**Criterios de Aceptación:**

- El sistema debe mostrar los **datos personales**: Nombre, Email, Teléfono, Rol, Dirección y Biografía.
    
- Debe visualizarse el **estado de cuenta** con indicador de verificación y fechas de registro y última conexión.
    
- Se deben mostrar las **estadísticas mensuales** con indicadores como: Pedidos Procesados, Clientes Atendidos, Sesiones Realizadas y Horas Trabajadas.
    
- La sección de **actividad reciente** debe listar cronológicamente las acciones del usuario con fecha y hora.
    
- La información debe ser visible solo para el usuario autenticado.
    

**Checklist de Tareas:**  
☑ Crear vista de perfil con secciones organizadas.  
☑ Mostrar los datos personales y estado de cuenta.  
☑ Calcular y visualizar las métricas mensuales.  
☑ Mostrar lista de actividad reciente.  
☑ Proteger la información para que solo el usuario la vea.

**Campos de la Vista:**

- Nombre
    
- Email
    
- Teléfono
    
- Rol
    
- Dirección
    
- Biografía
    
- Fecha de Registro
    
- Última Conexión
    
- Estado de Verificación
    
- Indicadores de rendimiento (Pedidos, Clientes, Sesiones, Horas)
    

**Botones de Acción:**

- Editar Perfil
    
- Cambiar Email
    
- Cambiar Contraseña
    

---

## 🧾 **HU02 – Autogestión de Seguridad y Datos Personales**

**Etiquetas:**  
🔒 SEGURIDAD (rojo)  
👤 PERFIL (celeste)  
🟡 PRIORIDAD ALTA (amarillo)

**Descripción:**  
Como **usuario del sistema**, quiero **actualizar mis datos personales y credenciales de acceso**, para mantener mi información segura y actualizada sin depender del administrador.

**Criterios de Aceptación:**

- Debe permitirse **editar** los datos personales: Nombre, Teléfono, Dirección y Biografía.
    
- Para **cambiar el email**, se debe solicitar la **contraseña actual** y confirmación del nuevo email.
    
- Para **cambiar la contraseña**, se debe ingresar la **contraseña actual**, la **nueva contraseña** y su **confirmación**.
    
- El sistema debe validar que las contraseñas coincidan y cumplan con los requisitos mínimos de seguridad.
    
- Se debe mostrar un **mensaje de confirmación** cuando los cambios se realicen con éxito.
    

**Checklist de Tareas:**  
☑ Implementar formulario editable de perfil.  
☑ Agregar validaciones de identidad antes de cambios sensibles.  
☑ Crear formularios separados para cambio de email y contraseña.  
☑ Mostrar confirmaciones o alertas según el resultado.  
☑ Actualizar la información en tiempo real en el perfil del usuario.

**Campos del Formulario:**  
**Editar Perfil:**

- Nombre
    
- Teléfono
    
- Dirección
    
- Biografía
    

**Cambiar Email:**

- Contraseña Actual
    
- Nuevo Email
    
- Confirmar Nuevo Email
    

**Cambiar Contraseña:**

- Contraseña Actual
    
- Nueva Contraseña
    
- Confirmar Nueva Contraseña
    

**Botones de Acción:**

- Guardar Cambios
    
- Cambiar Email
    
- Cambiar Contraseña
    
- Cancelar
# REPORTES
## 🧾 **HU01 – Generación y Visualización de Reportes**

**Etiquetas:**  
📈 REPORTES (azul oscuro)  
👁️ VISUALIZACIÓN (verde)  
🟡 PRIORIDAD ALTA (amarillo)

**Descripción:**  
Como **usuario del sistema**, quiero **visualizar los reportes por área (Ventas, Inventario, Producción, Clientes, Financiero y Contratos)**, para analizar los resultados y métricas del negocio en un solo módulo centralizado.

**Criterios de Aceptación:**

- El sistema debe mostrar los **reportes clasificados por categoría** (Ventas, Inventario, Producción, Clientes, Financiero, Contratos).
    
- Cada reporte debe incluir **tarjetas de resumen (métricas)** y **tablas de detalle** con los datos correspondientes.
    
- Las métricas deben actualizarse automáticamente al aplicar filtros de tiempo.
    
- Las tablas deben permitir **ordenar y consultar la información detallada**.
    
- La interfaz debe ser **visual, clara y sin necesidad de conocimientos técnicos**.
    

**Checklist de Tareas:**  
☑ Crear vista principal del módulo de reportes.  
☑ Cargar dinámicamente las métricas y tablas por categoría.  
☑ Implementar conexión con los módulos de origen (Ventas, Producción, Inventario, etc.).  
☑ Validar que las métricas se actualicen según el periodo seleccionado.  
☑ Mostrar totales, promedios y porcentajes correctamente formateados.

**Campos de la Vista:**

- Categoría de Reporte (Ventas / Inventario / Producción / Clientes / Financiero / Contratos)
    
- Métricas de resumen (tarjetas)
    
- Tablas de detalle
    
- Periodo seleccionado
    

**Botones de Acción:**

- Filtrar
    
- Exportar
    
- Actualizar
    

---

## 🧾 **HU02 – Filtrado y Análisis por Periodo de Tiempo**

**Etiquetas:**  
⏱️ FILTROS (celeste)  
📅 FECHAS (verde claro)  
🟢 PRIORIDAD MEDIA (verde)

**Descripción:**  
Como **usuario del sistema**, quiero **filtrar los reportes por periodos de tiempo definidos o personalizados**, para analizar la información de acuerdo con mis necesidades de evaluación temporal.

**Criterios de Aceptación:**

- Debe existir un **filtro por fecha personalizada (inicio y fin)**.
    
- Se deben incluir **opciones predeterminadas**: Hoy, Esta Semana, Este Mes, Este Trimestre y Este Año.
    
- Al aplicar un filtro, los **datos de las métricas y tablas deben actualizarse automáticamente**.
    
- Debe mostrarse visualmente el rango seleccionado.
    
- El filtro debe mantenerse activo mientras el usuario permanezca en el módulo.
    

**Checklist de Tareas:**  
☑ Implementar selector de rango de fechas.  
☑ Añadir opciones rápidas de filtro temporal.  
☑ Conectar el filtro con los datos de reportes.  
☑ Validar que el cambio de periodo refresque la información.  
☑ Mostrar mensaje o animación de carga durante la actualización.

**Campos del Formulario:**

- Fecha de Inicio
    
- Fecha de Fin
    
- Selección rápida: Hoy / Semana / Mes / Trimestre / Año
    

**Botones de Acción:**

- Aplicar Filtro
    
- Restablecer
    

---

## 🧾 **HU03 – Exportación de Reportes**

**Etiquetas:**  
📤 EXPORTACIÓN (naranja)  
🧾 DOCUMENTOS (gris)  
🟣 PRIORIDAD ALTA (morado)

**Descripción:**  
Como **usuario del sistema**, quiero **exportar los datos de los reportes en formatos Excel o PDF**, para poder compartir o guardar la información de forma externa.

**Criterios de Aceptación:**

- El sistema debe permitir exportar el **reporte visible** (según los filtros activos).
    
- Se deben ofrecer las opciones de **Excel (.xlsx)** y **PDF (.pdf)**.
    
- La exportación debe incluir los **nombres de columnas, títulos y totales visibles**.
    
- El archivo generado debe tener un **nombre identificable** (ej. “Reporte_Ventas_Octubre_2025”).
    
- Se requiere definir si se exportará **solo lo visible** o **todas las categorías del módulo** (pendiente de alcance).
    

**Checklist de Tareas:**  
☑ Implementar botones de exportación (Excel y PDF).  
☑ Incluir encabezado, fecha y nombre del reporte en los archivos.  
☑ Validar compatibilidad del formato y estructura del contenido.  
☑ Probar exportaciones con distintos filtros activos.  
☑ Añadir confirmación o mensaje al completar la descarga.

**Campos del Formulario:**

- Tipo de archivo (Excel / PDF)
    
- Rango de datos (Visible / Completo)
    

**Botones de Acción:**

- Exportar a Excel
    
- Exportar a PDF
# CONTRATOS
## 🧾 **HU01 – Registro y Gestión de Contratos**

**Etiquetas:**  
📄 CONTRATOS (azul oscuro)  
🧮 ADMINISTRACIÓN (gris)  
🟡 PRIORIDAD ALTA (amarillo)

**Descripción:**  
Como **usuario administrador o responsable de contratos**, quiero **registrar, visualizar, editar y eliminar contratos** con toda la información relevante (cliente, servicio, fechas, valores y estado), para mantener un control completo sobre los acuerdos establecidos con los clientes.

**Criterios de Aceptación:**

- El formulario debe permitir registrar todos los campos definidos en los atributos del contrato.
    
- El campo **Estado** debe estar disponible al crear o editar el contrato, con las opciones definidas en el flujo de vida.
    
- Se debe calcular automáticamente el **Saldo** como `Valor Total - Monto Pagado`.
    
- La vista principal debe mostrar una **tabla con los contratos registrados** y sus principales datos (Cliente, Servicio, Tipo, Estado, Valor Total, Progreso de Pago).
    
- El usuario podrá **editar o eliminar** contratos mediante las acciones en la columna “Acciones”.
    
- Se debe solicitar confirmación antes de eliminar un contrato.
    

**Checklist de Tareas:**

-  Crear formulario de registro con validaciones básicas.
    
-  Incluir campo **Estado** con lista desplegable (Borrador, Activo, etc.).
    
-  Calcular automáticamente el **Saldo**.
    
-  Implementar CRUD completo (Crear, Leer, Editar, Eliminar).
    
-  Mostrar tabla de contratos con búsqueda general.
    
-  Agregar confirmación al eliminar.
    
-  Incluir botón **“Reset de Datos”** (limpieza total, con confirmación).
    

**Campos del Formulario:**

- Cliente
    
- Servicio
    
- Tipo de Contrato _(Anual, Semestral, Mensual, Por Proyecto)_
    
- Responsable
    
- Fecha de Inicio
    
- Fecha de Fin
    
- Valor Total
    
- Monto Pagado
    
- Saldo _(automático)_
    
- Nro. de Estudiantes _(opcional)_
    
- Observaciones
    
- Cláusulas
    
- Estado _(Borrador, Firmado, Activo, En Ejecución, Finalizado, Entregado, Pagado, Cerrado, Pendiente, Completado, Vencido)_
    

**Botones de Acción:**

- Guardar
    
- Editar
    
- Eliminar
    
- Reset de Datos
    
- Descargar PDF
    

---

## 🧾 **HU02 – Monitoreo y Control del Estado de Contratos**

**Etiquetas:**  
📊 MONITOREO (verde)  
🔁 ESTADOS (celeste)  
🟠 PRIORIDAD MEDIA (naranja)

**Descripción:**  
Como **usuario del sistema**, quiero **visualizar el estado actual de los contratos y sus métricas financieras**, para identificar rápidamente los contratos activos, vencidos o completados y tomar decisiones oportunas.

**Criterios de Aceptación:**

- Debe mostrarse un resumen con las tarjetas: **Total Contratos**, **Activos**, **Valor Total** y **Total Pagado**.
    
- Los estados deben tener etiquetas o colores diferenciados para facilitar la lectura visual.
    
- El sistema debe calcular automáticamente el **progreso de pago** de cada contrato:  
    `Progreso = (Monto Pagado / Valor Total) * 100`.
    
- El campo **Estado** debe poder actualizarse mediante una acción controlada (“Cambiar a Activo”, “Marcar como Pagado”, etc.) respetando el flujo de transición.
    
- Se debe permitir filtrar los contratos por Estado, Tipo o Cliente.
    
- Los estados “Vencido” y “Completado” deben poder actualizarse automáticamente según las condiciones (fecha fin y 100% pago, respectivamente).
    

**Checklist de Tareas:**

-  Mostrar tarjetas con métricas de resumen.
    
-  Aplicar colores o etiquetas visuales por estado.
    
-  Calcular y mostrar el progreso de pago (%).
    
-  Habilitar cambio guiado de estado.
    
-  Agregar filtros por Estado, Tipo y Cliente.
    
-  Implementar actualización automática de estados especiales.
    

**Campos del Formulario (solo si aplica a edición):**

- Estado
    
- Monto Pagado _(para recalcular progreso)_
    
- Valor Total _(para referencia del cálculo)_
    

**Botones de Acción:**

- Filtrar
    
- Cambiar Estado
    
- Actualizar
    
- Ver Detalle
    
- Descargar Reporte
# PRODUCCION
## 🧾 **HU01 – Registro y Gestión de Órdenes de Producción**

**Etiquetas:**  
⚙️ PRODUCCIÓN (azul oscuro)  
📋 GESTIÓN (gris)  
🟡 PRIORIDAD ALTA (amarillo)

**Descripción:**  
Como **usuario del área de Producción o Administrador**, quiero **crear, editar y administrar Órdenes de Producción (OP)** con toda la información necesaria, para controlar los trabajos en curso y asignar responsables según su prioridad y tipo de servicio.

**Criterios de Aceptación:**

- El formulario debe permitir registrar todos los atributos de la OP (N° OP, Pedido, Cliente, Descripción, Tipo, Estado, Prioridad, Operario, Fecha Estimada).
    
- El campo **Operario** solo debe mostrar usuarios con rol de “Operario”.
    
- El campo **Estado** debe incluir las opciones: _Pendiente, En Proceso, Terminado, Entregado._
    
- El sistema debe validar que todos los campos obligatorios estén completos antes de guardar.
    
- Debe existir una **tabla de gestión** que liste todas las Órdenes de Producción con sus datos clave.
    
- Las acciones básicas (Ver, Editar, Eliminar) deben estar disponibles en cada registro.
    
- La eliminación debe requerir confirmación.
    

**Checklist de Tareas:**

-  Crear formulario para registrar nueva Orden de Producción.
    
-  Validar selección del Operario según su rol.
    
-  Implementar CRUD completo (Crear, Consultar, Editar, Eliminar).
    
-  Mostrar tabla de Órdenes con columnas principales.
    
-  Agregar confirmación antes de eliminar un registro.
    
-  Asociar la OP con su Pedido y Cliente.
    

**Campos del Formulario:**

- N° OP
    
- Pedido
    
- Cliente
    
- Descripción
    
- Tipo _(Enmarcado, Minilab, Graduación, Corte Láser, Edición Digital, Otro)_
    
- Estado _(Pendiente, En Proceso, Terminado, Entregado)_
    
- Prioridad _(Baja, Normal, Media, Alta)_
    
- Operario
    
- Fecha Estimada
    

**Botones de Acción:**

- Guardar
    
- Editar
    
- Eliminar
    
- Ver Detalle
    
- Añadir Nueva OP
    

---

## 🧾 **HU02 – Visualización y Filtrado de Órdenes de Producción**

**Etiquetas:**  
👀 VISUALIZACIÓN (verde)  
🔍 FILTROS (celeste)  
🟠 PRIORIDAD MEDIA (naranja)

**Descripción:**  
Como **usuario del sistema**, quiero **visualizar y filtrar las Órdenes de Producción** según su estado, tipo, prioridad o cliente, para facilitar el seguimiento de los trabajos en curso y detectar los que requieren atención inmediata.

**Criterios de Aceptación:**

- La vista principal debe mostrar pestañas automáticas: _Todos, Pendientes, En Proceso, Terminados, Entregados._
    
- Cada pestaña debe agrupar las OP según su Estado.
    
- El sistema debe permitir **búsqueda general** por N° OP, Cliente, Pedido o Descripción.
    
- Los filtros deben poder combinarse (por Estado, Tipo o Prioridad).
    
- Debe existir una opción para **añadir manualmente** una nueva OP desde la misma vista.
    
- La interfaz debe actualizarse automáticamente al cambiar el estado de una OP.
    

**Checklist de Tareas:**

-  Crear pestañas automáticas por estado.
    
-  Implementar campo de búsqueda general.
    
-  Agregar filtros por Tipo, Estado y Prioridad.
    
-  Permitir adición manual de OP desde la vista principal.
    
-  Actualizar lista automáticamente según cambios de estado.
    

**Campos del Formulario (para filtros o búsqueda):**

- N° OP
    
- Cliente
    
- Pedido
    
- Descripción
    
- Tipo _(selector)_
    
- Estado _(selector)_
    
- Prioridad _(selector)_
    

**Botones de Acción:**

- Buscar
    
- Filtrar
    
- Añadir Nueva OP
    
- Actualizar Vista
# GASTOS 
## 🧾 **HU01 – Registro y Control de Gastos Operativos**

**Etiquetas:**  
💰 FINANZAS (verde oscuro)  
📋 GESTIÓN (gris)  
🟡 PRIORIDAD ALTA (amarillo)

**Descripción:**  
Como **usuario administrativo o financiero**, quiero **registrar y administrar los gastos operativos** de la empresa, diferenciando entre **gastos de personal** y **gastos de servicios/suministros**, para mantener un control actualizado de las obligaciones financieras y pagos.

**Criterios de Aceptación:**

- El sistema debe permitir registrar dos tipos de gastos: **Personal (Nómina)** y **Servicios/Suministros**.
    
- Cada gasto debe tener un código identificador único.
    
- En el caso de gastos de **Personal**, el sistema debe calcular automáticamente el **Salario Neto** con la fórmula:
    
    > Salario Neto = (Salario Base + Bonificaciones) – Descuentos.
    
- En el caso de **Servicios**, se deben registrar los campos: Tipo de Servicio, Proveedor, Monto, Fechas y Estado.
    
- El campo **Estado** debe incluir las opciones:
    
    - _Personal:_ Pendiente, Pagado (y opcionalmente Atrasado).
        
    - _Servicios:_ Pendiente, Pagado, Vencido.
        
- El sistema debe permitir **editar, consultar y eliminar** los registros existentes.
    
- La eliminación debe requerir una **confirmación de seguridad**.
    

**Checklist de Tareas:**

-  Crear formulario para registrar un gasto de personal (nómina).
    
-  Crear formulario para registrar un gasto de servicio/suministro.
    
-  Implementar cálculo automático del salario neto.
    
-  Habilitar CRUD completo para ambos tipos de gasto.
    
-  Validar estados y fechas de pago/vencimiento.
    
-  Mostrar alertas visuales para gastos **vencidos o pendientes**.
    

**Campos Clave:**

- Personal: Código, Nombre, Cargo, Salario Base, Bonificaciones, Descuentos, Fecha de Pago, Estado, Salario Neto.
    
- Servicios: Código, Tipo de Servicio, Proveedor, Monto, Fecha de Vencimiento, Fecha de Pago, Estado, Periodo.
    

**Botones de Acción:**

- Guardar
    
- Editar
    
- Eliminar
    
- Ver Detalle
    
- Añadir Nuevo Gasto
    

---

## 🧾 **HU02 – Visualización y Filtrado de Gastos**

**Etiquetas:**  
👁️ VISUALIZACIÓN (verde)  
🔍 FILTROS (celeste)  
🟠 PRIORIDAD MEDIA (naranja)

**Descripción:**  
Como **usuario del sistema**, quiero **visualizar y filtrar todos los gastos registrados** (tanto de personal como de servicios), para poder identificar fácilmente los pagos pendientes, vencidos o completados.

**Criterios de Aceptación:**

- La vista principal debe mostrar **una tabla unificada** de gastos, diferenciando el tipo de gasto (Personal o Servicio).
    
- Las columnas deben incluir: Código, Tipo/Nombre/Proveedor, Monto, Estado, Fechas (Vencimiento/Pago) y Acciones.
    
- Debe existir una **búsqueda general** por nombre de empleado, tipo de servicio o proveedor.
    
- Los filtros deben permitir segmentar por:
    
    - Tipo de Gasto (Personal / Servicio)
        
    - Estado (Pendiente, Pagado, Vencido)
        
    - Periodo (Mes o rango de fechas).
        
- El sistema debe actualizar la información automáticamente cuando se modifique el estado o las fechas.
    
- Se debe mostrar un **resumen financiero** mediante tarjetas en la parte superior con las métricas:
    
    - Nómina Pendiente
        
    - Servicios Pendientes
        
    - Servicios Vencidos
        

**Checklist de Tareas:**

-  Implementar tabla unificada de visualización.
    
-  Configurar búsqueda general (nombre, servicio o proveedor).
    
-  Agregar filtros dinámicos por tipo, estado y periodo.
    
-  Mostrar tarjetas de resumen con los montos correspondientes.
    
-  Sincronizar estados automáticamente con base en fechas de vencimiento.
    

**Campos para Filtro/Búsqueda:**

- Tipo de Gasto
    
- Estado
    
- Nombre/Proveedor
    
- Periodo o Fecha
    

**Botones de Acción:**

- Buscar
    
- Filtrar
    
- Añadir Nuevo Gasto
    
- Actualizar Vista
# ACTIVOS
## 🧾 **HU01 – Registro y Control de Activos Fijos**

**Etiquetas:**  
🏢 INVENTARIO (azul oscuro)  
⚙️ ADMINISTRACIÓN (gris)  
🟢 PRIORIDAD ALTA (verde)

**Descripción:**  
Como **usuario administrativo**, quiero **registrar y gestionar los activos fijos** de la empresa, incluyendo su información general, costo, forma de pago, vida útil y estado, para mantener un control completo de los bienes y su situación operativa.

**Criterios de Aceptación:**

- El sistema debe permitir registrar los activos con sus datos principales: nombre, categoría, proveedor, fecha de compra, costo total, tipo de pago, vida útil y estado.
    
- Si el **Tipo de Pago** es _Financiado_ o _Leasing_, el sistema debe **crear automáticamente** un registro en el submódulo **Financiamientos**.
    
- Si el **Estado** es _Mantenimiento_, el sistema debe **generar un registro automático** en el submódulo **Mantenimientos**.
    
- El campo **Depreciación Mensual** se calculará automáticamente:
    
    > Depreciación = Costo Total / Vida Útil (meses).
    
- El usuario podrá **consultar, editar o eliminar** activos desde la tabla principal.
    
- Cada activo debe tener un **ID único** que lo identifique en los demás submódulos.
    

**Checklist de Tareas:**

-  Crear formulario de registro de activos.
    
-  Implementar cálculo automático de depreciación.
    
-  Activar flujo automático hacia _Financiamientos_ y _Mantenimientos_ según condiciones.
    
-  Crear vista de listado de activos con acciones CRUD.
    
-  Validar campos requeridos y formato de fechas.
    

**Campos del Formulario:**  
Nombre del Activo, Categoría, Proveedor, Fecha de Compra, Costo Total, Tipo de Pago, Vida Útil, Depreciación Mensual, Estado.

**Botones de Acción:**  
Guardar, Editar, Eliminar, Ver Detalle, Añadir Activo.

---

## 🧾 **HU02 – Gestión de Financiamientos de Activos**

**Etiquetas:**  
💰 FINANZAS (verde oscuro)  
📅 PAGOS (azul)  
🟡 PRIORIDAD MEDIA (amarillo)

**Descripción:**  
Como **usuario financiero**, quiero **gestionar los financiamientos asociados a los activos**, para llevar el control de los pagos, cuotas y fechas de vencimiento de cada crédito o leasing activo.

**Criterios de Aceptación:**

- El sistema debe crear un financiamiento automáticamente cuando un activo tenga **Tipo de Pago: Financiado o Leasing**.
    
- Los campos **Cuota Mensual** y **Fecha de Fin** se deben calcular automáticamente:
    
    > Cuota Mensual = Monto Financiado / Cuotas Totales  
    > Fecha de Fin = Fecha de Inicio + número de cuotas.
    
- Se debe mostrar una tabla con el progreso de pagos (**Cuotas Pagadas / Cuotas Totales**).
    
- El usuario podrá editar, consultar o eliminar registros de financiamiento.
    
- Debe permitir filtrar financiamientos por **Estado**, **Entidad Financiera** o **Activo Asociado**.
    
- Al eliminar un activo, se debe eliminar su financiamiento relacionado.
    

**Checklist de Tareas:**

-  Generar formulario de financiamiento.
    
-  Implementar cálculo automático de cuota y fecha final.
    
-  Crear tabla de financiamientos con progreso de pagos.
    
-  Sincronizar eliminación de activo con su financiamiento.
    
-  Agregar filtros y búsqueda de registros.
    

**Campos del Formulario:**  
Activo, Tipo de Pago, Entidad Financiera, Monto Financiado, Cuotas Totales, Cuota Mensual, Fecha de Inicio, Fecha de Fin, Estado.

**Botones de Acción:**  
Guardar, Editar, Eliminar, Ver Detalle, Registrar Pago.

---

## 🧾 **HU03 – Mantenimiento y Control de Repuestos de Activos**

**Etiquetas:**  
🔧 MANTENIMIENTO (naranja)  
🧩 REPUESTOS (morado)  
🟠 PRIORIDAD ALTA (rojo claro)

**Descripción:**  
Como **usuario técnico o de mantenimiento**, quiero **registrar, programar y controlar los mantenimientos de los activos**, incluyendo el uso de repuestos, para asegurar su funcionamiento adecuado y controlar el inventario de insumos.

**Criterios de Aceptación:**

- El sistema debe permitir registrar **mantenimientos preventivos o correctivos**.
    
- Al registrar un mantenimiento, se actualizará automáticamente el **Estado del Activo**.
    
- El campo **Próximo Mantenimiento** debe calcularse automáticamente a partir de la fecha actual.
    
- Si se agregan **repuestos**, el sistema debe **descontar el stock** del módulo de repuestos.
    
- El sistema debe permitir visualizar los mantenimientos realizados, su costo y proveedor.
    
- Si el stock de un repuesto llega al nivel mínimo, debe mostrarse una **alerta visual**.
    

**Checklist de Tareas:**

-  Crear formulario de registro de mantenimiento.
    
-  Implementar actualización automática del estado del activo.
    
-  Configurar cálculo automático del próximo mantenimiento.
    
-  Integrar consumo de repuestos con decremento de stock.
    
-  Mostrar alertas de stock mínimo.
    
-  Habilitar tabla de mantenimiento con acciones CRUD.
    

**Campos del Formulario:**  
Activo, Tipo de Mantenimiento, Costo, Proveedor, Fecha de Mantenimiento, Estado del Mantenimiento, Estado del Activo, Próximo Mantenimiento, Descripción, Repuestos Asociados.

**Botones de Acción:**  
Guardar, Editar, Eliminar, Ver Detalle, Añadir Repuesto.
# INVENTARIO
## 🧾 **HU01 – Registro y Control de Productos del Inventario**

**Etiquetas:**  
📦 INVENTARIO (azul oscuro)  
🧰 CONTROL DE STOCK (gris)  
🟢 PRIORIDAD ALTA (verde)

**Descripción:**  
Como **usuario encargado del inventario**, quiero **registrar y mantener actualizados los productos e insumos** del sistema, para tener control del stock disponible, los costos unitarios y totales, y asegurar la trazabilidad de los materiales por categoría.

**Criterios de Aceptación:**

- El sistema debe permitir **registrar productos** según su **categoría y subcategoría** (Ej: Moldura, Vidrio, Paspartú, Minilab, etc.).
    
- El campo **Costo Total** se debe **calcular automáticamente** como:
    
    > Costo Total = Costo Unitario × Stock Disponible.
    
- Cada producto debe tener su propio **Stock Mínimo** configurado para activar alertas.
    
- El usuario podrá **crear, editar, eliminar y consultar** productos desde la tabla principal.
    
- Los formularios deben adaptarse según el tipo de producto seleccionado.
    
- El inventario debe actualizarse automáticamente cuando otro módulo (como Producción o Pedidos) consuma un insumo.
    

**Checklist de Tareas:**

-  Crear formularios adaptativos por categoría y subcategoría.
    
-  Implementar cálculo automático del costo total.
    
-  Permitir CRUD completo para cada producto.
    
-  Sincronizar cambios de stock con otros módulos (Pedidos, Producción, Activos).
    
-  Validar campos requeridos (nombre, costo, stock, categoría).
    

**Campos del Formulario:**  
Nombre del Producto, Categoría, Subcategoría, Material, Color, Tamaño/Dimensiones, Costo Unitario, Stock Disponible, Stock Mínimo, Costo Total, Proveedor (opcional).

**Botones de Acción:**  
Guardar, Editar, Eliminar, Ver Detalle, Añadir Producto.

---

## 🧾 **HU02 – Monitoreo de Stock y Alertas de Reposición**

**Etiquetas:**  
⚠️ ALERTAS (amarillo)  
📊 MONITOREO (celeste)  
🟠 PRIORIDAD MEDIA (naranja)

**Descripción:**  
Como **usuario del sistema**, quiero **monitorear el nivel de stock** de los productos y recibir **alertas automáticas** cuando un producto esté igual o por debajo del nivel mínimo configurado, para poder realizar pedidos de reposición a tiempo.

**Criterios de Aceptación:**

- El sistema debe generar **alertas visuales** (ícono o color de advertencia) para productos con **Stock ≤ Stock Mínimo**.
    
- Las alertas deben mostrarse en una **tarjeta de resumen** (ejemplo: “3 productos con bajo stock”).
    
- Se debe poder **filtrar y visualizar** solo los productos en alerta.
    
- Las métricas principales deben mostrar:
    
    - Total de productos registrados.
        
    - Total de stock disponible.
        
    - Total de alertas activas.
        
    - Valor total del inventario.
        
- Debe permitir exportar o imprimir un **reporte de alertas** con detalle de productos críticos.
    

**Checklist de Tareas:**

-  Implementar cálculo de métricas principales.
    
-  Generar alertas automáticas de stock bajo.
    
-  Crear vista de filtros y reportes de productos en alerta.
    
-  Mostrar alertas en dashboard principal.
    
-  Probar actualización automática tras consumos de otros módulos.
    

**Campos del Formulario:**  
No aplica (función de monitoreo automático).

**Botones de Acción:**  
Actualizar, Ver Productos en Alerta, Exportar Reporte.

---

## 🧾 **HU03 – Integración del Inventario con Otros Módulos**

**Etiquetas:**  
🔄 SINCRONIZACIÓN (morado)  
💼 OPERACIONES (gris oscuro)  
🔵 PRIORIDAD MEDIA (celeste oscuro)

**Descripción:**  
Como **administrador del sistema**, quiero que el **módulo de Inventario se integre** con otros módulos (Pedidos, Producción, Activos y Gastos) para que las actualizaciones de stock y costos se realicen de forma automática y consistente en todo el sistema.

**Criterios de Aceptación:**

- Cuando se registre una **Nota de Venta o Pedido**, el sistema debe **restar automáticamente** el stock correspondiente.
    
- Si un activo en mantenimiento consume repuestos, el stock debe **disminuir en el inventario**.
    
- Al registrar un **nuevo gasto de compra**, el **costo unitario y total** del producto en inventario debe **actualizarse**.
    
- En **producción**, los materiales utilizados deben reflejarse como **consumo de stock**.
    
- El sistema debe guardar un **historial de movimientos** (ingresos y salidas) por producto.
    

**Checklist de Tareas:**

-  Crear lógica de sincronización de stock entre módulos.
    
-  Implementar actualización automática de costos por nuevos gastos.
    
-  Registrar movimientos de entrada y salida en un historial.
    
-  Validar integridad del stock al eliminar o modificar registros externos.
    
-  Configurar reportes de movimientos por módulo origen.
    

**Campos del Formulario:**  
No aplica directamente (flujo automatizado entre módulos).

**Botones de Acción:**  
Sincronizar Manualmente, Ver Historial de Movimientos.
# CLIENTES
### **HU01 – Registro de Cliente**

**Etiquetas:**  
📘 CLIENTES (azul oscuro)  
🧩 REGISTRO (verde)  
⚙️ FORMULARIO (celeste)  
📊 PRIORIDAD ALTA (rojo)

**Descripción:**  
Como administrador del sistema, quiero registrar nuevos clientes desde un formulario dinámico, para poder mantener una base de datos centralizada con información completa de personas, colegios o empresas.

**Criterios de Aceptación:**

1. El formulario debe cambiar los campos según el **tipo de cliente** seleccionado (Particular, Colegio o Empresa).
    
2. Todos los campos obligatorios deben validarse antes de guardar.
    
3. Al guardar correctamente, el sistema mostrará un mensaje de confirmación: “Cliente registrado con éxito.”
    
4. No se permitirá registrar dos clientes con el mismo **DNI o RUC**.
    

**Checklist de Tareas:**

-  Crear botón **+ NUEVO CLIENTE**.
    
-  Implementar formulario dinámico según el tipo de cliente.
    
-  Validar campos obligatorios y formato de DNI/RUC.
    
-  Guardar datos en la base de clientes.
    
-  Mostrar mensaje de éxito o error.
    

**Campos del Formulario:**

- Nombre Completo*
    
- DNI / RUC*
    
- Teléfono de Contacto*
    
- Email
    
- Dirección
    
- Institución Educativa / Empresa
    
- Detalles Adicionales
    

**Botones de Acción:**

- 💾 **Guardar Cliente**
    
- ❌ **Cancelar Registro**
    

---

### **HU02 – Búsqueda y Filtrado de Clientes**

**Etiquetas:**  
📘 CLIENTES (azul oscuro)  
🔍 BÚSQUEDA (verde)  
🎯 FILTROS (celeste)  
📊 PRIORIDAD MEDIA (amarillo)

**Descripción:**  
Como usuario del sistema, quiero buscar y filtrar clientes por nombre, documento o tipo de cliente, para poder localizar registros específicos de forma rápida y eficiente.

**Criterios de Aceptación:**

1. El buscador debe permitir buscar por **nombre, teléfono, email, DNI o RUC**.
    
2. El filtro debe permitir seleccionar **Tipo de Cliente** (Todos, Particular, Colegio, Empresa).
    
3. Debe existir un botón **“Limpiar Filtros”** para volver al listado completo.
    
4. La búsqueda debe actualizar los resultados **sin necesidad de recargar la página**.
    

**Checklist de Tareas:**

-  Implementar barra de búsqueda general.
    
-  Crear botón de filtros avanzados.
    
-  Agregar opción de limpiar filtros.
    
-  Conectar búsqueda con base de datos de clientes.
    

**Campos de Búsqueda / Filtro:**

- Nombre o Razón Social
    
- DNI / RUC
    
- Tipo de Cliente (Dropdown)
    
- Teléfono / Email
    

**Botones de Acción:**

- 🔍 **Buscar**
    
- 🧹 **Limpiar Filtros**
    

---

### **HU03 – Visualización y Gestión de Clientes (CRUD)**

**Etiquetas:**  
📘 CLIENTES (azul oscuro)  
📄 VISUALIZACIÓN (verde)  
🛠️ GESTIÓN CRUD (celeste)  
📊 PRIORIDAD ALTA (rojo)

**Descripción:**  
Como administrador, quiero visualizar el listado completo de clientes con sus datos principales y poder ejecutar acciones básicas (ver, editar o eliminar), para mantener actualizada la información registrada.

**Criterios de Aceptación:**

1. La tabla debe mostrar los datos principales del cliente (nombre, tipo, contacto, dirección, pedidos, total gastado y última compra).
    
2. Cada fila debe tener iconos de acción para **Ver, Editar o Eliminar**.
    
3. Al intentar eliminar un cliente, el sistema debe solicitar una **confirmación previa**.
    
4. La opción **Ver Detalles** debe mostrar el historial de pedidos y datos completos del cliente.
    

**Checklist de Tareas:**

-  Diseñar tabla de clientes con columnas definidas.
    
-  Implementar las acciones CRUD básicas.
    
-  Agregar confirmación de eliminación.
    
-  Vincular campo “Pedidos” y “Total Gastado” con el módulo de Pedidos.
    
-  Mostrar alerta visual al completar una acción con éxito.
    

**Campos Mostrados en la Tabla:**

- Cliente (Nombre / RUC / DNI)
    
- Tipo
    
- Contacto
    
- Dirección
    
- Pedidos
    
- Total Gastado (S/)
    
- Último Pedido
    
- Acciones
    

**Botones de Acción:**

- 👁️ **Ver Detalles**
    
- ✏️ **Editar**
    
- 🗑️ **Eliminar**
# PEDIDOS
### **HU01 – Creación de Pedido**

**Etiquetas:**  
📦 PEDIDOS (azul oscuro)  
🧾 REGISTRO (verde)  
💳 PAGOS (celeste)  
📊 PRIORIDAD ALTA (rojo)

**Descripción:**  
Como usuario del sistema, quiero registrar nuevos pedidos seleccionando el tipo de cliente y tipo de documento (Proforma, Nota de Venta o Contrato), para generar correctamente la orden y controlar el flujo de producción y pagos.

**Criterios de Aceptación:**

1. El formulario debe cambiar dinámicamente según el **Tipo de Cliente** (Particular, Colegio, Empresa).
    
2. El tipo de documento seleccionado define la lógica de pago y el botón de acción:
    
    - **Proforma:** Solo calcula total y saldo.
        
    - **Nota de Venta:** Registra ingreso y descuenta del inventario.
        
    - **Contrato:** Crea un registro vinculado en el módulo **Contratos** y programa eventos en la **Agenda**.
        
3. Debe permitir agregar productos al detalle del pedido con sus cantidades y precios.
    
4. Al guardar, el sistema debe mostrar un mensaje: **“Pedido registrado correctamente.”**
    
5. Los campos obligatorios deben validarse antes del registro.
    

**Checklist de Tareas:**

-  Crear botón **+ NUEVO PEDIDO**.
    
-  Implementar formulario dinámico por tipo de cliente.
    
-  Incorporar lógica de tipo de documento.
    
-  Validar campos obligatorios y totales.
    
-  Generar registro del pedido con estado inicial “Pendiente”.
    

**Campos del Formulario (Comunes):**

- Cliente (según tipo)
    
- Tipo de Documento (Proforma, Nota de Venta, Contrato)
    
- Detalle de Productos
    
- Detalles Adicionales / Servicios Extras
    
- Total, A Cuenta, Saldo
    

**Botones de Acción:**

- 💾 **Guardar Proforma**
    
- 🧾 **Procesar Venta**
    
- 📄 **Crear Contrato**
    
- ❌ **Cancelar**
    

---

### **HU02 – Búsqueda y Filtrado de Pedidos**

**Etiquetas:**  
📦 PEDIDOS (azul oscuro)  
🔍 BÚSQUEDA (verde)  
🎯 FILTROS (celeste)  
📊 PRIORIDAD MEDIA (amarillo)

**Descripción:**  
Como usuario del sistema, quiero buscar y filtrar pedidos según tipo de documento, cliente o estado, para localizar rápidamente órdenes específicas y hacer seguimiento eficiente.

**Criterios de Aceptación:**

1. La barra de búsqueda debe permitir encontrar pedidos por **cliente, número de pedido o teléfono**.
    
2. Los filtros deben permitir seleccionar:
    
    - **Tipo de Documento:** Proforma, Nota de Venta o Contrato.
        
    - **Estado:** Pendiente, En Proceso, Completado, Cancelado, Atrasado.
        
3. El botón **“Limpiar Filtros”** debe restablecer la vista inicial.
    
4. Los resultados deben actualizarse sin recargar la página.
    

**Checklist de Tareas:**

-  Implementar barra de búsqueda.
    
-  Crear panel de filtros con selección múltiple.
    
-  Añadir campo “Estado: Atrasado” para pedidos fuera de fecha.
    
-  Implementar botón **Limpiar Filtros**.
    
-  Mostrar resultados actualizados dinámicamente.
    

**Filtros Disponibles:**

- Tipo de Documento
    
- Estado del Pedido
    
- Cliente (nombre o razón social)
    
- Fecha de Entrega
    

**Botones de Acción:**

- 🔍 **Buscar**
    
- 🧹 **Limpiar Filtros**
    

---

### **HU03 – Gestión y Control de Pedidos (CRUD + Resumen)**

**Etiquetas:**  
📦 PEDIDOS (azul oscuro)  
📋 VISUALIZACIÓN (verde)  
⚙️ GESTIÓN CRUD (celeste)  
📊 PRIORIDAD ALTA (rojo)

**Descripción:**  
Como administrador, quiero visualizar la lista completa de pedidos con sus datos financieros y de estado, para poder observar, editar o eliminar registros, y obtener un resumen total de los montos y saldos.

**Criterios de Aceptación:**

1. La tabla debe mostrar los datos principales del pedido: número, fecha, cliente, tipo, estado, fecha de entrega, total, a cuenta y saldo.
    
2. Cada pedido debe incluir iconos de acción:
    
    - 👁️ **Ver Detalles** (abrir vista completa del pedido).
        
    - ✏️ **Editar Pedido**.
        
    - 🗑️ **Eliminar Pedido** (con confirmación previa).
        
3. En la parte inferior debe mostrarse el **Total Absoluto** y el **Saldo Absoluto** de los pedidos visibles.
    
4. Si la fecha actual supera la fecha de entrega y el pedido no está “Completado”, su estado se marcará automáticamente como **Atrasado**.
    
5. Los cambios en los estados deben reflejarse en tiempo real.
    

**Checklist de Tareas:**

-  Diseñar tabla principal con columnas definidas.
    
-  Agregar lógica para estado automático “Atrasado”.
    
-  Implementar acciones CRUD.
    
-  Calcular y mostrar los totales de resumen.
    
-  Confirmar eliminaciones antes de proceder.
    

**Columnas de la Tabla:**

- Número
    
- Fecha Inicio
    
- Cliente
    
- Tipo
    
- Estado
    
- Fecha de Entrega
    
- Total
    
- A Cuenta
    
- Saldo
    
- Acciones
    

**Totales Inferiores:**

- **Total Absoluto (S/)**
    
- **Saldo Absoluto (S/)**
    

**Botones de Acción:**

- 👁️ **Ver Detalles**
    
- ✏️ **Editar Pedido**
    
- 🗑️ **Eliminar**
# AGENDA
### **HU01 – Visualización General de la Agenda**

**Etiquetas:**  
🗓️ AGENDA (azul oscuro)  
👁️ VISUALIZACIÓN (verde)  
📅 CALENDARIO (celeste)  
📊 PRIORIDAD MEDIA (amarillo)

**Descripción:**  
Como administrador del sistema, quiero visualizar todas las citas, sesiones y entregas en un calendario interactivo, para tener control sobre las actividades programadas y optimizar la planificación del tiempo.

**Criterios de Aceptación:**

1. La vista principal debe mostrar los eventos organizados en formato calendario, distribuidos por día y hora.
    
2. Cada evento debe mostrarse con una **etiqueta de color** según su tipo:
    
    - Azul: Sesión Fotográfica
        
    - Verde: Entrega
        
    - Amarillo: Recordatorio
        
3. Al hacer clic en una etiqueta, debe abrirse una ventana con los **detalles completos del evento**.
    
4. Si no existen eventos en la fecha seleccionada, el sistema debe mostrar el mensaje:  
    _“No hay eventos para este día.”_
    
5. La vista debe permitir cambiar entre los modos: **Día**, **Semana**, **Mes** y **Trimestral**.
    

**Checklist de Tareas:**

-  Implementar vista de calendario principal.
    
-  Configurar vistas (Día, Semana, Mes, Trimestral).
    
-  Mostrar etiquetas por tipo de evento.
    
-  Crear ventana emergente con detalles del evento.
    
-  Mostrar mensaje cuando no hay eventos.
    

**Botones de Acción:**

- 🔁 **Cambiar Vista (Día / Semana / Mes / Trimestre)**
    
- ⬅️➡️ **Navegar entre fechas**
    

---

### **HU02 – Creación de Nuevo Evento**

**Etiquetas:**  
🗓️ AGENDA (azul oscuro)  
➕ REGISTRO (verde)  
🕒 PROGRAMACIÓN (celeste)  
📊 PRIORIDAD ALTA (rojo)

**Descripción:**  
Como usuario del sistema, quiero registrar nuevos eventos (sesiones fotográficas, entregas o recordatorios) en la Agenda, para mantener organizadas las actividades relacionadas con clientes o pedidos.

**Criterios de Aceptación:**

1. El formulario debe contener los siguientes campos obligatorios:
    
    - Cliente / Título
        
    - Tipo de Evento
        
    - Descripción
        
    - Fecha y Hora
        
    - Ubicación
        
    - Estado
        
2. Los tipos de evento disponibles deben ser:
    
    - Sesión Fotográfica
        
    - Entrega
        
    - Recordatorio
        
3. El sistema debe asignar automáticamente un **Número de Evento** (ej. EVT-0001).
    
4. Al guardar, debe mostrarse el mensaje **“Evento registrado correctamente.”**
    
5. Si el usuario cancela, el formulario debe cerrarse sin guardar.
    

**Checklist de Tareas:**

-  Crear botón **+ NUEVO EVENTO**.
    
-  Implementar formulario de registro con validaciones.
    
-  Asignar numeración automática.
    
-  Configurar estados iniciales (Programado / Pendiente).
    
-  Agregar botón **Cancelar** con cierre del formulario.
    

**Botones de Acción:**

- 💾 **Guardar Evento**
    
- ❌ **Cancelar**
    

---

### **HU03 – Gestión de Eventos (CRUD)**

**Etiquetas:**  
🗓️ AGENDA (azul oscuro)  
⚙️ GESTIÓN CRUD (verde)  
✏️ EDICIÓN / ELIMINACIÓN (celeste)  
📊 PRIORIDAD MEDIA (amarillo)

**Descripción:**  
Como administrador, quiero consultar, editar o eliminar los eventos registrados en la Agenda, para mantener actualizada la programación de actividades.

**Criterios de Aceptación:**

1. Al hacer clic sobre un evento, se deben mostrar sus datos completos:  
    Cliente, Tipo, Fecha y Hora, Ubicación, Descripción, Estado.
    
2. Debe existir un botón **Editar** que permita modificar todos los campos del evento.
    
3. Debe existir un botón **Eliminar** con confirmación previa:  
    _“¿Desea eliminar este evento de forma definitiva?”_
    
4. Los cambios realizados deben actualizarse en el calendario de manera inmediata.
    
5. El sistema debe guardar un historial de modificaciones básicas (fecha de creación y última edición).
    

**Checklist de Tareas:**

-  Crear ventana de detalle del evento.
    
-  Implementar botones **Editar** y **Eliminar**.
    
-  Configurar mensaje de confirmación antes de eliminar.
    
-  Sincronizar actualizaciones en la vista del calendario.
    
-  Registrar timestamp de modificación.
    

**Botones de Acción:**

- ✏️ **Editar Evento**
    
- 🗑️ **Eliminar Evento**
    

---

### **HU04 – Listado de Próximos Eventos**

**Etiquetas:**  
🗓️ AGENDA (azul oscuro)  
📋 LISTADO (verde)  
📆 CRONOLÓGICO (celeste)  
📊 PRIORIDAD MEDIA (amarillo)

**Descripción:**  
Como usuario del sistema, quiero visualizar un listado con los próximos eventos ordenados cronológicamente, para identificar rápidamente las actividades más cercanas.

**Criterios de Aceptación:**

1. Los eventos deben mostrarse como **tarjetas** ordenadas ascendentemente por **Fecha y Hora**.
    
2. Cada tarjeta debe incluir:
    
    - Nombre del Cliente / Título
        
    - Número de Evento (EVT-XXXX)
        
    - Tipo de Evento
        
    - Fecha y Hora
        
3. Se deben mostrar **16 eventos por página**, con navegación por botones **Anterior / Siguiente**.
    
4. Los eventos vencidos deben mostrarse en un tono gris atenuado.
    
5. Al hacer clic en una tarjeta, debe abrirse el detalle del evento correspondiente.
    

**Checklist de Tareas:**

-  Crear contenedor de tarjetas de eventos.
    
-  Implementar orden cronológico automático.
    
-  Aplicar paginación (16 por página).
    
-  Resaltar eventos próximos (por color o icono).
    
-  Activar navegación entre páginas.
    

**Botones de Acción:**

- ⬅️ **Anterior**
    
- ➡️ **Siguiente**
    

---

### **HU05 – Filtros de Eventos**

**Etiquetas:**  
🗓️ AGENDA (azul oscuro)  
🔍 FILTROS (verde)  
⚙️ CATEGORIZACIÓN (celeste)  
📊 PRIORIDAD MEDIA (amarillo)

**Descripción:**  
Como usuario del sistema, quiero filtrar los eventos de la Agenda por tipo (Sesión, Entrega o Recordatorio), para visualizar solo las actividades relevantes según mi necesidad.

**Criterios de Aceptación:**

1. El filtro debe ofrecer las siguientes opciones:
    
    - Todos
        
    - Sesión Fotográfica
        
    - Entrega
        
    - Recordatorio
        
2. Los resultados deben actualizarse automáticamente al seleccionar un filtro.
    
3. El sistema debe mantener visible el filtro activo.
    
4. Debe incluir un botón **“Limpiar Filtros”** para volver a mostrar todos los eventos.
    

**Checklist de Tareas:**

-  Crear menú de filtros de eventos.
    
-  Implementar actualización dinámica de la vista.
    
-  Mostrar resaltado del filtro activo.
    
-  Agregar botón **Limpiar Filtros**.
    

**Botones de Acción:**

- 🔍 **Filtrar**
    
- 🧹 **Limpiar Filtros**
# DASHBOARD
## 🧾 **HU01 – Visualización General y Métricas del Dashboard**

**Etiquetas:**  
📊 **DASHBOARD (azul oscuro)** – 💰 **MÉTRICAS (verde)** – ⚙️ **FILTROS TEMPORALES (celeste)** – 🟡 **PRIORIDAD ALTA**

### **Descripción:**

Como **administrador del sistema**, quiero visualizar en el dashboard un resumen general de la información operativa y financiera, con filtros por rango de tiempo (día, semana o mes), para analizar el rendimiento del negocio de manera rápida y efectiva.

---

### **Criterios de Aceptación:**

1. El dashboard debe mostrar **tarjetas métricas** actualizadas según el filtro temporal aplicado.
    
2. El filtro temporal debe afectar solo las **4 primeras métricas** del panel principal.
    
3. Las métricas deben calcularse de acuerdo a la fuente y lógica indicada:
    
    - **Ingresos del Día:** suma de montos pagados en pedidos completados.
        
    - **Pedidos Activos:** cantidad de pedidos en estado _Pendiente_ o _En Proceso_.
        
    - **Entregados a Tiempo:** pedidos completados cuya entrega fue antes o en la fecha programada.
        
    - **Valor de Inventario:** suma total de los costos de materiales disponibles.
        
4. Los valores deben actualizarse automáticamente al cambiar el filtro (Hoy, Semana, Mes).
    
5. El usuario debe poder visualizar las métricas sin tiempos de espera extensos ni errores de carga.
    

---

### **Checklist de Tareas:**

-  Implementar el filtro de tiempo con opciones: Hoy, Semana y Mes.
    
-  Configurar la obtención de datos desde los módulos: Pedidos, Producción e Inventario.
    
-  Calcular dinámicamente los valores de cada tarjeta según el filtro activo.
    
-  Validar que las métricas cambien sin recargar toda la página.
    
-  Diseñar la lógica de actualización automática (refresco de datos).
    
-  Probar con datos de prueba para confirmar la exactitud de las cifras mostradas.
    

---

### **Campos del Formulario (Filtro Temporal):**

- **Filtro de Fecha:**
    
    - Hoy
        
    - Semana
        
    - Mes
        

---

### **Botones de Acción:**

- 🔄 **Actualizar Datos** – Refresca las métricas según el filtro.
    
- 📅 **Aplicar Filtro** – Aplica el rango de tiempo seleccionado.
    

---

## 🧾 **HU02 – Panel de Alertas y Estados Operativos**

**Etiquetas:**  
🚨 **ALERTAS (rojo)** – 🧩 **OPERACIONES (morado)** – 📋 **ESTADOS (verde)** – 🟠 **PRIORIDAD MEDIA**

### **Descripción:**

Como **administrador**, quiero visualizar alertas importantes y el estado general de producción, clientes y contratos, para identificar posibles problemas o tareas pendientes sin tener que revisar cada módulo por separado.

---

### **Criterios de Aceptación:**

1. El panel superior debe mostrar un máximo de **5 alertas activas** al mismo tiempo.
    
2. Cada alerta debe generarse automáticamente según la lógica definida:
    
    - **Stock Crítico:** si un material tiene stock menor o igual al mínimo.
        
    - **Mantenimiento Preventivo:** si un activo tiene mantenimiento próximo (dentro de 7 días).
        
    - **Entregas Urgentes:** si la fecha de entrega está a menos de 2 días.
        
3. Deben mostrarse **tarjetas por estado** para:
    
    - **Producción:** Pendiente, En Proceso, Completadas y Atrasadas.
        
    - **Clientes:** Totales, Nuevos del Mes, Activos e Inactivos.
        
    - **Contratos:** Valor Total, Activos, Pagos Pendientes y Por Vencer.
        
4. El sistema debe actualizar automáticamente las métricas cuando se modifique la información en los módulos relacionados.
    

---

### **Checklist de Tareas:**

-  Crear la lógica que genera y actualiza las alertas según las condiciones.
    
-  Conectar las tarjetas de estado con sus módulos correspondientes (Producción, Clientes y Contratos).
    
-  Validar que las métricas se actualicen sin errores ni duplicados.
    
-  Configurar orden de prioridad para las alertas (las más urgentes primero).
    
-  Probar los casos límite: sin alertas, sin datos o con valores nulos.
    

---

### **Campos del Panel:**

- **Alertas Activas:** Stock Crítico, Mantenimiento, Entregas.
    
- **Tarjetas de Estado:**
    
    - Producción: Pendiente, En Proceso, Completadas, Atrasadas.
        
    - Clientes: Totales, Nuevos del Mes, Activos, Inactivos.
        
    - Contratos: Valor Total, Activos, Pagos Pendientes, Por Vencer.
        

---

### **Botones de Acción:**

- 🧭 **Ver Detalles** – Redirige al módulo correspondiente según la alerta seleccionada.
    
- 🔁 **Actualizar Panel** – Refresca manualmente todas las tarjetas y alertas.