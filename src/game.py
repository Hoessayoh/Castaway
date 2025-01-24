from player import Player
from world import World
from fish import Fish
from ui import UI

# Initialize objects
player = Player()
world = World()
ui = UI()

fish_group = pygame.sprite.Group()
for i in range(5):  # Create 5 fish
    fish = Fish(800 + i * 100, 300)
    fish_group.add(fish)

# Inside the game loop
player.update()
fish_group.update()
ui.update()

screen.fill(WATER_COLOR)  # Draw background
world.draw(screen)
fish_group.draw(screen)
player.draw(screen)
ui.draw(screen)
