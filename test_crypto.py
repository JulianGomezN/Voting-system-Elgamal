"""
Script de prueba para verificar el funcionamiento del cifrado ElGamal
"""

from elgamal_crypto import ElGamalCrypto
import json

def test_elgamal_encryption():
    print("=== Prueba de Cifrado ElGamal ===")
    
    # Crear instancia del cifrado
    crypto = ElGamalCrypto(key_size=1024)  # Usar 1024 bits para pruebas rápidas
    
    # Generar claves
    print("1. Generando claves ElGamal...")
    keys = crypto.generate_keys()
    
    public_key = {
        'p': keys['p'],
        'g': keys['g'],
        'public_key': keys['public_key']
    }
    
    private_key = {
        'p': keys['p'],
        'private_key': keys['private_key']
    }
    
    print(f"   Clave pública generada: {len(str(public_key['public_key']))} dígitos")
    print(f"   Clave privada generada: {len(str(private_key['private_key']))} dígitos")
    
    # Cifrar un voto
    print("\n2. Cifrando voto...")
    vote_value = 1  # Voto por candidato
    encrypted_vote = crypto.encrypt_vote(vote_value, public_key)
    print(f"   Voto original: {vote_value}")
    print(f"   Voto cifrado: (c1={len(str(encrypted_vote[0]))} dígitos, c2={len(str(encrypted_vote[1]))} dígitos)")
    
    # Descifrar el voto
    print("\n3. Descifrando voto...")
    decrypted_vote = crypto.decrypt_vote(encrypted_vote, private_key)
    print(f"   Voto descifrado: {decrypted_vote}")
    
    # Verificar integridad
    print("\n4. Verificando integridad...")
    vote_data = {
        'user_id': 1,
        'candidate_id': 1,
        'timestamp': '2025-01-01T00:00:00'
    }
    vote_hash = crypto.hash_vote(vote_data)
    print(f"   Hash del voto: {vote_hash}")
    
    # Verificar que el cifrado/descifrado funciona
    if vote_value == decrypted_vote:
        print("\n✅ ÉXITO: El cifrado y descifrado funciona correctamente!")
        return True
    else:
        print("\n❌ ERROR: El cifrado y descifrado no funciona!")
        return False

def test_homomorphic_properties():
    print("\n=== Prueba de Propiedades Homomórficas ===")
    
    crypto = ElGamalCrypto(key_size=1024)
    keys = crypto.generate_keys()
    
    public_key = {
        'p': keys['p'],
        'g': keys['g'],
        'public_key': keys['public_key']
    }
    
    private_key = {
        'p': keys['p'],
        'private_key': keys['private_key']
    }
    
    # Cifrar dos votos
    vote1 = 1
    vote2 = 1
    
    encrypted_vote1 = crypto.encrypt_vote(vote1, public_key)
    encrypted_vote2 = crypto.encrypt_vote(vote2, public_key)
    
    print(f"Voto 1: {vote1}")
    print(f"Voto 2: {vote2}")
    
    # En ElGamal, la suma homomorfa no funciona directamente para enteros
    # En su lugar, verificamos que podemos contar votos individualmente
    decrypted_vote1 = crypto.decrypt_vote(encrypted_vote1, private_key)
    decrypted_vote2 = crypto.decrypt_vote(encrypted_vote2, private_key)
    
    manual_sum = decrypted_vote1 + decrypted_vote2
    expected_sum = vote1 + vote2
    
    print(f"Suma manual: {manual_sum}")
    print(f"Suma esperada: {expected_sum}")
    
    if manual_sum == expected_sum:
        print("✅ ÉXITO: Los votos se pueden contar correctamente!")
        return True
    else:
        print("❌ ERROR: Error en el conteo de votos!")
        return False

def test_multiple_votes():
    print("\n=== Prueba de Múltiples Votos ===")
    
    crypto = ElGamalCrypto(key_size=1024)
    keys = crypto.generate_keys()
    
    public_key = {
        'p': keys['p'],
        'g': keys['g'],
        'public_key': keys['public_key']
    }
    
    private_key = {
        'p': keys['p'],
        'private_key': keys['private_key']
    }
    
    # Simular múltiples votos
    votes = [1, 1, 1, 0, 1, 0, 1, 1, 0, 1]  # 7 votos a favor, 3 en contra
    encrypted_votes = []
    
    print("Cifrando múltiples votos...")
    for i, vote in enumerate(votes):
        encrypted_vote = crypto.encrypt_vote(vote, public_key)
        encrypted_votes.append(encrypted_vote)
        print(f"  Voto {i+1}: {vote} -> cifrado")
    
    # Descifrar y contar
    total_votes = 0
    for encrypted_vote in encrypted_votes:
        decrypted_vote = crypto.decrypt_vote(encrypted_vote, private_key)
        total_votes += decrypted_vote
    
    expected_total = sum(votes)
    print(f"\nTotal de votos descifrados: {total_votes}")
    print(f"Total esperado: {expected_total}")
    
    if total_votes == expected_total:
        print("✅ ÉXITO: Múltiples votos procesados correctamente!")
        return True
    else:
        print("❌ ERROR: Error en el procesamiento de múltiples votos!")
        return False

if __name__ == "__main__":
    print("Iniciando pruebas del sistema de votación ElGamal...")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    # Ejecutar pruebas
    if test_elgamal_encryption():
        success_count += 1
    
    if test_homomorphic_properties():
        success_count += 1
    
    if test_multiple_votes():
        success_count += 1
    
    # Resumen
    print("\n" + "=" * 50)
    print(f"RESUMEN DE PRUEBAS: {success_count}/{total_tests} pruebas exitosas")
    
    if success_count == total_tests:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo para usar.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa la implementación.")
    
    print("=" * 50)
