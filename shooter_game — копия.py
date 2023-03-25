#Создай собственный Шутер!
нужно проверить есть ли в директории запуска приложения файл с названием notes_data.json
если такого файла нет( при первом запуске его и не должно быть)
то его нужно создать
заполнить по образцу
"""  {
    "добро пожаловать в самое лучшее приложение": {
        "текст" : "Ваш незаменимый помощник в звметках", 
        "теги" []
        }
}"""


from pygame import *
import random
from time import time as timer
# ! timer (oн жe time) - нужна для засечения времени

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fireSound = mixer.Sound('fire.ogg')

# шрифты и надписи
font.init()

font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True,(0, 255, 0))
lose = font1.render('YOU LOSE!', True,(255, 0, 0))
font2 = font.SysFont(None, 36)

img_back = "cosmos_5.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_meteor = "asteroid_3.png"


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load(img_back), (win_width, win_height))

lost = 0
score = 0
life = 3

#герои игры
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, random.randint(80, win_width - 80), -40, 80, 40, random.randint(1,5))
    monsters.add(monster)

meteors = sprite.Group()
for i in range(2):
    meteorit = Meteor(img_meteor, random.randint(80, win_width - 80), -60, 60, 60, random.randint(5,10))
    meteors.add(meteorit)

bullets = sprite.Group()

run = True
finish = False
# ! будет отвечать за перезарядку 
rel_time = False
# ! подсчёт выпущенных пуль
num_fire = 0

clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                #.fireSound.play()
                ship.fire()

                if num_fire >= 5 and rel_time == False:

                    last_time = timer()

                    rel_time = True

    if finish != True:
        window.blit(background, (0,0))
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        meteors.draw(window)
        

        if rel_time == True:

            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Ждите, идёт перезарядка...', 1, (200, 0, 0))
                window.blit(reload, (170, 200))
            else:
                num_fire = 0
                rel_time = False

        # ! проверка столкновения пуль и монстров(оба исчезают при косании)
        collides = sprite.groupcollide(monsters, bullets,True, True)
        # ! данный цикд работает столко раз сколько монстров сбито
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, random.randint(80, win_width - 80), -40, 80, 40, random.randint(1,5))
            monsters.add(monster)

        ship.update()
        monsters.update()
        bullets.update()
        meteors.update()
       
        if sprite.spritecollide( ship, monsters, True) or sprite.spritecollide( ship, meteors, True):
            life -=1

    


        # ! условия проигрыша
        if lost >= 10 or life <= 0: 
            finish = True
            window.blit(lose, (win_width//4, win_height//2))
        # ! условия выигрыша
        if score >= 10:
            finish = True
            window.blit(win, (win_width//4, win_height//2))

        if life == 3:
            life_color = (0, 255, 0)
        elif life == 2:
            life_color = (255, 238, 0)
        else:
            life_color = (255, 0, 0)

         # счетчики
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # жизни
        text_life = font2.render('Жизни: '  + str(life), 1, life_color)
        window.blit(text_life, (10, 80))

        display.update()
    else:
        finish = False
        lost = 0 
        score = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in meteors:
            m.kill()
        for ufo in monsters:
            ufo.kill()

        time.delay(3000)
        for i in range(5):
            monster = Enemy(img_enemy, random.randint(80, win_width - 80), -40, 80, 40, random.randint(1,5))
            monsters.add(monster)
    time.delay(50)


    