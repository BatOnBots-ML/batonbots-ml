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

from radar import Radar
from gun import Gun

class Robot( Radar, Gun ):
    """
    Esta classe é utilizada apenas para o desenho dos robots no campo de batalha.
    """
    def __init__( self, robotName, skinImgs, screen, initPos, initDir ):
        """
            'robotName' - String com um máximo de 15 caracteres que indica o nome do robot.            
            'skinImgs' - Lista com as imagens para o corpo, arma e radar do robot. [ bodyImg, gunImg, radarImg ]
            screen - objecto do tipo 'pygame.display' onde o robot irá ficar.
            'initPos' - Tupla com o x e y iniciais
            'initDir' - Direcção inicial do robot
        """
        self._name = robotName
        # Imagem base que não vai ser alterada
        self._baseBodyImg = skinImgs[ 0 ]
        self.screen = screen
        
        # Imagem que vai sofrer as alterações para depois se dezenhada na Surface.
        self._bodyImg = None
        # Vai conter sempre o rectangulo actual da imagem
        self._bodyRect = self._baseBodyImg.get_rect()

        Gun.__init__( self, skinImgs[ 1 ] )
        Radar.__init__( self, skinImgs[ 2 ] )
        
        # Inicializa a posição do robot com a sua posição inicial
        x, y = initPos
        self.update( x, y, initDir, initDir, initDir )
        
        self.angle = 0



    def update_body( self, x, y, deg ):
        """
        Actualiza a posição do robot.
        
        'x' - Posição do corpo do robot no eixo do X.
        'y' - Posição do corpo do robot no eixo do Y.
        'deg' - Graus de viragem do corpo do robot
        
        """
        self._bodyImg = pygame.transform.rotate( self._baseBodyImg, -deg )
        self._bodyRect = self._bodyImg.get_rect()
        
        self._bodyRect.center = ( x, y )


    def blit_body( self ):
        # Dezenha o corpo do robot
        self.screen.blit( self._bodyImg, self._bodyRect )


    def blit( self ):
        """
            Desenha todas as parte do robot no objecto 'pygame.Surface' dado.
        """
        self.blit_body()
        self.blit_gun()
        self.blit_radar()    


    def update( self, x, y, roDeg, gDeg, raDeg ):
        """
        Actualiza as posições e as direcções do corpo, arma e radar do robot.
        """
        self.angle = roDeg
        self.update_body( x, y, roDeg )   
        self.update_gun( x, y, gDeg )
        self.update_radar( x, y, raDeg, gDeg )

        

    ################################### Nome do robot ##################################
    def get_robot_name( self ):
        """
            Retorna o nome do robot.
        """
        return self._name

    def get_name( self ):
        """
        Retorna o nome do robot.
        Existe para criar compatibilidade com o mecanismo que dezenha os objectos no campo de batalha.
        Para mais pormenores ver a descrição da lista dos objectos no modulo battleRoom.
        """
        return self._name
