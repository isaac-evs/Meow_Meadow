import pygame
from timer import Timer
from settings import *
from support import *
from debug import debug

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group):
        super().__init__(group)

        #animations
        self.import_assets()
        self.status = "down_idle"
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.z = LAYERS["main"]

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 25

        # timers
        self.timers = {
            "tool_use": Timer(350,self.use_tool),
            "tool_switch": Timer(200),
            "seed_use": Timer(350,self.use_seed),
            "seed_switch": Timer(200)
        }

        # tools
        self.tools = ["hoe", "axe", "water"]
        self.tool_index = 0
        self.selected_tool  = self.tools[self.tool_index]

        # seeds
        self.seeds = ["corn", "tomato"]
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def import_assets(self):
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
                           "right_hoe" : [], "left_hoe" : [], "up_hoe" : [], "down_hoe" : [],
                           "right_axe" : [], "left_axe" : [], "up_axe" : [], "down_axe" : [],
                           "right_water": [], "left_water": [], "up_water": [], "down_water": []}

        for animation in self.animations.keys():
            full_path = "../graphics/character/" + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 0.5 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["tool_use"].active:
            # movement
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            # tool use
            if keys[pygame.K_SPACE]:
                self.timers["tool_use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 1

            # change tool
            if keys[pygame.K_q] and not self.timers["tool_switch"].active:
                self.timers["tool_switch"].activate()
                self.tool_index += 1
                if self.tool_index >= len(self.tools):
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]

            # seed use
            if keys[pygame.K_z]:
                self.timers["seed_use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # change seed
            if keys[pygame.K_x] and not self.timers["seed_switch"].active:
                self.timers["seed_switch"].activate()
                self.seed_index += 1
                if not self.seed_index < len(self.seeds):
                    self.seed_index = 0
                self.selected_seed = self.seeds[self.seed_index]

    def use_tool(self):
        pass

    def use_seed(self):
        pass

    def get_status(self):

        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"

        # tool use
        if self.timers["tool_use"].active:
            self.status = self.status.split("_")[0] + "_" + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):

        # normalize vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)
