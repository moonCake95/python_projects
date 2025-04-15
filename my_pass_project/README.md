# 🔐 Secure Password Manager

A secure and simple password manager written in Python, using Fernet encryption to store and retrieve passwords safely.

🔒 Encrypt passwords securely  
🔓 Decrypt only with a master password  
📂 Auto clipboard copying (optional)  
🛡️ Strong encryption with file permissions  

## 📌 Features

- ✔️ Key Generation: Generates an encryption key and securely stores it.
- ✔️ Strong Encryption: Converts data.txt into data.enc to prevent unauthorized access.
- ✔️ Decryption with Password: Restores data.txt, requiring authentication.
- ✔️ Secure File Storage: Stores secrets in ~/.your_hidden_dir/ with strict permissions.
- ✔️ Auto Clipboard Copying (Optional): Uses pyperclip to copy passwords securely.
- ✔️ GUI Support: Utilizes tkinter for the graphical interface and messagebox for alerts. Supports finding passwords by website and optionally by email.

## 📂 Project Structure

```
Secure Password Manager
├── main.py                      # Main GUI application
├── secure_data.py               # Encrypt/Decrypt script
├── hash_password.py (optional)  # Used once to generate hashed master password
├── README.md                    # This documentation
└── ~/.your_hidden_dir/          # Secure storage directory (hidden)
    ├── .secret.key              # Encryption key
    ├── .master_password         # Master password file
    └── secure_data              # Directory for encrypted data
        ├── data.enc             # Encrypted passwords file
        └── hashed_password.txt  # Optional hashed master password (temporary file)
```

## ⚙️ Installation

### 1️⃣ Install Dependencies

Ensure you have Python 3 installed, then run:

```
pip install cryptography 
pip install pyperclip
```

### 2️⃣ Generate Encryption Key (Run Once)

```
python secure_data.py
```

Choose Option 1 to generate a key. The key is saved at:  
📍 ~/.your_hidden_dir/.secret.key

### 3️⃣ Set Up Master Password

Run the following command:

```
echo -n 'your_secure_password' > ~/.your_hidden_dir/.master_password
chmod 600 ~/.your_hidden_dir/.master_password
```

Replace "your_secure_password" with a strong password.

### 4️⃣ Optional Hashed Master Password:

Create hash_password.py file temporarily:

```
import hashlib

master_password = "your_master_password"
hashed_pw = hashlib.sha256(master_password.encode()).hexdigest()

with open('hashed_password.txt', 'w') as file:
    file.write(hashed_password)
```

Run it once:

```
python hash_password.py
```

Then encrypt hashed_password.txt using your script and delete hash_password.py afterward.

## 📂 Secure Storage Setup

### Environment Variables

Set these paths in your .bash_profile or .zshrc to keep paths private and secure:

```
export SECRET_KEY_PATH=".your_hidden_dir/.secret.key"
export MASTER_PASS_PATH=".your_hidden_dir/.master_password"
export SECURE_DATA_PATH=".your_hidden_dir/data.enc"
export HASHED_PASSWORD_PATH=".your_hidden_dir/hashed_password.enc"
```

## 🚀 Usage

### Main Application (GUI)

Run your main application with:

```
python main.py
```

- Generate strong passwords.
- Easily store passwords.
- Clipboard auto-copy support.
- Find stored credentials by website and (optionally) by email.

Run the script and select an option:

```
python secure_data.py
```

### 🎛️ Menu Options

1. Generate Encryption Key (Run once)
2. Encrypt data.json → Creates data.enc & deletes original file
3. Decrypt data.enc → Restores data.json (requires master password)
4. Exit

### 🔽 Example: Encrypting a File

Choose an option:  
1️⃣  -> Generate Key (Run once)  
2️⃣  -> Encrypt data.json  
3️⃣  -> Decrypt data.enc  
4️⃣  -> Exit  
> 2  
🔒 data.json has been encrypted and saved as "data.enc".

## 🛡️ Security Considerations

- 🔹 Keep your encryption key safe! Losing it means losing access to encrypted data.
- 🔹 Set strict permissions on sensitive files:

```
chmod 600 ~/.your_hidden_dir/.secret.key ~/.your_hidden_dir/.master_password
```

- 🔹 Never store passwords in plaintext! Always encrypt your data.

## 📌 Troubleshooting

### ❌ Incorrect Password?

Check for extra newline characters:

```
cat ~/.your_hidden_dir/.master_password | od -c
```

If you see a \n, rewrite it:

```
echo -n "your_secure_password" > ~/.your_hidden_dir/.master_password
```

### ❌ Permission Denied?

Fix it with:

```
chmod 600 ~/.your_hidden_dir/.secret.key ~/.your_hidden_dir/.master_password
```

### ❌ Missing Key File?

If you see:

❌ Encryption key file not found

Regenerate it:

```
python secure_data.py  # Choose Option 1
```

## 📜 License

This project is for educational purposes. Use at your own risk.

## 🎯 Happy Securing! 🔐
