from cryptography.fernet import Fernet
import getpass
import os
import json

# -------------------- GENERATE A KEY (Run this once & save the key) --------------------
def generate_key():
    key = Fernet.generate_key()
    key_path = os.environ['SECRET_KEY_PATH']  # Save key in a hidden file
    os.makedirs(os.path.dirname(key_path), exist_ok=True)  # Ensure directory exists
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    print('🔑 Key Generated! Save it safely.')

# -------------------- LOAD THE ENCRYPTION KEY --------------------
def load_key():
    key_path = os.environ['SECRET_KEY_PATH']  # Hidden path
    if not os.path.exists(key_path):
        raise ValueError("❌ Encryption key file not found. Run 'python secure_data.py' and generate a key first.")
    with open(key_path, 'rb') as key_file:
        return key_file.read()  # Read the key securely

# -------------------- ENCRYPT FILE --------------------
def encrypt_file(filename):
  key = load_key()
  fernet = Fernet(key)
  # Read the original file
  with open(filename, 'rb') as file:
    file_data = file.read()
  encrypted_data = fernet.encrypt(file_data)   # Encrypt the data
  
  encrypted_path = os.environ['SECURE_DATA_PATH']
  os.makedirs(os.path.dirname(encrypted_path), exist_ok=True)  # Ensure directory exists
  # Save encrypted file
  with open(encrypted_path, 'wb') as file:
    file.write(encrypted_data)
  
  print(f'🔒 {filename} has been encrypted and saved as "data.enc".')
  
  # Securely delete the original file
  os.remove(filename)
  
  # Encrypt hashed_file.txt
  password_file = 'hashed_password.txt'
  if os.path.exists(password_file):
    with open(password_file, 'rb') as f:
      password_data = f.read()
    encrypt_password = fernet.encrypt(password_data)
    
    encrypted_pass_path = os.environ['SECURE_HASH_PATH']
    os.makedirs(os.path.dirname(encrypted_pass_path), exist_ok=True) # Ensure directory exists
    with open(encrypted_pass_path, 'wb') as f:
      f.write(encrypt_password)
    
    print('🔒 hashed_file has been encrypted and saved as "hashed_password.enc"')
    
    # Securely delete the original hashed password file
    os.remove(password_file)

# -------------------- LOAD MASTER PASSWORD --------------------
def load_master_password():
  password_path = os.environ['MASTER_PASS_PATH']
  if not os.path.exists(password_path):
    raise ValueError('❌ Master password file not found. Set it up first.')
  with open(password_path, 'r') as f:
    return f.read().strip()

# -------------------- DECRYPT FILE --------------------
def decrypt_file():
  key = load_key()
  fernet = Fernet(key)
  
  # Request password before decryption
  master_password = getpass.getpass('🔑 Enter master password: ')
  stored_password = load_master_password()
  if master_password != stored_password:
    print('❌ Incorrect password. Decryption aborted.')
    return
  
  # path for encrypted files
  encrypted_data_path = os.environ['SECURE_DATA_PATH']
  encrypted_pass_path = os.environ['SECURE_HASH_PATH']
  
  # Check if encrypted files exist
  if not os.path.exists(encrypted_data_path):
    print('❌ Encrypted file not found. Decryption aborted.')
    return
  
  # Read the encrypted file
  with open(encrypted_data_path, 'rb') as file:
    encrypted_data = file.read()
  decrypted_data = fernet.decrypt(encrypted_data)  # Decrypt the data
  
  # Convert decrypted bytes into dictionary
  decoded_data = decrypted_data.decode('utf-8')
  json_data = json.loads(decoded_data)
  
  # Save to JSON file
  with open('data.json', 'w') as f:
    json.dump(json_data, f, indent=4)
  
  print('🔓 File decrypted and saved as "data.json".')
  
  
  # Decrypt hashed_password file
  if os.path.exists(encrypted_pass_path):
    with open(encrypted_pass_path, 'rb') as f:
      encrypted_password = f.read()
    decrypted_password = fernet.decrypt(encrypted_password)
    
    with open('hashed_password.txt', 'wb') as f:
      f.write(decrypted_password)
    
    print('🔓 hashed_password file has been decrypted and restored.')

# -------------------- MAIN MENU --------------------
if __name__ == '__main__':
  while True:
    choice = input('\nChoose an option:\n1️⃣  -> Generate Key (Run once)\n2️⃣  -> Encrypt data.json\n3️⃣  -> Decrypt data.enc\n4️⃣  -> Exit\n> ')
    if choice == '1':
      generate_key()
    elif choice == '2':
      encrypt_file('data.json')
    elif choice == '3':
      decrypt_file()
    elif choice == '4':
      break
    else:
      print('❌ Invalid option. Please try again.')