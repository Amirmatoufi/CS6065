import pygame

from uts import load_sprite, get_rand_pos
from models import milano, asteroid

class Rocks():
    MIN_MIL_DIST = 250
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((900,858))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.asteroids = []
        self.bullets = []
        self.milano = milano((450, 429), self.bullets.append)

        for _ in range(6):
            while True:
                position = get_rand_pos(self.screen)
                if (position.distance_to(self.milano.position) > self.MIN_MIL_DIST):
                    break

            self.asteroids.append(asteroid(position))

    def main_loop(self):
        while True:
            self._motion_inputs()
            self._process_logic()
            self._draw()



    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Shooter")

    def _get_objects(self):
        objects = [*self.asteroids, *self.bullets]

        if self.milano:
            objects.append(self.milano)

        return objects

    def _motion_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            elif(
                self.milano and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
            ):
                self.milano.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.milano:
            if is_key_pressed[pygame.K_RIGHT]:
                self.milano.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.milano.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.milano.accelerate()

    def _process_logic(self):
        for obj in self._get_objects():
            obj.move(self.screen)

        if self.milano:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.milano):
                    self.milano = None
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

    def _draw(self):
        self.screen.blit(self.background, (0,0))

        for obj in self._get_objects():
            obj.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(100)
