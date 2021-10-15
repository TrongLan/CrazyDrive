import pygame
from pygame import mixer
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
pygame.init()

# man hinh
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("CRAYZY DRIVE")
#nhac
mixer.music.load("C:/Users/KTC/Desktop/LEARNING/lap_trinh_python/bai_tap_code_python/duan/image/backmusic.mp3")
mixer.music.play(-1)
# nền
background = pygame.image.load("C:/Users/KTC/Desktop/LEARNING/lap_trinh_python/bai_tap_code_python/duan/image/startbackground.png")
# tải ảnh các nút
play = pygame.image.load("C:/Users/KTC/Desktop/LEARNING/lap_trinh_python/bai_tap_code_python/duan/image/playbig.png")
exit = pygame.image.load("C:/Users/KTC/Desktop/LEARNING/lap_trinh_python/bai_tap_code_python/duan/image/exit1.png")
intruction = pygame.image.load("C:/Users/KTC/Desktop/LEARNING/lap_trinh_python/bai_tap_code_python/duan/image/book.png")
guideplayer = pygame.image.load("C:/Users/KTC/Desktop/LEARNING/lap_trinh_python/bai_tap_code_python/duan/image/guidebackground.png")
guide = False
move = 2000
# tạo nút bấm
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action  
start_but = Button(440, 300, play)
exit_but = Button(670, 330, exit)
intruction_but = Button(300, 330, intruction)      
running = True
while running:
    if guide == False: 
        screen.blit(background, (0, 0))
        start_but = Button(440, 300, play)
        exit_but = Button(670, 330, exit)
        intruction_but = Button(300, 330, intruction)
    if start_but.draw(screen):
        print("yes")
    if exit_but.draw(screen):
        pygame.quit()
    if intruction_but.draw(screen):
        guide = True
        screen.blit(guideplayer, (0, 0))
        start_but = Button(440+move, 300+move, play)
        exit_but = Button(670+move, 330+move, exit)
        intruction_but = Button(300+move, 330+move, intruction)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        if event.type == pygame.MOUSEBUTTONDOWN:
            guide = False
    pygame.display.update()
pygame.quit()