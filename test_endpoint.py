#!/usr/bin/env python
"""
Script de prueba para el endpoint totals_summary
"""
import requests
import json

# Datos de configuración
BASE_URL = "http://localhost:8000"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYyMzg2MTAyLCJpYXQiOjE3NjIzNTczMDIsImp0aSI6IjZmZmFmNjg3MDIyYTRhZDViOWM3ZDFiMWZkNzhkZGUyIiwidXNlcl9pZCI6IjEifQ.WqqQkd1OWosu6PUrX2ygdmyv_iT67vVCcYdnVRJb4Rs"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def test_totals_summary():
    """Probar el endpoint totals_summary"""
    
    url = f"{BASE_URL}/api/commerce/orders/totals_summary/"
    
    print("🧪 PROBANDO ENDPOINT TOTALS_SUMMARY")
    print(f"📡 URL: {url}")
    print(f"🔑 Authorization: Bearer {ACCESS_TOKEN[:50]}...")
    
    try:
        response = requests.get(url, headers=headers)
        
        print(f"\n📊 RESPUESTA:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response Body:")
            print(json.dumps(data, indent=2))
            
            # Verificar que los datos coincidan con lo que creamos
            expected_total = 6000.0  # 1000 + 2000 + 3000
            expected_balance = 1000.0  # 500 + 500 + 0
            
            # Los campos pueden tener nombres diferentes
            actual_total = data.get('total_absoluto', 0) or data.get('absolute_total', 0)
            actual_balance = data.get('saldo_absoluto', 0) or data.get('absolute_balance', 0)
            
            print(f"\n✅ VERIFICACIÓN:")
            print(f"Total esperado: {expected_total}")
            print(f"Total actual: {actual_total}")
            print(f"Balance esperado: {expected_balance}")
            print(f"Balance actual: {actual_balance}")
            
            if abs(actual_total - expected_total) < 0.01:
                print("✅ Total coincide ✓")
            else:
                print("❌ Total no coincide ✗")
                
            if abs(actual_balance - expected_balance) < 0.01:
                print("✅ Balance coincide ✓")
            else:
                print("❌ Balance no coincide ✗")
                
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_totals_summary()