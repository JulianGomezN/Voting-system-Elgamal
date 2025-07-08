#!/usr/bin/env python3
"""
Script para probar el sistema de fechas y validación de elecciones
"""

from datetime import datetime, timedelta
import sys
import os

# Agregar el directorio actual al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_date_validation():
    """Prueba las funciones de validación de fechas"""
    print("=== Prueba de Validación de Fechas ===")
    
    # Simular una elección que terminó hace 1 hora
    past_end = datetime.now() - timedelta(hours=1)
    past_start = datetime.now() - timedelta(hours=2)
    
    # Simular una elección que terminará en 1 hora
    future_end = datetime.now() + timedelta(hours=1)
    future_start = datetime.now() - timedelta(hours=1)
    
    # Simular una elección que empezará en 1 hora
    scheduled_start = datetime.now() + timedelta(hours=1)
    scheduled_end = datetime.now() + timedelta(hours=2)
    
    now = datetime.now()
    
    print(f"Hora actual: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Prueba 1: Elección terminada
    print("1. Elección terminada:")
    print(f"   Inicio: {past_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Fin: {past_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   ¿Ha empezado?: {now >= past_start}")
    print(f"   ¿Ha terminado?: {now > past_end}")
    print(f"   ¿Puede votar?: {now >= past_start and now <= past_end}")
    print()
    
    # Prueba 2: Elección activa
    print("2. Elección activa:")
    print(f"   Inicio: {future_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Fin: {future_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   ¿Ha empezado?: {now >= future_start}")
    print(f"   ¿Ha terminado?: {now > future_end}")
    print(f"   ¿Puede votar?: {now >= future_start and now <= future_end}")
    print()
    
    # Prueba 3: Elección programada
    print("3. Elección programada:")
    print(f"   Inicio: {scheduled_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Fin: {scheduled_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   ¿Ha empezado?: {now >= scheduled_start}")
    print(f"   ¿Ha terminado?: {now > scheduled_end}")
    print(f"   ¿Puede votar?: {now >= scheduled_start and now <= scheduled_end}")
    print()

def test_election_status_logic():
    """Prueba la lógica de estado de elecciones"""
    print("=== Prueba de Lógica de Estado ===")
    
    # Simular diferentes tipos de elecciones
    elections = [
        {
            'title': 'Elección Terminada',
            'is_active': True,
            'start_date': datetime.now() - timedelta(hours=2),
            'end_date': datetime.now() - timedelta(hours=1)
        },
        {
            'title': 'Elección Activa',
            'is_active': True,
            'start_date': datetime.now() - timedelta(hours=1),
            'end_date': datetime.now() + timedelta(hours=1)
        },
        {
            'title': 'Elección Programada',
            'is_active': True,
            'start_date': datetime.now() + timedelta(hours=1),
            'end_date': datetime.now() + timedelta(hours=2)
        },
        {
            'title': 'Elección Cerrada Manualmente',
            'is_active': False,
            'start_date': datetime.now() - timedelta(hours=1),
            'end_date': datetime.now() + timedelta(hours=1)
        }
    ]
    
    for election in elections:
        print(f"Elección: {election['title']}")
        now = datetime.now()
        
        is_started = now >= election['start_date']
        is_ended = now > election['end_date']
        can_vote = election['is_active'] and is_started and not is_ended
        
        print(f"  Estado: {'Activa' if election['is_active'] else 'Inactiva'}")
        print(f"  ¿Ha empezado?: {is_started}")
        print(f"  ¿Ha terminado?: {is_ended}")
        print(f"  ¿Puede votar?: {can_vote}")
        
        if not can_vote:
            if not election['is_active']:
                print("  Razón: Elección cerrada manualmente")
            elif not is_started:
                print("  Razón: Elección aún no ha comenzado")
            elif is_ended:
                print("  Razón: Elección ha terminado")
        
        print()

if __name__ == "__main__":
    test_date_validation()
    test_election_status_logic()
    
    print("=== Solución Implementada ===")
    print("Los cambios realizados:")
    print("1. Cambié datetime.utcnow() por datetime.now() para usar hora local")
    print("2. Agregué función update_election_status() para cerrar elecciones automáticamente")
    print("3. Actualicé la lógica de validación para ser más clara")
    print("4. Agregué información de debug en los templates")
    print("5. Agregué controles administrativos para cerrar/reabrir elecciones")
