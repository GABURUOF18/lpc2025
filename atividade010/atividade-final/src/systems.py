import math
from random import uniform, choice
import pygame as pg

import config as C
import sounds
from sprites import Asteroid, Ship, UFO, Drone, Swarm
from utils import Vec, rand_edge_pos, text

class World:
    def __init__(self) -> None:
        self.ship = Ship(Vec(C.WIDTH / 2, C.HEIGHT / 2))
        self.bullets = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.ufos = pg.sprite.Group()
        self.drones = pg.sprite.Group()
        self.swarms = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.ship)

        self.lives = C.START_LIVES
        self.wave = 0
        self.wave_cool = C.WAVE_DELAY
        self.safe = C.SAFE_SPAWN_TIME
        self.spawn_pattern = "linear"
        self.enemies_defeated = 0  # Rastreia inimigos derrotados
        self.spawn_multiplier = 1.0  # Multiplicador de spawn
        self.score = 0  # Pontuação

        self.start_wave()

    def start_wave(self) -> None:
        """Inicia uma nova rodada com padrões de spawn variados."""
        self.wave += 1
        
        # Dificuldade: 20 inimigos na wave 1, dobrando a cada wave
        num_enemies = C.BASE_ENEMIES * (2 ** (self.wave - 1))
        current_speed = C.BASE_SPEED + (self.wave - 1) * C.SPEED_INC
        
        # Define padrão de spawn baseado na wave
        patterns = ["linear", "spiral", "cluster", "random"]
        self.spawn_pattern = patterns[(self.wave - 1) % len(patterns)]
        
        print(f"★ WAVE {self.wave} ★ | Enemies: {num_enemies} | Speed: {current_speed:.1f} | Pattern: {self.spawn_pattern.upper()}")

        if self.spawn_pattern == "linear":
            self._spawn_linear(num_enemies, current_speed)
        elif self.spawn_pattern == "spiral":
            self._spawn_spiral(num_enemies, current_speed)
        elif self.spawn_pattern == "cluster":
            self._spawn_cluster(num_enemies, current_speed)
        else:
            self._spawn_random(num_enemies, current_speed)

    def _spawn_linear(self, num_enemies: int, speed: float) -> None:
        """Inimigos em linha reta de uma borda."""
        target = self.ship.pos if self.ship.alive else Vec(C.WIDTH / 2, C.HEIGHT / 2)
        
        for i in range(num_enemies):
            pos = Vec(uniform(0, C.WIDTH), -50)  # Nascem de cima
            direction = (target - pos).normalize() if (target - pos).length() > 0 else Vec(0, 1)
            direction = direction.rotate(uniform(-15, 15))
            vel = direction * speed
            
            enemy_type = choice(["kamikaze", "kamikaze", "drone"])
            if enemy_type == "kamikaze":
                ufo = UFO(pos, vel)
                self.ufos.add(ufo)
                self.all_sprites.add(ufo)
            else:
                drone = Drone(pos, vel, target)
                self.drones.add(drone)
                self.all_sprites.add(drone)

    def _spawn_spiral(self, num_enemies: int, speed: float) -> None:
        """Inimigos em padrão espiral."""
        center = Vec(C.WIDTH / 2, C.HEIGHT / 2)
        
        for i in range(num_enemies):
            angle = (i / max(1, num_enemies)) * 360 + self.wave * 45
            radius = 300 + (i % 3) * 100
            
            x = center.x + math.cos(math.radians(angle)) * radius
            y = center.y + math.sin(math.radians(angle)) * radius
            pos = Vec(x, y)
            
            direction = (center - pos).normalize()
            vel = direction * speed
            
            enemy_type = choice(["swarm", "swarm", "kamikaze", "drone"])
            if enemy_type == "kamikaze":
                ufo = UFO(pos, vel)
                self.ufos.add(ufo)
                self.all_sprites.add(ufo)
            elif enemy_type == "drone":
                drone = Drone(pos, vel, center)
                self.drones.add(drone)
                self.all_sprites.add(drone)
            else:
                swarm = Swarm(pos, vel)
                self.swarms.add(swarm)
                self.all_sprites.add(swarm)

    def _spawn_cluster(self, num_enemies: int, speed: float) -> None:
        """Inimigos em grupos (clusters)."""
        num_clusters = max(2, num_enemies // 4)
        enemies_per_cluster = num_enemies // num_clusters
        
        for cluster in range(num_clusters):
            cluster_center = rand_edge_pos()
            target = self.ship.pos if self.ship.alive else Vec(C.WIDTH / 2, C.HEIGHT / 2)
            
            for i in range(enemies_per_cluster):
                offset = Vec(uniform(-100, 100), uniform(-100, 100))
                pos = cluster_center + offset
                
                direction = (target - pos).normalize() if (target - pos).length() > 0 else Vec(1, 0)
                vel = direction * speed * uniform(0.8, 1.2)
                
                enemy_type = choice(["kamikaze", "drone", "swarm", "swarm"])
                if enemy_type == "kamikaze":
                    ufo = UFO(pos, vel)
                    self.ufos.add(ufo)
                    self.all_sprites.add(ufo)
                elif enemy_type == "drone":
                    drone = Drone(pos, vel, target)
                    self.drones.add(drone)
                    self.all_sprites.add(drone)
                else:
                    swarm = Swarm(pos, vel)
                    self.swarms.add(swarm)
                    self.all_sprites.add(swarm)

    def _spawn_random(self, num_enemies: int, speed: float) -> None:
        """Inimigos aleatórios em qualquer posição."""
        target = self.ship.pos if self.ship.alive else Vec(C.WIDTH / 2, C.HEIGHT / 2)
        
        for _ in range(num_enemies):
            pos = rand_edge_pos()
            direction = (target - pos).normalize() if (target - pos).length() > 0 else Vec(1, 0)
            direction = direction.rotate(uniform(-20, 20))
            vel = direction * speed
            
            enemy_type = choice(["kamikaze", "drone", "swarm", "swarm"])
            if enemy_type == "kamikaze":
                ufo = UFO(pos, vel)
                self.ufos.add(ufo)
                self.all_sprites.add(ufo)
            elif enemy_type == "drone":
                drone = Drone(pos, vel, target)
                self.drones.add(drone)
                self.all_sprites.add(drone)
            else:
                swarm = Swarm(pos, vel)
                self.swarms.add(swarm)
                self.all_sprites.add(swarm)

    def spawn_asteroid(self, pos: Vec, vel: Vec, size: str) -> None:
        asteroid = Asteroid(pos, vel, size)
        self.asteroids.add(asteroid)
        self.all_sprites.add(asteroid)

    def try_fire(self) -> None:
        if len(self.bullets) >= C.MAX_BULLETS:
            return
        bullet = self.ship.fire()
        if bullet is None:
            return
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
        sounds.SHOT.play()

    def hyperspace(self) -> None:
        if not self.ship.alive:
            return
        self.ship.pos.xy = (uniform(0, C.WIDTH), uniform(0, C.HEIGHT))
        self.ship.vel.xy = (0, 0)

    def update(self, dt: float, keys: pg.key.ScancodeWrapper, joystick: pg.joystick.Joystick = None) -> None:
        self.ship.control(keys, dt, joystick)
        
        if joystick and self.ship.alive:
            if joystick.get_button(0): 
                self.try_fire()

        self.all_sprites.update(dt)
        
        # Atualizar tiros de todos os tipos de inimigos
        for ufo in self.ufos:
            bullet = ufo.fire()
            if bullet:
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)
        
        for drone in self.drones:
            bullet = drone.fire()
            if bullet:
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)
        
        for swarm in self.swarms:
            bullet = swarm.fire()
            if bullet:
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)

        if self.safe > 0:
            self.safe -= dt
            self.ship.invuln = 0.5
        else:
            self.ship.invuln = max(self.ship.invuln - dt, 0.0)

        self.handle_collisions()

        # Checa se acabou a rodada
        enemies_alive = len(self.asteroids) + len(self.ufos) + len(self.drones) + len(self.swarms)
        if enemies_alive == 0:
            if self.wave_cool > 0:
                self.wave_cool -= dt
            else:
                self.start_wave()
                self.wave_cool = C.WAVE_DELAY

    def handle_collisions(self) -> None:
        # Tiros vs Asteroides
        hits = pg.sprite.groupcollide(
            self.asteroids, self.bullets, False, True,
            collided=lambda a, b: (a.pos - b.pos).length() < a.r
        )
        for asteroid, _ in hits.items():
            self.split_asteroid(asteroid)

        # Tiros vs UFOs
        ufo_hits = pg.sprite.groupcollide(
            self.ufos, self.bullets, True, True,
            collided=lambda u, b: (u.pos - b.pos).length() < u.r
        )
        for ufo, _ in ufo_hits.items():
            if hasattr(ufo, "channel") and ufo.channel:
                ufo.channel.stop()
            sounds.BREAK_MEDIUM.play()
            self.score += 100

        # Tiros vs Drones
        drone_hits = pg.sprite.groupcollide(
            self.drones, self.bullets, True, True,
            collided=lambda d, b: (d.pos - b.pos).length() < d.r
        )
        for drone, _ in drone_hits.items():
            sounds.BREAK_MEDIUM.play()
            self.score += 150

        # Tiros vs Swarms
        swarm_hits = pg.sprite.groupcollide(
            self.swarms, self.bullets, True, True,
            collided=lambda s, b: (s.pos - b.pos).length() < s.r
        )
        for swarm, _ in swarm_hits.items():
            sounds.BREAK_LARGE.play()
            self.score += 200

        # Player colide
        if self.ship.alive and self.ship.invuln <= 0 and self.safe <= 0:
            for asteroid in self.asteroids:
                if (asteroid.pos - self.ship.pos).length() < (asteroid.r + self.ship.r):
                    self.ship_die()
                    break
            if self.ship.alive:
                for ufo in self.ufos:
                    if (ufo.pos - self.ship.pos).length() < (ufo.r + self.ship.r):
                        self.ship_die()
                        break
            if self.ship.alive:
                for drone in self.drones:
                    if (drone.pos - self.ship.pos).length() < (drone.r + self.ship.r):
                        self.ship_die()
                        break
            if self.ship.alive:
                for swarm in self.swarms:
                    if (swarm.pos - self.ship.pos).length() < (swarm.r + self.ship.r):
                        self.ship_die()
                        break
            if self.ship.alive:
                hits = pg.sprite.spritecollide(
                    self.ship, self.enemy_bullets, True,
                    collided=pg.sprite.collide_circle
                )
                if hits:
                    self.ship_die()

    def split_asteroid(self, asteroid: Asteroid) -> None:
        """Destroi o asteroide (SEM MULTIPLICAR)."""
        # Toca o som
        sounds.BREAK_LARGE.play()
        
        # Apenas remove o asteroide atual
        asteroid.kill()
        
        # A lógica de criar novos pedaços foi removida daqui.

    def ship_die(self) -> None:
        if not self.ship.alive:
            return
        sounds.BREAK_LARGE.play()
        self.lives -= 1
        self.ship.alive = False

        if self.lives >= 0:
            self.ship.pos.xy = (C.WIDTH / 2, C.HEIGHT / 2)
            self.ship.vel.xy = (0, 0)
            self.ship.angle = -90.0
            self.ship.invuln = C.SAFE_SPAWN_TIME
            self.safe = C.SAFE_SPAWN_TIME
            self.ship.alive = True
        else:
            self.__init__()

    def draw(self, surf: pg.Surface, font: pg.font.Font) -> None:
        for spr in self.all_sprites:
            spr.draw(surf)

        # Barra superior de status
        pg.draw.rect(surf, (15, 15, 40), (0, 0, C.WIDTH, 80))
        pg.draw.line(surf, (100, 150, 255), (0, 80), (C.WIDTH, 80), width=3)
        
        # Linha 1: Wave, Lives, Score
        text(surf, font, f"⭐ WAVE {self.wave}", 15, 10, (255, 200, 0))
        lives_color = C.RED_DANGER if self.lives <= 1 else C.WHITE
        text(surf, font, f"❤ LIVES: {self.lives}", 200, 10, lives_color)
        text(surf, font, f"📊 SCORE: {self.score}", C.WIDTH - 250, 10, (0, 255, 100))
        
        # Linha 2: Pattern, Multiplicador (Wave Doubling)
        pattern_icon = {"linear": "→→→", "spiral": "⊙⊙⊙", "cluster": "◆◆◆", "random": "???"}.get(self.spawn_pattern, "???")
        text(surf, font, f"Pattern: {pattern_icon}", 15, 40, (150, 200, 255))
        
        # Mostrar multiplicador baseado na wave
        wave_multiplier = 2 ** (self.wave - 1)
        text(surf, font, f"Enemies 2^{self.wave-1}: {wave_multiplier}x", 250, 40, (255, 150, 100))
        
        # Contador total de inimigos
        enemies_total = len(self.asteroids) + len(self.ufos) + len(self.drones) + len(self.swarms)
        enemy_color = (0, 255, 0) if enemies_total == 0 else C.RED_DANGER
        text(surf, font, f"Enemies: {enemies_total}", C.WIDTH - 250, 40, enemy_color)
        
        # Detalhes dos inimigos (linha 3)
        details_y = 60
        details_x = 15
        if len(self.ufos) > 0:
            text(surf, font, f"🔴 Kamikazes: {len(self.ufos)}", details_x, details_y, (255, 100, 100))
            details_x += 180
        if len(self.drones) > 0:
            text(surf, font, f"🟢 Drones: {len(self.drones)}", details_x, details_y, (100, 255, 100))
            details_x += 150
        if len(self.swarms) > 0:
            text(surf, font, f"🟠 Swarms: {len(self.swarms)}", details_x, details_y, (255, 150, 0))