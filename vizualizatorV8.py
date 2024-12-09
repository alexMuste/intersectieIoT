import pygame
import sys
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
text_color = (0, 0, 0)
car_color = (0, 0, 255)
pedestrian_color = (64, 128, 128)

# Timere pentru semafoare
verde_vehicul = 30
rosu_vehicul = 10
verde_pietoni = 10
rosu_pietoni = 30

# Starea semafoarelor
stare_semafor = "verde"
semafor_pietoni = "roșu"

# Vehicule și pietoni
masini = [
    {"x": 100, "y": 290, "direction": "right"},
    {"x": 700, "y": 210, "direction": "left"},
]
pietoni = [
    {"x": 400, "y": 370, "direction": "up"},
    {"x": 430, "y": 180, "direction": "down"},
]

# Viteze
viteza_masina = 120  # Pixeli pe secundă
viteza_pieton = 60  # Pixeli pe secundă

# Timpul curent
last_update = pygame.time.get_ticks()
interval = 1000  # 1 secundă

# Font pentru afișare
font = pygame.font.Font(None, 36)

# Ceas pentru controlul timpului
clock = pygame.time.Clock()

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


# Funcții pentru desenare
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

# Funcția principală
running = True
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

    # Actualizează timerul la fiecare secundă
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= interval:
        last_update = current_time
        if stare_semafor == "verde":
            verde_vehicul -= 1
            if verde_vehicul == 0:
                stare_semafor = "roșu"
                rosu_vehicul = 10
                verde_vehicul = 30
                semafor_pietoni = "verde"
        elif stare_semafor == "roșu":
            rosu_vehicul -= 1
            if rosu_vehicul == 0:
                stare_semafor = "verde"
                verde_vehicul = 30
                semafor_pietoni = "roșu"
        if semafor_pietoni == "verde":
            verde_pietoni -= 1
            if verde_pietoni == 0:
                semafor_pietoni = "roșu"
                rosu_pietoni = 30
        elif semafor_pietoni == "roșu":
            rosu_pietoni -= 1
            if rosu_pietoni == 0:
                semafor_pietoni = "verde"
                verde_pietoni=10

    # Mișcare vehicule
    for vehicle in masini:
        if stare_semafor == "verde":
            if vehicle["direction"] == "right":
                vehicle["x"] += viteza_masina * delta_time
                if vehicle["x"] > screen_width:
                    vehicle["x"] = -40
            elif vehicle["direction"] == "left":
                vehicle["x"] -= viteza_masina * delta_time
                if vehicle["x"] < -40:
                    vehicle["x"] = screen_width

    # Mișcare pietoni
    for pedestrian in pietoni:
        if semafor_pietoni == "verde":
            if pedestrian["direction"] == "up":
                pedestrian["y"] -= viteza_pieton * delta_time
                if pedestrian["y"] < 180:
                    pedestrian["y"] = 370
            elif pedestrian["direction"] == "down":
                pedestrian["y"] += viteza_pieton * delta_time
                if pedestrian["y"] > 370:
                    pedestrian["y"] = 180

    # Desenează semafor vehicul
    draw_semafor1(300, 90, stare_semafor)

    # Desenează semafor pieton
    draw_semafor2(300, 360, semafor_pietoni)

    # Desenează vehicule
    for vehicle in masini:
        pygame.draw.rect(screen, car_color, (int(vehicle["x"]), vehicle["y"], 100, 50))

    # Desenează pietoni
    for pedestrian in pietoni:
        pygame.draw.circle(screen, pedestrian_color, (int(pedestrian["x"]), int(pedestrian["y"])), 10)

    # Verificăm coliziunea între pietoni și vehicule
    accident_detected = False  # Folosim o variabilă pentru a verifica dacă a avut loc un accident
    for vehicle in masini:
        for pedestrian in pietoni:
            if detect_collision(pedestrian, vehicle):
                accident_detected = True
                break  # Ocolim restul verificărilor după ce am găsit o coliziune

    # Dacă s-a detectat un accident, afișăm mesajul
    if accident_detected:
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text = font.render("Accident! Coliziune între pieton și vehicul!", True, (255, 0, 0))
        screen.blit(text, (screen_width // 8, screen_height -100))  # Afișăm mesajul în centrul ecranului


    # Afișează timer vehicul
    text = font.render(str(verde_vehicul if stare_semafor == "verde" else rosu_vehicul), True, text_color)
    screen.blit(text, (300, 65))

    # Afișează timer pieton
    text_pieton = font.render(str(verde_pietoni if semafor_pietoni == "verde" else rosu_pietoni), True, text_color)
    screen.blit(text_pieton, (265, 370))

    # Actualizează fereastra
    pygame.display.flip()

pygame.quit()
sys.exit()
