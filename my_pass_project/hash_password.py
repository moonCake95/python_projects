import hashlib

password = input('Enter your master password: ')
hashed_password = hashlib.sha256(password.encode()).hexdigest()

with open('hashed_password.txt', 'w') as f:
  f.write(hashed_password)

print('Hashed password saved securely. Delete this script after running it.')