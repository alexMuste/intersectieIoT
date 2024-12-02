import pygame
import sys
import socket
import threading
import time

# Inițializează Pygame
pygame.init()

# Dimensiunea ferestrei
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulare Intersecție")

# Culori
background_color = (50, 50, 50)
road_color = (100, 100, 100)
red_light = (255, 0, 0)
green_light = (0, 255, 0)
car_color = (0, 0, 255)
pedestrian_color = (0, 255, 0)

# Conectare la server
server_host = '127.0.0.1'
server_port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# Variabile pentru stocarea datelor primite
semafor_state = "roșu"
vehicles = [{"x": 100, "y": 250}]  # Pozițiile vehiculelor (fixe)
pedestrians = [{"x": 400, "y": 300}]  # Pozițiile pietonilor (fixe)

# Funcția pentru actualizarea datelor de la server
def fetch_server_data():
    global semafor_state, vehicles, pedestrians

    while True:
        try:
            # Trimite cerere către server pentru a obține starea semaforului și numărul de pietoni
            client_socket.sendall(b"prezenta masina")  # Sau altă cerere pentru a cere starea semaforului
            data = client_socket.recv(1024)
            if data:
                state = data.decode()
                # Extrage starea semaforului și numărul de pietoni din mesaj
                parts = state.split()
                semafor_state = parts[0].split(":")[1]
                nr_pietoni = int(parts[1].split(":")[1])
                print(f"Stare semafor: {semafor_state}, Pietoni: {nr_pietoni}")
        except Exception as e:
            print(f"Eroare la conectarea cu serverul: {e}")
            break
        time.sleep(1)  # Actualizare la fiecare 1 sec

# Pornire fir pentru actualizarea datelor
threading.Thread(target=fetch_server_data, daemon=True).start()

# Funcția pentru afișarea semaforului
def draw_semaphore(x, y, state):
    color = green_light if state == "verde" else red_light
    pygame.draw.rect(screen, (50, 50, 50), (x, y, 50, 150))  # Fundal semafor
    pygame.draw.circle(screen, color, (x + 25, y + 50), 20)

# Funcția principală de afișare
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Umple ecranul cu fundalul
    screen.fill(background_color)

    # Desenează drumul (zona intersecției)
    pygame.draw.rect(screen, road_color, (300, 200, 200, 200))

    # Desenează semaforul
    draw_semaphore(370, 180, semafor_state)

    # Actualizare mișcare vehicule/pietoni pe baza semaforului
    if semafor_state == "verde":
        # Mașinile se mișcă, pietonii așteaptă
        for vehicle in vehicles:
            vehicle["x"] += 2
            if vehicle["x"] > 800:  # Resetare poziție dacă ies din ecran
                vehicle["x"] = -40

    elif semafor_state == "roșu":
        # Pietonii se mișcă, mașinile așteaptă
        for pedestrian in pedestrians:
            pedestrian["y"] -= 2
            if pedestrian["y"] < 0:  # Resetare poziție dacă ies din ecran
                pedestrian["y"] = 600

    # Desenează vehiculele
    for vehicle in vehicles:
        pygame.draw.rect(screen, car_color, (vehicle["x"], vehicle["y"], 40, 20))

    # Desenează pietonii
    for pedestrian in pedestrians:
        pygame.draw.circle(screen, pedestrian_color, (pedestrian["x"], pedestrian["y"]), 10)

    # Actualizează fereastra
    pygame.display.flip()

    # Controlează viteza animației
    clock.tick(60)  # 60 FPS
