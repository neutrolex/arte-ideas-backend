#!/usr/bin/env python
"""
Script para crear datos de prueba para probar el endpoint totals_summary en Postman
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.core.models import Tenant
from apps.crm.models import Cliente
from apps.commerce.models import Order
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def create_test_data():
    """Crear datos de prueba para el endpoint totals_summary"""
    
    print("🚀 Creando datos de prueba...")
    
    # Crear Tenant
    tenant, created = Tenant.objects.get_or_create(
        name="Estudio de Prueba",
        defaults={
            'slug': 'estudio-prueba',
            'business_name': 'Estudio Fotográfico Prueba S.A.C.',
            'business_ruc': '12345678901',
            'business_phone': '123456789',
            'business_email': 'prueba@estudio.com',
            'business_address': 'Av. Prueba 123'
        }
    )
    
    if created:
        print(f"✅ Tenant creado: {tenant.name}")
    else:
        print(f"ℹ️  Tenant ya existía: {tenant.name}")
    
    # Crear usuario administrador
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@estudio.com',
            'role': 'admin',
            'tenant': tenant
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Usuario administrador creado: admin")
    else:
        print(f"ℹ️  Usuario administrador ya existía: admin")
    
    # Crear clientes
    cliente1, created = Cliente.objects.get_or_create(
        tenant=tenant,
        dni='12345678',
        defaults={
            'tipo_cliente': 'particular',
            'nombres': 'Juan',
            'apellidos': 'Pérez',
            'email': 'juan@test.com',
            'telefono': '987654321',
            'direccion': 'Av. Cliente 123'
        }
    )
    
    if created:
        print(f"✅ Cliente creado: {cliente1}")
    
    cliente2, created = Cliente.objects.get_or_create(
        tenant=tenant,
        dni='87654321',
        defaults={
            'tipo_cliente': 'particular',
            'nombres': 'María',
            'apellidos': 'Gómez',
            'email': 'maria@test.com',
            'telefono': '987654322',
            'direccion': 'Av. Cliente 456'
        }
    )
    
    if created:
        print(f"✅ Cliente creado: {cliente2}")
    
    # Crear pedidos de prueba
    orders_data = [
        {
            'order_number': 'ORD-001',
            'total': 1000.00,
            'paid_amount': 500.00,
            'balance': 500.00,
            'status': 'pending'
        },
        {
            'order_number': 'ORD-002',
            'total': 2000.00,
            'paid_amount': 1500.00,
            'balance': 500.00,
            'status': 'in_progress'
        },
        {
            'order_number': 'ORD-003',
            'total': 3000.00,
            'paid_amount': 3000.00,
            'balance': 0.00,
            'status': 'completed'
        }
    ]
    
    orders_created = 0
    for order_data in orders_data:
        order, created = Order.objects.get_or_create(
            tenant=tenant,
            order_number=order_data['order_number'],
            defaults={
                'cliente': cliente1,
                'document_type': 'proforma',
                'client_type': 'particular',
                'start_date': timezone.now().date(),
                'delivery_date': timezone.now().date() + timedelta(days=7),
                'total': order_data['total'],
                'paid_amount': order_data['paid_amount'],
                'balance': order_data['balance'],
                'status': order_data['status']
            }
        )
        
        if created:
            orders_created += 1
            print(f"✅ Pedido creado: {order.order_number} - Total: S/.{order.total} - Balance: S/.{order.balance}")
    
    if orders_created == 0:
        print("ℹ️  Los pedidos de prueba ya existían")
    
    # Calcular y mostrar los totales esperados
    all_orders = Order.objects.filter(tenant=tenant)
    total_absoluto = sum(order.total for order in all_orders)
    saldo_absoluto = sum(order.balance for order in all_orders)
    
    print(f"\n📊 RESUMEN DE DATOS CREADOS:")
    print(f"   - Total de pedidos: {all_orders.count()}")
    print(f"   - Total absoluto esperado: S/.{total_absoluto:.2f}")
    print(f"   - Saldo absoluto esperado: S/.{saldo_absoluto:.2f}")
    
    print(f"\n🔑 CREDENCIALES DE ACCESO:")
    print(f"   - Usuario: admin")
    print(f"   - Contraseña: admin123")
    print(f"   - URL del endpoint: http://localhost:8000/api/commerce/orders/totals_summary/")
    
    print(f"\n✨ Datos de prueba creados exitosamente!")

if __name__ == "__main__":
    create_test_data()