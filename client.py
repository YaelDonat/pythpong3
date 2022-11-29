import math
import pygame
import sys
import random
import socket
import threading
from ball import Ball
from player import Player

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((900,500))
        pygame.display.set_caption("Ultimate Pong: 2P")
        self.run = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip= input("server ip: ")
        self.port= int(input("port: "))
        
        self.player1_x, self.player1_y = 20, 250
        self.player2_x, self.player2_y = 860, 250
        self.player_size = [20, 80]
        self.speed_y_1, self.speed_y_2 = 0, 0
        self.player1 = Player(self.player1_x, self.player1_y, self.player_size)
        self.player2 = Player(self.player2_x, self.player2_y, self.player_size)
        self.ball_direction = [-1, 1]
        self.ball = Ball(450, 250, 10, random.choice(self.ball_direction))
        self.score_1, self.score_2 = 0, 0
        self.ball_x, self.ball_y = None, None
        self.player1_position = 250
        self.recv_data = False
        self.rect = pygame.Rect(0, 0, 900, 500)
    
    def play(self):
        self.client.connect((self.ip, self.port))
        self.new_thread(self.get_data)
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                ###
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.speed_y_2 = -10
                    if event.key == pygame.K_z:
                        self.speed_y_2 = 10
                ###  
                if event.type == pygame.KEYUP:
                    self.speed_y_2 = 0
                ###
            self.player1.rect.clamp_ip(self.rect)
            self.player2.move(self.speed_y_2)
            self.player2.rect.clamp_ip(self.rect)
            self.ball.rect.clamp_ip(self.rect)
            if self.recv_data:
                self.ball.rect.x = self.ball_x
                self.ball.rect.y = self.ball_y
                self.player1.rect.y = self.player1_position

            self.player1.move(self.speed_y_1)
            self.player2.move(self.speed_y_2)
            
            position_y_player_2 = f"{ self.player2.rect.y }"
            self.client.send(position_y_player_2.encode('utf-8'))
            self.recv_data = True

            self.screen.fill((50,50,50))
            self.message('big', f"Ultimate Pong", [320 , 50, 20 ,20], (255, 255, 255))
            self.message('big', f"{ self.score_1 }", [300 , 200, 50 ,50], (255, 255, 255))
            self.message('big', f"{ self.score_2 }", [585 , 200, 50 ,50], (255, 255, 255))

            self.player1.show(self.screen)
            self.player2.show(self.screen)
            self.ball.show(self.screen)

            pygame.display.flip()
            clock = pygame.time.Clock()
            clock.tick(30)
    
    def message(self, font, msg, msg_rect, color):
        if font == 'small':
            font = pygame.font.Font('fonts/GamePlayed-vYL7.ttf', 20)
        if font == 'medium':
            font = pygame.font.Font('fonts/GamePlayed-vYL7.ttf', 30)
        if font == 'big':
            font = pygame.font.Font('fonts/GamePlayed-vYL7.ttf', 40)
        msg = font.render(msg, True, color)
        self.screen.blit(msg, msg_rect)

    def new_thread(self, target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
    
    def get_data(self):
        while True:
            data_received = self.client.recv(128).decode('utf-8')
            data_received = data_received.split(',')
            # print(data_received)
            self.player1_position = int(data_received[0])
            self.ball_x = int(data_received[1])
            self.ball_y = int(data_received[2])
            self.score_1, self.score_2 = int(data_received[3]), int(data_received[4])

if __name__ == "__main__":
    pygame.init()
    g = Game()
    g.play()
    pygame.quit()