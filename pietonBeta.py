import threading
import socket
import time
import random

pietoni = False

# Trimite mesaje despre prezența pietonului sus
def pieton(client_socket):
    global pietoni
    while True:
        if not pietoni:
            random_duration = random.uniform(3, 20)
            time.sleep(random_duration)
            state = "prezenta pieton"
            pietoni = True
            client_socket.sendall(state.encode())
            print(f"{state}")


# Funcția pentru a primi constant culoarea semaforului de la server
def primire_semafor(client_socket):
    global pietoni
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Conexiunea cu serverul a fost întreruptă.")
                break
            semafor_culoare = data.decode()
            print(f"{semafor_culoare}")

            # Acțiune în funcție de culoarea semaforului
            if semafor_culoare == "ROSU":
                pietoni = False
                print("Pietonii pot traversa.")
            elif semafor_culoare == "VERDE":
                print("Pietonii trebuie să aștepte.")

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


    # Pornire fir de execuție pentru simularea trimiterii mesajelor de la pieton jos
    threading.Thread(target=pieton, args=(client_socket,), daemon=True).start()

    # Pornire fir de execuție pentru recepționarea constantă a culorii semaforului
    threading.Thread(target=primire_semafor, args=(client_socket,), daemon=True).start()

    # Menține conexiunea deschisă și activează firurile
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deconectare...")
        client_socket.close()

if __name__ == "__main__":
    main()
