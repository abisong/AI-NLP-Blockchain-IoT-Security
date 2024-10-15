from cryptography.fernet import Fernet

# In a real-world scenario, this key should be securely stored and not hard-coded
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()
