import requests

url = 'http://fpga_'  

def check_machine_avaliable(num):
    return requests.get(url+str(num)+"/busy").status_code == 200

def help_cmd():
    pass

def list_cmd():
    pass

def run_cmd():
    list_cmd()
    machine = int(input("Enter machine number >>> "))
    
    if not check_machine_avaliable(machine):
        print("Machine is busy")
        return 
    
    sources = input("Enter design filenames separated by space: ").split()
    files = {}  # Укажите путь к файлу, который нужно отправить

    for s in sources:
        files[s] = open(s, 'rb')

    response = requests.post(url +str(machine) + "/run", files=files)

    with open('waves/dump.vcd', 'wb') as file:
        file.write(response.content)
        
commands = {
    "help" : help_cmd,
    "list" : list_cmd,
    "run" : run_cmd
}

def invoke_cmd(cmd):
    try:
        commands[cmd]()
    except Exception as e:
        print(e)
        print("unknown command")

def run():
    while True:
        cmd = input("Enter command >>> ")
        invoke_cmd(cmd)

if __name__ == '__main__':
    run()
