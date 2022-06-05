import pygame
import random
import os

# 我們不太會改變的變數 通常當作固定參數 全部以大寫作為提示
# foot per second = FPS 每秒顯示偵數
FPS = 60
WIDTH, HEIGHT = 500,600

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# init game and creat display 
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("軒耀大冒險I")
clock = pygame.time.Clock()

# 載入圖片

background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
# rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
rock_imgs = []
for i in range(7):
    # 在字串內放變數 也可以像這樣寫 往後可以參考
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50,40))
        self.image = pygame.transform.scale(player_img, (50,38))
        # 讓黑色變成透明ㄎ
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
    def update(self):
        # 回傳現在鍵盤上的按鍵有按的true 沒按的 false
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        # 黑色去掉
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        # 重新定位rock 的中心位置動態取得轉動的中心
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10,20))
        self.image = bullet_img
        # 黑色去掉
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            # 把子彈從群組裡刪除
            self.kill()

# pygame 的控制精靈 Group 方便我們跟新物件
all_sprites = pygame.sprite.Group()

rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 加入飛行船(玩家) player
player = Player()
all_sprites.add(player)

# 一次生成多顆rock
for i in range(8):
    # 加入 隕石 rock
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# game loop
running = True
while running:
    # 一秒鐘之內只能執行10次
    clock.tick(FPS)
    # get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # update
    all_sprites.update()
    # 判斷 bullet 和 rock 的碰撞刪除 因為我們兩個都要刪掉 所以兩個都是 True 被刪掉的值會以字典的形式儲存
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    
    # 每少一顆rock 就補一顆
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
    
    # 判斷飛行船是否被撞擊
    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    # 被撞到就結束遊戲 
    if hits:
        running = False

    # display
    screen.fill(BLACK)
    # 把我們的背景圖片畫上去
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()