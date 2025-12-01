import pygame


class Player:
    def __init__(self, x, y, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 55, 55))
        self.left = False
        self.right = False
        self.attacking = False
        self.attack_cooldown = 20
        self.health = 500
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, bullet_group, target):
        speed = 10
        dx = 0
        dy = 0
        dmg = 7.5
        self.left = False
        self.right = False

        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            speed = 5
            dmg = 500
        if key[pygame.K_a]:
            dx = -speed
            self.left = True
        if key[pygame.K_d]:
            dx = speed
            self.right = True
        if key[pygame.K_w]:
            dy = -speed
        if key[pygame.K_s]:
            dy = speed

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = self.rect.right - self.rect.right
        if self.rect.bottom + dy > screen_height:
            dy = screen_height - self.rect.bottom
        if self.rect.top + dy < 400:
            dy = -self.rect.top + 400

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy
        if key[pygame.K_SPACE]:
            self.attack(surface, target, dmg, bullet_group)

    def update(self):
        if self.attacking is True:
            self.update_action(3)
        elif self.left is True:
            self.update_action(1)
        elif self.right is True:
            self.update_action(2)
        else:
            self.update_action(0)

        if self.health <= 0:
            self.alive = False

        animation_cooldown = 150
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            if self.action == 3:
                self.attacking = False

    def attack(self, surface, target, dmg, bullet_group):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect1 = pygame.Rect(self.rect.centerx - 1, 0, 3, self.rect.centery)
            pygame.draw.rect(surface, (0, 0, 255), attacking_rect1)
            self.attack_cooldown = 8
            if attacking_rect1.colliderect(target.rect):
                target.health -= dmg

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        # pygame.draw.rect(surface, (0, 255, 0), self.rect)
        surface.blit(self.image, (
            self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        # pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(662, 0, 10, 1000))
