#-*- coding: utf-8 -*-

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

"""
Descrição: Modulo com as varias animações que aparecem no jogo.
           Invocado no modulo 'battleRoom'.
"""

from math import sin, cos, radians
import pygame

from log.logging_mod import Logging
log = Logging()
printd = log.debug
printi = log.info
printe = log.error
printw = log.warning



class CircleAnimation( pygame.sprite.Sprite ):
    """
    Cria a animação que é mostrada segundos antes da batalha iniciar.

    Nota: Para se poder utilizar o 'alpha channel' é preciso criar um objecto do tipo 'pygame.Surface' com a flag 'pygame.SRCALPHA'.
          Ex.: screen = pygame.Surface( (width, height), flags = pygame.SRCALPHA )
    """
    def __init__(self, screen, color = (13, 124, 26, 255), width = 8, x = 50, y = 50, radius = 20, nCircles = 6, stepSize = 8):

        pygame.sprite.Sprite.__init__( self )
        
        # Objecto do tipo 'pygame.Surface' onde a animação vai ser desenhada
        self._screen = screen
        
        # Quando o utilizador não especifica o valor para o alpha, considera-se 255
        # Esta variável é criada para que se possa alterar o valor alpha mais facilmente apartir do exterior
        # caso se queira trabalhar com ele. Deve ser alterado antes do metodo 'draw()' ser invocado        
        if ( len(color) == 4 ):
            self.alpha = color[3]

        else:
            self.alpha = 255

        # Cor das linhas da animação
        self.color = color
        # Espessura das linhas da animação
        self.width = width
        # Centro da animação
        self.x = x
        self.y = y
        # Raio da circunferencia. Equivale ao tamanho de cada linha
        self.radius = radius
        # Número de linhas que a animação vai ter
        self.nCircles = nCircles
        # Tamanho em pixeis da deslocação das bolas
        self.stepSize = stepSize
        # Variável paramétrica que vai sendo incrementada
        self.t = 0
        # Lista com as coordenadas de cada linha
        self.circles = []
        # Inicia a lista das linhas com as coordenadas (x, y) iniciais
        for circle in range( self.nCircles ):
            self.circles.append( (0, 0) )
        # Por fim calcula a distancia entre cada circunferencia
        self.distance =  int(360 / self.nCircles)


    def update(self):
        self.t += self.stepSize
        t = self.t

        for circle in self.circles:
            x, y = circle
            pos = self.circles.index( circle )           
            t += self.distance

            x = int(self.x + ( cos(radians( t )) * self.radius ))
            y = int(self.y + ( sin(radians( t )) * self.radius ))

            self.circles[pos] = (x, y)


    def draw( self ):
        for circle in self.circles:
            pygame.draw.circle( self._screen, (self.color[0], self.color[1], self.color[2], self.alpha), circle, 6, 0 )

        if self.t >= 360:
            self.t = 0


##########################################################################################################################
##########################################################################################################################
##########################################################################################################################




class TextFadeAnimation( pygame.sprite.Sprite ):
    """
    Nota: Não esquecer que para utilizar o 'alpha channel', ao renderizar a font, a flag 'antialias' tem de estar a False.
    """
    def __init__(self, screen, pos = (100, 100), text = 'Sample', fontName = 'arial', fontMaxSize = 40, color = (13, 124, 26), speed= 4):
        pygame.sprite.Sprite.__init__(self)

        # Display onde a animação vai ser mostrada
        self._screen = screen
        # Tupla com as coordenadas(x e y) onde a animação deve ser mostrada
        self.x = pos[0]
        self.y = pos[1]
        # Texto da animação
        self.text = text
        # Nome da 'font' que se quer utilizar
        self.fontName = fontName
        # Tamanho máximo da animação
        self.fontMaxSize = fontMaxSize
        # Cor do texto
        self.color = color
        # Velocidade da animação
        self.speed = speed

        # Valor que controla a translucides do texto (alpha channel)
        self.alpha = 0
        # Tamanho do texto. Vai aumentando ou diminuindo durante a animação
        self.fontSize = 1


        # Cria o tipo 'pygame.font.Font'.
        try:
            self.font = pygame.font.SysFont(self.fontName, self.fontSize)
            self.font.set_bold(True)
            
        except:
            printe("")
            printe( "O 'SystemFont '" + str(self.fontName) + "' não foi encontrado." )
            self.font = pygame.font.Font(None, self.fontSize)
            self.font.set_bold(True)


        # Font rederizada
        #self.fontR = None
        self.fontR = self.font.render( self.text, False, self.color )
        # Rectângulo do texto
        self.rect = (self.x, self.y, 0, 0)
        # Flag que indica se a animação deve aumentar ou diminuir o tamanho do texto
        # '+' - Quando a animação está a aumentar
        # '-' - Quando a animação está a diminuir
        self.oper = '+'

        # Contador para provocar um atraso quando a animação está no tamanho máximo.
        # Quando o valor é maior que zero, indica que está a fazer delay.
        self.delay = 0


        # Parte secundária a esta animação. Serve para adicionar a segunda animação(CircleAnimation) e para ser retirada
        # tem de ser em conjunto com a parte que está no metodo 'draw()'
        # É preciso calcular a altura máxima do texto parra saber a que distância colocar a CircleAnimation
        try:
            font_ = pygame.font.SysFont(self.fontName, self.fontMaxSize)
            font_.set_bold(True)
            
        except:
            font_ = pygame.font.Font(None, self.fontMaxSize)
            font_.set_bold(True)

        fontR_ = self.font.render( self.text, False, self.color )
        fontMaxHeight = fontR_.get_height()
        # O 20 é o raio por defeito da animação CircleAnimation. E o 2 é um espaço que se dá entre as duas animações
        y = self.y + fontMaxHeight + (20*2) + 2
        # Cria a animação CircleAnimation
        self.CircleAnimation = CircleAnimation( self._screen, x = self.x, y = y, color = self.color )


    def increase(self):
        if ( self.delay > 0 ):
            if ( self.delay < (self.speed * 3) ):
                self.delay += 1
                return
            else:
                self.delay = 0
                self.oper = '-'
                return 
        # Controla o valor alpha da animação
        elif ( (self.fontSize <= self.fontMaxSize) and ((self.fontSize + self.speed) <= self.fontMaxSize) ):
            self.fontSize += self.speed
            # Faz com que o valor alpha seja proporcional ao tamanho da letra durante a animação
            self.alpha += int(255 / int(self.fontMaxSize / self.speed))
        elif ( (self.fontSize + self.speed) > self.fontMaxSize ):
            self.fontSize = self.fontMaxSize
            self.alpha = 255
            self.delay = 1
        else:
            self.fontSize = 0
            self.alpha = 0
            self.oper = '+'


    def decrease(self):
        # Controla o valor alpha da animação
        if ( (self.fontSize >= 0) and ((self.fontSize - self.speed) >= 0) ):
            self.fontSize -= self.speed
            # Faz com que o valor alpha seja proporcional ao tamanho da letra durante a animação
            self.alpha -= int(255 / int(self.fontMaxSize / self.speed))

        elif ( ((self.fontSize + self.speed) <= 0) ):
            self.fontSize = 0
            self.alpha = 0
            self.oper = '+'

        else:
            self.fontSize = 0
            self.alpha = 0
            self.oper = '+'


    def update(self):
        if ( self.oper == '+' ):
            self.increase()
        
        elif ( self.oper == '-' ):
            self.decrease()

        # Cria o tipo 'pygame.font.Font'.
        try:
            self.font = pygame.font.SysFont(self.fontName, self.fontSize)
            self.font.set_bold(True)
        except:
            printe( "O 'SystemFont '" + str(self.fontName) + "' não foi encontrado." )
            self.font = pygame.font.Font(None, self.fontSize)
            self.font.set_bold(True)
        
        self.fontR = self.font.render( self.text, False, self.color )
        self.fontR.set_alpha( self.alpha )

        width  = self.fontR.get_width()
        height  = self.fontR.get_height()
        self.rect = ( self.x - (width / 2), self.y - (height / 2), width, height )


    def draw(self):
        """
        Escreve o texto.
        Cada vez que é invocado avança a animação um ciclo.
        """
        self.update()
        self._screen.blit( self.fontR, self.rect )

        ## Parte da animação CircleAnimation ##
        self.CircleAnimation.update()
        self.CircleAnimation.alpha = self.alpha
        self.CircleAnimation.draw()
        #######################################


##########################################################################################################################
##########################################################################################################################
##########################################################################################################################