# -*- coding: utf-8 -*-

"""
    Copyright (C) 2013  BatOnBots-ML.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    Pre Alpha 0.1
"""


from os import path
import pygame

class Explosion( object ):
    """
    Gera a animação da explosão de uma bala e do robot.
    A cada execução do metodo 'blit' avança na animação.
    """
    def __init__( self, surface, sprite, explosionID, position ):
        """
         - surface - superficie onde a explosão é desenhada
         - sprite - lista com as partes da explosão
         - explosionID - nome que identifica a explosão: explosionX - onde o 'X' é o ID e é o mesmo da bala que originou a explosão
         - posion - tuple com a posição onde se quer desenhar a explosão. Já com o desconto para o centro
        """
        # ID da explosão
        self._explosionID = explosionID
        # Onde serão guardadas as diferentes partes da sprite
        self._spriteParts = sprite
        #
        self._surface = surface
        # peça da sprite em que a animação se encontra
        # Vai sendo incrementado cada vez que o metodo 'update()' é invocado
        self._step = 0
        # Tuple com a posição em que as peças serao desenhadas na surface
        self._pos = position
        

    def get_name( self ):
        return self._explosionID


    def blit( self ):
        self._surface.blit( self._spriteParts[self._step], self._pos )
        self._step += 1
        if ( self._step == len(self._spriteParts) ):
            return -1
        else:
            return 0








if ( __name__ == "__main__" ):

    def reset_explosion():
        global explosion
        explosion = Explosion( display, 0, (168, 168) )
    
    
    
    pygame.display.init()
    display = pygame.display.set_mode( (400, 400) )
    
    explosion = Explosion( display, 0, (168, 168) )
    clock = pygame.time.Clock()
    
    
    alive = 1
    while alive:
        display.fill( (255, 255, 255) )
        for event in pygame.event.get():
            if ( event.type == pygame.QUIT ):
                alive = 0
        if ( explosion.blit() == -1 ):
            reset_explosion()
    
        clock.tick( 25 )
        pygame.display.flip()
        
    pygame.display.quit()



