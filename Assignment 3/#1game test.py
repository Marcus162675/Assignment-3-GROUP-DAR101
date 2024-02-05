import pygame

screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('game for assignemnt 3')

                    level1()
def level1():
    image = pygame.image.load("M:\WEDS01\Semester 3 2023\HIT137\Assignment 3\Game assests\level1.png")
    image = pygame.transform.scale(image, (640,480))
    while True:
        screen.blit(image,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                print ('jump')
menu()