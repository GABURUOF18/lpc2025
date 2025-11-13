import pygame
import sys
import os

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo do Personagem")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Classe do Personagem
class Player:
    def __init__(self):
        # Posição e movimento
        self.x = 100
        self.y = 400
        self.width = 50
        self.height = 80
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        self.is_jumping = False
        self.facing_right = True
        
        # Animações
        self.walk_frames = []
        self.current_frame = 0
        self.animation_speed = 0.2
        
        # Estados
        self.is_shooting = False
        self.shoot_cooldown = 0
        self.shoot_duration = 10
        
        # Criar sprites temporários (substitua por suas imagens)
        self.create_temp_sprites()
    
    def create_temp_sprites(self):
        sprites_dir = "atividade00/assets/megaman_classic"
        if not os.path.exists(sprites_dir):
            print(f"[ERRO] Pasta de sprites não encontrada: {sprites_dir}")
            self.idle_sprite = None
            self.walk_frames = []
            self.jump_sprite = None
            self.shoot_sprite = None
            return

        all_pngs = [f for f in os.listdir(sprites_dir) if f.lower().endswith('.png')]

        def load_img(name):
            path = os.path.join(sprites_dir, name)
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                return img
            except Exception:
                print(f"[ERRO] Falha ao carregar {name}")
                return None

        # Sprite parado: primeiro PNG que contenha 'idle' ou 'start'
        idle_candidates = [f for f in all_pngs if 'idle' in f or 'start' in f]
        self.idle_sprite = load_img(idle_candidates[0]) if idle_candidates else None
        if not self.idle_sprite:
            print("[ERRO] Nenhum sprite de idle/start encontrado! O personagem parado ficará invisível.")

        # Walk frames: PNGs que contenham 'walk' ou 'walking'
        walk_candidates = [f for f in all_pngs if 'walk' in f]
        self.walk_frames = [load_img(f) for f in walk_candidates if load_img(f)]
        if not self.walk_frames:
            print("[ERRO] Nenhum sprite de walk encontrado! Personagem andando ficará invisível.")

        # Jump sprite: PNG que contenha 'jump'
        jump_candidates = [f for f in all_pngs if 'jump' in f]
        self.jump_sprite = load_img(jump_candidates[0]) if jump_candidates else None
        if not self.jump_sprite:
            print("[ERRO] Nenhum sprite de jump encontrado! Personagem pulando ficará invisível.")

        # Shoot sprite: PNG que contenha 'shoot' ou 'gun'
        shoot_candidates = [f for f in all_pngs if 'shoot' in f or 'gun' in f]
        self.shoot_sprite = load_img(shoot_candidates[0]) if shoot_candidates else None
        if not self.shoot_sprite:
            print("[ERRO] Nenhum sprite de shoot/gun encontrado! Personagem atirando ficará invisível.")
    
    def jump(self):
        if not self.is_jumping:
            self.vel_y = -self.jump_power
            self.is_jumping = True
    
    def shoot(self):
        if not self.is_shooting:
            self.is_shooting = True
            self.shoot_cooldown = self.shoot_duration
            
            # Calcular posição do projétil baseado na direção
            if self.facing_right:
                proj_x = self.x + self.width
            else:
                proj_x = self.x - 20
            proj_y = self.y + self.height // 2 - 5
            
            return Projectile(proj_x, proj_y, self.facing_right)
        return None

    def update(self):
        # Aplicar gravidade
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Verificar colisão com o chão
        if self.y > 400:
            self.y = 400
            self.vel_y = 0
            self.is_jumping = False

        # Movimento horizontal
        self.x += self.vel_x

        # Limitar movimento na tela
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

        # Atualizar animação
        if not self.is_jumping and not self.is_shooting:
            if self.vel_x != 0:
                self.current_frame += self.animation_speed

                # Limite para número de frames
                if self.walk_frames:
                    if self.current_frame >= len(self.walk_frames):
                        self.current_frame = 0
                else:
                    if self.current_frame >= 1:
                        self.current_frame = 0

        # Cooldown do tiro
        if self.is_shooting:
            self.shoot_cooldown -= 1
            if self.shoot_cooldown <= 0:
                self.is_shooting = False
    
    def draw(self, screen):
        current_sprite = None
        fallback = None

        if self.is_shooting:
            current_sprite = self.shoot_sprite
            if current_sprite is None:
                fallback = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.rect(fallback, (255, 165, 0), (0, 0, self.width, self.height))
        elif self.is_jumping:
            current_sprite = self.jump_sprite
            if current_sprite is None:
                fallback = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.rect(fallback, (0, 255, 0), (0, 0, self.width, self.height))
        elif self.vel_x != 0:
            if self.walk_frames:
                frame_index = int(self.current_frame) % len(self.walk_frames)
                current_sprite = self.walk_frames[frame_index]
            else:
                fallback = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.rect(fallback, BLUE, (0, 0, self.width, self.height))
        else:
            current_sprite = self.idle_sprite
            if current_sprite is None:
                fallback = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.rect(fallback, BLUE, (0, 0, self.width, self.height))

        # Desenhar sprite ou fallback na direção correta
        sprite_to_draw = current_sprite if current_sprite is not None else fallback
        if sprite_to_draw is not None:
            if self.facing_right:
                screen.blit(sprite_to_draw, (self.x, self.y))
            else:
                flipped_sprite = pygame.transform.flip(sprite_to_draw, True, False)
                screen.blit(flipped_sprite, (self.x, self.y))

# Classe do Projétil
class Projectile:
    def __init__(self, x, y, facing_right):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 10
        self.speed = 10
        self.facing_right = facing_right
        self.active = True
        
        # Tentar usar imagem de bala do pacote de assets
        try:
            bullet_path = "assets/megaman_classic/bullet-0001.png"
            img = pygame.image.load(bullet_path).convert_alpha()
            self.sprite = pygame.transform.scale(img, (self.width, self.height))
        except Exception:
            # Criar sprite temporário do projétil
            self.sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.ellipse(self.sprite, (255, 255, 0), (0, 0, self.width, self.height))
    
    def update(self):
        if self.facing_right:
            self.x += self.speed
        else:
            self.x -= self.speed
        
        # Desativar se sair da tela
        if self.x < -50 or self.x > SCREEN_WIDTH + 50:
            self.active = False
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

# Função principal
def main():
    clock = pygame.time.Clock()
    player = Player()
    projectiles = []
    
    # Fonte para texto
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        # Processar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_f:
                    projectile = player.shoot()
                    if projectile:
                        projectiles.append(projectile)
        
        # Capturar teclas pressionadas
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal
        player.vel_x = 0
        if keys[pygame.K_LEFT]:
            player.vel_x = -player.speed
            player.facing_right = False
        if keys[pygame.K_RIGHT]:
            player.vel_x = player.speed
            player.facing_right = True
        
        # Atirar (tecla F)
        if keys[pygame.K_f] and not player.is_shooting:
            projectile = player.shoot()
            if projectile:
                projectiles.append(projectile)
        
        # Atualizar
        player.update()
        
        # Atualizar projéteis
        for projectile in projectiles[:]:
            projectile.update()
            if not projectile.active:
                projectiles.remove(projectile)
        
        # Desenhar
        screen.fill(BLACK)
        
        # Desenhar chão
        pygame.draw.rect(screen, (100, 100, 100), (0, 480, SCREEN_WIDTH, SCREEN_HEIGHT - 480))
        
        # Desenhar personagem e projéteis
        player.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)
        
        # Desenhar instruções
        instructions = [
            "Setas: Mover",
            "Espaço: Pular",
            "F: Atirar"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            screen.blit(text, (10, 10 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()