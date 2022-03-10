from pygame.math import Vector2
from pygame.transform import rotozoom

from uts import load_sprite, wrap, get_rand_vel

UP = Vector2 (0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap(self.position + self.velocity, surface)

    def collides_with(self, other_object):
        distance = self.position.distance_to(other_object.position)
        return distance < self.radius + other_object.radius

class milano(GameObject):
    MANEUVERABILITY = 4
    ACCELERATION = 0.4
    BULLET = 3

    def __init__(self, position, bullet_callback):
        self.bullet_callback = bullet_callback
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("milano"), Vector2(0))

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.bullet_callback(bullet)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

class asteroid(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("asteroids"), get_rand_vel(1, 3))

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
