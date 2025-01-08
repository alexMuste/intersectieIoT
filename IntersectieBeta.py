import socket
import threading
import time

# Variabile globale pentru starea semaforului și numărul de pietoni
stare_semafor = "roșu"
pozitie_masina = ""
prezenta_pieton = ""
clients = []  # Lista de clienți conectați


# Funcția pentru gestionarea conexiunii cu un client
def handle_client(client_socket):
    global stare_semafor, pozitie_masina, prezenta_pieton

    try:
        while True:
            data = client_socket.recv(1024)  # Primește date de la client
            if not data:
                break  # Dacă clientul a deconectat

            message = data.decode()
            # Cerere Pieton
            if message.startswith("prezenta pieton"):
                prezenta_pieton = "prezenta pieton"
                print(f"prezenta pieton")

            # Cerere Masina
            elif message.startswith("prezenta masina"):
                pozitie_masina = "prezenta masina"
                print("prezenta masina")

            # Comenzi de schimbare a semaforului
            elif message == "verde":
                stare_semafor = "VERDE"
                print("Semafor VERDE.")

            elif message == "rosu":
                stare_semafor = "ROSU"
                print("Semafor ROSU.")

            # Răspunde cu starea semaforului
            state = f"{stare_semafor}"
            client_socket.sendall(state.encode())  # Trimite starea semaforului clientului



    except Exception as e:
        print(f"Eroare la gestionarea clientului: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)  # Elimină clientul din lista când se deconectează

# Funcția pentru a trimite actualizarea stării semaforului către toți clienții conectați
def update_semafor():
    global stare_semafor
    while True:
        try:
            # Trimite starea semaforului către fiecare client
            for client in clients:
                try:
                    semafor_message = f"{stare_semafor}"
                    client.sendall(semafor_message.encode())

                except Exception as e:
                       print(f"Eroare la trimiterea mesajului către client: {e}")
                       clients.remove(client)  # Elimină clientul din lista dacă nu mai răspunde

            time.sleep(5)  # Schimbă semaforul și trimite la intervale de 5 secunde

        except Exception as e:
            print(f"Eroare la actualizarea semaforului: {e}")
            break

def update_masini():
    global pozitie_masina
    while True:
        try:
            for client in clients:
                try:
                        masini = f"{pozitie_masina}"
                        client.sendall(masini.encode())
                except Exception as e:
                       print(f"Eroare la trimiterea mesajului către client: {e}")
                       clients.remove(client)  # Elimină clientul din lista dacă nu mai răspunde
            pozitie_masina = ""
            time.sleep(5)

        except Exception as e:
            print(f"Eroare la actualizarea semaforului: {e}")
            break

def update_pietoni():
    global prezenta_pieton
    while True:
        try:
            for client in clients:
                try:
                        pietoni = f"{prezenta_pieton}"
                        client.sendall(pietoni.encode())
                except Exception as e:
                       print(f"Eroare la trimiterea mesajului către client: {e}")
                       clients.remove(client)  # Elimină clientul din lista dacă nu mai răspunde
            prezenta_pieton = ""
            time.sleep(5)

        except Exception as e:
            print(f"Eroare la actualizarea semaforului: {e}")
            break
# Funcția principală
def main():
    server_host = '127.0.0.1'  # Adresa locală
    server_port = 12345        # Portul pentru conexiune

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)  # Permite până la 5 conexiuni simultane
    print("Server pornit și așteaptă conexiuni...")

    # Pornire fir de execuție pentru actualizarea semaforului
    threading.Thread(target=update_semafor, daemon=True).start()
    threading.Thread(target=update_masini, daemon=True).start()
    threading.Thread(target=update_pietoni, daemon=True).start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexiune acceptată de la {addr}")
        clients.append(client_socket)  # Adaugă clientul la lista de clienți conectați

        # Pornire fir de execuție pentru gestionarea clientului
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    main()
