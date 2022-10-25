


def send_command(command: bytes):
    time.sleep(0.1)
    print("Client: ", command.decode("utf-8"), end='')
    socket_manager.send(command)
    while True:
        buffer = socket_manager.recv(1024).decode("utf-8")

        if buffer[:4] == "xyz-":
            print(buffer)
            buffer = socket_manager.recv(1024).decode("utf-8")
            print(buffer)
        else:
            match buffer[0]:
                case '2':
                    print("Server: Successful response: ", buffer, end='')
                case '4' | '5':
                    print("Server: Command cannot be executed: ", buffer, end='')
                case '1' | '3':
                    print("Server: Error or incomplete answer: ", buffer, end='')
            match buffer[1]:
                case '0':
                    print("Response type: Syntactic")
                case '1':
                    print("Response type: Informational. Corresponds to the informational message.")
                case '2':
                    print("Response type: Compound. The message refers to either a control connection or a data connection.")
                case '3':
                    print("Response type: Corresponds to messages about user authentication and rights.")
                case '4':
                    print("Response type: Undefined.")
                case '5':
                    print("Response type: File system. Corresponds to a file system status message.")
            break
    return buffer
