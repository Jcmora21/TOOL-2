# transfer.py
import socket
import random
import os

# Folder to store files
FOLDER = 'files'
os.makedirs(FOLDER, exist_ok=True)

def generate_pin():
    return str(random.randint(100000, 999999))

def send_file():
    filename = input("Enter the file name to send (including extension): ")
    filepath = os.path.join(FOLDER, filename)
    
    if not os.path.isfile(filepath):
        print("File not found!")
        return

    server = socket.socket()
    server.bind(('0.0.0.0', 0))  # Random port
    server.listen(1)

    ip = socket.gethostbyname(socket.gethostname())
    port = server.getsockname()[1]
    pin = generate_pin()

    print(f"\n=== Send this PIN to the receiver: {pin} ===")
    print(f"IP: {ip} Port: {port}\nWaiting for connection...")

    conn, addr = server.accept()
    print(f"Connected to {addr}")

    # Step 1: verify the PIN
    received_pin = conn.recv(1024).decode()
    if received_pin != pin:
        print("Wrong PIN! Connection refused.")
        conn.close()
        return

    # Step 2: send the file
    with open(filepath, 'rb') as f:
        data = f.read(1024)
        while data:
            conn.send(data)
            data = f.read(1024)

    print("File sent successfully!")
    conn.close()

def receive_file():
    server_ip = input("Sender IP: ")
    server_port = int(input("Sender port: "))
    pin = input("Received PIN: ")

    client = socket.socket()
    client.connect((server_ip, server_port))

    # Send the PIN first
    client.send(pin.encode())

    filename = input("Enter a name to save the file (including extension): ")
    save_path = os.path.join(FOLDER, filename)

    with open(save_path, 'wb') as f:
        while True:
            data = client.recv(1024)
            if not data:
                break
            f.write(data)

    print(f"File '{filename}' received successfully!")
    client.close()

def main():
    print("\nWelcome to Send-File!")
    print("[1] Send file")
    print("[2] Receive file")
    choice = input("Choose an option: ")

    if choice == '1':
        send_file()
    elif choice == '2':
        receive_file()
    else:
        print("Invalid option.")

if __name__ == '__main__':
    main()
