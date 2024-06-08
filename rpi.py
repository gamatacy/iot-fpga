from flask import Flask
from flask import request, send_file
import random
import subprocess

import os

is_busy = False
app = Flask(__name__)

@app.route('/run', methods = ['GET', 'POST'])
def run():
    hash = random.getrandbits(128)
    uploaded_files = request.files
    folder_name = 'request_' + str(hash)
    os.mkdir(folder_name)

    for file_name, file in uploaded_files.items():
        file.save(os.path.join(folder_name, file.filename))  

    command = f"cd {folder_name} && iverilog -g2005-sv -o {hash} ./*.*v && vvp {hash}" 
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    files = {}  # Укажите путь к файлу, который нужно отправить
    files[0] = open(folder_name + '/dump.vcd', 'rb')

    # return 'Request №' + str(hash) + ' executed', files
    return send_file(folder_name + '/dump.vcd', as_attachment=True)

@app.route('/busy', methods = ['GET', 'POST'])
def busy():
    print(request.data)
    if is_busy:
        return "Busy", 252
    return "Success", 200

if __name__ == '__main__':
    if os.environ.get('RPI_HOST') != '735':
        app.run(debug=True, port=80, host=os.environ.get('RPI_HOST'))
