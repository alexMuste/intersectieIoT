import socket
import threading

#variabila pentru a retine culoarea semaforului
semafor_state = ""

nr_pieton = 0

# Funcția pentru gestionarea conexiunii cu un client
def handle_client(client_socket):
    global semafor_state
    global nr_pieton

    while True:
        try:
            # Primește date de la client
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()

            #Cerere Pieton------------------------------
            if message.startswith("prezenta pieton"):
                # Trimite starea semaforului către client
                client_socket.sendall(semafor_state.encode())
                print(f"Prezenta Pieton")
                nr_pieton += 1
            #Cerere Masina---------------------------------
            if message.startswith("prezenta masina"):
                # Trimite starea semaforului către client
                client_socket.sendall(semafor_state.encode())
                print(f"Prezenta Masina")
                if semafor_state == " verde":
                    print("Masina trece")
                    print(f"Pietoni {nr_pieton} astepta")
                else:
                    print("Masina asteapta")
                    print(f"Trec {nr_pieton} pietoni")
                    nr_pieton = 0

            #Actualizare semafor-------------------------------
            elif message.startswith("Semafor:"):
                # Actualizează starea semaforului
                semafor_state = message.split(":")[1]
                print(f"Stare semafor actualizată: {semafor_state}")

        except Exception as e:
            print(f"Eroare la gestionarea clientului: {e}")
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
