import threading
import socket
import time
import random

masini = False


def masina(client_socket):
    global masini
    while True:
        # Trimite mesajul despre prezența mașinii
        if not masini:
            random_duration = random.uniform(0.5, 1)
            time.sleep(random_duration)
            state = "prezenta masina"
            masini = True
            client_socket.sendall(state.encode())
            print(f"{state}")

# Funcția pentru a primi culoarea semaforului de la server
def primire_semafor(client_socket):
    global masini
    while True:
        try:
            # Așteaptă un mesaj de la server
            data = client_socket.recv(1024)
            if not data:
                print("Conexiunea cu serverul a fost întreruptă.")
                break
            semafor_culoare = data.decode()
            print(f"{semafor_culoare}")

            if semafor_culoare == "VERDE":
                masini = False

                print("Semaforul este verde! Masinele pot trece")
            elif semafor_culoare == "ROSU":
                print("Semaforul este roșu! Mașinele asteapta.")

        except Exception as e:
            print(f"Eroare la recepția datelor: {e}")
            break
# Funcția principală
def main():
    # Configurare conexiune către server
    server_host = '127.0.0.1'  # Adresa serverului
    server_port = 12345        # Portul serverului

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    print("Conectat la server.")

    # Pornire fir de execuție pentru simularea trimiterii mesajelor de la "mașină_dreapta"
    threading.Thread(target=masina, args=(client_socket,),daemon=True).start()

    threading.Thread(target=primire_semafor, args=(client_socket,),daemon = True).start()

    # Menține conexiunea deschisă
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deconectare...")
        client_socket.close()

if __name__ == "__main__":
    main()
