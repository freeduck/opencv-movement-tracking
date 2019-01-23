import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Border(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, color, width, height,xpos,ypos):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(Border,self).__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        self.height = height
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        
    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        print("gygag")
        self.rect.y = -self.height-100
 
    def update(self,puckx,pucky):
        pass
     
 
 
class Block(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(Block,self).__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        self.rect.y = random.randrange(-700, -20)
        self.rect.x = random.choice([random.randrange(0,1400)])
 
    def update(self,puckx,pucky):
        """ Called each frame. """
 
        # Move block down one pixel
        self.rect.y += 1
 
        # If block is too far down, reset to top of screen.
        if self.rect.y > 810:
            self.reset_pos()
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super(Player,self).__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, color, (int(width/2),int(height/2)),int(min(width,height)/2), 0)
        
        #self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        
    def update(self,puckx,pucky):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
 
        # Fetch the x and y out of the list,
        # just like we'd fetch letters out of a string.
        # Set the player object to the mouse location
        self.rect.x = puckx - 15
        self.rect.y = pucky - 15
