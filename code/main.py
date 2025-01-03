from setting import *
from support import *
from game_timer import Timer
from monster import *
from random import choice
from ui import UI , OpponentUI
from attack import AttackAnimationSprite

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()
        self.audio['music'].play(-1)
        self.player_active = True

        #groups
        self.all_sprites = pygame.sprite.Group()

        #data
        player_monsters_list = ['Sparchu','Friolera','Jacana','Gulfin','Draem','Pluma']
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monsters_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        monster_name = choice(list(MONSTER_DATA.keys()))
        self.opponent = Opponent(monster_name,self.front_surfs[monster_name],self.all_sprites)

        #ui
        self.ui = UI(self.monster , self.player_monsters , self.simple_srufs , self.get_input)
        self.opponentUi = OpponentUI(self.opponent)

        #timers
        self.timers = {
            'player end': Timer(1000,func= self.opponent_turn),
            'opponent end': Timer(1000, func= self.player_turn)
            }

    def get_input(self,state,data = None):
        if state == 'Attack':
            self.apply_attack(self.opponent , data)
        elif state == 'Escape':
            self.running = False
        elif state == 'Heal':
            self.monster.health += 50
            AttackAnimationSprite(self.monster,self.attack_frames['green'],self.all_sprites)
            self.audio['green'].play()
        elif state == 'Switch':
            self.monster.kill()
            self.monster = data
            self.all_sprites.add(self.monster)
            self.ui.monster = self.monster
        
        self.player_active = False
        self.timers['player end'].activate()

    def apply_attack(self,target,attack):
        attack_data = ABILITIES_DATA[attack]
        attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]
        target.health -= attack_data['damage'] * attack_multiplier
        AttackAnimationSprite(target, self.attack_frames[attack_data['animation']] ,self.all_sprites)
        self.audio[attack_data['animation']].play()

    def opponent_turn(self):
        if self.opponent.health <= 0:
            self.player_active = True
            self.opponent.kill()
            moster_name = choice(list(MONSTER_DATA.keys()))
            self.opponent = Opponent(moster_name,self.front_surfs[moster_name],self.all_sprites)
            self.opponentUi.monster = self.opponent
        else:
            attack = choice(self.opponent.abilities)
            self.apply_attack(self.monster,attack)
            self.timers['opponent end'].activate()
    
    def player_turn(self):
        self.player_active = True
        if self.monster.health <= 0:
            availabile_monster = [monster for monster in self.player_monsters if monster.health > 0]
            if availabile_monster:
                self.monster.kill()
                self.monster = availabile_monster[0]
                self.all_sprites.add(self.monster)
                self.ui.monster = self.monster
            else:
                self.running = False
        

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def import_assets(self):
        self.back_surfs = folder_importer('images','back')
        self.bg_surfs = folder_importer('images','other')
        self.front_surfs = folder_importer('images','front')
        self.simple_srufs = folder_importer('images','simple')
        self.attack_frames = tile_importer(4,'images','attacks')
        self.audio = audio_importer('audio')

    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            if isinstance(sprite,Creature):
                floor_rect = self.bg_surfs['floor'].get_frect(center= sprite.rect.midbottom + pygame.Vector2(0,-10))
                self.display_surface.blit(self.bg_surfs['floor'],floor_rect)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            #updates
            self.update_timers()
            self.all_sprites.update(dt)
            if self.player_active:
                self.ui.update()

            #draw
            self.display_surface.blit(self.bg_surfs['bg'],(0,0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)
            self.ui.draw()
            self.opponentUi.draw()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
