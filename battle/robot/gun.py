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

import pygame
from math import sin, cos, radians

class Gun():
    def __init__( self, gunImg ):
        
        # Imagem base que não vai ser alterada
        self._baseGunImg = gunImg
        self._gunRect = self._baseGunImg.get_rect()
        
        # Imagem que vai sofrer as alterações para depois ser dezenhada na Surface.
        self._gunImg = None

        # Uma vez que o x e y que chegam aqui são o centro do corpo do robot e o centro da arma não é o mesmo que o 
        # do corpo é preciso recuar o centro da arma com a ajuda deste valor para que fique no sitio certo 
        self.GUN_ORBIT_RADIUS = -11



    def update_gun( self, x, y, deg ):
        """
        Actualiza a posição e a direcção da Arma do robot.
        """
        newCenter = (self.GUN_ORBIT_RADIUS * (cos(radians(deg))) + x,
                     self.GUN_ORBIT_RADIUS * (sin(radians(deg))) + y)
        self._gunImg = pygame.transform.rotate(self._baseGunImg, -deg)
        self._gunRect = self._gunImg.get_rect()
        self._gunRect.center = newCenter

    def blit_gun( self ):
        self.screen.blit( self._gunImg, self._gunRect )




