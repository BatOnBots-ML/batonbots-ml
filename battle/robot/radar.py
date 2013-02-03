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
from math import pi, radians, cos, sin


class Radar():
    def __init__(self, radarImg):
        
        # Imagem base que não vai ser alterada
        self._baseRadarImg = radarImg
        self._radarRect = self._baseRadarImg.get_rect()
        
        # Imagem que vai sofrer as alterações para depois ser dezenhada na Surface.
        self._radarImg = None
        
        # Uma vez que o x e y que chegam aqui são o centro do corpo do robot e o radar anda mais ou menos
        # em volta do corpo, é preciso defenir um raio para calcular a sua posição 
        self.RADAR_ORBIT_RADIUS = 49


    def update_radar(self, x, y, raDeg, gDeg):
        """
        Actualiza a posição e a direcção do radar do robot.
        """
        # O '2.02' serve para adiantar a posição na circunferencia onde se movimenta com o objectivo de acertar a
        # posição com o braço da arma onde deve ficar
        newCenter = ( self.RADAR_ORBIT_RADIUS * cos(radians(gDeg) + 2.02) + x,
                     self.RADAR_ORBIT_RADIUS * sin(radians(gDeg) + 2.02) + y )
        
        self._radarImg = pygame.transform.rotate(self._baseRadarImg, -raDeg)
        self._radarRect = self._radarImg.get_rect()
        self._radarRect.center = newCenter


    def blit_radar(self):
        self.screen.blit(self._radarImg, self._radarRect)




