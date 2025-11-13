# === Imports ===
import pygame
import math

# === Constantes ===
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60
BLACK = (0, 0, 0)
BLUE = (66, 135, 245)
RED = (245, 66, 66)

TRI_WIDTH = 60
TRI_HEIGHT = 40
TRI_SPEED = 1
BALL_RADIUS = 10
BALL_SPEED = 8

# === Classes ===
class Ball:
    def __init__(self, x, y, angle, color, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED
        self.owner = owner  # 'p1' ou 'p2'

    def move(self):
        rad = math.radians(self.angle)
        self.x += self.speed * math.sin(rad)
        self.y += -self.speed * math.cos(rad)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def is_offscreen(self):
        return (
            self.x < -self.radius or self.x > SCREEN_WIDTH + self.radius or
            self.y < -self.radius or self.y > SCREEN_HEIGHT + self.radius
        )


class Ship:
    def start_dying(self):
        self.dying = True
        self.dying_frames = 0
        
    def __init__(self, x, y, color, angle=0):
        self.width = TRI_WIDTH
        self.height = TRI_HEIGHT
        self.x = x
        self.y = y
        self.color = color
        self.speed = TRI_SPEED
        self.angle = angle
        self.brake = 1
        self.toggle_last = False
        self.dying = False
        self.dying_frames = 0

    def move_forward(self):
        rad = math.radians(self.angle)
        dx = self.speed * math.sin(rad)
        dy = -self.speed * math.cos(rad)
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

    def rotate(self, delta):
        self.angle = (self.angle + delta) % 360

    def draw(self, surface):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        top = (self.x + self.width // 2, self.y)
        left = (self.x, self.y + self.height)
        right = (self.x + self.width, self.y + self.height)
        points = [left, right, top]
        def rotate_point(px, py):
            rad = math.radians(self.angle)
            dx = px - cx
            dy = py - cy
            qx = cx + dx * math.cos(rad) - dy * math.sin(rad)
            qy = cy + dx * math.sin(rad) + dy * math.cos(rad)
            return (int(qx), int(qy))
        rotated_points = [rotate_point(px, py) for (px, py) in points]
        pygame.draw.polygon(surface, self.color, rotated_points)
        tip = rotated_points[2]
        base_left = rotated_points[0]
        base_right = rotated_points[1]
        vx = base_right[0] - base_left[0]
        vy = base_right[1] - base_left[1]
        base_len = math.hypot(vx, vy)
        mini_height = 18
        mini_base = 16
        if base_len == 0:
            mini_left = mini_right = tip
        else:
            perp_vx = -(vy / base_len)
            perp_vy = vx / base_len
            mini_base_cx = tip[0] + perp_vx * mini_height
            mini_base_cy = tip[1] + perp_vy * mini_height
            unit_vx = vx / base_len
            unit_vy = vy / base_len
            mini_left = (
                int(mini_base_cx - unit_vx * (mini_base / 2)),
                int(mini_base_cy - unit_vy * (mini_base / 2))
            )
            mini_right = (
                int(mini_base_cx + unit_vx * (mini_base / 2)),
                int(mini_base_cy + unit_vy * (mini_base / 2))
            )
        mini_points = [mini_left, mini_right, tip]
        pygame.draw.polygon(surface, (255, 0, 0), mini_points)

    def get_tip_position(self):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        top = (self.x + self.width // 2, self.y)
        left = (self.x, self.y + self.height)
        right = (self.x + self.width, self.y + self.height)
        points = [left, right, top]
        def rotate_point(px, py):
            rad = math.radians(self.angle)
            dx = px - cx
            dy = py - cy
            qx = cx + dx * math.cos(rad) - dy * math.sin(rad)
            qy = cy + dx * math.sin(rad) + dy * math.cos(rad)
            return (qx, qy)
        rotated_points = [rotate_point(px, py) for (px, py) in points]
        tip = rotated_points[2]
        return tip

    def collides_with_ball(self, ball):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        dist = math.hypot(ball.x - cx, ball.y - cy)
        return dist < (self.width // 2 + ball.radius // 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dois Triângulos Independentes")
    clock = pygame.time.Clock()

    ship1 = Ship(100, SCREEN_HEIGHT//2 - TRI_HEIGHT//2, BLUE, angle=90)
    ship2 = Ship(SCREEN_WIDTH-100-TRI_WIDTH, SCREEN_HEIGHT//2 - TRI_HEIGHT//2, RED, angle=270)

    running = True
    ship1_toggle_last = False
    ship2_toggle_last = False
    balls = []
    ship1_shoot_last = False
    ship2_shoot_last = False
    ship1_alive = True
    ship2_alive = True
    ROTATE_FRAMES = 36  # 3 voltas = 1080° / 30° por frame = 36 frames
    ROTATE_DEGREES_PER_FRAME = 30
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        keys = pygame.key.get_pressed()
        
        # BRAKE toggle: Q para ship1, P para ship2 (edge detection)
        if ship1_alive and keys[pygame.K_q]:
            if not ship1_toggle_last:
                ship1.brake = 1 - ship1.brake
            ship1_toggle_last = True
        else:
            ship1_toggle_last = False
            
        if ship2_alive and keys[pygame.K_p]:
            if not ship2_toggle_last:
                ship2.brake = 1 - ship2.brake
            ship2_toggle_last = True
        else:
            ship2_toggle_last = False
            
        # Player 1 controls (A/D rotate, Q toggle BRAKE, SPACE atira)
        if ship1_alive:
            if not ship1.dying:
                if keys[pygame.K_a]:
                    ship1.rotate(-5)
                if keys[pygame.K_d]:
                    ship1.rotate(5)
                if ship1.brake == 0:
                    ship1.move_forward()
                # Player 1 shoot (SPACE)
                if keys[pygame.K_SPACE]:
                    if not ship1_shoot_last:
                        tip = ship1.get_tip_position()
                        balls.append(Ball(tip[0], tip[1], ship1.angle, BLUE, 'p1'))
                    ship1_shoot_last = True
                else:
                    ship1_shoot_last = False
            else:
                # Animação de rotação ao morrer
                if ship1.dying_frames < ROTATE_FRAMES:
                    ship1.rotate(ROTATE_DEGREES_PER_FRAME)
                    ship1.dying_frames += 1
                else:
                    ship1_alive = False
                    
        # Player 2 controls (LEFT/RIGHT rotate, P toggle BRAKE, RCTRL atira)
        if ship2_alive:
            if not ship2.dying:
                if keys[pygame.K_LEFT]:
                    ship2.rotate(-5)
                if keys[pygame.K_RIGHT]:
                    ship2.rotate(5)
                if ship2.brake == 0:
                    ship2.move_forward()
                # Player 2 shoot (RCTRL)
                if keys[pygame.K_RCTRL]:
                    if not ship2_shoot_last:
                        tip = ship2.get_tip_position()
                        balls.append(Ball(tip[0], tip[1], ship2.angle, RED, 'p2'))
                    ship2_shoot_last = True
                else:
                    ship2_shoot_last = False
            else:
                # Animação de rotação ao morrer
                if ship2.dying_frames < ROTATE_FRAMES:
                    ship2.rotate(ROTATE_DEGREES_PER_FRAME)
                    ship2.dying_frames += 1
                else:
                    ship2_alive = False
                    
        # Atualiza bolas
        for ball in balls:
            ball.move()
        balls = [b for b in balls if not b.is_offscreen()]
        
        # Colisão bolas x naves
        if ship1_alive and not ship1.dying:
            for ball in balls:
                if ship1.collides_with_ball(ball) and ball.owner == 'p2' and ship2_alive:
                    ship1.start_dying()
                    
        if ship2_alive and not ship2.dying:
            for ball in balls:
                if ship2.collides_with_ball(ball) and ball.owner == 'p1' and ship1_alive:
                    ship2.start_dying()
                    
        screen.fill(BLACK)
        
        if ship1_alive:
            ship1.draw(screen)
        if ship2_alive:
            ship2.draw(screen)
            
        for ball in balls:
            ball.draw(screen)
            
        font = pygame.font.SysFont("Arial", 24)
        txt1 = font.render(f"Player 1 BRAKE: {'ON' if ship1.brake else 'OFF'} (Q, SPACE atira)", True, (200,200,255))
        txt2 = font.render(f"Player 2 BRAKE: {'ON' if ship2.brake else 'OFF'} (P, RCTRL atira)", True, (255,200,200))
        
        screen.blit(txt1, (20, 20))
        screen.blit(txt2, (SCREEN_WIDTH - txt2.get_width() - 20, 20))
        
        if not ship1_alive:
            win2 = font.render("Player 2 venceu!", True, (255,255,0))
            screen.blit(win2, (SCREEN_WIDTH//2 - win2.get_width()//2, SCREEN_HEIGHT//2))
            
        if not ship2_alive:
            win1 = font.render("Player 1 venceu!", True, (255,255,0))
            screen.blit(win1, (SCREEN_WIDTH//2 - win1.get_width()//2, SCREEN_HEIGHT//2 + 40))
            
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()