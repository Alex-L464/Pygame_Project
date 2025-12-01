import pygame
import random


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, x_speed, y_speed, attack_type, bullet_group):
        super(Bullet, self).__init__()
        if attack_type == 0:
            self.image = pygame.image.load('assets/images/player/bullet.png').convert_alpha()
        if attack_type == 1:
            self.image = pygame.image.load('assets/images/player/bullet.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = [x_speed, y_speed]
        self.attack_type = attack_type
        self.bullet_age = 0
        self.bullet_data = [attack_type]

    def update(self, bullet_group, split_group):
        random_num = random.randint(0, 10)
        SPLIT_AGE = 100
        bullets_to_split = []
        bullet_bunch = []
        if self.attack_type == 1 and self.bullet_data[0] == 1:
            for bullet in split_group:
                self.bullet_age += 1
                if bullet in bullets_to_split:
                    continue

                if self.bullet_age >= SPLIT_AGE:
                    self.bullet_age = 0
                    bullets_to_split.append(bullet)
                    split_group.remove(bullet)

                for x in bullets_to_split:
                    self.attack_type = 0
                    bullet_bunch.append(Bullet(x.rect.centerx, x.rect.bottom, 10, 0, 0, bullet_group))
                    bullet_bunch.append(Bullet(x.rect.centerx, x.rect.bottom, -10, 0, 0, bullet_group))
                    bullet_bunch.append(Bullet(x.rect.centerx, x.rect.bottom, 0, 10, 0, bullet_group))
                    bullet_bunch.append(Bullet(x.rect.centerx, x.rect.bottom, 0, -10, 0, bullet_group))
                    bullet_bunch.append(Bullet(x.rect.centerx, x.rect.bottom, 10, 10, 0, bullet_group))
                    bullet_bunch.append(Bullet(x.rect.centerx, x.rect.bottom, 10, -10, 0, bullet_group))
                    bullet_bunch.append(Bullet(x.rect.centerx, x.rect.bottom, -10, 10, 0, bullet_group))
                    bullet_bunch.append(Bullet(x.rect.centerx, x.rect.bottom, -10, -10, 0, bullet_group))
                    bullet_group.add(bullet_bunch)
                    self.attack_type = 0
                    break
                break
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.bottom >= 1200:
            self.kill()
        if self.rect.left + self.speed[0] > 1370:
            self.kill()
            self.speed[0] = self.speed[0] * -1
        if self.rect.right + self.speed[0] < -25:
            self.kill()
            self.speed[0] = self.speed[0] * -1
        if self.rect.top + self.speed[0] < 0:
            self.kill()

    def draw(screen):
        screen.blit(self.image, self.rect)
