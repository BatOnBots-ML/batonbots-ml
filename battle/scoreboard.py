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
Descrição: Modulo com as classes que tratam do quadro de informações com os resultados que 
           fica do lado direito do campo de batalha.
           
           O ScoreBoard é o rectângulo do lado direito do campo de batalha, e pode
           ter dentro varios jogadores com as respectivas informações.
           
"""

import os
import pygame
from pygame.locals import *


from log.logging_mod import Logging
log = Logging()
printd = log.debug
printi = log.info
printe = log.error
printw = log.warning





class Button( object ):
    
    def __init__( self, screen, callback, pos = (10, 10), text = 'Sample Button', borderColor = (0, 0, 0), textColor = (193, 5, 0), bgColor = (27, 62, 80) ):
        # Surface onde vai ser dezenhado
        self.screen = screen
        # Tupla com as coordenadas onde vai ser dezenhado. (z, y)
        self.x = pos[ 0 ]
        self.y = pos[ 1 ]
        # Texto que vai aparecer dentro
        self.text = text
        # Metodo que é invocado quando é clickado
        self.callback = callback
        
        # Largura e altura do botão
        self.width = 60
        self.height = 30
        
        self.rect = ( self.x, self.y, self.width, self.height )
        
        # Cor ddo contorno
        self.borderColor = borderColor
        # Cor do texto
        self.textColor = textColor
        # Cor de fundo
        self.bgColor = bgColor
        
        # Cores que são utilizadas quando o botão fica desabilitado
        # Cor ddo contorno
        self.disableBorderColor = (255, 255, 255)
        # Cor do texto
        self.disableTextColor = (200, 200, 200)
        # Cor de fundo
        self.disableBgColor = (50, 50, 50)
        
        self.MY_FONT = pygame.font.SysFont('arial', 20, bold = True, italic = False)

        # largura do contorno
        # Se for 2, faz um efeito de sombra
        self.borderW = 2
        # Flag para indicar se o botão está activo ou não
        self.enabled = False



    def create_button( self ):        
        # A cor iniciar é a de botão desabilitado
        self.font = self.MY_FONT.render( str(self.text), True, self.disableTextColor )
        
        self.width = self.font.get_width() + 10
        self.height  = self.font.get_height() + 10
        
        self.x -= ( self.width / 2 )
        self.y -= ( self.height / 2 )  



    def draw( self ):
        if ( self.enabled ):
            # Desenha o contorno
            pygame.draw.rect( self.screen, self.borderColor, (self.x, self.y, self.width, self.height ), self.borderW)
            # Desenha o fundo
            self.screen.fill( self.bgColor, (self.x, self.y, self.width, self.height ) )
            # Desenha o texto
            self.screen.blit( self.font, (self.x + 5, self.y + 5) )
        
        else:
            # Desenha o contorno
            pygame.draw.rect( self.screen, self.disableBorderColor, (self.x, self.y, self.width, self.height ), self.borderW)
            # Desenha o fundo
            self.screen.fill( self.disableBgColor, (self.x, self.y, self.width, self.height ) )
            # Desenha o texto
            self.screen.blit( self.font, (self.x + 5, self.y + 5) )

        

    def sensitive( self, flag ):
        """
        Serve para abilitar ou desabilitar o botão.
        
        'flag' - True para abilitar. False para desabilitar
        """
        if ( flag ):
            self.enabled = True
            # É preciso alterar a cor do texto aqui porque não faz sentido estar a alterar a cor da letra a cada 'draw()'
            self.font = self.MY_FONT.render( str(self.text), True, self.textColor )
        
        else:
            self.enabled = False
            # É preciso alterar a cor do texto aqui porque não faz sentido estar a alterar a cor da letra a cada 'draw()' 
            self.font = self.MY_FONT.render( str(self.text), True, self.disableTextColor )


    def set_callback( self, callback ):
        self.callback = callback


    def clicked( self, event ):
        """
        É invocado a cada evento '5-MouseButtonDown'. É invocado pelo 'main_loop()' do ServerInterface.
        Primeiro verifica se o botão está abilitado e só cajo esteja invoca o callback.
        
        'event' - Objecto do tipo 'pygame.event' 
        """
        if ( self.enabled ):
            # Verifica se o click foi dentro do rectângulo do botão
            clickX, clickY = event.pos
            # Verifica no eixo do X
            if ( (clickX >= self.x) and ( clickX <= self.x + self.width ) ):
                # Verifica no eixo do Y
                if ( (clickY >= self.y) and ( clickY <= self.y + self.height ) ):
                    self.sensitive( False )
                    if ( self.callback != None ):
                        self.callback()






class Score( pygame.sprite.Sprite ):
    """
        ScoreBoard
    """
    
    def __init__(self, screen, x, y, playerName, robotName, robotColor, state, robotArmor=[100, 100, 100, 100], robotDamage=0, robotEnergy=100, gunTemperature=0, skinName='hk'):
        '''
            'screen' -  surface do ScoreBoard onde o Score vai ser dezenhado. 
            'x' - Coordenada no eixo do X onde o Score vai ser dezenhado
            'y' - Vem a zero porque este valor é passado pelo metodo 'draw' do ScoreBoard
            - playerName
            - robotName
            - robotArmor
            - robotLife
            - robotEnergy
            - gunTemperature
            - skinName
            - robotColor
        '''
        pygame.sprite.Sprite.__init__( self )
        
        #surface do ScoreBoard onde a Score vai ser dezenhado.
        self._screen = screen
        self.x = x
        self.y = y
        # Nome do jogador
        self._playerName  = playerName
        # Nome do robot
        self._robotName = robotName
        # Cor do robot na batalha
        self._robotColor = robotColor
        # Estado do jogador
        self._state = state
        # Armadura do robot
        self._robotArmor = robotArmor
        # Vida do robot
        self._robotDamage = robotDamage
        # Energia do robot
        self._robotEnergy = robotEnergy
        # Temperatura da arma do robot
        self._gunTemperature = gunTemperature
        # Nome da skin que o robot está a utilizar
        self._skinName = skinName
        
        # Nome da sample dos robot's. Supostamente este valor será sempre igual
        self.SAMPLE_SKIN = 'sample.png'
        # Sample do robot. Será do tipo 'pygame.image'.
        self._sample_img = None
        
        # Font que vai ser utilizada para dezenhar o Score
        self.MY_FONT = pygame.font.SysFont('arial', 11, bold = True, italic = False)
        
        # Guarda guarda a altura da 'Font' para quando se Desenha um valor(playerName, robotName, etc) se saber
        # onde começar a desenhar no eixo do 'y' para não desenhar valores em cima uns dos outros.
        # A cada valor que é desenhado, este atributo é incrementado com a altura dessa 'Font' depois de rederizada.
        self._fontHeight = 0
        
        # Carrega a sample da skin do robot
        self._load_sample()
        # Guarda a largura e altura da sample
        self._sampleWidth, self._sampleHeight = self._sample_img.get_size()
        



    def _load_sample(self):
        """
            Carrega a sample do robot.
        """
        try: 
            # Carrega a sample do robot.
            fullname = os.path.join('data', 'skins', self._skinName, self.SAMPLE_SKIN)
            # self._sample_img vai guardar a mascara do robot sem alterações
            self._sample_img = pygame.image.load(fullname).convert_alpha()
            
            self.image = self._sample_img
        
            return 0
            
        except pygame.error, err:
            printe("")
            printe( "Não foi possível carregar a sample do robot!" )
            printe( "Descrição: " + str(err) )

        return -1



    def _draw_robot_armor( self ):
        # Lateral Esquerdo
        startPos = (self.x - 4, self.y)
        endPos = (self.x - 4, self.y + self._sampleHeight)
        pygame.draw.line( self._screen, (226, 0, 6), startPos, endPos, 2 )

        startPos = (self.x - 4, self.y + self._sampleHeight)
        endPos = (self.x - 4, ((self.y + self._sampleHeight) - (self._robotArmor[ 3 ] / 3.125) ))
        # Verde
        pygame.draw.line( self._screen, (0, 226, 50), startPos, endPos, 2 )
        #########################################################################

        # Lateral Direita
        startPos = (self.x + self._sampleWidth + 2, self.y)
        endPos = (self.x + self._sampleWidth + 2, self.y + self._sampleHeight)
        pygame.draw.line( self._screen, (226, 0, 6), startPos, endPos, 2 )

        startPos = (self.x + self._sampleWidth + 2, (self.y + self._sampleHeight))
        endPos = (self.x + self._sampleWidth + 2, ((self.y + self._sampleHeight) - (self._robotArmor[ 1 ] / 3.125) ))
        # Verde
        pygame.draw.line( self._screen, (0, 226, 50), startPos, endPos, 2 )
        #########################################################################

        # Frente
        startPos = (self.x, self.y - 4)
        endPos = (self.x + self._sampleWidth, self.y - 4)
        pygame.draw.line( self._screen, (226, 0, 6), startPos, endPos, 2 )
    
        startPos = (self.x, self.y - 4)
        endPos = ((self.x + (self._robotArmor[ 0 ] / 3.125)), self.y - 4)
        # Verde
        pygame.draw.line( self._screen, (0, 226, 50), startPos, endPos, 2 )
        #########################################################################
        
        # Traseira
        startPos = (self.x, self.y + self._sampleHeight + 2)
        endPos = (self.x + self._sampleWidth, self.y + self._sampleHeight + 2)
        pygame.draw.line( self._screen, (226, 0, 6), startPos, endPos, 2 )
        
        startPos = (self.x, self.y + self._sampleHeight + 2)
        endPos = ((self.x + (self._robotArmor[ 2 ] / 3.125)), self.y + self._sampleHeight + 2)
        # Verde
        pygame.draw.line( self._screen, (0, 226, 50), startPos, endPos, 2 )        
        #########################################################################



    def _draw_state(self):
        x = ( self.x + (self._sample_img.get_width() / 2) )
        y = ( self.y + self._sampleHeight + 25 )
        
        if ( self._state == 'player_not_ready' ):
            pygame.draw.circle( self._screen, (0, 0, 0), (x, y) , 16 )
            pygame.draw.circle( self._screen, (226, 0, 6), (x, y) , 15 )
            
        else:
            pygame.draw.circle( self._screen, (0, 0, 0), (x, y) , 16 )
            pygame.draw.circle( self._screen, (0, 226, 50), (x, y) , 15 )
        


    def _draw_player_name(self):
        font = self.MY_FONT.render( str(self._playerName), True, self._robotColor )
        x = ( self.x + self._sampleWidth + 6 )
        self._screen.blit( font, (x, self.y) )
        
        

    def _draw_robot_name(self):
        font = self.MY_FONT.render( str(self._robotName), True, self._robotColor )
        # Vai buscar a altura da letra (que é igual ao playerName) e adiciona mais 4 pixeis. O resultado é o ponto y
        # onde o robotName vai ser dezenhado.
        self._fontHeight += (font.get_height())
        x = ( self.x + self._sampleWidth + 6 )
        y = ( self.y + self._fontHeight )
        
        self._screen.blit( font, (x, y) )
        


    def _draw_robot_damage( self ):
        font = self.MY_FONT.render( 'Estragos', True, self._robotColor )
        
        self._fontHeight += (font.get_height())
        x = ( self.x + self._sampleWidth + 6 ) 
        y = ( self.y + self._fontHeight )
        self._screen.blit( font, (x, y) )
        
        self._fontHeight += (font.get_height())
        
        
        # Desenha o resto da barra vazia em vermelho
        startPos = (self.x + self._sampleWidth + 6, self.y + self._fontHeight)
        endPos = (self.x + self._sampleWidth + 6 + 100, self.y + self._fontHeight)
        pygame.draw.line( self._screen, (0, 226, 50), startPos, endPos, 2 )
        
        startPos = (self.x + self._sampleWidth + 6, self.y + self._fontHeight)
        endPos = (self.x + self._sampleWidth + 6 + self._robotDamage, self.y + self._fontHeight)
        pygame.draw.line( self._screen, (226, 0, 6), startPos, endPos, 2 )
        


    def _draw_robot_energy( self ):
        font = self.MY_FONT.render( 'Energia', True, self._robotColor )
        # Neste caso, em vez de incrementar a altura da fonte, incrementa apenas 2 pixeis porque o que foi dezenhado 
        # antes foi apenas a barra de estado que é mais fina e tem tamanho estáctico
        self._fontHeight +=  2
        self._screen.blit( font, (self.x + self._sampleWidth + 6, self.y + self._fontHeight) )
        
        self._fontHeight += font.get_height()

        # Desenha o resto da barra vazia em vermelho
        startPos = (self.x + self._sampleWidth + 6, self.y + self._fontHeight)
        endPos = (self.x + self._sampleWidth + 6 + 100, self.y + self._fontHeight)
        pygame.draw.line( self._screen, (226, 0, 6), startPos, endPos, 2 )
        
        # Desenha a energia que ainda resta ao robot
        startPos = (self.x + self._sampleWidth + 6, self.y + self._fontHeight)
        endPos = (self.x + self._sampleWidth + 6 + self._robotEnergy, self.y + self._fontHeight)
        # Verde
        pygame.draw.line( self._screen, (0, 226, 50), startPos, endPos, 2 )



    def _draw_gun_temperature( self ):
        font = self.MY_FONT.render( 'Temperatura da Arma', True, self._robotColor )
        # Neste caso, em vez de incrementar a altura da fonte, incrementa apenas 2 pixeis porque o que foi dezenhado 
        # antes foi apenas a barra de estado que é mais fina e tem tamanho estáctico
        self._fontHeight +=  2
        self._screen.blit( font, (self.x + self._sampleWidth + 6, self.y + self._fontHeight) )
        
        self._fontHeight += font.get_height()
        
        # Desenha o resto da barra vazia em vermelho
        startPos = (self.x + self._sampleWidth + 6, self.y + self._fontHeight)
        endPos = (self.x + self._sampleWidth + 6 + 100, self.y + self._fontHeight)
        # Verde
        pygame.draw.line( self._screen, (0, 226, 50), startPos, endPos, 2 )
        
        # Desenha a energia que ainda resta ao robot
        startPos = (self.x + self._sampleWidth + 6, self.y + self._fontHeight)
        endPos = (self.x + self._sampleWidth + 6 + self._gunTemperature, self.y + self._fontHeight)
        pygame.draw.line( self._screen, (226, 0, 6), startPos, endPos, 2 )




    def draw( self, y ):
        self.y = y
        self._fontHeight = 0
        self._screen.blit( self._sample_img, (self.x, y) )
        self._draw_robot_armor()
        self._draw_player_name()
        self._draw_robot_name()
        self._draw_robot_damage()
        self._draw_robot_energy()
        self._draw_gun_temperature()
        self._draw_state()







    ##############################################################################
    #                            Metodos para actualização dos valores           #
    ##############################################################################

    def refresh_damage(self, damage):
        self._robotDamage = damage
    
    def refresh_armor( self, armor ):
        self._robotArmor = armor

    def refresh_energy(self, energy):
        self._robotEnergy = energy


    def refresh_gun_temperature(self, temperature):
        self._gunTemperature = temperature


    def refresh_state(self, state):
        self._state = state
    
    def get_player_state(self):
        return self._state

    ##############################################################################
    
    
    def get_player_name(self):
        return self._playerName
    

    def get_robot_name( self ):
        return self._robotName


    def set_death( self ):
        """
        Invocado quando o robot é destruido.
        Mete os valores todos a zero.
        """
        # Armadura do robot
        self._robotArmor = [ 0, 0, 0, 0 ]
        # Vida do robot
        self._robotDamage = 100
        # Energia do robot
        self._robotEnergy = 0
        # Temperatura da arma do robot
        self._gunTemperature = 100


    def reset( self ):
        """
        Faz um reset a todos os contadores que são alterados ao longo da batalha.
        É utilizado quando um round é iniciado.
        """
        self._robotArmor = [ 100, 100, 100, 100 ]
        self._robotDamage = 0
        self._robotEnergy = 100
        self._gunTemperature = 0











#class ScoreBoard(pygame.sprite.Sprite):
class ScoreBoard(pygame.surface.Surface):
    def __init__(self, screen, pos, width, height, color, owner):
        """
            ScoreBoard( self.screen, 611, 47, 178, 542 , (150, 150, 0))
        """
        # Posição (x, y) onde o scoreboard vai ser dezenhado
        self.pos = pos
        #
        self.width = width
        self.height = height
        pygame.Surface.__init__(self, (width, height)) #, 0, 32)
        self.fill( color )
        # Lista de Scores a mostrar no ScoreBoard.
        # Cada jogador tem um Score, excepto os Espectadores.
        self.scoresList = []
        # Cor de fundo
        self._color = color
        # Indica se o jogador local é o owner da batalha
        self.owner = owner
        # Screen onde o ScoreBoard é dezenhado
        self._screen = screen
        # Posição inicial para os Scores
        self._initYPos = 60
        # Altura de cada Score
        self._scoreHeight = 100
        
        x = self.pos[0] + (self.width / 2 )
        y = self.pos[1] + 515
          
        self.buttonStartBattle = Button( self._screen, None, (x, y), 'Iniciar Batalha' )
        self.buttonStartBattle.create_button()
        
    
    
    def get_score(self, name):
        """
        É utilizado para ir à lista de 'Score's' buscar o Score que se quer apartir do nome do jogador ou do 
        nome do robot.
        
        Retorna a instância da Score se encontrar o nome do jogador ou do robot.
        None, se não encontrar.
        """
        for score in self.scoresList:
            if ( (name == score.get_player_name()) or (name == score.get_robot_name()) ):
                return score


    def get_score_by_pos( self, position ):
        """
        Retorna o Score de uma determinada posição da lista.
        """
        # Em principio não é preciso controlar o valor de "position"
        return self.scoresList[ position ]
    
    
    def draw( self ):
        """
        Desenha o ScoreBoard no 'screen' fornecido.
        """
        yPos = self._initYPos 
        for score in self.scoresList:
            score.draw( yPos )
            yPos += self._scoreHeight
        
        # Se o jogador local não for o owner da batalha não precisa do botão porque não pode iniciar a batalha
        if ( self.owner ):
            self.buttonStartBattle.draw()



    def add_score(self, playerName, robotName, robotColor, playerStatus, robotArmor=[100, 100, 100, 100], robotDamage=0, robotEnergy=100, gunTemperature=0, skinName='hk'):
        """
        Adiciona Score's ao ScoreBoard.
        
        'info' - é uma lista com os argumentos para a classe Score.
        Score(self, playerName, robotName, robotColor, robotArmor=[100, 100, 100, 100], robotDamage=100, robotEnergy=100, gunTemperature=0, skinName='hk'):
        """
        #newScore = Score( self, 10, self.position_y, playerName, robotName, robotColor, robotArmor, robotDamage, robotEnergy, gunTemperature, skinName )
        newScore = Score( self._screen, 620, 0, playerName, robotName, robotColor, playerStatus, robotArmor, robotDamage, robotEnergy, gunTemperature, skinName )
        self.scoresList.append( newScore )



    def remove_player(self, name):
        """
        Remove score's dos jogadores.
        
        'name' - Nome do jogador ou do robot a ser removido.
        """
        for score in self.scoresList:
            if ( (name == score.get_player_name()) or (name == score.get_robot_name()) ):
                self.scoresList.remove( score )
                return


    def set_score_state(self, playerName, state):
        """
        Actualiza o status do Score (player_ready/player_not_ready)
        """
        score = self.get_score( playerName )
        score.refresh_state( state )



