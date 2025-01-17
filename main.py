import pygame,random,sys,math

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (150, 133, 108)
DARKBROWN = (99, 88, 71)
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(center=position)
class TextSprite(pygame.sprite.Sprite):
  def __init__(self, text, font, color, position):
      super().__init__()
      self.font = font
      self.color = color
      self.text = text
      self.update_text(self.text)
      self.rect = self.image.get_rect()
      self.rect.center = position
  def update_text(self, text):
      self.image = self.font.render(text, True, self.color)

def rotate_image(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=Owl.rect.center).center)
    return rotated_image, new_rect
def sine_graph(a, b):
    points = []
    for x in range(600):
        y = SCREEN_HEIGHT // 3 - int(a * math.tan(b * (x - 360 // 2)))
        points.append(y)
    return points
def jump_function(a, b, c, x):
    return a * (x ** 2) + b * x + c

def spawn_hazard(spawn_height):
    global Hazard_list
    pos_y = random.randint(-120,140)
    Hazard = Sprite(hazard_image, (850,pos_y))
    Hazard.scored = False
    Hazard_rep = Sprite(hazard_image_flipped, (850,pos_y+spawn_height))
    Hazard_rep.scored = True
    Hazard_list.append(Hazard)
    Hazard_list.append(Hazard_rep)
    game_map.add(Hazard,Hazard_rep)
def score():
    global score_count
    for hazard in Hazard_list:
        if Owl.rect.centerx >= hazard.rect.centerx and hazard.scored == False:
            hazard.scored = True
            score_count += 1 
            score_text.update_text(str(score_count))
            return True
    return False


# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping Owl")
text_font = pygame.font.SysFont("arial", 50, bold=True)
text_font_2 = pygame.font.SysFont("arial", 35, bold=True)
title = pygame.font.SysFont("arial", 80, bold=True)

# Load and create game sprite
background_image = pygame.image.load("Images/background.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (background_image.get_width(), background_image.get_height()))
menu_text = TextSprite("Rolling Owl", title, BROWN, (SCREEN_WIDTH*3//5, 250))
info_text = TextSprite("Press Space to Start", text_font_2, DARKBROWN, (SCREEN_WIDTH*3//5, 250))

background = Sprite(background_image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
owl_image = pygame.image.load("Images/Owl.png").convert_alpha()
Owl = Sprite(owl_image, (100, SCREEN_HEIGHT // 2))
hazard_image = pygame.image.load("Images/hazard.png").convert_alpha()
hazard_image = pygame.transform.scale(hazard_image, (hazard_image.get_width()*3, hazard_image.get_height()*3))
hazard_image_flipped = pygame.transform.flip(hazard_image, (False), (True))
score_text = TextSprite(str(0), text_font, BROWN, (25,0))
score_text.rect.topleft = (10,0)

points = sine_graph(7,0.01)
point_counter = 0
try:
    with open("high_score.txt", "r") as file:
        high_score_text = file.read()
        high_score = int(high_score_text.split(" ")[2])
except:
    with open("high_score.txt", "w") as file:
        file.write("High Score: 0")
        high_score_text = "High Score: 0"
        high_score = 0
high_score_text = TextSprite(high_score_text, text_font, BROWN, (0,50))
high_score_text.rect.topright = (SCREEN_WIDTH-10,0)
Hazard_list = []
game_map = pygame.sprite.Group(background, Owl, score_text, high_score_text, menu_text,info_text)

# Game variables
angle = 0
rotating = True  # Always rotate
jumping = False
time = 40
jump_start_y = Owl.rect.y
difference = 0
velocity=6
x_velocity = 0
score_count = 0
spawn_height= 600

# Parabola parameters
a = 0.02  
b = 0       
c = jump_start_y 

# Main game loop
running = False
menu_running = True
clock = pygame.time.Clock()
while menu_running:
    

    time = (pygame.time.get_ticks() // 1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                difference += time
                game_map.remove(menu_text,info_text)
                menu_running = False
                running = True
    Owl.rect.y +=3
    if Owl.rect.y > SCREEN_HEIGHT+70:
        Owl.rect.y = -70
    elif Owl.rect.y < -80:
        Owl.rect.y = SCREEN_HEIGHT + 60
    angle -= 3  # Continuous rotation
    if angle <= -360:
        angle = 0
    try:
        if point_counter <= len(points):
            menu_text.rect.y = points[point_counter]
            info_text.rect.y = points[point_counter] +100
            point_counter += 2
    except:
        point_counter = 0
    Owl.image, Owl.rect = rotate_image(Owl.original_image, angle)
    screen.fill(WHITE)
    game_map.draw(screen)
    
    pygame.display.update()
    clock.tick(120)

while running:
    time = (pygame.time.get_ticks() // 1000) - difference
    if time == 2:
        spawn_hazard(spawn_height)
        difference += 2
    if score(): 
        if score_count %5 == 0:
            velocity +=1
            spawn_height -= 10
    for hazard in Hazard_list:
        if hazard.rect.x < -250:
            game_map.remove(hazard)
            Hazard_list.remove(hazard)
            continue
        else:
            hazard.rect.x -= velocity
        if pygame.sprite.collide_rect(Owl, hazard):
            if int(score_count) > high_score:
                print("Score")
                with open('high_score.txt', 'w') as file:
                   file.write("High Score: "+str(score_count))
            running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  
                jumping = True
                start = -50 
                jump_start_y = Owl.rect.y - Owl.rect.height
            if event.key == pygame.K_a:
                x_velocity = -3
            if event.key == pygame.K_d:
                x_velocity = 3
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                if x_velocity < 0:
                    x_velocity = 0
            if event.key == pygame.K_d:
                if x_velocity > 0:
                    x_velocity = 0
    if not jumping:
        angle -= 3  # Continuous rotation
        if angle <= -360:
            angle = 0
        Owl.image, Owl.rect = rotate_image(Owl.original_image, angle)
    elif jumping:
        Owl.rect.y = jump_function(a, b, jump_start_y, start)
        start += 2  # Increment time for smoother motion
        if start >= 20:
            jumping = False

    background.rect.x -= 3
    if background.rect.x < -800:
        background.rect.x = 0
    Owl.rect.y +=4
    Owl.rect.x += x_velocity
    if Owl.rect.y > SCREEN_HEIGHT+70:
        Owl.rect.y = -70
    elif Owl.rect.y < -80:
        Owl.rect.y = SCREEN_HEIGHT + 60

    game_map.draw(screen)
    pygame.display.flip()
    clock.tick(90)

pygame.quit()
sys.exit()
