import math
import pygame
import sys
from player import Player
from ball import Ball
import random
import socket
import threading

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((900,500))
        pygame.display.set_caption("Ultimate Pong: 2P")
        self.run = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip , self.port = '127.0.0.1' , 9999
        self.client_socket, self.addr = None, None
        self.server.bind((self.ip, self.port))
        self.server.listen(1)
        self.position_y = 250
        self.player1_x, self.player1_y = 20, 250
        self.player2_x, self.player2_y = 860, 250
        self.player_size = [20, 80]
        self.speed_y_1, self.speed_y_2 = 0, 0
        self.player1 = Player(self.player1_x, self.player1_y, self.player_size)
        self.player2 = Player(self.player2_x, self.player2_y, self.player_size)
        self.rect = pygame.Rect(0, 0, 900, 500)
        self.ball_direction = [-1, 1]
        self.ball = Ball(450, 250, 10, random.choice(self.ball_direction))
        self.speed_ball_x, self.speed_ball_y = 15, 2
        self.shoot_ball = False
        self.score_1, self.score_2 = 0, 0
    
    def play(self):
        self.new_thread(self.wait_for_conn)

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                ###
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.speed_y_1 = -10
                    if event.key == pygame.K_DOWN:
                        self.speed_y_1 = 10
                    if event.key == pygame.K_SPACE:
                        self.shoot_ball = True
                ###  
                if event.type == pygame.KEYUP:
                    self.speed_y_1 =0
                ###
            self.player1.move(self.speed_y_1)
            self.player2.rect.y = int(self.position_y)
            #permets de definir les limites a ne pas depasser (clamp_ip)
            self.player1.rect.clamp_ip(self.rect)
            self.player2.move(self.speed_y_2)
            self.player2.rect.clamp_ip(self.rect)
            self.ball.rect.clamp_ip(self.rect)

            if self.shoot_ball:
                self.ball.move(self.speed_ball_x, self.speed_ball_y)

            ### collision rect / ball
            if self.player1.rect.colliderect(self.ball.rect) or self.player2.rect.colliderect(self.ball.rect):
                self.speed_ball_x = self.changeDirectBall(self.speed_ball_x, 0)
                self.speed_ball_y = self.changeDirectBall(self.speed_ball_y, 60)
                self.ball.random_speed_y = random.randint(1, 7)
            ### collision ball / screen
            if self.ball.rect.top <= 0 or self.ball.rect.bottom >= 500:
                self.speed_ball_y = self.changeDirectBall(self.speed_ball_y, 0)
            
            ### Remise de la balle au centre
            if self.ball.rect.right >= 915:
                self.ball.rect.x, self.ball.rect.y = 450, 250
                self.score_1 += 1
                self.shoot_ball = False  
            if self.ball.rect.left <= -15:
                self.ball.rect.x, self.ball.rect.y = 450, 250
                self.score_2 += 1
                self.shoot_ball = False

            ### data send
            data_send = f"{ self.player1.rect.y},{ self.ball.rect.x},{ self.ball.rect.y},{ self.score_1 },{ self.score_2 }"
            if self.client_socket is not None:
                self.client_socket.send(data_send.encode('utf-8'))

            self.screen.fill((50,50,50))
            self.message('big', f"Ultimate Pong", [320 , 50, 20 ,20], (255, 255, 255))
            self.message('big', f"{ self.score_1 }", [300 , 200, 50 ,50], (255, 255, 255))
            self.message('big', f"{ self.score_2 }", [585 , 200, 50 ,50], (255, 255, 255))

            if self.shoot_ball is False :
                self.message('small', f"Press space to start the game ! ", [300, 100, 
                300, 50], (255, 255, 255))

            self.ball.show(self.screen)
            self.player1.show(self.screen)
            self.player2.show(self.screen)
            pygame.display.flip()
            clock = pygame.time.Clock()
            clock.tick(30)
    
    def changeDirectBall(self, speed, angle):
        speed = - (speed * math.cos(angle))
        return speed
    
    def message(self, font, msg, msg_rect, color):
        if font == 'small':
            font = pygame.font.Font('fonts\GamePlayed-vYL7.ttf', 20)
        if font == 'medium':
            font = pygame.font.Font('fonts\GamePlayed-vYL7.ttf', 30)
        if font == 'big':
            font = pygame.font.Font('fonts\GamePlayed-vYL7.ttf', 40)
        msg = font.render(msg, True, color)
        self.screen.blit(msg, msg_rect)

    def wait_for_conn(self):
        self.client_socket, self.addr = self.server.accept()
        self.get_data()

    def get_data(self):
        while True:
            self.position_y = self.client_socket.recv(128).decode('utf-8')

    def new_thread(self, target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    pygame.init()
    g = Game()
    g.play()
    pygame.quit()