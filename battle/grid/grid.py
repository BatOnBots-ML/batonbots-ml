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

# Utilizado para ver a resolução que está a ser utilizada
# IMPORTANTE: se ficar depois do "import pygame" dá problemas pelo menos em windows!
from gtk import Window
import pygame


from decimal import Decimal
 
class Grid( object ):
    '''
    Gera a GUI que mostra as estatisticas no final da batalha orientada aos robôs.
    '''


    def __init__(self, screen, maxWindowSize = None ):
        self._screen = screen
        # Objecto do tipo pygame.Surface que vai ser desenhado no screen
        self._surface = None
        # Tupla com o número de colunas e linhas que a grelha vai ter. É calculado posteriormente
        self._tableSize = ()
        # Tupla com o tamanho da janela. -este tamanho é calculado consuate os dados da gridList e tem como máximo self.maxWindowSize
        self._windowSize = ()
        # Tupla com o tamanho da surface- este tamanho é calculado consuate os dados da gridList
        self._surfaceSize = ()
        # Posição apartir da qual a self._surface é desenhada no self._screen
        self._surfOffSet = (0, 0)
        # Tamanho máximo da janela. Se exceder este tamanho entra em funcionamento de slide
        if ( maxWindowSize != None ):
            self._maxWindowSize = maxWindowSize
        else:
            # Vê a resolução que está a ser utilizada
            win = Window()
            scr = win.get_screen()
            # O height é a altura sem contar com as possíveis barras. O 100 é um remendo para dar o desconto das
            # possíveis barras 
            self._maxWindowSize = ( scr.get_width(), scr.get_height() - 100 )
            del win
            del scr
        # Flag que indica se deve ou não fazer slide horizontal
        self._doHSlide = False
        # Flag que indica se deve ou não fazer slide vertical
        self._doVSlide = False
        # Cursor que é mostrado na janela. É carregado apartir do metodo 'create'
        self._cursor = None
        
        # Lista apartir da qual a grelha vai ser criada
        # Ex. de uma batalha com duas rondas e dois robots 
        #[   ['Robot1', 0, 0, 0, 0, 0, 0, 1.0], ['Robot2', 0, 0, 0, 3, 0, 0, 0.0], ['Robot3', 0, 15, 0, 1, 1, 0, 1.1]   ]
        self._gridList = []
        # Margem esquerda(em pixeis)
        self._leftMargin = 30
        # Margem direita(em pixeis)
        self._rightMargin = 30
        # Margem superior(em pixeis)
        self._topMargin = 40
        # Margem inferior(em pixeis)
        self._bottomMargin = 20
        # Nome da batalha que vai aparecer como titulo na janela
        self._battleName = ""
        # battleName já rederizado
        self._title = None
        
        self._titleColor = (193, 5, 0)
        self._textColor = (255, 199, 0)
        self._backGroundColor = (27, 62, 80)
        self._headerColor = (193, 5, 0)
        
        self._TITLE_FONT = pygame.font.SysFont( pygame.font.get_default_font(), 32, bold = True, italic = False )
        self._HEADER_FONT = pygame.font.SysFont( pygame.font.get_default_font(), 18, bold = True, italic = False )
        self._TEXT_FONT = pygame.font.SysFont( pygame.font.get_default_font(), 16, bold = False, italic = False )

        # Espaço entre o texto da grelha e as linhas(em pixeis)
        self._columnPitch = 10
        # Espaço entre cada linha da grelha(em pixeis)
        self._rowPitch = 10

        # Guarda a altura em que o ultimo componente foi desenhado entre cada fase de desenho da grelha
        self._yLocation = 0
        # Lista que guarda a largura de cada coluna
        self._columnsWidthList = []
        
        # Texto para o cabeçalho da tabela
        # Apesar de quando o cabeçalho é desenhado na surface ser feito o encoding para utf-8, quando se faz o calculo
        # da largura do texto, a medida não é a correcta porque não está a fazer os calculos com com a string com o 
        # encoding correcto. Para evitar isso, a solução mais rápida foi adicionar logo aqui o enconding correcto.
        # Futuramente, se for feito o sistema de multi-linguas, este terá de ter suporte unicode!
        self.transDict = {
                          "robotName": "Nome",
                          "kills": u"Destruídos",
                          "deaths": u"Destruído",
                          "damageCaused": "Danos Causados",
                          "damage": "Danos Sufridos",
                          "totalShots": "Tiros Disparados",
                          "goodShots": "Tiros Certeiros",
                          "accuracy": "Pontaria(%)",
                          "won": "Venceu",
                          "totalScore": u"Pontuação"
                        }





    #################################################################################################
    
    def _draw_title( self ):
        #titleFontSize = self._title.size()
        titleFontSize = self._TITLE_FONT.size( self._battleName )
        x = (self._surfaceSize[0] / 2) - (titleFontSize[0] / 2)
        y = self._topMargin - (titleFontSize[1] / 2)
        # Actualiza o apontador
        self._yLocation = y + (titleFontSize[1] / 2)
        self._surface.blit( self._title, (x, y) )
    
    
    def _draw_header( self ):
        x = self._leftMargin
        # SE MUDAR O 40 AQUI TAMBÉM TEM DE SER ALTERADO NO METODO '_calc_window_size'!!!!!!!!!!
        y = self._yLocation + 40
        i = 0
        # É preciso esta lista em vez da retornada por self.transDict.keys() porque esta ultima altera a ordem e não pode 
        keys = [
                "robotName",
                "kills",
                "deaths",
                "damageCaused",
                "damage",
                "totalShots",
                "goodShots",
                "accuracy",
                "won",
                "totalScore"
        ]
        for key in keys:
            unicStr = unicode( str(self.transDict[key]), encoding = "utf-8", errors = "replace" )
            rendText = self._HEADER_FONT.render( unicStr, True, self._headerColor, self._backGroundColor )
            _x = x + (  ( self._columnsWidthList[ i ] / 2 ) - ( self._HEADER_FONT.size(self.transDict[key])[0] / 2 )  )
            self._surface.blit( rendText, (_x, y) )
            x += self._columnsWidthList[ i ]
            i += 1
        # Actualiza o apontador
        self._yLocation = y + self._HEADER_FONT.size( self.transDict[key] )[ 1 ]


    def _draw_data( self ):
        y = self._yLocation + self._rowPitch
        for row in self._gridList:
            i = 0
            x = self._leftMargin
            for value in row:
                unicValue = unicode( str(value), encoding = "utf-8", errors = "replace" )
                rendText = self._TEXT_FONT.render( unicValue, True, self._textColor, self._backGroundColor )
                #_x = x + (  ( self._columnsWidthList[i] / 2 ) - ( (self._TEXT_FONT.size(str(value))[0] + self._columnPitch) / 2 )  )
                _x = x + (  ( self._columnsWidthList[i] / 2 ) - ( self._TEXT_FONT.size(str(value))[0] / 2 )  )
                self._surface.blit( rendText, (_x, y) )
                x += self._columnsWidthList[i]
                i += 1
            y += self._TEXT_FONT.size( str(value) )[ 1 ] + self._rowPitch


    def draw( self ):
        self._surface.fill( self._backGroundColor )
        self._screen.fill( self._backGroundColor )
        self._draw_title()
        self._draw_header()
        self._draw_data()
        self._screen.blit( self._surface, self._surfOffSet )
        
        
    #################################################################################################
  
    
    def _set_cursor( self ):
        size = (24, 16)
        # Quando faz slide horizontal e vertical
        if ( self._doHSlide and self._doVSlide ):
            cursData, mask = pygame.cursors.compile( pygame.cursors.sizer_xy_strings, black='X', white='.', xor='o' )
            # Quando faz slide horizontal
        elif ( self._doHSlide ):
            cursData, mask = pygame.cursors.compile( pygame.cursors.sizer_x_strings, black='X', white='.', xor='o' )
        # Quando faz slide vertical
        elif ( self._doVSlide ):
            cursData, mask = pygame.cursors.compile( pygame.cursors.sizer_y_strings, black='X', white='.', xor='o' )
            size = (16, 24)
        else:
            return
            
        self._cursor = ( size, (7, 0), cursData, mask )
        pygame.mouse.set_cursor( *self._cursor )


    def _config_window( self ):
        pygame.display.set_mode( self._windowSize )


    def _calc_rows_num( self ):
        """
        Calcula o número de linhas que vão ser precisas com base na gridList recebida.
        Coloca a informação no atributo self._tableSize
        """
        # O número de colunas é sempre o mesmo
        columns = 10
        for n in range(columns): self._columnsWidthList.append(0) 
        # Utiliza-se como amostra o primeiro round menos 1 porque o primeiro campo de cada round é o nome da batalha
        rows = len( self._gridList[0] ) - 1
        self._tableSize = ( columns, rows )



    def _calc_window_size( self ):
        """
        Calcula o tamanho da janela com base no cabeçalho da grelha ou no nome da batalha(titulo).
        Calcula o tamanho dos dois, e escolhe o que for maior.
        
        Configura o atributo self._windowSize e o _surfaceSize com uma tupla com a largura e altura da janela.
        """
        headerWidth = 0
        titleWidth = 0
        rowHeight = 0
        width = 0
        i = 0
        # É preciso esta lista em vez da retornada por self.transDict.keys() porque esta ultima altera a ordem e não pode 
        keys = [
                "robotName",
                "kills",
                "deaths",
                "damageCaused",
                "damage",
                "totalShots",
                "goodShots",
                "accuracy",
                "won",
                "totalScore"
        ]
        
        ###### Calcula a largura
        for key in keys:
            w = self._columnPitch + self._HEADER_FONT.size( self.transDict[key] )[0] + self._columnPitch
            # Configura a largura da coluna
            self._columnsWidthList[ i ] = w
            # Incrementa a largura do cabeçalho
            headerWidth += w
            i += 1
        width = headerWidth
        ##
        titleWidth = self._TITLE_FONT.size( self._battleName )[0]
        if ( titleWidth > width ): width = titleWidth
        ##
        width += self._leftMargin + self._rightMargin
        ######
        
        ###### Calcula a altura
        rowHeight = self._TEXT_FONT.size("W")[1]
        # O 40 é uma solução rápida para criar o espaço que vai ser deixado entre o titulo(battleName) e a grelha
        height = self._topMargin + (rowHeight * self._tableSize[ 1 ]) + self._bottomMargin + 40
        ######
        
        self._surfaceSize = (width, height)

        # Impoe os limites de tamanho na janela
        if ( (width > self._maxWindowSize[0]) and (height > self._maxWindowSize[1]) ):
            self._windowSize = ( self._maxWindowSize[0], self._maxWindowSize[1] )
            self._doHSlide = True
            self._doVSlide = True
        elif( width > self._maxWindowSize[0] ): 
            self._windowSize = ( self._maxWindowSize[0], height )
            self._doHSlide = True
        elif( height > self._maxWindowSize[1] ): 
            self._windowSize = ( width, self._maxWindowSize[1] )
            self._doVSlide = True
        elif ( (width < self._maxWindowSize[0]) and (height < self._maxWindowSize[1]) ):
            self._windowSize = ( width, height )
        
        # Inicia a surface
        self._surface = pygame.Surface( self._surfaceSize )





    #######################################################
    def _h_slide( self, event ):
        x = self._surfOffSet[ 0 ] + event.rel[0]
        if ( x > 0 ):
            x = 0
        if ( x < (self._maxWindowSize[0] - self._surfaceSize[0]) ):
            x = (self._maxWindowSize[0] - self._surfaceSize[0])

        offSet = ( x, self._surfOffSet[1] )
        self._surfOffSet = offSet


    def _v_slide( self, event ):
        y = self._surfOffSet[ 1 ] + event.rel[1]
        if ( y > 0 ):
            y = 0
        if ( y < (self._maxWindowSize[1] - self._surfaceSize[1]) ):
            y = (self._maxWindowSize[1] - self._surfaceSize[1])

        offSet = ( self._surfOffSet[0], y )
        self._surfOffSet = offSet


    def _slide( self, event ):
        if ( self._doHSlide ):
            self._h_slide( event )
        if ( self._doVSlide ):
            self._v_slide( event )
            
            
    
    
    def events_handler( self, event ):
        """
        Controla os eventos do rato.
        
         Retorna True se o evento não for o pygame.QUIT e false se for. Isto serve para o main_loop saber quando terminar.
        """
        alive = True
        if event.type == pygame.QUIT:
            alive = False
        elif (event.type == pygame.MOUSEMOTION):
            if ( event.buttons == (1, 0, 0) ):
                self._slide( event )
        
        return alive
    #######################################################
  
  
  


    def load_data( self, gridList ):
        """
        Carrega para a tabela a informação passada pela gridList.
        
         - gridList - Lista com a informação para carregar para a tabela:
        Ex. de uma batalha(gridList) com duas rondas e dois robots 
        [   ['Robô1', 1, 2, 3, 4, 5, 600, 0, 1.0, 0], ['Robô2', 0, 0, 0, 3, 0, Decimal(0.04), 1, 0.0, 0], ['Robot Com Nome Grand', 0, 0, 15, 0, 0, 0, 2, 0.8, 0]    ] 
        """
        # Largura total da linha. Serve para o tamanho final da janela
        width = 0
        #
        rowHeight = 0
        height = 0
        i = 0
        for row in self._gridList:
            rowWidth = 0
            i = 0
            for value in row:
                w = self._columnPitch + self._TEXT_FONT.size( str(value) )[0] + self._columnPitch
                # Verifica se o texto que vai ser carregado para cada coluna é mais largo que o cabeçalho da coluna
                if ( w > self._columnsWidthList[i] ):
                    self._columnsWidthList[ i ] = w
                    rowWidth += w
                else:
                    rowWidth += self._columnsWidthList[ i ]
                i += 1
                    
            rowWidth += self._leftMargin + self._rightMargin
            if ( rowWidth > width ): width = rowWidth
            

        ###### Calcula a altura
        rowHeight = self._TEXT_FONT.size("W")[1]
        # O 40 é uma solução rápida para criar o espaço que vai ser deixado entre o titulo(battleName) e a grelha
        height = self._topMargin + (rowHeight * self._tableSize[ 1 ]) + self._bottomMargin + 40
        ######
        
        self._surfaceSize = (width, height)
        
        # Impoe os limites de tamanho na janela
        # Impoe os limites de tamanho na janela
        if ( (width > self._maxWindowSize[0]) and (height > self._maxWindowSize[1]) ):
            self._windowSize = ( self._maxWindowSize[0], self._maxWindowSize[1] )
            self._doHSlide = True
            self._doVSlide = True
        elif( width > self._maxWindowSize[0] ): 
            self._windowSize = ( self._maxWindowSize[0], height )
            self._doHSlide = True
        elif( height > self._maxWindowSize[1] ): 
            self._windowSize = ( width, self._maxWindowSize[1] )
            self._doVSlide = True
        elif ( (width < self._maxWindowSize[0]) and (height < self._maxWindowSize[1]) ):
            self._windowSize = ( width, height )
        
        # Inicia a surface
        self._surface = pygame.Surface( self._surfaceSize )


        
        # Actualiza a janela
        self._config_window()
        
        




    def create( self, gridList, battleName ):
        """
        Lista apartir da qual a grelha vai ser criada
        Ex. de uma batalha(gridList) com duas rondas e dois robots 
        [   ['Robô1', 1, 2, 3, 4, 5, 600, 0, 1.0, 0], ['Robô2', 0, 0, 0, 3, 0, Decimal(0.04), 1, 0.0, 0], ['Robot Com Nome Grand', 0, 0, 15, 0, 0, 0, 2, 0.8, 0]    ]
        """
        self._gridList = gridList
        self._calc_rows_num()
        self._battleName = unicode( str(battleName), encoding = "utf-8", errors = "replace" )
        self._title = self._TITLE_FONT.render( self._battleName, True, self._titleColor, self._backGroundColor  )
        self._calc_window_size()
        # Configura o tamanho da janela
        self._config_window()
        # Carrega para a tabela a informação da gridList
        self.load_data( gridList )
        # Configura o cursor que vai utilizar
        self._set_cursor()


















if ( __name__ == "__main__" ):
    pygame.font.init()
    pygame.display.init()
    screen = pygame.display.set_mode((600, 600), 0, 32)
    clock = pygame.time.Clock()
    alive = True
    
    grid = Grid( screen )
    #gridList = [   [31.0, ['MMMMMMMM', 0, 1, 0, 0, 0, 0, 0, 1.0], ['Mr. Anderson', 0, 0, 0, 0, 3, 0, 0, 0.0]], [32.0, ['Mr. Anderson', 0, 2, 15, 0, 1, 1, 0, 1.1], ['Mr. Smith', 0, 0, 0, 15, 0, 0, 0, 0.8]]    ]
    gridList = [   ['Robô1', 1.0, 0, 2, 3, 4, 5, 100, 0, 1.0], ['Robô2', 3, 2, 0, 0, 3, 0, 0.04, 1, 0.0], ['Robot Com Nome Grand', 0, 1, 0, 15, 0, 0, 0, 2, 0.8]    ]
    grid.create( gridList, "Titulo da Batalhã!!" )
    while  alive:
        for event in pygame.event.get():
            alive = grid.events_handler( event )


        
        pygame.display.flip()
        grid.draw()
        clock.tick(25)
        
    
    pygame.font.quit()
    pygame.display.quit()
    #pygame.quit()
    
    
    