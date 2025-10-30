import pygame
import pytmx
from pytmx import load_pygame
import math


class Base_Player():
    def __init__(self, player_name, pos, speed=5):
        self.image = pygame.image.load("asset/img/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 200))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.name = player_name

        self.vector = pygame.math.Vector2
        self.velocity = self.vector()
        self.acceleration = self.vector(0,0)
        self.pos = self.vector(pos)
        self.friction = 0.3


    def update(self):
        self.rect.x += 5
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     self.rect.x -= self.speed
        # if keys[pygame.K_RIGHT]:
        #     self.rect.x += self.speed
        # if keys[pygame.K_UP]:
        #     self.rect.y -= self.speed
        # if keys[pygame.K_DOWN]:
        #     self.rect.y += self.speed
    def wall_collision(self, map_size):
        if self.rect.left < - 50:
            self.rect.left = -50
        if self.rect.right > map_size[0]:
            self.rect.right = map_size[0]
        if self.rect.top < -50:
            self.rect.top = -50
        if self.rect.bottom > map_size[1]:
            self.rect.bottom = map_size[1]

    def draw(self, surface: pygame.Surface, camera):
        surface.blit(self.image, camera.apply(self.rect))

    def draw_name(self, surface: pygame.Surface, font: pygame.font.Font, camera):

        player_name = font.render(self.name, True, (255,0,0))
        surface.blit(player_name, camera.apply(self.rect, move_to=(160, 0)))

class Player(Base_Player):
    def __init__(self, player_name, pos):
        super().__init__(player_name, pos)
        self.boost  =1.5



    def update(self):
        self.acceleration = self.vector(0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -self.speed * self.is_boosting()
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = self.speed * self.is_boosting()
        if keys[pygame.K_UP]:
            self.acceleration.y = -self.speed * self.is_boosting()
        if keys[pygame.K_DOWN]:
            self.acceleration.y = self.speed  * self.is_boosting()
        




        self.acceleration -= self.velocity * self.friction
        self.velocity += self.acceleration
        self.pos += self.velocity + 0.5 * self.acceleration




        self.rect.topleft = self.pos


        # if keys[pygame.K_LEFT]:
        #     self.rect.x -= self.speed + self.is_boosting()

        # if keys[pygame.K_RIGHT]:
        #     self.rect.x += self.speed + self.is_boosting()
        # if keys[pygame.K_UP]:
        #     self.rect.y -= self.speed + self.is_boosting()
        # if keys[pygame.K_DOWN]:
        #     self.rect.y += self.speed + self.is_boosting()

    def is_boosting(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            return self.boost
        return 1

class NPC(Base_Player):
    def __init__(self, player_name, pos):
        super().__init__(player_name, pos)


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity: pygame.Rect, move_to=(0,0)):
        entity = entity.move(move_to)
        return entity.move(-self.camera.topleft[0], -self.camera.topleft[1])

    def update(self, target: pygame.Rect , map_width, map_height):

        x = target.centerx - self.width // 2
        y = target.centery - self.height // 2

        if map_width <= self.width:
            x = 0
        else:
            x = max(0, min(x, map_width - self.width))

        if map_height <= self.height:
            y = 0
        else:
            y = max(0, min(y, map_height - self.height))

        self.camera.topleft = (x, y)



class TileMap(pygame.sprite.Sprite):
    def __init__(self, tmx_data, *groups):
        super().__init__(*groups)
        self.tmx_data = tmx_data
        self.width = tmx_data.width * tmx_data.tilewidth
        self.height = tmx_data.height * tmx_data.tileheight


class TwoPI:
    def __init__(self):

        # pygame
        pygame.init()
        WIDTH, HEIGHT = 2500, 1400
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2PI Game")
        self.clock = pygame.time.Clock()
        self.group = pygame.sprite.Group()

        # camera
        self.camera = Camera(WIDTH, HEIGHT)

        # game variables
        self.font = pygame.font.Font("Font/LuckiestGuy.ttf", 30)
        self.running = True
        self.tmx_data = load_pygame("asset/tmx/map.tmx")
        self.map = (self.tmx_data.width * self.tmx_data.tilewidth, self.tmx_data.height * self.tmx_data.tileheight)
        self.player_spawn = (1000, 1350)

        # Timer
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000) 


    def GameRun(self):
        self.player = Player("Grim", self.player_spawn)
        self.NPC = [NPC("NPC_1", (1100, 1350)), NPC("NPC_999", (1000, 1350))]
        while self.running:
            self.update()
            self.draw(self.screen)
            self.handle_events()
            pygame.display.flip()

            self.clock.tick(60)
        pygame.quit()

    def update(self):
        self.player.update()
        self.player.wall_collision(self.map)

        for npc in self.NPC:
            npc.update()
            npc.wall_collision(self.map)

        self.camera.update(self.player.rect, self.tmx_data.width * 256, self.tmx_data.height * 256)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.timer_event:
                self.NPC.append(NPC(f"NPC_{len(self.NPC)+1}", (1000, 1350)))


    def draw(self, surface: pygame.Surface):

        # Tilemap
        for layer in self.tmx_data.visible_layers:
            
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, surf in layer.tiles():
                    pos = (x * 256, y * 256)
                    surf_rect: pygame.Rect = surf.get_rect(bottomleft=pos)
                    surface.blit(surf, self.camera.apply(surf_rect))

        self.player.draw(surface, self.camera)
        self.player.draw_name(surface, self.font, self.camera)
        for npc in self.NPC:
            npc.draw(surface, self.camera)
            npc.draw_name(surface, self.font, self.camera)
        
        # NPC_name = self.font.render(self.NPC.name, True, (255,0,0))
        # surface.blit(NPC_name, self.camera.apply(self.NPC.rect, move_to=(160, 0)))



if __name__ == "__main__":
    game = TwoPI()
    game.GameRun()