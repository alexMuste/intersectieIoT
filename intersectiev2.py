import socket
import threading
import time

# Variabile pentru a reține starea semaforului și numărul de pietoni
semafor_state = "roșu"
nr_pieton = 0
semafor_timer = 0  # Cronometru pentru schimbarea semaforului


# Funcția pentru gestionarea conexiunii cu un client
def handle_client(client_socket):
    global semafor_state, nr_pieton, semafor_timer

    while True:
        try:
            # Primește date de la client (nu facem nimic special pentru că serverul schimbă starea automat)
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode()

            # Cerere Pieton
            if message.startswith("prezenta pieton"):
                nr_pieton += 1
                print(f"Prezenta pieton! Total pietoni: {nr_pieton}")

            # Cerere Masina
            if message.startswith("prezenta masina"):
                print(f"Prezenta masina")

            # Răspunde cu starea semaforului și numărul de pietoni
            state = f"Semafor:{semafor_state} Pietoni:{nr_pieton}"
            client_socket.sendall(state.encode())

        except Exception as e:
            print(f"Eroare la gestionarea clientului: {e}")
            break

    client_socket.close()


# Funcția de actualizare a stării semaforului
def update_semafor():
    global semafor_state, semafor_timer

    while True:
        # Cronometrează timpul semaforului
        if semafor_state == "verde":
            if semafor_timer >= 30:  # După 30 secunde, schimbă la roșu
                semafor_state = "roșu"
                semafor_timer = 0
                print(f"Stare semafor schimbată: {semafor_state}")
        elif semafor_state == "roșu":
            if semafor_timer >= 10:  # După 10 secunde, schimbă la verde
                semafor_state = "verde"
                semafor_timer = 0
                print(f"Stare semafor schimbată: {semafor_state}")

        # Crește timer-ul
        semafor_timer += 1
        time.sleep(1)  # Incrementăm timer-ul la fiecare secundă


# Funcția principală
def main():
    server_host = '127.0.0.1'  # Adresa locală
    server_port = 12345  # Portul pentru conexiune

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)  # Permite până la 5 conexiuni simultane
    print("Server pornit și așteaptă conexiuni...")

    # Pornire fir de execuție pentru actualizarea semaforului
    threading.Thread(target=update_semafor, daemon=True).start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexiune acceptată de la {addr}")

        # Pornire fir de execuție pentru clientul conectat
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True
        client_thread.start()


if __name__ == "__main__":
    main()
