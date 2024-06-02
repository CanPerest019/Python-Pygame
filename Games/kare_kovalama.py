import pygame
import random

# Ekran boyutları
WIDTH = 600
HEIGHT = 400

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Oyuncu ve düşmanlar için sınıflar
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Ekran sınırlarına çarpma kontrolü
        self.rect.x = max(0, min(self.rect.x, WIDTH - 50))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            global score
            score += 1

# Oyun başlatma
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Silah Oyunu")
clock = pygame.time.Clock()

# Skoru başlat
score = 0

# Oyuncu oluşturma
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Düşmanlar oluşturma
enemies = pygame.sprite.Group()
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Ana oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Oyuncu ve düşmanların güncellenmesi
    all_sprites.update()

    # Düşmanların ekran dışına çıkması durumunda yeniden konumlandırılması
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        print(f"Oyun bitti! Skorunuz: {score}")
        print("Oyunumu Oynadığınız İçin Teşekkür ederim \n Yapımcı:CanPerest")
        running = False

    # Ekranı temizleme
    screen.fill(BLACK)

    # Oyuncu ve düşmanları çizme
    all_sprites.draw(screen)

    # Ekranı güncelleme
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
