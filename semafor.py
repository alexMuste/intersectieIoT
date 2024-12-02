import threading
import socket
import time

# Funcția pentru simularea semaforului
def semafor_logic(client_socket):
    while True:
        # Trimite starea VERDE
        state = "Semafor: verde"
        client_socket.sendall(state.encode())
        print(f"{state}")
        time.sleep(30)

        # Trimite starea ROȘU
        state = "Semafor: rosu"
        client_socket.sendall(state.encode())
        print(f"{state}")
        time.sleep(10)

# Funcția principală
def main():
    # Configurare conexiune către server
    server_host = '127.0.0.1'  # Adresa serverului
    server_port = 12345        # Portul serverului

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    print("Conectat la server.")

    # Pornire fir de execuție pentru logica semaforului
    semafor_thread = threading.Thread(target=semafor_logic, args=(client_socket,))
    semafor_thread.daemon = True
    semafor_thread.start()

    # Menține conexiunea deschisă
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deconectare...")
        client_socket.close()

if __name__ == "__main__":
    main()
