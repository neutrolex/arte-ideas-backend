#!/usr/bin/env python
"""
Script para obtener el token JWT del usuario admin
"""
import os
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def get_auth_token():
    """Obtener token JWT para el usuario admin"""
    
    # URL del endpoint de login
    login_url = "http://localhost:8000/api/core/auth/login/"
    
    # Datos de login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        # Hacer petición de login
        response = requests.post(login_url, json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access', '')
            refresh_token = data.get('refresh', '')
            
            print("🔑 TOKEN DE ACCESO OBTENIDO:")
            print(f"Access Token: {access_token}")
            print(f"Refresh Token: {refresh_token}")
            print(f"\n📋 PARA POSTMAN:")
            print(f"Authorization: Bearer {access_token}")
            
            # Guardar tokens en un archivo para referencia
            with open('postman_tokens.json', 'w') as f:
                json.dump({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'login_url': login_url,
                    'totals_summary_url': 'http://localhost:8000/api/commerce/orders/totals_summary/'
                }, f, indent=2)
            
            print(f"\n✅ Tokens guardados en postman_tokens.json")
            
        else:
            print(f"❌ Error al obtener token: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_auth_token()