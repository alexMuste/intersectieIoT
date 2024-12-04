import pygame
import sys
import socket
import threading
import time

import math

# Inițializează Pygame
pygame.init()

# Dimensiunea ferestrei
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulare Intersecție")

# Culori
background_color = (216, 216, 216)
road_color = (100, 100, 100)
red_light = (255, 0, 0)
green_light = (0, 255, 0)
car_color = (0, 0, 255)
pedestrian_color = (64, 128, 128)

# Conectare la server
server_host = '127.0.0.1'
server_port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# Variabile pentru stocarea datelor primite
stare_semafor = "roșu"
vehicles = [{"x": 100, "y": 250}]  # Pozițiile vehiculelor (fixe)
pedestrians = [{"x": 400, "y": 370}]  # Pozițiile pietonilor (fixe)
semafor_pietoni = "roșu"  # Semaforul pietonilor începe pe roșu
import math


def detect_collision(pedestrian, vehicle, pedestrian_radius=10, vehicle_width=40, vehicle_height=20, y_min=180,
                     y_max=370):
    # Verifică dacă pietonul și vehiculul sunt în intervalul dorit pe axa Y
    if not (y_min <= pedestrian["y"] <= y_max) or not (y_min <= vehicle["y"] <= y_max):
        return False

    # Calculăm distanța dintre centrele celor două obiecte (pieton și vehicul)
    # Vehiculul va fi considerat un dreptunghi
    vehicle_center_x = vehicle["x"] + vehicle_width / 2
    vehicle_center_y = vehicle["y"] + vehicle_height / 2

    # Distanța dintre centrul pietonului și centrul vehiculului
    distance = math.sqrt((vehicle_center_x - pedestrian["x"]) ** 2 + (vehicle_center_y - pedestrian["y"]) ** 2)

    # Dacă distanța este mai mică sau egală cu suma razei pietonului și jumătate din lățimea vehiculului
    # (considerând vehiculul ca dreptunghi)
    if distance <= pedestrian_radius + (vehicle_width / 2):
        print(
            f"Coliziune detectată între pietonul la ({pedestrian['x']}, {pedestrian['y']}) și vehiculul la ({vehicle['x']}, {vehicle['y']})")
        return True
    return False


def draw_liniiT(start_x, start_y, end_x, width, stripe_width=10, gap=10, color=(255, 255, 255)):
    x = start_x
    while x < end_x-1:
        pygame.draw.rect(screen, color, (start_y, x, stripe_width+100, width))
        x += stripe_width + gap  # Lasă un spațiu între benzi



# Funcția pentru actualizarea datelor de la server
def fetch_server_data():
    global stare_semafor, vehicles, pedestrians

    while True:
        try:
            # Trimite cerere către server pentru a obține starea semaforului și numărul de pietoni
            client_socket.sendall(b"prezenta masina")  # Sau altă cerere pentru a cere starea semaforului
            data = client_socket.recv(1024)
            if data:
                state = data.decode()
                # Extrage starea semaforului și numărul de pietoni din mesaj
                parts = state.split()
                stare_semafor = parts[0].split(":")[1]
                nr_pietoni = int(parts[1].split(":")[1])
                print(f"Stare semafor: {stare_semafor}, Pietoni: {nr_pietoni}")
        except Exception as e:
            print(f"Eroare la conectarea cu serverul: {e}")
            break
        time.sleep(1)  # Actualizare la fiecare 1 sec

# Pornire fir pentru actualizarea datelor
threading.Thread(target=fetch_server_data, daemon=True).start()

# Funcția pentru afișarea semaforului
def draw_semafor1(x, y, state):
    color = green_light if state == "verde" else red_light
    pygame.draw.rect(screen, (20, 20, 20), (x, y, 40, 70))  # Fundal semafor
    pygame.draw.circle(screen, color, (x + 20, y + 23), 15)

def draw_semafor2(x,y,state):
    color = green_light if state == "verde" else red_light
    pygame.draw.rect(screen, (20, 20, 20), (x, y, 40, 50))  # Fundal semafor
    pygame.draw.circle(screen, color, (x + 20, y + 23), 8)

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
    pygame.draw.rect(screen, road_color, (0, 200, 1000, 150))

    # Adaugă trecerea de pietoni
    draw_liniiT(start_x=202, start_y=350, end_x=352, width=20, stripe_width=15, gap=10)

    # Desenează semaforul
    draw_semafor1(300, 90, stare_semafor)
    draw_semafor2(300, 360, semafor_pietoni)

    # Actualizare mișcare vehicule/pietoni pe baza semaforului
    if stare_semafor == "verde":
        # Mașinile se mișcă, pietonii așteaptă
        # Controlează viteza animației
        clock.tick(60)  # 60 FPS
        for vehicle in vehicles:
            vehicle["x"] += 2
            if vehicle["x"] > 800:  # Resetare poziție dacă ies din ecran
                vehicle["x"] = -40

    elif stare_semafor == "roșu":
        # Pietonii se mișcă, mașinile așteaptă
        # Controlează viteza animației
        clock.tick(20)  # 20 FPS
        for pedestrian in pedestrians:
            pedestrian["y"] -= 2
            if pedestrian["y"] < 180:  # Resetare poziție dacă ies din ecran
                pedestrian["y"] = 370


    # Desenează vehiculele
    for vehicle in vehicles:
        pygame.draw.rect(screen, car_color, (vehicle["x"], vehicle["y"], 150, 70))

    # Desenează pietonii
    for pedestrian in pedestrians:
        pygame.draw.circle(screen, pedestrian_color, (pedestrian["x"], pedestrian["y"]), 10)

    # Verificăm coliziunea între pietoni și vehicule
    accident_detected = False  # Folosim o variabilă pentru a verifica dacă a avut loc un accident
    for vehicle in vehicles:
        for pedestrian in pedestrians:
            if detect_collision(pedestrian, vehicle):
                accident_detected = True
                break  # Ocolim restul verificărilor după ce am găsit o coliziune

    # Dacă s-a detectat un accident, afișăm mesajul
    if accident_detected:
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text = font.render("Accident! Coliziune între pieton și vehicul!", True, (255, 0, 0))
        screen.blit(text, (screen_width // 8, screen_height -100))  # Afișăm mesajul în centrul ecranului

    # Sincronizare semafor pietoni
    if stare_semafor == "verde":
        semafor_pietoni = "roșu"
    elif stare_semafor == "roșu":
        semafor_pietoni = "verde"

    if semafor_pietoni == "verde":
        # Pietonii se mișcă
        for pedestrian in pedestrians:
            pedestrian["y"] -= 2
            if pedestrian["y"] < 180:  # Resetare poziție dacă ies din ecran
                pedestrian["y"] = 370
    elif semafor_pietoni == "roșu":
        # Pietonii așteaptă
        pass

    # Actualizează fereastra
    pygame.display.flip()

    # Controlează viteza animației
    #clock.tick(60)  # 60 FPS