import threading
import socket
import time

# Funcția pentru simularea semaforului
def masina(client_socket):
    while True:
        # Trimite mesajul despre prezența mașinii
        state = "prezenta masina"
        client_socket.sendall(state.encode())
        print(f"{state}")
        time.sleep(10)  # Trimite mesaj la fiecare 5 secunde (poate fi ajustat)

# Funcția pentru a primi culoarea semaforului de la server
def primire_semafor(client_socket):
    while True:
        try:
            # Așteaptă un mesaj de la server
            data = client_socket.recv(1024)
            if not data:
                print("Conexiunea cu serverul a fost întreruptă.")
                break
            semafor_culoare = data.decode()
            print(f"Culoare semafor: {semafor_culoare}")

            if semafor_culoare.lower() == " verde":
                print("Semaforul este verde! Mașinele pot trece.")
            elif semafor_culoare.lower() == " rosu":
                print("Semaforul este roșu! Mașina se oprește.")

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

    # Pornire fir de execuție pentru simularea trimiterii mesajelor de la "mașină"
    masina_thread = threading.Thread(target=masina, args=(client_socket,))
    masina_thread.daemon = True
    masina_thread.start()

    # Pornire fir de execuție pentru recepția culorii semaforului
    primire_thread = threading.Thread(target=primire_semafor, args=(client_socket,))
    primire_thread.daemon = True
    primire_thread.start()

    # Menține conexiunea deschisă
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deconectare...")
        client_socket.close()

if __name__ == "__main__":
    main()
