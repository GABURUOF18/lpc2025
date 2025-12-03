import random
import sys
from dataclasses import dataclass

import pygame as pg

import config as C
from systems import World
from utils import text


@dataclass
class Scene:
    name: str


class Game:
    def __init__(self):
        pg.init()
        
        # Joystick Initialization
        pg.joystick.init()
        self.joystick = None
        if pg.joystick.get_count() > 0:
            self.joystick = pg.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick Conectado: {self.joystick.get_name()}")
        else:
            print("Nenhum Joystick detectado (Use teclado).")

        if C.RANDOM_SEED is not None:
            random.seed(C.RANDOM_SEED)
        self.screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
        pg.display.set_caption("Survival Asteroids - Rounds")
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("consolas", 20)
        self.big = pg.font.SysFont("consolas", 48)
        self.scene = Scene("menu")
        self.world = World()

    def run(self):
        while True:
            dt = self.clock.tick(C.FPS) / 1000.0
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit(0)
                
                # Events Game
                if self.scene.name == "play":
                    # Keyboard (Backup)
                    if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                        self.world.try_fire()
                    if e.type == pg.KEYDOWN and e.key == pg.K_LSHIFT:
                        self.world.hyperspace()
                    
                    # Joystick (One-click buttons)
                    if e.type == pg.JOYBUTTONDOWN:
                        # Botão 1 ('B' or 'Ball')
                        if e.button == 1: 
                            self.world.hyperspace()
                        # Start (Button 7) -> Pause or Menu

                # Menu Event
                elif self.scene.name == "menu":
                    if e.type == pg.KEYDOWN or e.type == pg.JOYBUTTONDOWN:
                        self.scene = Scene("play")

            keys = pg.key.get_pressed()
            self.screen.fill(C.BLACK)

            if self.scene.name == "menu":
                self.draw_menu()
            elif self.scene.name == "play":
                self.world.update(dt, keys, self.joystick)
                self.world.draw(self.screen, self.font)

            pg.display.flip()

    def draw_menu(self):
        # Background gradient effect with rectangles
        for i in range(0, C.HEIGHT, 20):
            alpha = int(100 * (i / C.HEIGHT))
            color = (20, 20, 60)
            pg.draw.line(self.screen, color, (0, i), (C.WIDTH, i), 2)
        
        text(self.screen, self.big, "⚔ BATTLE ARENA ⚔",
            C.WIDTH // 2 - 240, 120, (255, 100, 100))
        
        text(self.screen, self.font,
            "Survive waves of enemies and climb the ranks!",
            150, 220, (100, 200, 255))
        
        text(self.screen, self.font,
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            200, 260, (150, 150, 150))
        
        text(self.screen, self.font,
            "⬅ ➡  Move  |  SPACE  Shoot  |  SHIFT  Jump",
            160, 310, C.WHITE)
        
        text(self.screen, self.font,
            "🎮  Gamepad: L-Stick move, RT fire, B jump",
            180, 350, (200, 200, 100))
        
        text(self.screen, self.font,
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            200, 390, (150, 150, 150))
        
        text(self.screen, self.font,
            "Press ANY KEY to START", 300, 460, (0, 255, 100))
        
        text(self.screen, self.font,
            "Created by: Gabriel & Luís", 330, 600, (150, 150, 200))