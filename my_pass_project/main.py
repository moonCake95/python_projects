from tkinter import *
from tkinter import messagebox, simpledialog
import random
import string
import pyperclip
import hashlib
import os
import json

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
  if os.path.exists('data.enc') and not os.path.exists('data.json'):
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
  
  website = website_entry.get()
  email = user_entry.get()
  password = pass_entry.get()
  new_entry = {
    'email': email,
    'password': password,
  }

  if len(website) == 0 or len(email) == 0 or len(password) == 0:
    messagebox.showwarning(title='Warning', message='Please make sure all fields are filled out.')
    return
  else:
    is_ok = messagebox.askokcancel(title='website', message=f'These are the details entered: Website: {website}' 
                                                            f'\nEmail: {email}'
                                                            f'\nPassword: {password} \nIs it ok to save?')
    
    if is_ok:
      try:
        with open('data.json', 'r') as f:
          data = json.load(f)
      except FileNotFoundError:
        data = {}

      if website in data:
        existing_entries = data[website]
        if isinstance(existing_entries, list):
          # Prevent duplicate email for the same website
          if not any(entry['email'] == email for entry in existing_entries):
            existing_entries.append(new_entry)
          else:
            messagebox.showinfo("Info", f"Entry for {email} at {website} already exists.")
            return
        else:
          if existing_entries['email'] != email:
            data[website] = [existing_entries, new_entry]
          else:
            messagebox.showinfo("Info", f"Entry for {email} at {website} already exists.")
            return
      else:
        data[website] = [new_entry]
      
      with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
        
      website_entry.delete(0, END)
      user_entry.delete(0, END)
      pass_entry.delete(0, END)
      messagebox.showinfo(title='Success', message='Password has been saved!')

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
  
  website_data = website_entry.get()
  user_data = user_entry.get()
  try:
    with open('data.json', 'r') as data_file:
      data = json.load(data_file)
  except FileNotFoundError:
    messagebox.showerror("Error", "No data file found.")
    return
  else:
    if website_data in data:
      entries = data[website_data]
      if isinstance(entries, list):
        for entry in entries:
          if user_data == "" or entry['email'] == user_data:
            messagebox.showinfo(
              title='Found',
              message=f'Website: {website_data}\nEmail: {entry["email"]}\nPassword: {entry["password"]}'
            )
            pyperclip.copy(entry['password'])
            return
        messagebox.showinfo('Not Found', f'No matching entry for {user_data} at {website_data}.')
      else:
        entry = entries
        if user_data == "" or entry['email'] == user_data:
          messagebox.showinfo(
              title='Found',
              message=f'Website: {website_data}\nEmail: {entry["email"]}\nPassword: {entry["password"]}'
            )
          pyperclip.copy(entry['password'])
        else:
          messagebox.showinfo('Not Found', f'No matching entry for {user_data} at {website_data}.')
    else:
      messagebox.showinfo('Not Found', f'No details for {website_data} exist.')
  

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
website_entry = Entry(width=21)
user_entry = Entry(width=35)
pass_entry = Entry(width=21)

website_entry.focus()  # Focus on website entry field when the window opens

website_entry.grid(row=1, column=1, sticky='EW')
user_entry.grid(row=2, column=1, columnspan=2, sticky='EW')
pass_entry.grid(row=3, column=1, sticky='EW')

#  <------ Buttons ------>
search_btn = Button(text='Search', command=find_password)
generate_pass_btn = Button(text='Generate Password', command=generate_password)
add_btn = Button(text='Add', width=36, command=save)

search_btn.grid(row=1, column=2, sticky='EW')
generate_pass_btn.grid(row=3, column=2, sticky='EW')
add_btn.grid(row=4, column=1, columnspan=2, sticky='EW')

window.mainloop()