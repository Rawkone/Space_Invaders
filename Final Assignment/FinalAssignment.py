import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (199,21,133)
background_position = [0, 0]

# --- Classes
class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([20, 15])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        # Move the block down one pixel
        self.rect.y += 1
        if self.rect.y > screen_height:
            self.rect.y = random.randrange(-100, -10)
            self.rect.x = random.randrange(0, screen_width) 
            
class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
 
    def __init__(self,colour,width, height):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.image.load("player.bmp").convert()
        self.image = pygame.transform.scale(self.image, (width,height))
        
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0]
        self.rect.y = pos[1]
 
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3 
        
pygame.init()

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption("Instruction Screen")

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
# List of each block in the game
block_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
 
# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the sprites
 
for i in range(100):
    # This represents a block
    block = Block(PINK)
 
    # Set a random location for the block
    block.rect.x = random.randrange(900)
    block.rect.y = random.randrange(400)
 
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
 
# Create a red player block
player = Player(BLACK, 50,50)
all_sprites_list.add(player)
player_list.add(player)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
player.rect.y = 370
background_image = pygame.image.load("saturn_family1.bmp").convert()
# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
 
display_instructions = True
instruction_page = 1
name = ""
click_sound = pygame.mixer.Sound("laser5.ogg") 

# -------- Instruction Page Loop -----------
while not done and display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                name += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            elif event.key == pygame.K_RETURN:
                instruction_page += 1  
                if instruction_page == 4:
                    display_instructions = False                
 
    # Set the screen background
    screen.fill(BLACK)
 
    if instruction_page == 1:
        # Draw instructions, page 1
        # This could also load an image created in another program.
        # That could be both easier and more flexible.
 
        text = font.render("Instructions", True, WHITE)
        
        screen.blit(text, [10, 10])
       
        text = font.render("Enter your name: ", True, WHITE)
        screen.blit(text, [10, 40])    
       
        text = font.render(name, True, WHITE)
        screen.blit(text, [220, 40])        
 
        text = font.render("Hit enter to continue", True, WHITE)
        screen.blit(text, [10, 80])
       
        text = font.render("Page 1", True, WHITE)
        screen.blit(text, [10, 120])
 
    if instruction_page == 2:
        # Draw instructions, page 2
        text = font.render("SPACE INVADERS", True, WHITE)
        screen.blit(text, [10, 10])    
 
        text = font.render("Hit enter to continue", True, WHITE)
        screen.blit(text, [10, 40])
 
        text = font.render("Page 2", True, WHITE)
        screen.blit(text, [10, 80])
        
    if instruction_page == 3:
        # Draw instructions, page 3
        text = font.render("Move mouse to move character", True, WHITE)
        screen.blit(text, [10, 10])  
        
        text = font.render("Click to shoot", True, WHITE)
        screen.blit(text, [10, 40])     
        
        text = font.render("Gain points by shooting blocks", True, WHITE)
        screen.blit(text, [10, 70])        
     
        text = font.render("Hit enter to continue", True, WHITE)
        screen.blit(text, [10, 100])
     
        text = font.render("Page 3", True, WHITE)
        screen.blit(text, [10, 130]) 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
   
    score = 0
 
# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button
            bullet = Bullet()
            click_sound.play()
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x + 25
            bullet.rect.y = player.rect.y            
            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
            
    # Call the update() method on all the sprites
    all_sprites_list.update()  
    
    for player in player_list: 
                
        #see if a block hits player        
        player_hit_list = pygame.sprite.spritecollide(player,block_list,True)
        
        for player in player_hit_list:
            while not done and display_instructions:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.KEYDOWN:
                        if event.unicode.isalpha():
                            name += event.unicode
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        elif event.key == pygame.K_RETURN:
                            instruction_page += 1  
                            if instruction_page == 4:
                                display_instructions = False                
             
                # Set the screen background
                screen.fill(BLACK)
             
                if instruction_page == 1:
                    # Draw instructions, page 1
                    # This could also load an image created in another program.
                    # That could be both easier and more flexible.
             
                    text = font.render("GAME OVER", True, WHITE)
                    
                    screen.blit(text, [10, 10])
                # Limit to 60 frames per second
                clock.tick(60)
                 
                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()  
                
    # Set the screen background
    screen.fill(BLACK)
 
    if instruction_page == 1:
        # Draw instructions, page 1
        # This could also load an image created in another program.
        # That could be both easier and more flexible.
 
        text = font.render("GAME OVER", True, WHITE)
        
        screen.blit(text, [10, 10])
         
             
                
        # Call the update() method on all the sprites
                
        
 
    # Calculate mechanics for each bullet
    for bullet in bullet_list:
 
        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
 
        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)
            
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
    player_position = pygame.mouse.get_pos()
    x = player_position[0] + 25
    y = player_position[1]      
    screen.blit(background_image, background_position)

    all_sprites_list.draw(screen)
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()