import pygame
import math
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naves Espaciais - 2 Jogadores")

# Cores
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# Fonte para texto
font = pygame.font.SysFont('Arial', 20)
big_font = pygame.font.SysFont('Arial', 36)


# Classe da Nave
class Nave:
    def __init__(self, x, y, color, bullet_color, controls, bullet_key, player_name):
        self.x = x
        self.y = y
        self.color = color
        self.bullet_color = bullet_color
        self.angle = 0  # Ângulo em graus
        self.velocity = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.rotation_speed = 3
        self.size = 20
        self.bullets = []
        self.cooldown = 0
        self.max_cooldown = 15  # Frames de espera entre tiros
        self.score = 0
        self.lives = 3
        self.invulnerable = 0  # Invulnerabilidade após ser atingido
        self.controls = controls  # [esquerda, direita, acelerar, atirar]
        self.bullet_key = bullet_key
        self.player_name = player_name

    def update(self, keys):
        # Controles de rotação
        if keys[self.controls[0]]:  # Esquerda
            self.rotate(-1)
        if keys[self.controls[1]]:  # Direita
            self.rotate(1)

        # Controle de aceleração (sempre ativo)
        if keys[self.controls[2]]:  # Acelerar
            self.accelerate()

        # Atualiza posição baseada na velocidade e ângulo
        if self.velocity != 0:
            rad_angle = math.radians(self.angle)
            self.x += self.velocity * math.sin(rad_angle)
            self.y -= self.velocity * math.cos(rad_angle)

        # Mantém a nave dentro da tela
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT

        # Atualiza cooldown do tiro
        if self.cooldown > 0:
            self.cooldown -= 1

        # Atualiza invulnerabilidade
        if self.invulnerable > 0:
            self.invulnerable -= 1

        # Atira se a tecla estiver pressionada
        if keys[self.bullet_key] and self.cooldown == 0:
            self.shoot()

        # Atualiza balas
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2] * 10  # Velocidade X
            bullet[1] += bullet[3] * 10  # Velocidade Y

            # Remove balas que saíram da tela
            if (bullet[0] < 0 or bullet[0] > WIDTH or
                    bullet[1] < 0 or bullet[1] > HEIGHT):
                self.bullets.remove(bullet)

    def rotate(self, direction):
        # direction: 1 = direita, -1 = esquerda
        self.angle += direction * self.rotation_speed

    def accelerate(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_speed)

    def shoot(self):
        # Calcula a direção do tiro
        rad_angle = math.radians(self.angle)
        bullet_dx = math.sin(rad_angle)
        bullet_dy = -math.cos(rad_angle)

        # Posição inicial da bala (frente da nave)
        front_x = self.x + self.size * math.sin(rad_angle)
        front_y = self.y - self.size * math.cos(rad_angle)

        # Adiciona a bala
        self.bullets.append([front_x, front_y, bullet_dx, bullet_dy])
        self.cooldown = self.max_cooldown

    def get_vertices(self):
        # Calcula os vértices do triângulo
        rad_angle = math.radians(self.angle)

        # Ponto da frente
        front_x = self.x + self.size * math.sin(rad_angle)
        front_y = self.y - self.size * math.cos(rad_angle)

        # Pontos traseiros
        back_left_x = self.x + self.size * 0.5 * math.sin(rad_angle + math.radians(150))
        back_left_y = self.y - self.size * 0.5 * math.cos(rad_angle + math.radians(150))

        back_right_x = self.x + self.size * 0.5 * math.sin(rad_angle + math.radians(210))
        back_right_y = self.y - self.size * 0.5 * math.cos(rad_angle + math.radians(210))

        return [(front_x, front_y), (back_left_x, back_left_y), (back_right_x, back_right_y)]

    def draw(self, surface):
        # Desenha as balas
        for bullet in self.bullets:
            pygame.draw.circle(surface, self.bullet_color, (int(bullet[0]), int(bullet[1])), 3)

        # Desenha a nave (pisca se estiver invulnerável)
        if self.invulnerable <= 0 or pygame.time.get_ticks() % 200 < 100:
            vertices = self.get_vertices()

            # Desenha o corpo da nave
            pygame.draw.polygon(surface, self.color, vertices)

            # Desenha a ponta (primeiro vértice)
            pygame.draw.circle(surface, RED, (int(vertices[0][0]), int(vertices[0][1])), 5)

    def respawn(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.velocity = 0
        self.angle = random.randint(0, 360)
        self.invulnerable = 120  # 2 segundos de invulnerabilidade
        self.bullets.clear()

    def is_hit(self, bullet_x, bullet_y):
        if self.invulnerable > 0:
            return False

        # Verifica colisão simples baseada em distância
        distance = math.sqrt((self.x - bullet_x) ** 2 + (self.y - bullet_y) ** 2)
        return distance < self.size


def draw_hud(nave1, nave2):
    # Desenha informações do HUD para ambos os jogadores

    # Jogador 1 (esquerda)
    score_text1 = font.render(f"{nave1.player_name}: {nave1.score}", True, nave1.color)
    lives_text1 = font.render(f"Vidas: {nave1.lives}", True, nave1.color)
    screen.blit(score_text1, (20, 20))
    screen.blit(lives_text1, (20, 50))

    # Jogador 2 (direita)
    score_text2 = font.render(f"{nave2.player_name}: {nave2.score}", True, nave2.color)
    lives_text2 = font.render(f"Vidas: {nave2.lives}", True, nave2.color)
    screen.blit(score_text2, (WIDTH - score_text2.get_width() - 20, 20))
    screen.blit(lives_text2, (WIDTH - lives_text2.get_width() - 20, 50))

    # Instruções
    instructions1 = font.render("Jogador 1: WASD mover, ESPAÇO atirar", True, nave1.color)
    instructions2 = font.render("Jogador 2: Setas mover, ENTER atirar", True, nave2.color)

    screen.blit(instructions1, (WIDTH // 4 - instructions1.get_width() // 2, HEIGHT - 60))
    screen.blit(instructions2, (3 * WIDTH // 4 - instructions2.get_width() // 2, HEIGHT - 60))


def show_winner_screen(winner):
    screen.fill(BLACK)

    winner_text = big_font.render(f"{winner.player_name} VENCEU!", True, winner.color)
    score_text = font.render(f"Pontuação Final: {winner.score}", True, WHITE)
    restart_text = font.render("Pressione R para reiniciar ou ESC para sair", True, WHITE)

    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        clock.tick(60)


def check_winner(nave1, nave2):
    # Verifica se algum jogador alcançou 10 pontos
    if nave1.score >= 10:
        return nave1
    elif nave2.score >= 10:
        return nave2
    return None


def reset_game():
    # Cria as naves novamente
    nave1 = Nave(WIDTH // 4, HEIGHT // 2, BLUE, YELLOW,
                 [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_SPACE],
                 pygame.K_SPACE, "Jogador 1")

    nave2 = Nave(3 * WIDTH // 4, HEIGHT // 2, GREEN, PURPLE,
                 [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RETURN],
                 pygame.K_RETURN, "Jogador 2")

    return nave1, nave2


# Cria as naves
# Jogador 1: WASD + Espaço
nave1 = Nave(WIDTH // 4, HEIGHT // 2, BLUE, YELLOW,
             [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_SPACE],
             pygame.K_SPACE, "Jogador 1")

# Jogador 2: Setas + Enter
nave2 = Nave(3 * WIDTH // 4, HEIGHT // 2, GREEN, PURPLE,
             [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RETURN],
             pygame.K_RETURN, "Jogador 2")

# Loop principal
clock = pygame.time.Clock()
running = True
game_active = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_active:
        # Obtém o estado das teclas
        keys = pygame.key.get_pressed()

        # Atualiza as naves
        nave1.update(keys)
        nave2.update(keys)

        # Verifica colisões entre balas e naves
        for bullet in nave1.bullets[:]:
            if nave2.is_hit(bullet[0], bullet[1]):
                nave1.score += 1
                nave1.bullets.remove(bullet)
                nave2.lives -= 1
                if nave2.lives > 0:
                    nave2.respawn()
                else:
                    game_active = False
                break

        for bullet in nave2.bullets[:]:
            if nave1.is_hit(bullet[0], bullet[1]):
                nave2.score += 1
                nave2.bullets.remove(bullet)
                nave1.lives -= 1
                if nave1.lives > 0:
                    nave1.respawn()
                else:
                    game_active = False
                break

        # Verifica se há um vencedor por pontuação
        winner = check_winner(nave1, nave2)
        if winner:
            game_active = False
            final_winner = winner

        # Desenha tudo
        screen.fill(BLACK)

        # Desenha naves
        nave1.draw(screen)
        nave2.draw(screen)

        # Desenha HUD
        draw_hud(nave1, nave2)

    else:
        # Tela de vitória
        if 'final_winner' in locals():
            winner_to_show = final_winner
        else:
            # Se o jogo acabou por vidas, determina o vencedor pela pontuação
            winner_to_show = nave1 if nave1.score > nave2.score else nave2
            if nave1.score == nave2.score:
                winner_to_show = nave1  # Empate, escolhe um arbitrariamente

        restart = show_winner_screen(winner_to_show)
        if restart:
            # Reinicia o jogo
            nave1, nave2 = reset_game()
            game_active = True
        else:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()