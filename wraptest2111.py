import cv2
#import cv2.cv as cv
import numpy as np
import pygame
import math
import random
import os.path
import pickle
import cProfile
import time
#import pyglet
from kallibrer0512 import kallibrer
from findcircle_blob0512  import circleposition
from spriteclasses  import Player,Block,Border,BLACK,WHITE,GREEN,RED,BLUE
from puckmovement  import puck_movement
from random import randint
import copy

def startscreen(highscore_list):

    global screen
    started = False
    
    block_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    

    all_sprites_list.add(player)
    startBlock = Block(GREEN, 60, 60)
    all_sprites_list.add(startBlock)
    startBlock.rect.x = 630
    startBlock.rect.y = 320
    block_list.add(startBlock)
    all_sprites_list.draw(screen)
    

    while not started:
        for puck in puck_movement():
            
            player.update(puck[0],puck[1])
            
            all_sprites_list.draw(screen)     
            if len(highscore_list) == 0:
                Score = myfont.render("Score to beat:0",1, (0,50,0))
            else:
                Score = myfont.render("Score to beat set by "+highscore_list[0].keys()[0]+": "+str(highscore_list[0].values()[0]), 1, (0,50,0))
            
            screen.blit(Score,(10,10))
            # See if the player block has collided with anything.
            clock.tick(20)
            pygame.display.flip()
            blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False,pygame.sprite.collide_rect)
            #if blocks_hit_list is not None:
            for block in blocks_hit_list:
                print("HIT!!!!!")
                started = True
                return

def resultscreen(hitcount):

    global screen
    
    screen.init
    
    Score = myfont.render("Number of hits "+hitcount, 1, (0,50,0))
            
    screen.blit(Score,(10,10))
    
def main():
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("/home/lars/dev/Videos/Webcam/2017-12-20-223500.webm")
    #window = pyglet.window.Window()
    #cursor= window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
    #window.set_mouse_cursor(cursor)

        

     
    # Initialize Pygame
    pygame.init()
     
    # Set the height and width of the screen
    screen_width = 1300
    screen_height = 700
    screen = pygame.display.set_mode([screen_width, screen_height])
    screen.fill(WHITE)
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
     
    score = 0
    started = False

    myfont = pygame.font.SysFont("monospace", 30,True)


    player = Player(BLACK, 60, 60)
    topborder = Border(BLACK, 20, 117, 640,0)
    midborder = Border(BLACK, 20, 230, 640,235)
    lowborder = Border(BLACK, 20, 117, 640,583)
    bluehole = Border(BLUE, 20,117, 640,117)
    redhole = Border(RED, 20, 117, 640, 466)

    targettl = Border(GREEN, 120, 120,265,115)
    targetbl = Border(GREEN, 120, 120,265,415)
    targettr = Border(GREEN, 120, 120,915,115)
    targetbr = Border(GREEN, 120, 120,915,415)

    targets = [targettl,targetbl,targettr,targetbr]
    
    sprite_list = pygame.sprite.Group()
    target_list = pygame.sprite.Group()

    sprite_list.add(player)
    target = copy.copy(targets[randint(0,3)])

    sprite_list.add(redhole)
    sprite_list.add(bluehole)
    sprite_list.add(topborder)
    sprite_list.add(midborder)
    sprite_list.add(lowborder)
    
    sprite_list.add(target)

    target_list.add(target)


    # -------- Main Program Loop -----------

    start_ticks=pygame.time.get_ticks()

    started = False 
    done = False    
    score=0

    dest = np.array([ [0,0],[1299,0],[1299,699],[0,699] ],np.float32)
    
    undistinfo = pickle.load(open("undistinfo.p","rb"),fix_imports=True,encoding='latin1')
    mtx = undistinfo['mtx']
    dist = undistinfo['dist']
    ret, frame = cap.read()
    h,  w = frame.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    print("foer kallibrer")
    warp,mask,maskcorners,_ = kallibrer(cap,dest,newcameramtx,mtx,dist)
    hitcount = 0
    hole = ""
    print("am alive")
    myfont = pygame.font.SysFont("monospace", 30,True)
        
    time1 = time.clock()

    x=0
    dircount = 0
    pucksizelist = []
    
    for puck in puck_movement(lambda:circleposition(cap,warp,newcameramtx,mtx,dist,mask,maskcorners)):
        time2 = time.clock()
        #print('clocktime %0.6f' % (time2-time1))     
        #time1=time2,
        #pucksizelist.append([puck[0][2][2],puck[0][2][3]])
        x+=1
        # Calls update() method on every sprite in the list
        sprite_list.update(puck[0][2][0],puck[0][2][1])
        if puck[1]:
            dircount = dircount + 1

        if (puck[0][2][0] > 660 and puck[0][1][0] < 640) or (puck[0][2][0] < 640 and puck[0][1][0] > 660):
            if puck[0][2][1] > 350:
                hole = "Red"
            else:
                hole = "Blue"
            
            
        screen.fill(WHITE)
        sprite_list.draw(screen)
        
        target_hit_list = pygame.sprite.spritecollide(player, target_list, True,pygame.sprite.collide_rect)
            #if blocks_hit_list is not None:
        for target in target_hit_list:
            print("HIT!!!!!")
            hitcount += 1
            #randint(0,3)
            ctargets = [x for x in copy.copy(targets) if not x.rect.x == target.rect.x or not x.rect.y == target.rect.y]
            target = ctargets[randint(0,2)]
            sprite_list.add(target)
            target_list.add(target)
        

        # Draw all the spites
        #screen.blit(player.image,player.rect)
        # Limit to 20 frames per second
        clock.tick(30)
     
        # Go ahead and update the screen with what we've drawn.
        #timelimit = 100
        #timecount = timelimit - round(time2 - time1)
        
        #Timecount = myfont.render("time "+ str(timecount), 1, (0,50,0))
        Score = myfont.render("Count "+ str(dircount), 1, (0,50,0))
        Hole = myfont.render("Hole "+ str(hole), 1, (0,50,0))
        
        #screen.blit(Timecount,(10,10))        
        screen.blit(Score,(10,30))
        screen.blit(Hole,(10,50))
        
        pygame.display.flip()
        
        #if timelimit <= 0:
        #    return hitcount
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # = time.clock()
        #if x>100:
        #s    break
    #with open("pucksizelist","wb") as f: 
	#    pickle.dump(pucksizelist,f)
#cProfile.run('main()')

#while True:
main()
	#resultscreen(hitcount)

#while not    

pygame.quit()
