import sys
import pygame
import random

pygame.init()
pygame.mixer.init()

background = pygame.image.load('./img/background.png')
laserSound = pygame.mixer.Sound('./sounds/laser.wav')
explosionSound = pygame.mixer.Sound('./sounds/explosion.wav')
knockSound = pygame.mixer.Sound('./sounds/knock.wav')

boomList = []
for i in range(1,13):
    boom = pygame.image.load(f'./img/{i}.png')
    boomList.append(boom)

width = background.get_width()
height = background.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Invaders Game')
run = True
fps = 60
clock = pygame.time.Clock()
score = 0
life = 100
white = (255,255,255)
black = (0,0,0)

levels = [
    {'invasor_count': 5, 'invasor_speed': 2, 'player_lives': 3},
    {'invasor_count': 8, 'invasor_speed': 3, 'player_lives': 3},
    {'invasor_count': 10, 'invasor_speed': 4, 'player_lives': 3},
]

def scoreScreen(frame, text, size, x,y):
    font = pygame.font.SysFont('Small Fonts', size, bold=True)
    textFrame = font.render(text, True, white,black)
    textRect = textFrame.get_rect()
    textRect.midtop = (x,y)
    frame.blit(textFrame, textRect)
    
def lifeBar(frame, x,y, level):
    longi = 100
    alto = 20
    fill = int((level/100)*longi)
    border = pygame.Rect(x,y, longi, alto)
    fill = pygame.Rect(x,y,fill, alto)
    pygame.draw.rect(frame, (255,0,55),fill)
    pygame.draw.rect(frame, black, border,4)
    
def load_level(level_data):
    invasor_count = level_data.get('invasor_count', 10)
    invasor_speed = level_data.get('invasor_speed', 2)
    player_lives = level_data.get('player_lives', 3)

    print(f"Cargando Nivel:")
    print(f"Invasores: {invasor_count}")
    print(f"Velocidad de Invasores: {invasor_speed}")
    print(f"Vidas del Jugador: {player_lives}")
    print("-----------------------")

    playerGroup.empty()
    invaderGroup.empty()
    bulletPlayer.empty()
    bulletInvaders.empty()

    player = Player()
    playerGroup.add(player)
    bulletPlayer.add(player)

    for _ in range(invasor_count):
        invader = Invaders(random.randrange(1, width - 50), 10)
        invaderGroup.add(invader)
        playerGroup.add(invader)
        
def all_invasors_destroyed():
    return len(invaderGroup) == 0

    
class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./img/Player.png').convert_alpha()
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.centery = height-50
        self.speedX = 0
        self.life = 100
        
    def update(self):
        self.speedX = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedX = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedX = 5
         
        self.rect.x += self.speedX
        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0
            
    def piupiu(self):
        bullet = BulletPlayer(self.rect.centerx, self.rect.top)
        playerGroup.add(bullet)
        bulletPlayer.add(bullet)
        laserSound.play()
        
class Invaders(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./img/Invader.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, width-50)
        self.rect.y = 10
        self.speedY = random.randrange(-5,20)
        
    def update(self):
        self.time = random.randrange(-1, pygame.time.get_ticks()//5000)
        self.rect.x += self.time
        if self.rect.x >= width:
            self.rect.x = 0
            self.rect.y += 50
            
    def piupiuInvaders(self):
        bullet = BulletInvaders(self.rect.centerx, self.rect.bottom)
        playerGroup.add(bullet)
        bulletInvaders.add(bullet)
        laserSound.play()
        
class BulletPlayer(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.image.load('./img/BulletPlayer.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speed = -18
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
            
class BulletInvaders(pygame.sprite.Sprite):
    def __init__(self, x,y): 
        super().__init__()
        self.image = pygame.image.load('./img/BulletInvader.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = random.randrange(10, width)     
        self.speedY = 4
        
    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom > height:
            self.kill()
            
class Boom(pygame.sprite.Sprite):
    def __init__(self, position):
       super().__init__()
       self.image = boomList[0]
       scala = pygame.transform.scale(self.image, (20,20))
       self.rect = scala.get_rect()
       self.rect.center = position
       self.time = pygame.time.get_ticks()
       self.boomSpeed = 30
       self.frames = 0
       
    def update(self):
        time = pygame.time.get_ticks()
        if time - self.time > self.boomSpeed:
            self.time = time
            self.frames+=1
            if self.frames == len(boomList):
                self.kill()
            else:
                position = self.rect.center
                self.image = boomList[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position
                
playerGroup = pygame.sprite.Group()
invaderGroup = pygame.sprite.Group()
bulletPlayer = pygame.sprite.Group()
bulletInvaders = pygame.sprite.Group()

player = Player()
playerGroup.add(player)
bulletPlayer.add(player)

for x in range(10):
    invader = Invaders(x * 50, 10)
    invaderGroup.add(invader)
    playerGroup.add(invader)

current_level = 0
load_level(levels[current_level])
    
while run:
    clock.tick(fps)
    window.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.piupiu()
    
    playerGroup.update()
    invaderGroup.update()
    bulletPlayer.update()
    bulletInvaders.update()
    
    playerGroup.draw(window)
    
    if all_invasors_destroyed():
        current_level += 1
        if current_level < len(levels):
            level_data = levels[current_level]
            load_level(level_data)
        else:
            print("¡Has completado todos los niveles!")
            run = False
            
    impactPB = pygame.sprite.groupcollide(invaderGroup, bulletPlayer,True,True)
    for i in impactPB:
        score+=10
        i.piupiuInvaders()
        invader = Invaders(300,10)
        invaderGroup.add(invader)
        playerGroup.add(invader)
        
        explosion = Boom(i.rect.center)
        playerGroup.add(explosion)
        explosionSound.set_volume(0.3)
        explosionSound.play()
        
    impactIB = pygame.sprite.spritecollide(player, bulletInvaders, True)
    for j in impactIB:
        player.life -= 10
        if player.life <= 0:
            run = False
        explo = Boom(j.rect.center)
        playerGroup.add(explo)
        knockSound.play()
        
    impactPI = pygame.sprite.spritecollide(player, invaderGroup, False)
    for impact in impactPI:
        player.life -=100
        invader = Invaders(10,10)
        playerGroup.add(invader)
        invaderGroup.add(invader)
        if player.life <= 0:
            run = False
            
    scoreScreen(window, (' SCORE: '+ str(score)+'         '), 30, width-85, 2)
    lifeBar(window, width-285, 0, player.life)
    
    pygame.display.flip()
    
pygame.quit()