import pygame
import random
import sys

# Ekran boyutu ve hücre boyutu
HUCRE_BOYUTU = 20
HUCRE_SAYISI = 20
EKRAN_BOYUTU = HUCRE_BOYUTU * HUCRE_SAYISI

# Mayın sayısı
MAYIN_SAYISI = 40

# Renkler
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
GRI = (192, 192, 192)
KIRMIZI = (255, 0, 0)

# Pygame'i başlat
pygame.init()
ekran = pygame.display.set_mode((EKRAN_BOYUTU, EKRAN_BOYUTU))
pygame.display.set_caption("Mayın Tarlası")
saat = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Mayın Tarlası oluştur
def mayin_tarlasi_olustur():
    tarla = [[0 for _ in range(HUCRE_SAYISI)] for _ in range(HUCRE_SAYISI)]
    mayinlar = random.sample(range(HUCRE_SAYISI * HUCRE_SAYISI), MAYIN_SAYISI)
    for mayin in mayinlar:
        x = mayin // HUCRE_SAYISI
        y = mayin % HUCRE_SAYISI
        tarla[x][y] = -1
        for i in range(max(0, x - 1), min(HUCRE_SAYISI, x + 2)):
            for j in range(max(0, y - 1), min(HUCRE_SAYISI, y + 2)):
                if tarla[i][j] != -1:
                    tarla[i][j] += 1
    return tarla

# Hücreleri açma
def hucreleri_ac(tarla, gorunen, x, y):
    if gorunen[x][y]:
        return
    gorunen[x][y] = True
    if tarla[x][y] == 0:
        for i in range(max(0, x - 1), min(HUCRE_SAYISI, x + 2)):
            for j in range(max(0, y - 1), min(HUCRE_SAYISI, y + 2)):
                if not gorunen[i][j]:
                    hucreleri_ac(tarla, gorunen, i, j)

# Oyunu başlat
def oyun_baslat():
    global tarla, gorunen
    tarla = mayin_tarlasi_olustur()
    gorunen = [[False for _ in range(HUCRE_SAYISI)] for _ in range(HUCRE_SAYISI)]

# Oyun döngüsü
oyun_baslat()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x //= HUCRE_BOYUTU
            y //= HUCRE_BOYUTU
            if event.button == 1:  # Sol tıklama
                if tarla[x][y] == -1:
                    # Mayına bastı, oyunu yeniden başlat
                    oyun_baslat()
                else:
                    # Mayına basmadı, hücreyi aç
                    hucreleri_ac(tarla, gorunen, x, y)

    # Ekranı temizle
    ekran.fill(BEYAZ)

    # Hücreleri çiz
    for x in range(HUCRE_SAYISI):
        for y in range(HUCRE_SAYISI):
            rect = pygame.Rect(x * HUCRE_BOYUTU, y * HUCRE_BOYUTU, HUCRE_BOYUTU, HUCRE_BOYUTU)
            if gorunen[x][y]:
                if tarla[x][y] == -1:
                    # Mayın, kırmızı renkte göster
                    pygame.draw.rect(ekran, KIRMIZI, rect)
                else:
                    # Mayın değil, gri renkte göster ve komşu mayın sayısını yaz
                    pygame.draw.rect(ekran, GRI, rect)
                    if tarla[x][y] > 0:
                        text = font.render(str(tarla[x][y]), True, SIYAH)
                        ekran.blit(text, rect.move(5, 5))
            else:
                # Henüz açılmamış hücre, beyaz renkte göster
                pygame.draw.rect(ekran, BEYAZ, rect)
                pygame.draw.rect(ekran, SIYAH, rect, 1)

    pygame.display.flip()
    saat.tick(30)  # Oyun hızı
