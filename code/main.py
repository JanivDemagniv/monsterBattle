from setting import *
from support import *
from game_timer import Timer
from monster import Monster , Opponent
from random import choice
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()

        #groups
        self.all_sprites = pygame.sprite.Group()

        #data
        player_monsters_list = ['Sparchu','Cleaf','Jacana']
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monsters_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        monster_name = choice(list(MONSTER_DATA.keys()))
        self.opponent = Opponent(monster_name,self.front_surfs[monster_name],self.all_sprites)

        #ui
        self.ui = UI(self.monster)
    
    def import_assets(self):
        self.back_surfs = folder_importer('images','back')
        self.bg_surfs = folder_importer('images','other')
        self.front_surfs = folder_importer('images','front')

    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            floor_rect = self.bg_surfs['floor'].get_frect(center= sprite.rect.midbottom + pygame.Vector2(0,-10))
            self.display_surface.blit(self.bg_surfs['floor'],floor_rect)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            #updates
            self.all_sprites.update(dt)
            self.ui.update()

            #draw
            self.display_surface.blit(self.bg_surfs['bg'],(0,0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)
            self.ui.draw()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
