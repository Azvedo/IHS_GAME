import pygame, sys, random
from pygame.math import Vector2
import assets

class BULLET:
    def __init__(self, car_pos_x):
        #posicoes iniciais da bala
        self.bullet_pos_X = car_pos_x + 21
        self.bullet_pos_Y = 570
        #vetor da posicao da bala
        self.position = Vector2(self.bullet_pos_X, self.bullet_pos_Y)
        #retangulo para checar colisao da bala
        self.bullet_rect = pygame.Rect(self.bullet_pos_X,self.bullet_pos_Y, assets.bullet_width_adjust*0.9,assets.bullet_height_adjust)    
    def draw_bullet(self):
        #desenhando todas as balas
        screen.blit(assets.bullet_asset_center, self.position)
        


class CAR:
    def __init__(self):
        self.car_pos_x = screen.get_width() / 1.9
        self.car_pos_y = 570
        self.position = Vector2(self.car_pos_x, self.car_pos_y)
        self.direction = 0 # 0=meio, 1= direita e -1 = esquerda
        self.car_rect = pygame.Rect(self.car_pos_x+5,self.car_pos_y+3, assets.car_width_adjust*0.9,assets.car_height_adjust)
    def draw_car(self):
        if self.direction == 0:
            screen.blit(assets.car_asset_center,self.position)
        elif self .direction == 1:
            screen.blit(assets.car_to_right,self.position)
        elif self.direction == -1:
            screen.blit(assets.car_to_left,self.position)
        
class OBSTACULO:
    def __init__(self):
        #create a x and y position
        self.life = 3
        self.randomize()
        self.zombie_rect = pygame.Rect(self.pos.x, self.pos.y, assets.zombie_width_adjust*0.8, assets.zombie_height_adjust*0.5)
        

    def draw_obstaculo(self):
        self.zombie_rect.center = [self.pos.x+35 , self.pos.y+30]
        assets.image_counter += 1
        if assets.image_counter >= assets.image_delay:
            assets.image_index = (assets.image_index + 1) % len(assets.move_zombie)
            assets.image_counter = 0
        # Renderização do sprite
        current_image = assets.move_zombie[assets.image_index]
        screen.blit(current_image, self.pos)


    def randomize(self):
        self.x = random.randint(125, 405)
        self.y = 5
        self.pos = pygame.math.Vector2(self.x, self.y) #vetor de posições

    def move_obstaculo(self):
        self.pos.y += 8
        self.zombie_rect.y += 8

class MAIN():

    def __init__(self):
        self.car = CAR()
        self.obst = OBSTACULO()
        self.bullet_vector = [] 

    def draw_elements(self):
        self.car.draw_car()
        self.obst.draw_obstaculo()
        for bullet in self.bullet_vector:
            bullet.draw_bullet()
            if(bullet.position.y <= 0):
                self.bullet_vector.remove(bullet)
        
    def update(self):
        self.check_collision()
        self.car.direction = 0
        self.obst.move_obstaculo()
        for bullet in self.bullet_vector:
            bullet.position.y -= 10
        
    def game_over(self):
        pygame.quit()
        sys.exit()
    

    def check_collision(self):
       
        if (self.car.car_rect).colliderect(self.obst.zombie_rect):
           colliding = True
           if colliding:
                self.obst.life -= 1
                colliding = False
        
           print(self.obst.life)
           if self.obst.life <= 0:
               colliding = True
               self.obst.life = 3
               self.obst.randomize()

           


pygame.init()
screen_height = 700
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Meu jogo")
clock = pygame.time.Clock() # para garantir que o jogo não mude de velocidade de pc para pc



SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN() 

while True: # loop game
    # desenhar todos o elementos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game.game_over() #garante que vai fechar o jogo
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game.bullet_vector.append(BULLET(main_game.car.position.x))

    press = pygame.key.get_pressed()
    if press[pygame.K_LEFT] and main_game.car.position.x > 130:
        main_game.car.direction = -1
        main_game.car.position.x -= 10
        main_game.car.car_rect.x -=10  
    if press[pygame.K_RIGHT] and main_game.car.position.x < 407:
        main_game.car.direction = 1
        main_game.car.position.x += 10
        main_game.car.car_rect.x += 10 
    if press[pygame.K_UP]:
        main_game.car.position.y -= 5
        main_game.car.car_rect.y -= 5 
    if press[pygame.K_DOWN]:
        main_game.car.position.y += 5
        main_game.car.car_rect.y += 5

    screen.blit(assets.background_correct_size, (0,0)) 
    main_game.draw_elements()
    pygame.display.flip()
    clock.tick(60) # garante que o jogo rode a 60 fps
