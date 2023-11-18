import pygame
import sys
import json 
from pygame.locals import *
from random import randrange, choice
from config import *

#_________________________  Configuración  _________________________

# Inicializar modulos de Pygame
pygame.init()

# Pantalla
screen = pygame.display.set_mode(resolucion)
pygame.display.set_caption("Dieta!!")

# Imagenes
fondo = pygame.transform.scale(pygame.image.load("./assets/img/Protagonistayotros/fondmenu.JPG"), (WIDTH, HEIGHT))
imagen_jugador = pygame.image.load("./assets/img/Protagonistayotros/prota.png")

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

#musica
pygame.mixer.music.load("./assets/sounds/musica.mp3")
pygame.mixer.music.play(-1)#-1 loop infinito, 1 por defecto suena 2 veces
pygame.mixer.music.set_volume(0.5)

#efectos especiales
bonus = pygame.mixer.Sound("./assets/sounds/Magia.mp3")
game_over_musica = pygame.mixer.Sound("./assets/sounds/game over.mp3")
musica_pausa = pygame.mixer.Sound("./assets/sounds/pausa.mp3")
colision_fast_food = pygame.mixer.Sound("./assets/sounds/colision.mp3")

#_________________________   Funciones   _________________________


def crear_rect(imagen=None, left=0, top=0, width=50, height=50, color=rojo, gravedad=False):
    """Esta función toma distintos parametros para poder formar un rectángulo en la pantalla. Si obtiene una imagen, utiliza la funcion pygame.stransform.scale para redimensionarla a las dimensiones "width" y "height". Gravedad es un booleano, que indica si aplica gravedad al rectangulo """
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
    """ Toma como parametro una lista, donde se selecciona de forma aleatoria un elemento de la misma. """
    return choice(lista)

def cargar_frutas(lista, cantidad, imagen=None):
    """ Esta funcion toma los parametros lista, cantidad e imagen. Se itera cantidad para poder cargar los elementos en la lista.
    Se llama a la funcion crear rectángulo para crear uno con una imagen aletoria de la lista de frutas. Tambien les asigna posiciones aleatorias en el exe x y en el eje y."""
    for i in range(cantidad):
        lista.append(crear_rect(imagen=obtener_valor_aleatorio(image_fruit_list), left=randrange(0, WIDTH-50), top=randrange(HEIGHT, HEIGHT*2)))

def cargar_fastfood(lista, cantidad, imagen=None):
    for i in range(cantidad):
        lista.append(crear_rect(imagen=obtener_valor_aleatorio(image_fastfood_list), left=randrange(0, WIDTH-50), top=randrange(HEIGHT, HEIGHT*2)))

def menu_inicio():
    menu = pygame.font.SysFont(None, 24)
    fuente_titulo = pygame.font.SysFont(None, 50)

    titulo = fuente_titulo.render("Comer frutas!!", True, negro)
    titulo_rect = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    reglas = menu.render("Comé frutas para sumar puntaje. La comida chatarra te saca puntos", True, negro)
    reglas_rect = reglas.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    inicio = menu.render("Presioná ESPACIO para empezar", True, negro)
    inicio_rect = inicio.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4 - 30))  

    salir = menu.render("Presiona ESC para salir", True, negro)
    salir_rect = salir.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4 + 30))  

    fondo_menu = pygame.transform.scale(pygame.image.load("./assets/img/Protagonistayotros/fondo.jpg"), (WIDTH, HEIGHT))
    screen.blit(fondo_menu, origen)

    screen.blit(titulo, titulo_rect)
    screen.blit(reglas, reglas_rect)
    screen.blit(inicio, inicio_rect)
    screen.blit(salir, salir_rect)

    pygame.display.flip()

    """ Se utiliza un bucle while para esperar la entrada del usuario. Se verifican los eventos y responde a la tecla espacio para empezar el juego, o al ESC para salirse.
    Al presionar espacio, waiting_for_key se vuelve FALSE, por lo que rompe el bucle y permite que se lleve al inicio del juego. """

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
    game_over_fuente = pygame.font.SysFont(None, 72)
    game_over_texto = game_over_fuente.render(f'¡Has perdido!', True, blanco)
    game_over_rect = game_over_texto.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    retry_font = pygame.font.SysFont(None, 36)
    retry_text = retry_font.render(f'Tu score es de {score}', True, blanco)
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 50))

    fondo_menu_go = pygame.transform.scale(pygame.image.load("./assets/img/Protagonistayotros/fondogameover.PNG"), (WIDTH, HEIGHT))

    screen.blit(game_over_texto, game_over_rect)
    screen.blit(fondo_menu_go, origen)
    screen.blit(retry_text, retry_rect)

    pygame.display.flip()
    pygame.mixer.music.stop()
    game_over_musica.play()
    if score > score_record:
        with open("./data/score.json", "w") as file:
                file.write(str(score_record))
    
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    waiting_for_key = False
            
  
def pausa():
    """ Coloco la palabra GLOBAL para indicarle que es una variable global y no una local. Si no lo colocase, Pygame lo tomaría como una variable dentro de la función y  y no afectaría al resto del código, que es lo que queremos hacer. La variable "is_pausa" es una bandera que indica cuando el juego está o no en pausa. """
    global is_pausa
    
    
    fondo_pausa= pygame.transform.scale(pygame.image.load("./assets/img/Protagonistayotros/pausa.jpeg"), (WIDTH, HEIGHT))
    screen.blit(fondo_pausa, origen)
    
    # Pausar la música al entrar en pausa
    pygame.mixer.music.pause()
    musica_pausa.play()

    font = pygame.font.Font(None, 26)
    pausa_texto = "¡Mucha Fruta! Presiona 'P' para continuar, o 'E' para salir del juego"
    
    waiting_for_key = True
    while waiting_for_key:  
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Reanudar la música al salir de pausa
                    pygame.mixer.music.unpause()
                    musica_pausa.stop()
                    is_pausa = False
                    waiting_for_key = False  
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()

        pausa_text_surface = font.render(pausa_texto, True, (0, 0, 0))
        text_rect = pausa_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2)) 

        screen.fill((255, 255, 255))
        screen.blit(pausa_text_surface, text_rect)
        pygame.display.flip()

"""Se almacena el valor guardado en el archivo "score.json"""
try:
    with open("./data/score.json", "r") as file: 
        score_record = float(file.read()) 

except FileNotFoundError:
    print("No existe 'score.json'. Por lo tanto, se creará uno.")
    with open("./data/score.json", "w") as file: 
        file.write("0") 
        score_record = 0
#_________________________  Parametros  __________________________
""" Se crea al jugador"""
jugador = crear_rect(imagen_jugador, 100, HEIGHT-100, 100, 100, rojo)

""" Se crean la listas y contadores para la fruta y fast food"""
frutas_lista = []
frutas_contador = 5
cargar_frutas(frutas_lista, frutas_contador)

fastfood_lista = []
fastfood_contador = 5
cargar_fastfood(fastfood_lista, fastfood_contador)

"""Se crean los movimientos del jugador, que irán desde izquierda a derecha """
f_left = False
f_right = False

"""Se definen las fuentes del score y el score mismo."""
fuente_score = pygame.font.Font(None, 36)
fuente = pygame.font.SysFont(None,48)
score = 0


"""Configuracion de frutas y fast food. Se colocan los tiempos de aparicion inicial para ambos elementos"""
velocidad_frutas = 2
velocidad_fast_food = 2

tiempo_aparicion_frutas = pygame.time.get_ticks()
tiempo_aparicion_fastfood = pygame.time.get_ticks()

"""Configuración de vidas y la fuente."""
vidas = 3
fuente_vidas = pygame.font.Font(None, 36)



#_________________________________________________________________


#_________________________  Bucle principal  _________________________
is_running = True

while is_running:
    
    # Configuración de los FPS
    clock.tick(60)
    #_________________________  Configuración de eventos  _________________________

    """Se recorren todos los eventos hechos en Pygame. Cuando hay un evento tipo "QUIT" (cuando lo llame el usuario)  se rompe el bucle"""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        """Manejo de eventos cuando se presionan y sueltan las teclas (KEYDOWN KEYUP)"""
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
    """Movimientos del jugador. Si la condicion f_right es verdadera y el jugador no alcanzó el borde derecho, puede moverse libremente a la derecha."""
    if f_right and jugador["rect"].right < WIDTH:
        jugador["rect"].right += 10
    """Movimientos del jugador. Si la condicion f_left es verdadera y el jugador no alcanzó el borde izquierdo, puede moverse libremente a la izquierda."""
    if f_left and jugador["rect"].left > 0:
        jugador["rect"].left -= 10


    #_________________________   Configuración de Colisiones   _________________________

       # Frutas ------------------
    """Este es el temporizador para la generación de frutas. Se obtiene el tiempo actual en milisegundos utilizando pygame.time.get_ticks()
     Se verifica el tiempo que pasó (yo coloqué 5000, es decir, 5 segundos).
     Una vez pasado el tiempo, se llama a la función cargar_frutas para agregar frutas de forma aleatoria y el contador para agregar las que desee. En este caso, son 5 cada 5 segundos.
     Se reincia el temporizador para que sea un bucle."""
    
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_aparicion_frutas >= 5000: 
        cargar_frutas(frutas_lista, frutas_contador)
        tiempo_aparicion_frutas = tiempo_actual  # Reiniciar el temporizador
        print("Pasaron 5 segundos")

    """Se coloca un for para iterar sobre la copia de la lista frutas_lista. Al utilizar [:] creamos una copia superficial para iterar sobre los elementos sin que afecte la lista original. 
    Se almacena la posicion actual de la fruta con pos_atual."""
    
    for fruit in frutas_lista[:]:
        pos_actual = fruit["rect"].topleft

        """Se verifica si la fruta está por el borde superior, y si no comenzó a caer, la fruta se mueve hacia arriba. Una vez que toca el borde superior, cae hacia abajo. Si se cumple esa condicion, la """
        if fruit["rect"].top > 0 and not fruit["gravedad"]:
            fruit["rect"].top -= 3
            if fruit["rect"].top <= 0:
                fruit["gravedad"] = True

        """Si alcanzó la parte inferior de la pantalla, SE ELIMINA LA FRUTA"""
        if fruit["gravedad"] == True:
            fruit["rect"].top += velocidad_frutas 
            if fruit["rect"].top >= HEIGHT:
             frutas_lista.remove(fruit)
             

        """Acá se verifica que la colisión solo impacte cuando la fruta está bajando. Cuando se 'come' una fruta, aumenta el score en 1 y se remueve la fruta.
        Si el score es un multiplo de 5, la velocidad aumenta en 1    """
        # Verificar la colisión solo cuando la fruta está bajando
        if fruit["gravedad"] and pos_actual[1] < fruit["rect"].topleft[1]:
            if detectar_colision_circulos(fruit["rect"], jugador["rect"]):
                frutas_lista.remove(fruit)
                score += 1
                if score % 5 == 0:
                    velocidad_frutas += 1
                    print(velocidad_frutas)
                    print("colision")
                    bonus.play()
        

 ######### FAST FOOD
 
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_aparicion_fastfood >= 5000:  
        cargar_fastfood(fastfood_lista, fastfood_contador)
        tiempo_aparicion_fastfood = tiempo_actual   
        print("Pasaron 5 segundos") #Print para verificar si están pasando 5 segundos

        
    for fastfood in fastfood_lista[:]:
        # Guarda la posición actual de la fastfood
        pos_actual = fastfood["rect"].topleft
        
            
        if fastfood["rect"].top > 0 and not fastfood["gravedad"]:
            fastfood["rect"].top -= 3
            if fastfood["rect"].top <= 0:
                fastfood["gravedad"] = True

        """Acá queremos lograr que la fast_food caiga al mismo tiempo que la velocidad de las frutas, independientemente del score."""
        velocidad_fast_food = velocidad_frutas 

        if fastfood["gravedad"] == True:
            fastfood["rect"].top += velocidad_fast_food
            if fastfood["rect"].top >= HEIGHT:
                fastfood_lista.remove(fastfood)

        # Verificar la colisión solo cuando fastfood está bajando
        if fastfood["gravedad"] and pos_actual[1] < fastfood["rect"].topleft[1]:
            """Al igual que las frutas, se verifica que solo colisione cuando estén bajando. Pero a diferencia, si se 'come' una fast_food, el score disminuye y se resta una vida."""
            if detectar_colision_circulos(fastfood["rect"], jugador["rect"]):
                fastfood_lista.remove(fastfood)
                score -= 1
                vidas -= 1
                print(f'VF: {velocidad_fast_food}')
                print("colision")
                colision_fast_food.play()
        
        
    ############## Intento de funciones de colisiones
    """Calcula la distancia entre dos puntos. Desempaqueta las coordenadas de x e y.Devuelve la distancia entre los dos puntos"""
    def distancia_entre_puntos(pt1, pt2):
        x1, y1 = pt1
        x2, y2 = pt2
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

    """Toma un rect y calcula el radio en el rectángulo dividiendo la altura entre 2. Devuelve el radio calculado"""
    def calcular_radio(rect):
        return rect.height // 2

    """Toma dos rect que presentan círculos. Calcula los radios utilizando la función previamente hecha y verifica la colisión comparando la distancia con la suma de los radios. Devuelve True si hay colisión."""
    def detectar_colision_circulos(rect_1, rect_2):
        r1 = calcular_radio(rect_1)
        r2 = calcular_radio(rect_2)

        # Obtiene el centro de cada círculo
        center_1 = rect_1.center
        center_2 = rect_2.center

        # Calcula la distancia entre los centros de los círculos
        distancia = distancia_entre_puntos(center_1, center_2)

        # Verifica la colisión comparando la distancia con la suma de los radios
        return distancia <= (r1 + r2)

    """Verifica si un punto está dentro de un rectángulo tomando (x,y) y un rect. Se mira si las coordenadas están dentro del limite del rectangulo. Devuelve True si están dentro del punto"""
    def punto_en_rectangulo(punto, rect):
        x, y = punto
        return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

    #_________________________   Dibujo en la pantalla   _________________________


    # fondo
    screen.blit(fondo, origen)

    # jugador
    screen.blit(jugador["imagen"], jugador["rect"])
    #score
    score_texto = fuente_score.render(f"Score: {score}", True, blanco)
    rect_score = score_texto.get_rect()
    screen.blit(score_texto, (350,10))
    #vidas
    vidas_texto = fuente_vidas.render(f'Vidas: {vidas}', True, blanco)
    screen.blit(vidas_texto, (10, 10))
    #ultimo score
    record_texto = fuente_score.render(f"Record: {score}", True, blanco)
    rect_record = record_texto.get_rect()
    screen.blit(record_texto, (600,10))

    # Frutas
    for fruit in frutas_lista:
        screen.blit(fruit["imagen"], fruit["rect"])

    for fastfood in fastfood_lista:
        screen.blit(fastfood["imagen"], fastfood["rect"])
  
    
    # Actualizar pantalla
    pygame.display.flip()


#_________________________  GAME OVER  _________________________ 


