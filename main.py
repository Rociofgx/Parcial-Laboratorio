import pygame
import sys
import json 
from pygame.locals import *
from random import randrange, choice

#_________________________  Configuración  _________________________

# Inicializar modulos de Pygame
pygame.init()
try:
    with open("data/score.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    print("No se ha encontrado archivo")

# Pantalla
origen = (0, 0)
WIDTH = 800
HEIGHT = 600
resolution = WIDTH , HEIGHT 
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Test")

# Imagenes
fondo = pygame.transform.scale(pygame.image.load("./assets/img/Protagonistayotros/fondmenu.JPG"), (WIDTH, HEIGHT))
image_player = pygame.image.load("./assets/img/Protagonistayotros/prota.png")

image_fruit_1 = pygame.image.load("./assets/img/Frutas/PNG frutas/banana.png")
image_fruit_2 = pygame.image.load("./assets/img/Frutas/PNG frutas/cereza.png")
image_fruit_3 = pygame.image.load("./assets/img/Frutas/PNG frutas/frutilla.png")
image_fruit_4 = pygame.image.load("./assets/img/Frutas/PNG frutas/manzana.png")
image_fruit_5 = pygame.image.load("./assets/img/Frutas/PNG frutas/sandia.png")
image_fruit_list = [image_fruit_1, image_fruit_2, image_fruit_3, image_fruit_4, image_fruit_5]

image_fastfood_1 = pygame.image.load("./assets/img/Fast food/png/hamburger.png")
image_fastfood_2 = pygame.image.load("./assets/img/Fast food/png/pancho.png")
image_fastfood_3 = pygame.image.load("./assets/img/Fast food/png/papita.png")
image_fastfood_4 = pygame.image.load("./assets/img/Fast food/png/taco.png")
image_fastfood_list = [image_fastfood_1, image_fastfood_2, image_fastfood_3, image_fastfood_4]

# Configuración de reloj
clock = pygame.time.Clock()

# Colores
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)

#musica
pygame.mixer.music.load("./assets/sounds/musica.mp3")
pygame.mixer.music.play(-1)#-1 loop infinito, 1 por defecto suena 2 veces
pygame.mixer.music.set_volume(0.5)

#efectos especiales
bonus = pygame.mixer.Sound("./assets/sounds/Magia.mp3")
game_over_musica = pygame.mixer.Sound("./assets/sounds/game over.mp3")

is_menu_active = True
is_pausa = False

#_________________________   Funciones   _________________________

def pausa():
    global is_pausa
    clock = pygame.time.Clock()
    pygame.display.set_caption("Dieta!!")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mixer.music.pause()
    font = pygame.font.Font(None, 26)
    pausa_texto = "¡Mucha Fruta! Presiona 'ESC' para continuar, o 'E' para salir del juego"

    waiting_for_key = True
    while waiting_for_key:  
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.unpause()
                    is_pausa = False
                    waiting_for_key = False  
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()

        pause_text_surface = font.render(pausa_texto, True, (0, 0, 0))
        screen.fill((255, 255, 255))
        screen.blit(pause_text_surface, (WIDTH / 2 - 260, HEIGHT - 60))
        pygame.display.flip()
def create_rect(imagen=None, left=0, top=0, width=50, height=50, color=red, gravedad=False):
    rect = pygame.draw.rect(screen, color, (left, top, height, width))
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {
        "imagen":imagen,
        "rect":rect,
        "color":color,
        "gravedad":gravedad
    }


def obtener_valor_aleatorio(lista):
    return choice(lista)


def cargar_frutas(lista, cantidad, imagen=None):
    for i in range(cantidad):
        lista.append(create_rect(imagen=obtener_valor_aleatorio(image_fruit_list), left=randrange(0, WIDTH-50), top=randrange(HEIGHT, HEIGHT*2)))

def cargar_fastfood(lista, cantidad, imagen=None):
    for i in range(cantidad):
        lista.append(create_rect(imagen=obtener_valor_aleatorio(image_fastfood_list), left=randrange(0, WIDTH-50), top=randrange(HEIGHT, HEIGHT*2)))

def menu_inicio():
    menu = pygame.font.SysFont(None, 24)
    fuente_titulo = pygame.font.SysFont(None, 50)

    titulo = fuente_titulo.render("Comer frutas!!", True, black)
    titulo_rect = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    reglas = menu.render("Comé frutas para sumar puntaje. La comida chatarra te saca puntos", True, black)
    reglas_rect = reglas.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    inicio = menu.render("Presioná ESPACIO para empezar", True, black)
    inicio_rect = inicio.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4 - 30))  

    salir = menu.render("Presiona ESC para salir", True, black)
    salir_rect = salir.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4 + 30))  

    fondo_menu = pygame.transform.scale(pygame.image.load("./assets/img/Protagonistayotros/fondo.jpg"), (WIDTH, HEIGHT))
    screen.blit(fondo_menu, origen)

    screen.blit(titulo, titulo_rect)
    screen.blit(reglas, reglas_rect)
    screen.blit(inicio, inicio_rect)
    screen.blit(salir, salir_rect)

    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    waiting_for_key = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_over_menu():
    game_over_font = pygame.font.SysFont(None, 72)
    game_over_text = game_over_font.render(f'¡Has perdido!', True, white)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    retry_font = pygame.font.SysFont(None, 36)
    retry_text = retry_font.render(f'Tu score es de {score}', True, white)
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    fondo_menu_go = pygame.transform.scale(pygame.image.load("./assets/img/Protagonistayotros/fondmenu.JPG"), (WIDTH, HEIGHT))
    screen.blit(fondo_menu_go, origen)

    screen.blit(game_over_text, game_over_rect)
    screen.blit(retry_text, retry_rect)

    pygame.display.flip()
    pygame.mixer.music.stop()
    game_over_musica.play()
    
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    waiting_for_key = False
  

#_________________________  Parametros  __________________________

player = create_rect(image_player, 100, HEIGHT-100, 100, 100, red)

fruits_list = []
fruits_count = 5
cargar_frutas(fruits_list, fruits_count)

fastfood_list = []
fastfood_count = 5
cargar_fastfood(fastfood_list, fastfood_count)

f_left = False
f_right = False

font_score = pygame.font.Font(None, 36)
fuente = pygame.font.SysFont(None,48)
score = 0

velocidad_frutas = 2
velocidad_fast_food = 2

tiempo_aparicion_frutas = pygame.time.get_ticks()
tiempo_aparicion_fastfood = pygame.time.get_ticks()

vidas = 1
fuente_vidas = pygame.font.Font(None, 36)

game_over = False

#_________________________________________________________________


is_running = True

#_________________________  Bucle principal  _________________________


while is_running:
    
    # Configuración de los FPS
    clock.tick(60)

    #_________________________  Configuración de eventos  _________________________


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_d:
                f_right = True

            if event.key == K_a:
                f_left = True

            if event.key == K_p:  
                is_pausa = not is_pausa 

            if event.key == K_ESCAPE:
                is_pausa = False 

        if event.type == KEYUP:
            if event.key == K_d:
                f_right = False

            if event.key == K_a:
                f_left = False

    
    if is_pausa:
        pausa()
        continue

    

    if is_menu_active:
        menu_inicio()
        is_menu_active = False
        
    if vidas < 0:
        game_over = True
        game_over_menu()

    #_________________________  Configuración de movimientos  _________________________

    # Jugador -----------------
    if f_right and player["rect"].right < WIDTH:
        player["rect"].right += 10

    if f_left and player["rect"].left > 0:
        player["rect"].left -= 10

    

    #_________________________   Configuración de Colisiones   _________________________

       # Frutas ------------------

    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_aparicion_frutas >= 5000:  # 6000 milisegundos = 6 segundos
        cargar_frutas(fruits_list, fruits_count)
        tiempo_aparicion_frutas = tiempo_actual  # Reiniciar el temporizador
        print("Pasaron 5 segundos")

   
    for fruit in fruits_list[:]:
        # Guardar la posición actual de la fruta
        pos_actual = fruit["rect"].topleft

        
        if fruit["rect"].top > 0 and not fruit["gravedad"]:
            fruit["rect"].top -= 3
            if fruit["rect"].top <= 0:
                fruit["gravedad"] = True

        if fruit["gravedad"] == True:
            fruit["rect"].top += velocidad_frutas 
            if fruit["rect"].top >= HEIGHT:
             fruits_list.remove(fruit)


        # Verificar la colisión solo cuando la fruta está bajando
        if fruit["gravedad"] and pos_actual[1] < fruit["rect"].topleft[1]:
            if detectar_colision_circulos(fruit["rect"], player["rect"]):
                fruits_list.remove(fruit)
                score += 1
                if score % 5 == 0:
                    velocidad_frutas += 1
                    print(velocidad_frutas)
                    print("colision")
        

 ######### FAST FOOD
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_aparicion_fastfood >= 5000:  # 6000 milisegundos = 6 segundos
        cargar_fastfood(fastfood_list, fastfood_count)
        tiempo_aparicion_fastfood = tiempo_actual  # Reinic 
        print("Pasaron 5 segundos")

        
    for fastfood in fastfood_list[:]:
        # Guardar la posición actual de la fastfood
        pos_actual = fastfood["rect"].topleft
        
            
        if fastfood["rect"].top > 0 and not fastfood["gravedad"]:
            fastfood["rect"].top -= 3
            if fastfood["rect"].top <= 0:
                fastfood["gravedad"] = True

        if fastfood["gravedad"] == True:
            fastfood["rect"].top += 3
            if fastfood["rect"].top >= HEIGHT:
                fastfood_list.remove(fastfood)

        # Verificar la colisión solo cuando fastfood está bajando
        if fastfood["gravedad"] and pos_actual[1] < fastfood["rect"].topleft[1]:
            if detectar_colision_circulos(fastfood["rect"], player["rect"]):
                fastfood_list.remove(fastfood)
                score -= 1
                vidas -= 1
                velocidad_fast_food = velocidad_frutas
                print(f'VF: {velocidad_fast_food}')
                
                print("colision")
        
        
    

    ############## Intento de funciones de colisiones
    def calcular_radio(rect):
       return rect.height // 2

    def distancia_entre_puntos(pt1,pt2):
        x1,y1 = pt1
        x2,y2 = pt2

        return  ((x2 - x1)** 2 + (y2 - y1) **2 ) ** 0.5

    def detectar_colision_circulos(rect_1,rect_2):
        colision = False
        r1 = calcular_radio(rect_1)
        r2 = calcular_radio(rect_2)
        
        distancia = distancia_entre_puntos(rect_1.center,rect_2.center)
        if distancia <= (r1+r2):
                colision = True
        
        
        return colision


    def punto_en_rectangulo(punto, rect):
        x, y = punto
        return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom 

    #_________________________   Dibujo en la pantalla   _________________________


    # fondo
    screen.blit(fondo, origen)

    # Player
    screen.blit(player["imagen"], player["rect"])
    #score
    score_text = font_score.render(f"Score: {score}", True, white)
    rect_score = score_text.get_rect()
    screen.blit(score_text, (350,10))
    #vidas
    vidas_texto = fuente_vidas.render(f'Vidas: {vidas}', True, white)
    screen.blit(vidas_texto, (10, 10))


    # Frutas
    for fruit in fruits_list:
        screen.blit(fruit["imagen"], fruit["rect"])

    for fastfood in fastfood_list:
        screen.blit(fastfood["imagen"], fastfood["rect"])
  
    
    # Actualizar pantalla
    pygame.display.flip()


#_________________________  GAME OVER  _________________________ 
