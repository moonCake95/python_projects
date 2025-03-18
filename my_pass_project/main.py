from tkinter import *
from tkinter import messagebox, simpledialog
import random
import string
import pyperclip
import hashlib
import os

# ---------------------------- PASSWORD SECURITY ------------------------------- #
def load_hashed_password():
  try:
    with open('hashed_password.txt', 'r') as f:
      return f.read().strip()
  except FileNotFoundError:
    messagebox.showerror('Error', 'Master password not set! Run "hash_password.py" first.')
    return None

def verify_password():
  stored_hash = load_hashed_password()
  if stored_hash is None:
    return False
  
  user_input = simpledialog.askstring('Authentication', 'Enter master password:', show='*')
  user_hash = hashlib.sha256(user_input.encode()).hexdigest()
  
  if user_hash == stored_hash:
    return True
  else:
    messagebox.showerror('Error', 'Incorrect Password! Access Denied.')
    return False

# ---------------------------- CHECK ENCRYPTED DATA ------------------------------- #
def check_encrypted_file():
  '''Check if data.enc exists and data.txt does not exist.'''
  if os.path.exists('data.enc') and not os.path.exists('data.txt'):
    messagebox.showerror('Error', 'Encrypted file detected! Please decrypt "data.enc" first.')
    return False
  return True

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
  letters = string.ascii_letters + string.digits + string.punctuation
  password = ''.join(random.choice(letters) for i in range(12))
  pass_entry.delete(0, END)
  pass_entry.insert(END, password)
  pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
  if not verify_password():
    return # Prevent saving if authentication fails
  
  if not check_encrypted_file():
    return # Prevent saving if encrypted data exists

  if len(website_entry.get()) == 0 or len(user_entry.get()) == 0 or len(pass_entry.get()) == 0:
    messagebox.showwarning(title='Warning', message='Please make sure all fields are filled out.')
    return
  
  is_ok = messagebox.askokcancel(title='website', message=f'These are the details entered: Website: {website_entry.get()}' 
                                                          f'\nEmail: {user_entry.get()}'
                                                          f'\nPassword: {pass_entry.get()} \nIs it ok to save?')
  
  if is_ok:
    with open('data.txt', 'a') as f:
      f.write(f'Website: {website_entry.get()} | Username or Email: {user_entry.get()} | Password: {pass_entry.get()}\n')
      website_entry.delete(0, END)
      user_entry.delete(0, END)
      pass_entry.delete(0, END)
      messagebox.showinfo(title='Success', message='Password has been saved!')

# ---------------------------- INITIAL CHECK BEFORE STARTING ------------------------------- #
if not check_encrypted_file():
  exit()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager 🔑")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_image = PhotoImage(file='logo.png')
canvas.create_image(125, 100,image=logo_image)
canvas.grid(row=0, column=1)

#  <------ Labels ------>
website_label = Label(text='Website:')
user_label = Label(text='Email/Username:')
pass_label = Label(text='Password:')

website_label.grid(row=1, column=0)
user_label.grid(row=2, column=0)
pass_label.grid(row=3, column=0)

#  <------ Entry fields ------>
website_entry = Entry(width=35)
user_entry = Entry(width=35)
pass_entry = Entry(width=21)

website_entry.focus()  # Focus on website entry field when the window opens

website_entry.grid(row=1, column=1, columnspan=2, sticky='EW')
user_entry.grid(row=2, column=1, columnspan=2, sticky='EW')
pass_entry.grid(row=3, column=1, sticky='EW')

#  <------ Buttons ------>
generate_pass_btn = Button(text='Generate Password', command=generate_password)
add_btn = Button(text='Add', width=36, command=save)

generate_pass_btn.grid(row=3, column=2, sticky='EW')
add_btn.grid(row=4, column=1, columnspan=2, sticky='EW')



window.mainloop()