import random
import secrets
from Crypto.Util import number
from Crypto.Random import get_random_bytes
import hashlib

class ElGamalCrypto:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.p = None
        self.g = None
        self.private_key = None
        self.public_key = None
    
    def generate_prime(self, bits):
        """Generate a prime number of specified bits"""
        return number.getPrime(bits)
    
    def generate_keys(self):
        """Generate ElGamal key pair"""
        # Generate a large prime p
        self.p = self.generate_prime(self.key_size)
        
        # Generate generator g
        self.g = random.randrange(2, self.p - 1)
        
        # Generate private key (random number between 1 and p-2)
        self.private_key = random.randrange(1, self.p - 1)
        
        # Calculate public key: g^private_key mod p
        self.public_key = pow(self.g, self.private_key, self.p)
        
        return {
            'p': self.p,
            'g': self.g,
            'public_key': self.public_key,
            'private_key': self.private_key
        }
    
    def encrypt(self, message, public_key_data):
        """Encrypt a message using ElGamal encryption"""
        p = public_key_data['p']
        g = public_key_data['g']
        public_key = public_key_data['public_key']
        
        # Convert message to integer
        if isinstance(message, str):
            message_int = int.from_bytes(message.encode('utf-8'), 'big')
        else:
            message_int = message
        
        # Ensure message is smaller than p
        if message_int >= p:
            raise ValueError("Message too large for key size")
        
        # Generate random k
        k = random.randrange(1, p - 1)
        
        # Calculate c1 = g^k mod p
        c1 = pow(g, k, p)
        
        # Calculate c2 = message * (public_key^k) mod p
        c2 = (message_int * pow(public_key, k, p)) % p
        
        return (c1, c2)
    
    def decrypt(self, ciphertext, private_key_data):
        """Decrypt a ciphertext using ElGamal decryption"""
        c1, c2 = ciphertext
        p = private_key_data['p']
        private_key = private_key_data['private_key']
        
        # Calculate s = c1^private_key mod p
        s = pow(c1, private_key, p)
        
        # Calculate s_inv = s^(-1) mod p
        s_inv = pow(s, p - 2, p)
        
        # Calculate message = c2 * s_inv mod p
        message = (c2 * s_inv) % p
        
        return message
    
    def encrypt_vote(self, vote_option, public_key_data):
        """Encrypt a vote option
        
        Can accept:
        - Simple integer or string values
        - Dictionary with vote data (will be converted to JSON string)
        """
        if isinstance(vote_option, dict):
            # Convert dict to string for encryption
            import json
            vote_str = json.dumps(vote_option)
            return self.encrypt(vote_str, public_key_data)
        else:
            # Direct encryption for integers and strings
            return self.encrypt(vote_option, public_key_data)
    
    def decrypt_vote(self, encrypted_vote, private_key_data):
        """Decrypt a vote
        
        Returns:
        - Dictionary if the original vote was a dictionary (can be parsed as JSON)
        - Original integer or string value otherwise
        """
        decrypted_result = self.decrypt(encrypted_vote, private_key_data)
        
        # Try to convert back to bytes and then decode as JSON if possible
        try:
            byte_length = (decrypted_result.bit_length() + 7) // 8
            decrypted_bytes = decrypted_result.to_bytes(byte_length, 'big')
            decoded_str = decrypted_bytes.decode('utf-8')
            
            # Check if it's valid JSON (dictionary)
            import json
            try:
                return json.loads(decoded_str)
            except json.JSONDecodeError:
                # Not JSON, just return the decoded string
                return decoded_str
        except:
            # If any error occurs, return the original integer
            return decrypted_result
    
    def homomorphic_add(self, ciphertext1, ciphertext2, p):
        """Add two ciphertexts homomorphically"""
        c1_1, c2_1 = ciphertext1
        c1_2, c2_2 = ciphertext2
        
        # Homomorphic addition: (c1_1 * c1_2, c2_1 * c2_2)
        new_c1 = (c1_1 * c1_2) % p
        new_c2 = (c2_1 * c2_2) % p
        
        return (new_c1, new_c2)
    
    @staticmethod
    def hash_vote(vote_data):
        """Create a hash of vote data for integrity verification"""
        vote_str = str(vote_data)
        return hashlib.sha256(vote_str.encode()).hexdigest()
