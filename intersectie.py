import socket
import threading

# Funcția pentru gestionarea conexiunii cu un client
def handle_client(client_socket):
    while True:
        try:
            # Primește date de la client
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Stare primită: {data.decode()}")
        except:
            break
    client_socket.close()

# Funcția principală
def main():
    server_host = '127.0.0.1'  # Adresa locală
    server_port = 12345        # Portul pentru conexiune

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)  # Permite până la 5 conexiuni simultane
    print("Server pornit și așteaptă conexiuni...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexiune acceptată de la {addr}")

        # Pornire fir de execuție pentru clientul conectat
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    main()
