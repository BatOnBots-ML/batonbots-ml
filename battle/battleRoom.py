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


import os
from os import path
from random import randint, sample
from time import sleep, time
import pygame
from decimal import Decimal, getcontext

from scoreboard import ScoreBoard
from animations import TextFadeAnimation
from changes_queue import ChangesQueue
from battle.robot.robot import Robot
from bullet import Bullet
from grid.grid import Grid
from battle.bullet_explosion import Explosion
from log.logging_mod import Logging
log = Logging()
printd = log.debug
printi = log.info
printe = log.error
printw = log.warning



class Chron( object ):
    def __init__( self, time ):
        """
        time - tempo em segundos
        """
        self._time = self._init_time = self._convert_time( time )

    def _convert_time( self, sec ):
        minuts = 0
        seconds = 0
        
        minuts, seconds = str( float(sec) / float(60) ).split( "." )
        minuts = int( minuts )
        seconds = ( "0." + seconds )
        seconds = int( round(float(seconds) * 60, 0) )
        return ( minuts, seconds )


    ####################################################################################
    ##  Metodos Públicos
    ####################################################################################
    def decrease( self ):
        min, sec = self._time
        if ( (sec == 0) and (min > 0) ):
            if ( min > 0 ):
                min -= 1
                sec = 59
                self._time = ( min, sec )
                return (min, sec)
        sec -= 1
        self._time = ( min, sec )
        return self._time

    def get_time( self ):
        return ( self._time[0], self._time[1] )

    def set_time( self, time ):
        """
        time - tempo em segundos
        """
        self._time = self._init_time = self._convert_time( time )

    def reset( self ):
        self._time = self._init_time







#class BattleRoom( pygame.sprite.Sprite ):
class BattleRoom():

    def __init__( self, keepalive, bgName = 'background.png' ):
        """
        keepalive - Metodo do ServerInterface que faz o keepalive. É necessário para quando está a mostrar o quadro das
                    estatisticas.
        """
        self.transDict = {
                      'animText': 'Ronda'
                     }

        # Metodo do ServerInterface que faz o keepalive. É necessário para quando está a mostrar o quadro das estatisticas.
        self._keepalive = keepalive
        # Flag que serve para indicar se a batalha já foi iniciada ou não
        self.started = False

        # Nome do ficheiro da imagem de fundo
        self.bgName = bgName
        # Imagem de fundo
        self.bgImage = None
        # Instancia da classe 'Rect' da imagem de fundo
        self.bgRect = None
        # Instancia da classe 'pygame.Surface'
        self.background = None
        # Lista com as texturas para o fundo da batalha
        self.textures = []
        # Rectângulo da imagem da textura
        self.textureRect = None
        # Lista com o posicionamento das texturas
        self.texturesMap = []
        # Largura da janela da batalha
        self.SCREEN_WIDTH = 0
        # Altura da janela da batalha
        self.SCREEN_HEIGHT = 0
        # Rectângulo do campo de batalha. O campo de batalha é o espaço onde os robot's andam
        self.battleFieldRect = (0, 0, 600, 600)
        
        # Rectangulo de cada peça da animação da explosão das balas
        self._bulletExplosionPartsRect = pygame.Rect( 0, 0, 64, 64 )
        # Carrega a sprite para as explosões das balas
        self._bulletExplosionPartsList = self._load_bullet_explosion()
        
        # Rectangulo de cada peça da animação da explosão dos robots
        self._robotExplosionPartsRect = pygame.Rect( 0, 0, 128, 128 )
        # Carrega a sprite para as explosões das balas
        self._robotExplosionPartsList = self._load_robot_explosion()
        # ID das explosões dos robots. É incrementado cada vez que um robot explode
        self._robotExplosionID = 0
        
        # Objecto do tipo 'pygame.Surface' onde vai ser desenhado o mapa das texturas
        bfWidth = self.battleFieldRect[ 2 ]
        bfHeight = self.battleFieldRect[ 3 ]
        self.battleFieldImage = pygame.Surface( (bfWidth, bfHeight) )
        # 
        self.screen = None
        # Imagem das balas
        self._bulletImage = None
        
        # Instancia 'pygame.time.Clock'
        self.clock = pygame.time.Clock()
        # Lista com os objectos a desenhar na janela
        #self.objectsList = []
        # Titulo da janela
        self.windowTitle = "BatOnBots-ML - "
        #
        self._chron = Chron( 0 )
        # Nome da batalha que vai aparecer junto ao titulo da janel
        self.battleName = ''
        # Indica se foi o jogador local que criou a bataha. Serve para mostrar ou não o botão de iniciar a batalha
        self.battleOwner = False
        # Nome do jogador local
        self._playerName = ""
        # Instância da classe ScoreBoard
        self.scoreBoard = None
        # Coordenadas onde o ScoreBoard vai ser desenhado
        self.scoreBoardPos = (609, 47)
        
        # Quando 'True' indica ao metodo 'draw()' que deve mostrar a animação
        self.showAnimation = False
        # Animação que aparece quando a batalha é iniciada. É inicializano no metodo 'start_animation()' porque
        # quando a instancia desta classe é criada, o main loop do pygame ainda não foi iniciado
        self._animation = None
        
        # Guarda o número do round em que está
        self.round = 1
        # Esta variável não é constante!
        # Valores:
        #   - 4  : Antes da batalha iniciar
        #   - 45 : Durante a animação do delay
        #   - 25 : Durante a batalha 
        self.fps = 4
        # Flag para o 'main_loop()'
        self.alive = True
        
        # Vai ser uma lista com instancias da classe 'Robot' utilizada para desenhar as imagens de cada robot 
        # no campo de batalha.
        # Esta lista só é inicializada quando o interface recebe o comando '_init_positions' que é quando
        # é preciso começar a desenhar os robots.
        # ! Importante : Esta lista tem de ser limpa quando a batalha termina ou quando um novo round inicia 
        # porque existe um controlo no metodo 'draw' que depende do conteudo desta lista. Todos os objectos
        # nesta lista têm de ter pelo menos os seguintes metodos: 'blit()',  'get_name()', 'update()'
        self.objectsGroup = []
        
        # Guarda todas as alterações e eventos recebidas (nível 1)
        self.changesQueue = ChangesQueue()
        # Para onde é feito o dequeue da changesQueue (nível 2)
        #self.changesPerCycle = ChangesQueue()

        # Define uma casa decimal para os resultados dos calculos
        getcontext().prec = 2


    def _load_background(self):
        """
            Carrega a imagem que vai servir de background.
        """
        try:
            fullname = os.path.join('data', 'backgrounds', self.bgName)
            self.bgImage = pygame.image.load(fullname)#.convert_alpha()
            self.bgRect = self.bgImage.get_rect()
            self.background = pygame.Surface(self.bgImage.get_size())
            self.background.blit(self.bgImage, (0, 0))
            return 0
        except pygame.error, err:
            printe( "Não foi possível carregar a imagem de fundo!" )
            printe( "!!! Descrição: " + str(err) )
        return -1


    def _load_textures(self):
        """
        Carrega as texturas e coloca-as numa lista
        """
        nTextures = 3
        textureName = 'texture'
        textureExt= '.png'
        try:
            for i in range( nTextures ):
                fullname = os.path.join('data', 'backgrounds', textureName + str(i) + textureExt)
                self.textures.append ( pygame.image.load(fullname) )#.convert_alpha()
                self.textureRect = self.textures[i].get_rect()
            return 0
        except pygame.error, err:
            printe( "Não foi possível carregar as texturas!" )
            printe( "Descrição: " + str(err) )

        return -1


    def _config_window(self):
        """
            Cria a janela onde se vai passar a batalha.
        """
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.bgImage.get_size()
        try:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
            # Mete o titulo na janela
            self.set_title()
            return 0
        except pygame.error, err:
            printe( "Não foi possível criar a janela de jogo!" )
            printe( "Descrição: " + str(err) )
        return -1


    def create(self):
        """
        Inicia a sala de jogo.
        """
        printi( "A carregar imagem de fundo..." )
        if (self._load_background() == -1):
            return -1
        printi( "A carregar texturas..." )
        if (self._load_textures() == -1):
            return -1
        printi( "A configurar a janela de jogo..." )
        if (self._config_window() == -1):
            return -1
        # Cria o mapa das texturas
        self.generate_textures_map()
        # Cria uma imagem com o mapa das texturas. A imagem é um objecto do tipo 'pygame.Surface'.
        self.generate_battle_field()
        # Cria o quadro de resultados do lado direito da janela
        #self.scoreBoard = ScoreBoard( self.screen, self.scoreBoardPos, 229, 542 , (169, 171, 175), self.battleOwner)
        self.scoreBoard = ScoreBoard( self.screen, self.scoreBoardPos, 229, 542 , (137,137,137), self.battleOwner)
        return 0


    ################################################################
    def set_title( self ):
        """
        Mete o titulo na janela
        """
        pygame.display.set_caption( self.windowTitle )
    ################################################################


    def tictac( self ):
        min, sec = self._chron.decrease()
        chron = str( min ) + ":" + str( sec )
        self.windowTitle = "BatOnBots-ML - " + self.battleName + "  **  " + str(chron)
        self.set_title()
        

    def set_time( self, seconds = None ):
        if ( seconds != None ):
            self._chron.set_time( seconds )
        min, sec = self._chron.get_time()
        chron = str( min ) + ":" + str( sec )
        self.windowTitle = "BatOnBots-ML - " + self.battleName + "  **  " + str(chron)
        self.set_title()
    

    ################################################################
    def set_battle_name(self, battleName):
        self.battleName = battleName
        
    
    def get_battle_name(self):
        return self.battleName
    ################################################################    

    ################################################################
    def set_owner(self, owner):
        """
        'owner' - Bool -True se o jogador local for o owner da batalha.
                        False se não for.
        """
        self.battleOwner = owner
        
    
    def get_owner(self):
        return self.battleOwner
    ################################################################   


    ################################################################
    def set_player_name(self, playerName):
        """
        'playerNAme' - Nome do jogador local. É utilizado para actualizar o estado do robot.
        """
        self._playerName = playerName
        
    
    def get_player_name(self):
        return self._playerName
    ################################################################  


    def check_ready_for_battle(self):
        """
        É invocado quando um jogador muda de estado ou quando um jogador sai.
        
        Serve para alterar o estado do botão para iniciar a batalha.
        Verifica se todos os jogadores estão 'player_ready' e se há jogadores suficientes para iniciar a batalha.
        Por defeito o minimo são dois jogadores.
        """
        playersReady = True
        
        # Verifica o estado de cada jogador
        for player in self.scoreBoard.scoresList:
            playerState = player.get_player_state()
            if ( playerState == 'player_not_ready' ):
                playersReady = False
                break
            
        # Verifica se existe mais de 1 jogadore para poder iniciar a batalha 
        if ( len(self.scoreBoard.scoresList) < 2 ):
            playersReady = False
        
        if ( not self.started ):
            if ( playersReady ):
                self.scoreBoard.buttonStartBattle.sensitive( True )
            else:
                self.scoreBoard.buttonStartBattle.sensitive( False )


    def add_players(self, list):
        """
        Recebe uma lista com jogadores e adiciona-os ao ScoreBoard
        """
        #Por cada jogador a list
        # [ playerName, playerStatus, robotName, skinName, playerColor, robotArmor, robotDamage, robotEnergy, gunTemperature ]
        #[['Kein', 'player_not_ready', 'Mr. Smith', 'hk', (255, 0, 0), [100, 100, 100, 100], 0, 100, 0]]
        for player in list:
            # Adiciona ao ScoreBoard
            playerName = player[0]
            playerStatus = player[1]
            robotName = player[2]
            robotSkin = player[3]
            robotColor = player[4]
            robotArmor = player[5]
            robotDamage = player[6]
            robotEnergy = player[7]
            gunTemperature = player[8]
            
            self.scoreBoard.add_score( playerName, robotName, robotColor, playerStatus, robotArmor, robotDamage, robotEnergy, gunTemperature, robotSkin  )


    def _remove_player_score(self, name):
        """
        Remove jogadores da batalha.
        
        'playerName' - Nome do jogador ou do robot a ser removido.
        """
        self.scoreBoard.remove_player( name )
        

    def generate_textures_map(self):
        """
        """
        # Número máximo de texturas que o rectângulo do campo de batalha vai levar
        maxRep = 100
        map = []
        # As vezes que pode ser repetida cada tipo de textura. É utilizado um âmbito para se calcular o número 
        # aleatóriamente dentro desse âmbito.
        rangeRep1 = [0, 5]
        rangeRep2 = [0, 5]
        # Calcula as repetições 'aleatóriamente' dentro do âmbito dado.
        rep1 = randint( rangeRep1[0], rangeRep1[1] )
        rep2 = randint( rangeRep2[0], rangeRep2[1] )
        # Fica com o resto porque é a textura principal
        rep0 = maxRep - ( rep1 + rep2 )
        # Preenche o mapa de texturas com a textura principal
        for n in range(maxRep):
            map.append( n )
            self.texturesMap.append( 0 )

        result = sample(map,  (rep1 + rep2))
        for pos in range( (rep1 + rep2) ):
            if ( pos <= (rep1-1) ):
                    self.texturesMap[ result[ 0 ] ] = 1
                    result.pop(0)
            else:
                self.texturesMap[ result[ 0 ] ] = 2
                result.pop(0)


    def generate_battle_field( self ):
        x = 0
        y = 0
        # Numero de texturas que cada linha pode ter
        rowLen = 10
        i = 0
        # Mete uma cor de fundo. (R, G, B)
        self.battleFieldImage.fill( (0, 0, 0) )
        textureWidth = self.textureRect[2]
        textureHeight = self.textureRect[3]
        for texture in self.texturesMap:
            if ( i == rowLen ):
                y += textureHeight + 1
                x = 0
                i = 0
            #self.screen.blit(self.textures[ texture ], (x,y))
            self.battleFieldImage.blit(self.textures[ texture ], (x,y))
            x += textureWidth + 1
            i += 1
    ####################################################################################
    ####################################################################################


    def _load_bullet_explosion( self ):
        spriteName = "bullet_explosion.png"
        spritePath = path.join('data', spriteName)
        spriteImg = pygame.image.load( spritePath )#.convert_alpha()
        # Numero de colunas
        columns = 4
        # Linhas
        rows = 4
        #
        spriteParts = []
        for row in xrange( rows ):
            for column in xrange( columns ):
                part = pygame.Surface( (self._bulletExplosionPartsRect.width, self._bulletExplosionPartsRect.height), pygame.SRCALPHA )
                part.blit( spriteImg, (0, 0, self._bulletExplosionPartsRect.width, self._bulletExplosionPartsRect.height), self._bulletExplosionPartsRect )
                spriteParts.append( part )
                self._bulletExplosionPartsRect.move_ip( self._bulletExplosionPartsRect.width, 0 )
                
            self._bulletExplosionPartsRect.x = 0
            self._bulletExplosionPartsRect.move_ip( 0, self._bulletExplosionPartsRect.height )
        return spriteParts


    def _load_robot_explosion( self ):
        spriteName = "robot_explosion.png"
        spritePath = path.join('data', spriteName)
        spriteImg = pygame.image.load( spritePath )#.convert_alpha()
        
        # Numero de colunas
        columns = 8
        # Linhas
        rows = 3
        #
        spriteParts = []
        for row in xrange( rows ):
            for column in xrange( columns ):
                part = pygame.Surface( (self._robotExplosionPartsRect.width, self._robotExplosionPartsRect.height), pygame.SRCALPHA )
                part.blit( spriteImg, (0, 0, self._robotExplosionPartsRect.width, self._robotExplosionPartsRect.height), self._robotExplosionPartsRect )
                spriteParts.append( part )
                self._robotExplosionPartsRect.move_ip( self._robotExplosionPartsRect.width, 0 )
            
            self._robotExplosionPartsRect.x = 0
            self._robotExplosionPartsRect.move_ip( 0, self._robotExplosionPartsRect.height )
        return spriteParts


    def _load_skin(self, skinName):
        """
            Carrega as mascaras para os robots.
            'skinName' - Nome da mascara.
            
            Retorna uma lista com as imagens carregadas se tudo OK.
            Retorna '-1' se houver problemas.
        """
        try: 
            # Carrega o corpo do robot
            fullname = path.join('data', 'skins', skinName, 'body.png')
            bodyImg = pygame.image.load(fullname).convert_alpha()
            
            # Carrega a arma
            fullname = path.join('data', 'skins', skinName, 'gun.png')
            gunImg = pygame.image.load(fullname).convert_alpha()
            
            # Carrega o radar
            fullname = path.join('data', 'skins', skinName, 'radar.png')
            radarImg = pygame.image.load(fullname).convert_alpha()
            
            # Carrega a skin da bala que é carregada para todas as instancias da classe Bullet
            fullname = path.join('data', 'bullet.png')
            self._bulletImage = pygame.image.load(fullname).convert_alpha()

            return [ bodyImg, gunImg, radarImg ]
            
        except pygame.error, err:
            printe("")
            printe( "Não foi possível carregar a imagem!" )
            printe( "Descrição: " + str(err) )

        return -1


    def _change_color(self, robotColor, imgsList):
        """
        Dáda a cor do robot, pega na skin e faz a transformação para a cor do robot.
        
        'robotColor' - Nova cor da skin. Cor do tipo (R, G, B).
        'imgsList' - Lista com objectos do tipo 'pygame.image' aos quais se quer alterar a cor.
        
        Retorna a nova 'imgsList' com as cores alteradas.  
        """
        for img in imgsList:
            for x in range( img.get_size()[0] ):
                for y in range( img.get_size()[1] ):
                    colorAt = img.get_at( (x, y) )
                    if ( colorAt == (255, 0, 252, 255) ):
                        img.set_at((x, y), robotColor )
        return imgsList


    def _encap_init_positions(self, args = None):
        """
        É encapsulado quando o delay no servidor é terminado. Como argumento vêm as posições iniciais de cada robot.
        
        Formato: [ [robotName, skinName, color, x, y, degrees], [robotName, skinName, color, x, y, degrees]... ]
         Nota: 'color' está no formato (R, G, B)


        Gera a lista de robots do round e desenha pela primeira vez os robots no campo de batalha. 
        """
        printi( "_encap_init_positions(%s)" % args )
        # Transforma a string recebida numa lista
        #init_positions = eval( args[0] )
        init_positions = args
        # Por cada posição inicial
        for position in init_positions :
            # Carrega as imagens do robot
            imgsList = self._load_skin( position[1] )
            # Converte as cores das imagens para a cor do robot
            imgsList = self._change_color( position[2], imgsList )
            # Cria um objecto do tipo 'Robot'
            #Robot(robotName, skinImgs, screen, initPos, initDir)
            self.objectsGroup.append( Robot( position[0], 
                                                   imgsList, 
                                                   self.screen, 
                                                   (position[3], position[4]),
                                                   position[5] ) 
                                          )
    ####################################################################################
    ####################################################################################


    def _remove_bullet( self, bulletID ):
        for object in self.objectsGroup:
            if ( object.get_name() == bulletID ):
                self.objectsGroup.remove( object )
                return


    def _remove_explosion( self, explosionID ):
        for object in self.objectsGroup:
            if ( object.get_name() == explosionID ):
                self.objectsGroup.remove( object )
    
    
    def _encap_bullet_explode( self, args = None ):
        """
        Quando uma bala explode.
        
        - args - [bulletID, (x, y)] 
        """
        x = args[1][0] - ( self._bulletExplosionPartsRect.width / 2 )
        y = args[1][1] - ( self._bulletExplosionPartsRect.height / 2 )
        
        self._remove_bullet( args[0] )
        #explosionID = "explosionb" + str( args[0] )[-1:]
        explosionID = "explosionb" + str( args[0] )
        explosion = Explosion( self.screen, self._bulletExplosionPartsList, explosionID, (x, y) )
        self.objectsGroup.append( explosion )


    def _remove_robot( self, robotName ):
        for object in self.objectsGroup:
            if ( object.get_name() == robotName ):
                self.objectsGroup.remove( object )
                return
        

    def _encap_robot_destroyed( self, args = None ):
        """
        - args:  [ robotName, position ]
        """
        self._set_robot_score_death( args[0] )
        # Adiciona a explosão do robot
        robot = self._objectName_to_object( args[0] )
        x = args[1][0] - ( self._robotExplosionPartsRect.width / 2 )
        y = args[1][1] - ( self._robotExplosionPartsRect.height / 2 )
        
        explosionID = "explosionr" + str( self._robotExplosionID )
        self._robotExplosionID += 1
        explosion = Explosion( self.screen, self._robotExplosionPartsList, explosionID, (x, y) )
        self.objectsGroup.append( explosion )

        self._remove_robot( args[0] )
        

    def _encap_round_started( self, args = None ):
        """
        Metodo que invocado quando o '_round_started' encapsulado é recebido.
        
        - args - Lista com os argumentos. Neste caso é o número do round e a lista com as posições iniciais.  
        """
        # Limpa o grupo de objectos
        self.objectsGroup = []

        roundNum = int( args[ 0 ] )
        self.round = roundNum
        self._encap_init_positions( args[ 1 ] )
        
        # Faz um reset ao ScoreBoard
        for score in self.scoreBoard.scoresList:
            score.reset()

        # Faz reset ao cronometro na barra da janela
        self._chron.reset()
        self.set_time()

        # Aumenta a 'velocidade' do main loop por causa da animação
        self.fps = 45
        self.start_animation()
        

    def _encap_term_battle( self, args = None ):
        """
        Invocado quando a batalha termina. É diferente de quando a sala de jogo é fechada.
        
        """
        printd( "_encap_term_battle(" + str(args) + ')' )
        printd( self.changesQueue.changesList )
        # Volta a indicar que a batalha não está iniciada
        self.started = False
        # Reset ao contador de rounds
        self.round = 0
        # Limpa o grupo de robots
        self.objectsGroup = []
        # Limpa os comandos em buffer
        #self.changesQueue.reset()

        # Termina a animação.
        # Quando a batalha já foi iniciada, isto não é necessário. 
        # Mas quando por algum motivo a batalha é iniciada e segundos depois é terminada com a animação ainda 
        # a correr, é preciso termina-la
        if ( self.showAnimation ):
            self.stop_animation()
        self.fps = 4


    def _encap_term_battle_room( self, args = None ):
        """
        Invocado quando a sala da batalha é fechada.
        """
        printi( "_encap_term_battle_room( " + str(args) + ' )' )
        self.alive = False
        # Reset ao contador de rounds
        self.round = 0
        # Volta a indicar que a batalha não está iniciada
        self.started = False
        # Limpa todos os objectos
        self.objectsGroup = []


    def _encap_kicked_player( self, args = None ):
        """
        - args: robotName
        """
        printi( "_encap_kicked_player(" + str(args) + ')' )
        self._remove_player_score( args )
        self._remove_robot( args )
        
        # Verifica se há jogadores suficientes para iniciarem a batalha e se estão todos prontos
        # com o objectivo de abilitar ou desabilitar o botão de iniciar batalha
        self.check_ready_for_battle()


    def _encap_refresh_dynamic_scores( self, args = None ):
        """
        - args: Lista com a robotEnergy e gunTemp de todos os jogadores.
                Formato: [ [robotEnergy, gunTemp], [robotEnergy, gunTemp], [robotEnergy, gunTemp] ]
        """
        i = 0
        for refresh in args:
            robotEnergy, gunTemp = refresh
            score = self.scoreBoard.get_score_by_pos( i )
            score.refresh_energy( robotEnergy )
            score.refresh_gun_temperature( gunTemp )
            i += 1
        # Actualiza o cronometro no titulo da janela
        self.tictac()


    def _encap_damage( self, args = None ): 
        printd( "_encap_damage(" + str(args) + ')' )
        self._refresh_score_damage( args )


    def _new_bullet( self, bulletID, owner, bulletPosition ):
        bullet = Bullet( bulletID, owner, bulletPosition, self.screen, self._bulletImage )
        self.objectsGroup.append( bullet )
        return bullet

        
    def _is_bullet( self, data ):
        """
        A partir do nome do objecto, verifica se é suposto ser uma bala.
        Quando é uma bala, o nome do objecto é sempre "bulletX" onde "X" é o ID da bala.
        Verifica também o número de campos que a lista ("data") tem, para o caso de um robot ter um nome
        identico. (quando a lista é enviada por um robot, o número de campos difere).
        """
        objectName = data[0]
        if ( (objectName[:6] == "bullet") and (len(data) == 5) ):
            return True
        
        return False


    def _is_bullet_explosion( self, data ):
        """
        Verifica se é uma explusão de uma bala.
        """
        objName = data[0]
        if ( objName == "_bullet_explosion" ):
            return True
        else:
            return False
        

    def _objectName_to_object(self, name):
        """
        Procura na lista de objectos o objecto com o nome indicado e retorna o objecto com o nome correspondente.
        """
        for object in self.objectsGroup:
                objectName = object.get_name()
                if ( name == objectName ):
                    return object
        return -1
    

    def draw_objects_group(self):
        """
        Desenha os objectos no campo de batalha.
        
        Os eventos têm de ter apenas um argumento porque como são recebidos vários eventos e cada um tem o 
        seu numero de argumentos, para dar para todos, os argumentos têm de ser passados dentro de uma lista
        e assim, mesmo sendo vários argumentos, como vão dentro de uma lista é como se fossem só 1 e depois são
        'desencapsulados' dentro da função correspondente.
        """
        commands = {
                    '_round_started': self._encap_round_started,
                    '_term_battle': self._encap_term_battle,
                    '_term_battle_room': self._encap_term_battle_room,
                    '_kicked_by_inactivity': self._encap_term_battle_room,
                    '_kicked_player': self._encap_kicked_player,
                    # Actualização do scoreboard ( gunTemp e robotEnergy )
                    '_rs': self._encap_refresh_dynamic_scores,
                    
                    # Eventos da batalha
                    '_damage': self._encap_damage,
                    '_bullet_explode': self._encap_bullet_explode,
                    '_robot_destroyed': self._encap_robot_destroyed,
                    '_statistics': self._statistics
                    }
        
        changesPerCycle =  self.changesQueue.dequeue()
        printd( "#####################################      INICIO     #####################################" )
        printd( changesPerCycle )
        printd( "############################################################################################" )

        # Por cada movimentação que houve no ciclo
        for cycleChange in changesPerCycle:
            printd( "cycleChange: " )
            printd( cycleChange )
            eventName = cycleChange[ 0 ]
            ########################
            # Verifica se é um evento( _round_started, etc... )
            if ( eventName in commands ):
                commands[ eventName ]( cycleChange[1] )
                continue
            ########################
            object = self._objectName_to_object( eventName )
            isBullet = self._is_bullet( cycleChange )
            # Quando não consegue encontrar o objecto, verifica se o objecto é do tipo 'Bullet'. E caso seja, cria
            # uma nova bala. Se não for, descarta a entrada.
            if ( object == -1 ):
                # Se for uma explosão, não faz nada
                if ( (eventName == "_bullet_explosion") or (eventName == "_robot_explosion") ):
                    pass
                # Se é uma bala e não foi encontrada na lista de objectos é porque é uma nova bala que é preciso criar.
                elif ( isBullet ):
                    # Cria um novo objecto do tipo "Bullet" e adiciona-o à self.objectGroup
                    # [ bulletID, owner, bulletPosition, gunTemperature, robotEnergy ]
                    object = self._new_bullet( cycleChange[0], cycleChange[1], cycleChange[2] )
                    
                # Quando não é encontrado descarta a entrada
                else:
                    printi( "Evento descartado:" )
                    printi( "Descrição: " + str( cycleChange ) )
                    continue
            
            # Quando é uma explusão de uma bala
            #if ( self._is_bullet_explosion( cycleChange ) ):
            #        retVal = object.update()
            #        if ( retVal == -1 ):
            #            self._remove_bullet_explosion( eventName )
            # Como os argumentos são diferentes entre as balas e os robots...
            # Isto tem de ser uniformizado. Mas não esquecer que pelo menos com este mecanismo não podem
            # ter o mesmo numero de argumentos, ou então tem de se criar um campo especifico para o tipo
            # uma vez que basta um robot ter o nome de "bullet" para criar confusão caso os argumentos sejam em 
            # mesma quantidade
            if ( (not isBullet) and ((eventName != "_bullet_explosion") and (eventName != "_robot_explosion")) ):
                x, y = cycleChange[ 1 ]
                roDeg = cycleChange[ 2 ]
                gDeg = cycleChange[ 3 ]
                raDeg = cycleChange[ 4 ]
                
                # Actualiza o objecto com as alterações recebidas
                object.update( x, y, roDeg, gDeg, raDeg )
                
            elif ( (eventName != "_bullet_explosion") and (eventName != "_robot_explosion") ):
                # [ bulletID, owner, bulletPosition, gunTemperature, robotEnergy ]
                # ATENÇÃO QUE ESTE owner É O playerName E NÃO O robotName!
                owner = cycleChange[ 1 ]
                x, y = cycleChange[ 2 ]
                gunTemperature = [ owner, cycleChange[ 3 ] ]
                robotEnergy = [ owner, cycleChange[ 4 ] ]
                self._refresh_score_gun_temperature( gunTemperature )
                self._refresh_score_energy( robotEnergy )
                # AQUI É PARA ACTUALIZAR AS ESTATISTICAS DO OWNER DA BALA E PENSO QUE É SÓ NESTA PARTE.
                # O RESTO QUE FALTA É NOS METODOS 'update' e 'blit' DA CLASSE 'Robot'.
                # Actualiza o objecto com as alterações recebidas
                object.update( x, y )
        # Quando a animação está a correr não desenha mais nada no campo de batalha
        if ( not self.showAnimation ):
            # Desenha todos os objectos
            for object in self.objectsGroup:
                retVal = object.blit()
                # Para as explusões
                # Quando uma explusão chega ao fim, retorna -1
                if ( retVal == -1 ):
                    self._remove_explosion( object.get_name() )
        

    def draw(self):
        # Desenha a imagem de fundo        
        self.screen.blit(self.background, (0,0))
        # Desenha o campo de batalha
        self.screen.blit( self.battleFieldImage, (0, 0) )
        
        # Desenha o ScoreBoars nas coordenadas x e y
        self.screen.blit(self.scoreBoard, self.scoreBoardPos)
        self.scoreBoard.draw()
        
        # Quando a changesQueue não está vazia é sinal que há coisas para fazer e nesse caso é preciso para a animação
        if ( (len(self.changesQueue) > 0) and self.showAnimation ):
            self.stop_animation()
            self.fps = 25 # Utilizado pelo Clock.tick() no mainloop

        #Quando 'True', mostra a animação
        if ( self.showAnimation ):
            self._animation.draw()

        # Mesmo que a changes_queue esteja vazia é preciso escrever os objectos na batalha porque pode não haver 
        # alterações mas pode haver coisas para escrever.
        self.draw_objects_group()
        pygame.display.flip()
            

    #############################################################################
    def start_animation(self):
        """
        Mostra no campo de batalh a animação que a batalha está a iniciar.
        """
        self._animation = TextFadeAnimation( self.screen, ((self.battleFieldRect[ 2 ] / 2), (self.battleFieldRect[ 3 ] / 2)), self.transDict[ 'animText' ] + ' ' + str(self.round) )
        self.showAnimation = True
        

    def stop_animation(self):
        """
        Pára a animação.
        """
        self.showAnimation = False


    def _refresh_score_damage( self, stats ):
        playerName = stats[ 0 ]
        armor = stats[ 1 ]
        damage = stats[ 2 ]
        score = self.scoreBoard.get_score( playerName )
        score.refresh_armor( armor )
        score.refresh_damage( damage )


    def _refresh_score_gun_temperature( self, stats ):
        playerName = stats[ 0 ]
        gunTemperature = stats[ 1 ]
        score = self.scoreBoard.get_score( playerName )
        score.refresh_gun_temperature( gunTemperature )



    def _refresh_score_energy( self, stats ):
        playerName = stats[ 0 ]
        energy = stats[ 1 ]
        score = self.scoreBoard.get_score( playerName )
        score.refresh_energy( energy )


    def _set_robot_score_death( self, robotName ):
        score = self.scoreBoard.get_score( robotName )
        score.set_death()


    ########################################################################################
    def _sort_by_accuracy( self, scoreList ):
        """
        Ordena por pontaria
        """
        # Lista que vai ser retornada com os scores ordenados
        retList = []
        # Primeiro ordena por pontaria
        for score in scoreList:
            i = len( retList )
            for entry in retList:
                if ( score[8] > entry[8] ):
                    i = retList.index( entry )
                    break
            retList.insert( i, score )
        return retList


    def _calc_damage_ratio( self, damage1, damage2 ):
        """
        damage1 e damage2 são listas: [causado, sufrido]
        """
        if ( not (damage1[1] == 0) and  not (damage2[1] == 0) ):
            return ( damage1[0]/damage1[1], damage2[0]/damage2[1] )
        elif ( (damage1[1] == 0) and (damage2[1] == 0) ):
            return ( damage1[0], damage2[0] )
        else:
            """
            50 / 0 -> 50 / 2
            200 / 10
            
            (200 - 10)  > 50
            """
            if ( 0 in damage1 ):
                return (  damage1[0], (damage2[0] - damage2[1])  )
            else:
                return (  (damage1[0] - damage1[1]), damage2[0]  )


    def _sort_by_damage( self, scoreList ):
        """
        Ordena por relação de estragos causados/sufridos
        """
        # Lista que vai ser retornada com os scores ordenados
        retList = []
        # Guarda os empates
        rawList = []
        subRawList = []
        # Primeiro ordena por estragos
        for score in scoreList:
            i = len( retList )
            for entry in retList:
                damage1, damage2 = self._calc_damage_ratio( [score[3], float(score[4])], [entry[3], float(entry[4])] )
                if ( damage1 > damage2 ):
                    i = retList.index( entry )
                    break
            retList.insert( i, score )
    
        #########   Procura empates    ##########
        for i in xrange( 0, len(retList) - 1 ):
            damage1, damage2 = self._calc_damage_ratio( [retList[i][3], float(retList[i][4])], [retList[ i + 1][3], float(retList[ i + 1][4])] )
            if ( damage1 == damage2 ):
                subRawList.append( retList[i] )
            elif ( subRawList != [] ):
                subRawList.append( retList[i] )
                rawList.append( subRawList )
                subRawList = []
        # Para quando chega ao final da lista   
        if ( subRawList != [] ):
            subRawList.append( retList[i + 1] )
            rawList.append( subRawList )
        
        retList.append( rawList )
        return retList

        
    def _calc_deaths_ratio( self, deaths1, deaths2 ):
        """
        deaths1 e deaths2 são listas: [destuidos, destruido]
        """
        if ( not (deaths1[1] == 0) and  not (deaths2[1] == 0) ):
            return ( deaths1[0]/deaths1[1], deaths2[0]/deaths2[1] )
        elif ( (deaths1[1] == 0) and (deaths2[1] == 0) ):
            return ( deaths1[0], deaths2[0] )
        else:
            if ( 0 == deaths1[1] ):
                return (  deaths1[0], (deaths2[0] - deaths2[1])  )
            else:
                return (  (deaths1[0] - deaths1[1]), deaths2[0]  )
    
    
    def _sort_by_deaths( self, scoreList ):
        """
        Ordena por relação entre destruido e destruidos.
        """
        # Lista que vai ser retornada com os scores ordenados
        retList = []
        # Guarda os empates
        rawList = []
        subRawList = []
    
        # Primeiro ordena por mortes
        for score in scoreList:
            i = len( retList )
            for entry in retList:
                deaths1, deaths2 = self._calc_deaths_ratio( [score[1], float(score[2])], [entry[1], float(entry[2])] )
                if ( deaths1 > deaths2 ):
                    i = retList.index( entry )
                    break
            retList.insert( i, score )
        
        #########   Procura empates    ##########
        for i in xrange( 0, len(retList) - 1 ):
            deaths1, deaths2 = self._calc_deaths_ratio( [retList[i][1], float(retList[i][2])], [retList[ i + 1][1], float(retList[ i + 1][2])] )
            if ( deaths1 == deaths2 ):
                subRawList.append( retList[i] )
            elif ( subRawList != [] ):
                subRawList.append( retList[i] )
                rawList.append( subRawList )
                subRawList = []
        # Para quando chega ao final da lista   
        if ( subRawList != [] ):
            subRawList.append( retList[i + 1] )
            rawList.append( subRawList )
        
        retList.append( rawList )
        return retList


    def _sort_by_points( self, scoreList ):
        """
        Ordena por número de pontos.
        """
        # Lista que vai ser retornada com os scores ordenados
        retList = []
        # Guarda os empates
        rawList = []
        subRawList = []
        
        # Primeiro ordena por pontuação
        for score in scoreList:
            i = len( retList )
            for entry in retList:
                if ( score[9] > entry[9] ):
                    i = retList.index( entry )
                    break
            retList.insert( i, score )

        #########   Procura empates    ##########
        for i in xrange( 0, len(retList) - 1 ):
            if ( retList[i][9] == retList[ i + 1][9] ):
                subRawList.append( retList[i] )
            elif ( subRawList != [] ):
                subRawList.append( retList[i] )
                rawList.append( subRawList )
                subRawList = []
        # Para quando chega ao final da lista   
        if ( subRawList != [] ):
            subRawList.append( retList[i + 1] )
            rawList.append( subRawList )
        
        retList.append( rawList )
        return retList
        

    def _sort( self, roundsList ):
        """
        Ordena por ordem de melhor pontuação scores dentro da roundsList.
        
        - robotName, deaths, damageCaused, damage, totalShots, goodShots, accuracy, totalPoints
        roudnGrid - [   ['Robô1', 1, 0, 2, 3, 4, 5, 600, 0, 1.0], ['Robô2', 0, 1, 0, 0, 3, 0, Decimal(0.04), 1, 0.0], ['Robot Com Nome Grand', 0, 0, 0, 15, 0, 0, 0, 2, 0.8]    ]
        
        [['Robo1', 1, 100, 200, 3, 4, 5, 600, 60, 3.0],
        ['Robo2', 2, 250, 200, 3, 4, 5, 600, 0, 3.0],
        ['Robo3', 1, 100, 200, 3, 4, 5, 600, 40, 3.0],
        ['Robo4', 1, 400, 200, 3, 4, 5, 600, 0, 3.0],
        ['Robo5', 4, 100, 200, 3, 4, 5, 600, 0, 2.0],
        ['Robo6', 3, 100, 200, 3, 4, 5, 600, 0, 2.0],
        ['Robo7', 5, 100, 200, 3, 4, 5, 600, 0, 1.0]     ]
        """
        ######################################     Ordena por pontos      ###################################################
        sortedPoints = self._sort_by_points( roundsList )
        # Lista que guarda os empates de pontos que têm de ser desempatadas com o número de mortes ou relação entre estragos causados e sufridos
        # Formato [ score1, score2, socreX, rawList ]
        pointsRawList = sortedPoints.pop()
        ###########################    Ordena por mortes caso haja empates por pontos     #############################
        # Primeiro vê quais os scores empatados por pontos
        if ( pointsRawList != [] ):
            for raw in pointsRawList:
                pointer = sortedPoints.index( raw[0] )
                sortedDeaths = self._sort_by_deaths( raw )
                deathsRawList = sortedDeaths.pop()
                for itemIndex in xrange( len(sortedDeaths) ):
                    sortedPoints.pop( pointer )
                    sortedPoints.insert( pointer, sortedDeaths[itemIndex] )
                    pointer += 1
                    
                ############    Ordena por relação danos causados/danos sufridos caso haja empates por mortes    #############
                if ( deathsRawList != [] ):
                    for raw in deathsRawList:
                        pointer = sortedPoints.index( raw[0] )
                        sortedDamage = self._sort_by_damage( raw )
                        damageRawList = sortedDamage.pop()
                        for itemIndex in xrange( len(sortedDamage) ):
                            sortedPoints.pop( pointer )
                            sortedPoints.insert( pointer, sortedDamage[itemIndex] )
                            pointer += 1
                        
                        ############    Ordena por pontaria caso haja empates por estragos    #############
                        if ( damageRawList != [] ):
                            for raw in damageRawList:
                                pointer = sortedPoints.index( raw[0] )
                                sortedAccuracy = self._sort_by_accuracy( raw )
                                for itemIndex in xrange( len(sortedAccuracy) ):    
                                    sortedPoints.pop( pointer )
                                    sortedPoints.insert( pointer, sortedAccuracy[itemIndex] )
                                    pointer += 1
                    
        return sortedPoints
    ########################################################################################
    
        
    def _calc_accuracy( self, gridList, score ):
        """
         - gridList - Lista com as estatisticas de todos os rounds.
        """
        retVal = 0
        totalGoodShots = 0
        totalShots = 0
        
        for round_ in gridList:
            for s in round_:
                if ( s[0] == score[0] ):
                    # s = [robotName1, kills, deaths, damageCaused, damage, totalShots, goodShots, winner, totalScore]
                    totalShots += s[5]
                    totalGoodShots += s[6]

        if ( totalShots > 0 ):
            retVal = str(   round( (float(totalGoodShots * 100) / float(totalShots)), 2 )   )
        else:
            return 0
            
        return retVal


    def _get_index( self, robotName, gridList ):
        """
        Retorna  posição do robot na lista ou se não encontra retorna None.
        """
        for robot in gridList:
            if ( robot[0] == robotName ):
                return gridList.index( robot )
        return None
    
    
    def _get_user_oriented( self, gridList ):
        """
        Retorna as estatisticas orientadas ao robot. Ou seja, uma linha por cada robot ( com a soma de todos os rounds).
        r = [   [ ["robot1", 10, 0, 10, 10, 10, 10, 10, 10, 10], ["robot2", 20, 0, 20, 20, 20, 20, 20, 20, 20] ], [ ["robot2", 10, 0, 20, 30, 40, 50, 60, 70, 80], ["robot1", 1, 0, 2, 3, 4, 5, 6, 7, 8] ]    ]
        
        [ robotName1, kills, deaths, damageCaused, damage, totalShots, goodShots, accuracy, winner, totalScore ]
        """
        #from decimal import Decimal, getcontext
        roundCounter = 0
        i = 0
        __gridList = []
        for round_ in gridList:
            for robot in round_:
                i = self._get_index( robot[0], __gridList )
                # Quando é none é porque está a carregar o primeiro round e a lista ainda está vazia
                # Quando assim é, utiliza a ordem do round
                if ( i == None ):
                    i = round_.index( robot )
                    __gridList.append([robot[0], 0, 0, 0, 0, 0, 0, [], "-", 0])
                # kills
                __gridList[ i ][ 1 ] += robot[ 1 ]
                # kills
                __gridList[ i ][ 2 ] += robot[ 2 ]
                # damageCaused
                __gridList[ i ][ 3 ] += robot[ 3 ]
                # damage
                __gridList[ i ][ 4 ] += robot[ 4 ]
                # totalShots
                __gridList[ i ][ 5 ] += robot[ 5 ]
                # goodShots
                __gridList[ i ][ 6 ] += robot[ 6 ]
                # accuracy
                #__gridList[ i ][ 7 ].append( robot[ 7 ] )
                # won
                # Quando igual a 1 significa que ganhou este round
                if ( robot[ 8 ] != 0 ):
                    if ( __gridList[ i ][ 8 ] == "-" ):
                        __gridList[ i ][ 8 ] = str( roundCounter + 1 )
                    else:
                        __gridList[ i ][ 8 ] += "/" + str( roundCounter + 1 )
                # totalScore 
                __gridList[ i ][ 9 ] += float( robot[9] )
            # 
            roundCounter += 1
        
        for score in __gridList:
            # Calcula a pontaria media
            score[ 7 ] = self._calc_accuracy( gridList, score )
            # Calcula a pontuação total
            score[ 9 ] = str(  round((float(score[9]) / roundCounter), 2)  )

        return __gridList


    def _statistics( self, args = None ):
        """
        args = [   [ ["robot1", 0, 1, 50, 100, 20, 6, 0, 0, 0], ["robot2", 1, 0, 90, 100, 100, 6, 0, 0, 0] ]    ]
        """
        # Faz uma pequena pausa antes de mostrar as estatisticas
        sleep(2)
        # Indica que a batalha terminou
        self.started = False
        gridList = self._get_user_oriented( eval(args) )
        alive = True
        clock = pygame.time.Clock()
        TIMER = 5
        counter = time()
        elapsed = 0
        #
        grid = Grid( self.screen )
        gridListSorted = self._sort( gridList )
        grid.create( gridListSorted , self.battleName )
        # Faz o primeor keepalive
        self._keepalive()
        while  alive:
            for event in pygame.event.get():
                alive = grid.events_handler( event )
            # keepalive
            elapsed = time() - counter
            if ( elapsed >= TIMER ):
                self._keepalive()
                counter = time()

            pygame.display.flip()
            grid.draw()
            clock.tick(4)

        self._config_window()
        return 0




