#!/usr/bin/env python

import os
import pygame
import pygame.gfxdraw
from pygame._sdl2 import Window, Texture, Image, Renderer
import math
import random

screen_size_x=1600
screen_size_y=800
sprite_size=200

def load_image(file):
    main_dir = ""
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "images", file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface


def InitSprite(rend, img, size1,size2):
        sprite=pygame.sprite.Sprite()        
        alien_tmp=pygame.transform.scale(img, (size1, size2))
        tex1 = Texture.from_surface(rend, alien_tmp)
        img_new=Image(tex1)
        sprite.rect = img_new.get_rect()
        sprite.image = img_new
        return sprite


class MySprites(pygame.sprite.Sprite):
    
    def __init__(self, rend, max_x, max_y):
        size=random.randrange(200, 500)
        self.set_angel=0.00
        self.set_angel=random.randrange(-1, 2)
        self.images = []
        self.sprites =[]
        self.Sprite=pygame.sprite.Sprite
        self.PositionX=0
        self.PositionY=0
        self.g = 0.150
        self.g1 = 0.140
        self.g2 = 0.160
        self.gp = 0.00
        self.MaxPositionX=0
        self.MaxPositionY=0
        self.ArrowPositionX=0
        self.Speed=random.randrange(5.0, 10.0)
        self.PreviusPositionY=-1000
        self.ttt=0
        self.sprites=[]
        self.sprites= [InitSprite(rend,im, size,size) for im in (MySprites.images[0],MySprites.images[1],MySprites.images[2],MySprites.images[3]) ]
        self.PositionX=random.randrange(max_x/10, max_x/2)
        self.PositionY=max_y/2
        self.MaxPositionX=max_x - size
        self.MaxPositionY=max_y - size
        self.ArrowPositionX=random.randrange(0,2)
        st=random.randrange(0,2)
        self.gp=self.g1
        self.Sprite=self.sprites[0]
        self.Sprite.image.alpha=random.randrange(0, 20)
        if st==0:
            self.gp=self.g2


    def update(self):
        if self.Sprite.image.alpha<255:  
                        self.Sprite.image.alpha+=1
        #--------------------------------------------------
            #перемещение
        if self.ArrowPositionX > 0:                    
                self.PositionX+=1
                if self.PositionX > self.MaxPositionX: 
                                self.ArrowPositionX = 0  
                                self.set_angel=-self.set_angel
        else:                
            self.PositionX-=1
            if self.PositionX < 1: 
                    self.ArrowPositionX = 1
                    self.set_angel=-self.set_angel
        self.PositionY += self.Speed             
        if self.PositionY > self.MaxPositionY:                
                self.Speed = -self.Speed
                self.PositionY = self.MaxPositionY                                                   
        #сбрасываем или  набираем  скорость
        if (self.Speed > 0):            
                    self.Speed += self.g
            
        if self.Speed <= 0:            
                    self.Speed += self.gp
                    if self.Speed > 0:  # сменилось напрявление                  
                            difference = abs( self.PreviusPositionY - self.PositionY)  #изменения высоты
                            if difference < 1.0:                    
                                    #маленькое изменнение высоты
                                    if self.gp > self.g1:                        
                                        self.gp = self.g1;                        
                                    else: 
                                        self.gp -= 0.01;                                            
                            else:                    
                                    self.PreviusPositionY = self.PositionY;
            #уж слишком высоко
        if (self.PositionY < (-self.MaxPositionY)):
                        self.gp = self.g2; 
        #--------------------------------------------------
        self.Sprite.rect.x=self.PositionX
        self.Sprite.rect.y=self.PositionY
        self.Sprite.image.angle += self.set_angel
        #sprite2.image.angle -= 1
        self.ttt+=1

        if((self.ttt % 30)==0):
            rnd=random.randrange(0,4)
            self.ttt=0
            angle=self.Sprite.image.angle
            alpha=self.Sprite.image.alpha
            self.Sprite.image=self.sprites[rnd].image
            self.Sprite.rect.x=self.PositionX
            self.Sprite.rect.y=self.PositionY
            self.Sprite.image.angle=angle
            self.Sprite.image.alpha=alpha

   
def main(winstyle=0):
      
    index=0;
    mySprites=[]
    pygame.display.init()
    MySprites.images = [load_image(im) for im in ("cp0.png", "cp1.png", "cp2.png", "cp3.png" )]
    icon=pygame.transform.scale(MySprites.images[0], (32, 32))   

    win = Window("CaterPillar", (screen_size_x,screen_size_y), resizable=False)
    win.set_icon(icon)
    #win.set_fullscreen(True)
    renderer = Renderer(win)
    
    BackSprite=InitSprite(renderer,load_image("Table.png"),1600,800)

    mySprites.append(MySprites(renderer,screen_size_x,screen_size_y))

    renderer.draw_color = (0, 0, 0, 0)

    renderer.clear()

    group = pygame.sprite.Group()
    group.add(BackSprite)
    group.add(mySprites[0].Sprite)
    
    group.draw(renderer)
    clock = pygame.time.Clock()
        
    run=1
    try:
        while run==1:

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mySprites.append(MySprites(renderer,screen_size_x,screen_size_y))
                                        index+=1
                                        mySprites[index].update()
                                        group.add(mySprites[index].Sprite)
                                        
                    if event.type == pygame.QUIT:
                                                pygame.quit()
                                                run=0
                                                break

                renderer.clear()
                group.draw(renderer)
                renderer.present()                                
                for x in mySprites: 
                        x.update()
                clock.tick(120)
                win.title = str("FPS: {}".format(clock.get_fps()))
              

    finally:
        pygame.quit()


# call the "main" function if running this script
main()



