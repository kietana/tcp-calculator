from socket import *

serverAddress = ('140.118.145.198', 5000)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverAddress)

# Receive server's reply
print(clientSocket.recv(1024).decode())

while True:

    exp = ''  # Initialize expression string
    print("\nMode Selection:")
    print("-----------------------------------")
    print("1. Manual")
    print("2. Read file")
    print("-----------------------------------")
    mode = input("Select a mode (q to exit): ")

    # Exit the service
    if mode == 'q':
        clientSocket.send(mode.encode())
        print(clientSocket.recv(1024).decode())
        break

    # Invalid type of mode
    if mode not in {'1', '2'}:
        print("Invalid mode. Select again.")
        continue

    # Send valid mode to server
    clientSocket.send(mode.encode())
    print("Mode: " + mode)

    while mode == '1':
        exp = input("Enter expression (q to exit): ")
        clientSocket.send(exp.encode())
        if exp == 'q':
            break  # Exit the mode
        answer = clientSocket.recv(1024).decode()
        print("Answer: " + answer)

    while mode == '2':
        file_name = input("File name (q to exit): ")
        if file_name == 'q':
            clientSocket.send(file_name.encode())
            break  # Exit the mode

        try:
            file = open(file_name, 'r')
        except FileNotFoundError:
            print("File Not Found!")
        else:
            for line in file:
                exp = line.strip('\n')
                clientSocket.send(exp.encode())
                print("Answer: " + clientSocket.recv(1024).decode())
            file.close()

    print("-----------------------------------\nExited the mode.\n")

clientSocket.close()
