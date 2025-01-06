import pygame
import sys
import socket
import threading
import random
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
text_color = (0, 0, 0)
car_color = (0, 0, 255)
pedestrian_color = (64, 128, 128)


# Starea semafoarelor
stare_semafor = "verde"
semafor_pietoni = "roșu"

# Vehicule și pietoni
masini = [
    {"x": 100, "y": 290, "direction": "right", "stare_oprit": False},
    {"x": 700, "y": 210, "direction": "left", "stare_oprit": False},
]
pietoni = [
    {"x": 400, "y": 370, "direction": "up", "is_crossing": False},
    {"x": 430, "y": 180, "direction": "down", "is_crossing": False},
]

# Viteze
viteza_masina = 120  # Pixeli pe secundă
viteza_pieton = 60  # Pixeli pe secundă

# Conectare la server
server_host = '127.0.0.1'
server_port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))
print("Conectat la server.")

# Ceas pentru controlul timpului
clock = pygame.time.Clock()

# Font pentru afișare
font = pygame.font.Font(None, 36)
# Funcția pentru a detecta coliziuni între pieton și vehicul
def detect_collision(pedestrian, vehicle, pedestrian_radius=10, vehicle_width=40, vehicle_height=20, y_min=180, y_max=370):
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
        print(f"Coliziune detectată între pietonul la ({pedestrian['x']}, {pedestrian['y']}) și vehiculul la ({vehicle['x']}, {vehicle['y']})")
        return True
    return False


# Funcțiile pentru desenare
def draw_liniiT(start_x, start_y, end_x, width, stripe_width=10, gap=10, color=(255, 255, 255)):
    x = start_x
    while x < end_x - 1:
        pygame.draw.rect(screen, color, (start_y, x, stripe_width + 100, width))
        x += stripe_width + gap


def draw_semafor1(x, y, state):
    color = green_light if state == "verde" else red_light
    pygame.draw.rect(screen, (20, 20, 20), (x, y, 40, 70))
    pygame.draw.circle(screen, color, (x + 20, y + 23), 15)


def draw_semafor2(x, y, state):
    color = green_light if state == "verde" else red_light
    pygame.draw.rect(screen, (20, 20, 20), (x, y, 40, 50))
    pygame.draw.circle(screen, color, (x + 20, y + 23), 8)

prezenta_masina = False
prezenta_pieton = False

# Funcția pentru a primi date de la server
def primire_date(client_socket):
    global stare_semafor, semafor_pietoni, prezenta_masina, prezenta_pieton
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Conexiunea cu serverul a fost întreruptă.")
                break
            mesaj = data.decode()
            print(f"{mesaj}")

            if mesaj == "ROSU":
                stare_semafor = "rosu"
                semafor_pietoni = "verde"

            elif mesaj == "VERDE":
                stare_semafor = "verde"
                semafor_pietoni = "rosu"

            elif mesaj == "prezenta masina":
                prezenta_masina = True

            elif mesaj == "prezenta pieton":
                prezenta_pieton = True

        except Exception as e:
            print(f"Eroare la recepția datelor: {e}")
            break

# Funcția principală
running = True

# Thread pentru primirea semnalului semaforului
primire_date_thread = threading.Thread(target=primire_date, args=(client_socket,))
primire_date_thread.daemon = True
primire_date_thread.start()

while running:
    delta_time = clock.tick(60) / 1000.0  # Timpul scurs în secunde

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Umple ecranul cu fundalul
    screen.fill(background_color)

    # Desenează drumul
    pygame.draw.rect(screen, road_color, (0, 200, 1000, 150))

    # Adaugă trecerea de pietoni
    draw_liniiT(start_x=202, start_y=350, end_x=352, width=20, stripe_width=15, gap=10)

    if prezenta_masina:
        directions = random.choices(["right", "left"], k=random.randint(1, 2))
        for direction in directions:
            if direction == "right":
                masini.append({"x": 100, "y": 290, "direction": "right", "stare_oprit": False})
            elif direction == "left":
                masini.append({"x": 700, "y": 210, "direction": "left", "stare_oprit": False})
        prezenta_masina = False  # Resetăm semnalul după adăugare

    if prezenta_pieton:
        directions = random.choices(["up", "down"], k=random.randint(1, 2))
        for direction in directions:
            if direction == "up":
                pietoni.append({"x": 400, "y": 370, "direction": "up", "is_crossing": False})
            elif direction == "down":
                pietoni.append({"x": 430, "y": 180, "direction": "down", "is_crossing": False})
        prezenta_pieton = False  # Resetăm semnalul după adăugare

    # Mișcare vehicule
    for vehicle in masini:
        if stare_semafor == "rosu":
            if vehicle["direction"] == "left" and vehicle["x"] > 470 and vehicle["x"] < 475:
                vehicle["stare_oprit"] = True
            elif vehicle["direction"] == "right" and vehicle["x"] > 240 and vehicle["x"] < 245:
                vehicle["stare_oprit"] = True
            else:
                vehicle["stare_oprit"] = False
        elif stare_semafor == "verde":
            vehicle["stare_oprit"] = False

        if not vehicle["stare_oprit"]:
            if vehicle["direction"] == "right":
                vehicle["x"] += viteza_masina * delta_time
                if vehicle["x"] > screen_width:
                    masini.remove(vehicle)  # Eliminăm vehiculul care a ieșit din ecran
            elif vehicle["direction"] == "left":
                vehicle["x"] -= viteza_masina * delta_time
                if vehicle["x"] < -100:
                    masini.remove(vehicle)

    # Mișcare pietoni
    for pedestrian in pietoni[:]:
        if semafor_pietoni == "verde" and not pedestrian["is_crossing"]:
            pedestrian["is_crossing"] = True  # Pietonul începe traversarea
        elif semafor_pietoni == "rosu":
            pedestrian["is_crossing"] = False

        if pedestrian["is_crossing"]:
            if pedestrian["direction"] == "up":
                pedestrian["y"] -= viteza_pieton * delta_time
                if pedestrian["y"] <= 180:
                    pietoni.remove(pedestrian)
            elif pedestrian["direction"] == "down":
                pedestrian["y"] += viteza_pieton * delta_time
                if pedestrian["y"] >= 370:
                    pietoni.remove(pedestrian)

    # Desenează semafoarele
    draw_semafor1(30, 50, stare_semafor)
    draw_semafor2(200, 50, semafor_pietoni)

    # Desenează vehiculele
    for vehicle in masini:
        pygame.draw.rect(screen, car_color, (int(vehicle["x"]), vehicle["y"], 100, 50))

    # Desenează pietonii
    for pedestrian in pietoni:
        pygame.draw.circle(screen, pedestrian_color, (int(pedestrian["x"]), int(pedestrian["y"])), 10)

    # Actualizează ecranul
    pygame.display.flip()

# Închide conexiunea
client_socket.close()
pygame.quit()
sys.exit()

