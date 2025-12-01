import pygame
from bullet import Bullet
import random


# bullet_group = pygame.sprite.Group()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, data, sprite_sheet, animation_steps, death_sound):
        super().__init__()
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = [pygame.time.get_ticks(), pygame.time.get_ticks()]
        self.rect = pygame.Rect((x, y, 350, 400))
        self.split_bull = pygame.Rect((self.rect.centerx, self.rect.bottom, 10, 10))
        self.attacking = False
        self.attack_cooldown = 20
        self.attack_type = 0
        self.health = 5000
        self.alive = True
        self.stage = 0
        self.center = False
        self.is_center = False
        self.move_l = True
        self.attack_stage = 0
        self.repeat_times = [0, 0]
        self.ai_on = False
        self.test = 2000
        self.locked = [False, False, False]
        self.is_charging = False
        self.charge_attack = False
        self.enraged = False
        self.death_sound = death_sound

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

    def enemy_actions(self, screen_width, screen_height, surface, bullet_group, split_group, target, is_counting):
        random_numy = random.randint(2, 6)
        random_num_x = random.randint(2, 6)
        speed = 1 + (1 * self.stage)
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()

        if is_counting is True:
            dy = 1
        if is_counting is False:
            self.ai_on = True

        if key[pygame.K_c]:
            self.center = True

        if key[pygame.K_v]:
            self.is_center = True
            self.center = False

        if self.center is True:
            if self.rect.left > 502:
                dx = -speed
            elif self.rect.left < 498:
                dx = speed
            else:
                self.is_center = True
                if self.is_charging is False:
                    self.attack_cooldown = 200 - (40 * self.stage)
                    self.is_charging = True
        if self.alive is True and self.stage < 4:
            if key[pygame.K_LEFT] or self.move_l is True and self.center is False and self.ai_on is True:
                dx -= speed
            if key[pygame.K_RIGHT] or self.move_l is False and self.center is False and self.ai_on is True:
                dx += speed
            if key[pygame.K_k] or (self.attack_stage == 1 and self.ai_on is True):
                self.attack_type = 1
                if self.attack_cooldown == 0:
                    self.repeat_times[0] += 1
                    bullet_frag = Bullet(self.rect.centerx + 75, self.rect.bottom, 0, random_numy, 1, bullet_group)
                    bullet_frag2 = Bullet(self.rect.centerx - 75, self.rect.bottom, 0, random_numy, 1, bullet_group)
                    split_group.add(bullet_frag)
                    split_group.add(bullet_frag2)
                    self.update_time[0] = pygame.time.get_ticks()
                    self.attack_cooldown = 50 - (10 * self.stage)
                if self.repeat_times[0] == 1 + self.stage:
                    self.attack_stage = 0
                    self.repeat_times[0] = 0
                    self.repeat_times[1] += 1
                    if self.repeat_times[1] >= 5:
                        if self.stage >= 1:
                            self.attack_stage = 2
                            self.center = True
                            self.repeat_times[1] = 0

            if key[pygame.K_p] or (self.attack_stage == 0 and self.ai_on is True):
                if self.attack_cooldown == 0:
                    self.repeat_times[0] += 1
                    for i in range(0, 2 + self.stage):
                        bullet = Bullet(self.rect.centerx + 75 + (20 * i), self.rect.bottom - 50 - (20 * i),
                                        1 + (i * 1),
                                        5 - (i * 1), 0, bullet_group)
                        bullet2 = Bullet(self.rect.centerx - 85 - (20 * i), self.rect.bottom - 50 - (20 * i),
                                         -1 - (i * 1),
                                         5 - (i * 1), 0, bullet_group)
                        bullet_group.add(bullet)
                        bullet_group.add(bullet2)
                        self.attack_cooldown = 50 - (5 * self.stage)
                        self.attack_type = 0
                if self.repeat_times[0] == 5:
                    self.attack_stage = 1
                    self.repeat_times[0] = 0

            if key[pygame.K_l] or (
                    self.attack_stage == 2 and self.ai_on is True and self.is_center is True and self.stage >= 1):
                if target.rect.centerx >= self.rect.centerx and self.locked[0] is False:
                    self.move_l = False
                    self.locked[0] = True
                    self.charge_attack = True
                if target.rect.centerx < self.rect.centerx and self.locked[0] is False:
                    self.move_l = True
                    self.locked[0] = True
                    self.charge_attack = True
                if self.attack_cooldown <= 0:
                    self.is_charging = False
                    self.center = False
                    for i in range(0, 5):
                        bullet = Bullet(self.rect.centerx + (20 * i), self.rect.bottom - 50 + (20 * i), 0, 50, 0,
                                        bullet_group)
                        bullet2 = Bullet(self.rect.centerx - (20 * i), self.rect.bottom - 50 + (20 * i), 0, 50, 0,
                                         bullet_group)
                        bullet_group.add(bullet)
                        bullet_group.add(bullet2)

            if self.rect.left + dx < -75:
                dx = -self.rect.left - 75
                self.move_l = False
                self.is_center = False
                if self.locked[0] is True:
                    self.locked[0] = False
                    self.attack_stage = 0

            if self.rect.right + dx > screen_width + 75:
                dx = self.rect.right - self.rect.right
                self.move_l = True
                self.is_center = False
                if self.locked[0] is True:
                    self.locked[0] = False
                    self.attack_stage = 0

            if self.rect.bottom + dy > 400:
                dy = 400 - self.rect.bottom

            self.rect.x += dx
            self.rect.y += dy
            if key[pygame.K_z]:
                self.ai_on = True
            if key[pygame.K_x]:
                self.ai_on = False
        if self.stage == 4 and self.alive is True:
            self.rect.x += dx
            self.rect.y += dy
            if self.is_center is True:
                self.enraged = True
                self.test -= 1
                if self.action == 6 and self.alive is True:
                    for i in range(0, 15):
                        bullet = Bullet(self.rect.centerx + (20 * i), self.rect.bottom - 50 + (17 * i), 0, 50, 0,
                                        bullet_group)
                        bullet2 = Bullet(self.rect.centerx - (20 * i), self.rect.bottom - 50 + (17 * i), 0, 50, 0,
                                         bullet_group)
                        bullet_group.add(bullet)
                        bullet_group.add(bullet2)

                        if self.attack_cooldown <= 0 and self.alive is True:
                            self.repeat_times[0] += 1
                            bullet_frag = Bullet(self.rect.centerx + 75, self.rect.bottom, random_num_x, random.randint(0, 2), 1, bullet_group)
                            bullet_frag2 = Bullet(self.rect.centerx - 75, self.rect.bottom, -random_num_x, random.randint(0, 2), 1, bullet_group)
                            split_group.add(bullet_frag)
                            split_group.add(bullet_frag2)
                            self.update_time[0] = pygame.time.get_ticks()
                            if self.test <= 0:
                                self.alive = False
                            elif self.test <= 500:
                                self.attack_cooldown = 20
                            elif self.test <= 1000:
                                self.attack_cooldown = 30
                            elif self.test <= 1500:
                                self.attack_cooldown = 40
                            elif self.test <= 2000:
                                self.attack_cooldown = 60
                pass

        p_hit = pygame.sprite.spritecollide(target, bullet_group, False)
        s_hit = pygame.sprite.spritecollide(target, split_group, False)
        for x in p_hit:
            if self.enraged is True:
                target.health -= 15
                x.kill()
            else:
                target.health -= 2 + (2 * (1 * self.stage))
                x.kill()
        for y in s_hit:
            target.health -= 15 + (20 * (1 * self.stage))
            y.kill()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def update(self):
        if self.stage == 4 and self.enraged is True:
            if self.locked[2] is False:
                self.update_action(5)
            if self.locked[1] is False:
                self.update_time[1] = pygame.time.get_ticks()
                self.locked[1] = True
            if pygame.time.get_ticks() - self.update_time[1] > 950:
                self.update_action(6)
                self.locked[2] = True

        elif self.is_charging is True and self.locked[0] is True:
            if self.locked[2] is False and self.move_l is False:
                self.update_action(1)
            elif self.locked[2] is False and self.move_l is True:
                self.update_action(3)
            if self.locked[1] is False:
                self.update_time[1] = pygame.time.get_ticks()
                self.locked[1] = True
            if self.charge_attack is True and pygame.time.get_ticks() - self.update_time[
                1] > 900 and self.move_l is False:
                self.update_action(2)
                self.locked[2] = True
            elif self.charge_attack is True and pygame.time.get_ticks() - self.update_time[
                1] > 900 and self.move_l is True:
                self.update_action(4)
                self.locked[2] = True
        elif self.locked[0] is False:
            self.update_action(0)
            self.locked[1] = False
            self.locked[2] = False
        if self.stage == 3:
            self.health -= 1
        if self.health < (5000 * (3 / 4)):
            self.stage = 1
        if self.health < (5000 * (2 / 4)):
            self.stage = 2
        if self.health < (5000 * (1 / 4)):
            self.stage = 3
        if self.health <= 0:
            self.stage = 4
            self.center = True
        print("")
        print("Stage: " + str(self.stage))
        print("Attack Stage: " + str(self.attack_stage))
        print("Attack Cooldown: " + str(self.attack_cooldown))
        print("Repeat Times: " + str(self.repeat_times))
        print("Test: " + str(self.test))
        print(str(self.locked))
        animation_cooldown = 150
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time[0] > animation_cooldown:
            self.frame_index += 1
            self.update_time[0] = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        if self.alive is False:
            self.death_sound.play()

    def create_bullet(self):
        return Bullet(self.rect.x, self.rect.y)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time[0] = pygame.time.get_ticks()

    def draw(self, surface):
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(self.image, (
            self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
