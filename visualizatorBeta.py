import pygame
import sys
import socket
import threading
import random
import math
import time



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


afiseaza_mesaj_accident = False
afiseaza_mesaj = False  # Flag pentru a controla afișarea mesajului
timp_afisare = 0  # Contorul pentru durata de afișare




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
viteza_pieton = 30  # Pixeli pe secundă

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
        return True
    return False

# Funcțiile pentru desenare
#  Caracteristici trecere de pietoni
def draw_liniiT(start_x, start_y, end_x, width, stripe_width=10, gap=10, color=(255, 255, 255)):
    x = start_x
    while x < end_x - 1:
        pygame.draw.rect(screen, color, (start_y, x, stripe_width + 100, width))
        x += stripe_width + gap

# Caracteristici semafor masini
def draw_semafor1(x, y, state):
    # Fundalul semaforului
    pygame.draw.rect(screen, (20, 20, 20), (x, y, 40, 80))  # Extindem dimensiunea pentru al doilea cerc

    # Lumina roșie
    red_color = red_light if state == "rosu" else (50, 0, 0)  # Roșu aprins sau stins
    pygame.draw.circle(screen, red_color, (x + 20, y + 23), 15)

    # Lumina verde
    green_color = green_light if state == "verde" else (0, 50, 0)  # Verde aprins sau stins
    pygame.draw.circle(screen, green_color, (x + 20, y + 60), 15)  # Mai jos cu 50 pixeli pentru aliniere


# Caracteristici semafor pietoni
def draw_semafor2(x, y, state):
    color = green_light if state == "verde" else red_light
    pygame.draw.rect(screen, (20, 20, 20), (x, y, 30, 30))
    pygame.draw.circle(screen, color, (x + 15, y + 15), 8)

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

    if prezenta_masina and not masina_oprita:
        directions = random.choices(["right", "left"], k=random.randint(1, 2))
        for direction in directions:
            if direction == "right":
                masini.append({"x": 0, "y": 290, "direction": "right", "stare_oprit": False})
            elif direction == "left":
                masini.append({"x": 750, "y": 210, "direction": "left", "stare_oprit": False})
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
    ilegalitate_detectata  = False
#Masinile se opresc daca este semaforul rosu se opresc inainte de trecerea de pietoni
    for vehicle in masini:
        if stare_semafor == "rosu" and random.random() < 0.99:
            if vehicle["direction"] == "left" and vehicle["x"] > 470 and vehicle["x"] < 475 :
                vehicle["stare_oprit"] = True
            elif vehicle["direction"] == "right" and vehicle["x"] > 240 and vehicle["x"] < 245:
                vehicle["stare_oprit"] = True
            else:
                vehicle["stare_oprit"] = False
                if vehicle["direction"] == "left" and vehicle["x"] < 470 and vehicle["x"] > 355 :
                    ilegalitate_detectata = True
                elif vehicle["direction"] == "right" and vehicle["x"] > 245 and vehicle["x"] < 355 :
                    ilegalitate_detectata = True


# Daca este verde continua deplasarea doar daca nu exista pietoni pe trecere
        elif stare_semafor == "verde":
            masina_oprita = False
            for pedestrian in pietoni:
                if 200 < pedestrian["y"] < 350 and random.random() < 0.99:
                    masina_oprita = True
                    break
                vehicle["stare_oprit"] = masina_oprita

# Daca masinile au fost oprite, vor relua miscarea de deplasare
        if not vehicle["stare_oprit"]:
            if vehicle["direction"] == "right":
                vehicle["x"] += viteza_masina * delta_time
                if vehicle["x"] > screen_width:
                    masini.remove(vehicle)  # Eliminăm vehiculul care a ieșit din ecran
            elif vehicle["direction"] == "left":
                vehicle["x"] -= viteza_masina * delta_time
                if vehicle["x"] < -100:
                    masini.remove(vehicle)

        # Actualizare mișcare pietoni
    for pedestrian in pietoni[:]:  # Iterăm pe o copie a listei pentru a permite modificări
        if not pedestrian.get("is_crossing", False):
# Pietonul poate începe traversarea doar dacă semaforul este verde
            if semafor_pietoni == "verde":
                pedestrian["is_crossing"] = True  # Pietonul începe traversarea
        else:
# Pietonul continuă să traverseze indiferent de culoarea semaforului
            if pedestrian["direction"] == "up":
                pedestrian["y"] -= viteza_pieton * delta_time
                if pedestrian["y"] <= 180:  # A ajuns la capătul drumului
                    pietoni.remove(pedestrian)  # Eliminăm pietonul care a terminat traversarea
            elif pedestrian["direction"] == "down":
                pedestrian["y"] += viteza_pieton * delta_time
                if pedestrian["y"] >= 370:  # A ajuns la capătul drumului
                    pietoni.remove(pedestrian)  # Eliminăm pietonul care a terminat traversarea

    # Desenează semafoarele
    draw_semafor1(300, 355, stare_semafor)
    draw_semafor2(460, 140, semafor_pietoni)

    # Desenează vehiculele
    for vehicle in masini:
        pygame.draw.rect(screen, car_color, (int(vehicle["x"]), vehicle["y"], 100, 50))

    # Desenează pietonii
    for pedestrian in pietoni:
        pygame.draw.circle(screen, pedestrian_color, (int(pedestrian["x"]), int(pedestrian["y"])), 10)

# Verificăm coliziunea între pietoni și vehicule
    accident_detectat = False  # Folosim o variabilă pentru a verifica dacă a avut loc un accident
    for vehicle in masini:
        for pedestrian in pietoni:
            if detect_collision(pedestrian, vehicle):
                accident_detectat = True
                # in cazul in care a avut loc un accident pietonul dispare
                pietoni.remove(pedestrian)


    # Dacă s-a detectat un accident, afișăm mesajul
    if accident_detectat:
        afiseaza_mesaj_accident = True
        timp_afisare = 180
        accident_detectat = False

    if afiseaza_mesaj_accident:
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text = font.render("Accident! Coliziune între pieton și vehicul!", True, (255, 0, 0))
        screen.blit(text, (screen_width // 8, screen_height - 100))

        # Decrementăm contorul
        timp_afisare -= 1
        if timp_afisare <= 0:
            afiseaza_mesaj_accident = False  # Oprirea afișării mesajului


    # Verificăm dacă trebuie să afișăm mesajul
    if ilegalitate_detectata:
        afiseaza_mesaj = True
        timp_afisare = 180  # Numărul de cadre pentru care mesajul va fi afișat (~3 secunde la 60 FPS)
        ilegalitate_detectata = False  # Resetăm flag-ul

    if afiseaza_mesaj:
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text = font.render("Autoturismul cu numarul ******* a trecut pe ROSU!", True, (255, 0, 0))
        screen.blit(text, (screen_width // 8, screen_height - 150))
        # Decrementăm contorul
        timp_afisare -= 1
        if timp_afisare <= 0:
            afiseaza_mesaj = False  # Oprirea afișării mesajului

    # Actualizează ecranul
    pygame.display.flip()

# Închide conexiunea
client_socket.close()
pygame.quit()
sys.exit()
