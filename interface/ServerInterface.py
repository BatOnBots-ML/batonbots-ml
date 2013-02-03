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

"""
Descrição: Responsável por toda a comunicação entre o robot e o servidor.
"""


import pygtk
pygtk.require('2.0')
import select
import socket
import re
from time import time
import zlib, base64

import pygame

from battle.battleRoom import BattleRoom
from EventsBox import EventsBox
from log.logging_mod import Logging
log = Logging()
printd = log.debug
printi = log.info
printe = log.error
printw = log.warning






class ServerInterface():

    def __init__(self):
        ## Comandos começados por '_', é o servidor que envia
        ## Comandos NÃO começados por '_', é o robot que envia
        self._commandsDic = {
                            'exec_mode': self._set_exec_mode, # Configura o modo de execução dos comandos. Ex.: Lock/Block/Non-Lock
                            'execute': self._execute, # Comando que dá a ordem para executar os comandos na stack, quando se está a utilizar o modo 'block'.
                            
                            'robot_move_forward': self._robot_move_forward,
                            'robot_move_backward': self._robot_move_backward,
                            'robot_turn_right': self._robot_turn_right,
                            'robot_turn_left': self._robot_turn_left,
                            'robot_turn_to': self._robot_turn_to,
                            
                            'gun_turn_right': self._gun_turn_right,
                            'gun_turn_left': self._gun_turn_left,
                            'gun_turn_to': self._gun_turn_to,
                            'shoot': self._shoot,
                            
                            'radar_turn_right': self._radar_turn_right,
                            'radar_turn_left': self._radar_turn_left,
                            'radar_turn_to': self._radar_turn_to,
                            
                            'set_speed': self._set_speed,
                            'scan': self._scan,
                            'advanced_scan': self._advanced_scan,
                            'no_freeze_on': self._no_freeze_on,
                            'freeze_on': self._freeze_on,
                            'subscribe_events': self._subscribe_events,
                            'unsubscribe_events': self._unsubscribe_events,
                            'noop': self._noop,
                            'stop': self._stop,
                            'lock_gun_on_robot': self._lock_gun_on_robot,
                            'lock_radar_on_robot': self._lock_radar_on_robot,
                            'lock_gun_on_radar': self._lock_gun_on_radar,


                            #'_server_ready': self._set_server_ready, # Altera o estado do servidor para 'Ready'. Indica que pode receber comandos
                            '_term_battle_room': self._term_battle_room, # É enviado quando a sala da batalha é terminada
                            '_term_battle': self._term_battle, # É enviado quando a batalha é terminada
                            '_kicked_player': self._kicked_player, # Quando um jogador é kickado. Traz o nome do jogador que foi kicked para se poder actualizar o ScoreBoard
                            '_joined_player': self._joined_player, # Quando um jogador entra na batalha
                            # Indica ao jogador que não foi possível entrar na batalha porque ele já esta numa batalha
                            '_join_fail': self._join_fail,
                            # Recebe o nome do jogador e o seu estado ('player_ready' ou 'player_not_ready'). Serve para o ScoreBoard
                            '_player_status': self._set_player_status,
                            # Falg que indica que está a ser enviada uma lista com o perfil dos jogadores que estão
                            # na batalha onde o jogador entrou
                            '_players_list': self._players_list,
                            # Flag que indica que a sala em que o jogador tentou entrar está cheias
                            '_full_battle': self._full_battle,
                            # Flag que indica que o nome da batalha que se está a tentar criar
                            # já existe.
                            '_repeated_battle_name': self._repeated_battle_name,
                            # Quando o jogador tenta entrar numa batalha que j+a não existe
                            '_battle_doesnt_exist': self._battle_doesnt_exist,
                            # Flag que indica que está a ser enviada uma lista com as salas 
                            # de batalha disponiveis
                            '_battles_list': self._battles_list,
                            # Informa o jogador das alterações ocorridas a cada ciclo no campo de batalha
                            '_refresh_battle_picture': self._refresh_battle_picture,
                            # É recebido quando o robot excede o número máximo de comandos por segundo.
                            # Não é enviado para o robô. Serve apenas como debug
                            '_sov': self._sov,


                            ###  GetCommands  ### Enviados pelo robô
                            'get_robot_position': self.get_robot_position,
                            'get_bf_size': self.get_bf_size,
                            'get_speed': self.get_speed,
                            'get_seq_num': self.get_seq_num,
                            "get_robot_dir": self.get_robot_dir,
                            "get_gun_dir": self.get_gun_dir,
                            "get_radar_dir": self.get_radar_dir,
                            'get_exec_mode': self.get_exec_mode,
                            'get_robots': self.get_robots,
                            'get_alive_robots': self.get_alive_robots,
                            'get_energy': self.get_energy,
                            'get_damage': self.get_damage,
                            'get_armor': self.get_armor,
                            'get_gun_temp': self.get_gun_temp,
                            'get_round': self.get_round,
                            'get_round_time': self.get_round_time,
                            'get_rounds_num': self.get_rounds_num,
                            'get_elapsed_time': self.get_elapsed_time,
                            'get_no_freeze_on': self.get_no_freeze_on,
                            'get_subscribed_events': self.get_subscribed_events,
                            'get_commands_queue': self.get_commands_queue,
                            'ping': self.ping,
                            'get_gun_lock': self.get_gun_lock,
                            'get_radar_lock': self.get_radar_lock,
                            
                            ###  GetCommands  ### Resposta do servidor
                            '_get_robot_position': self._get_robot_position,
                            '_get_bf_size': self._get_bf_size,
                            '_get_speed': self._get_speed,
                            '_get_seq_num': self._get_seq_num,
                            "_get_robot_dir": self._get_robot_dir,
                            "_get_gun_dir": self._get_gun_dir,
                            "_get_radar_dir": self._get_radar_dir,
                            '_get_exec_mode': self._get_exec_mode,
                            '_get_robots': self._get_robots,
                            '_get_alive_robots': self._get_alive_robots,
                            '_get_energy': self._get_energy,
                            '_get_damage': self._get_damage,
                            '_get_armor': self._get_armor,
                            '_get_gun_temp': self._get_gun_temp,
                            '_get_round': self._get_round,
                            '_get_round_time': self._get_round_time,
                            '_get_rounds_num': self._get_rounds_num,
                            '_get_elapsed_time': self._get_elapsed_time,
                            '_get_no_freeze_on': self._get_no_freeze_on,
                            '_get_subscribed_events': self._get_subscribed_events,
                            '_get_commands_queue': self._get_commands_queue,
                            '_ping': self._ping,
                            '_get_gun_lock': self._get_gun_lock,
                            '_get_radar_lock': self._get_radar_lock
                        }
        
        
        # Comandos de controlo são comandos que são enviados pelo robot mas que não são passados para o servidor.
        # Logo não vão para a stack e têm de ser tratados de forma diferente. Isto não é verdade para o 'exec_mode'!!
        self.controlCommands = [ 'exec_mode', 'execute' ]

        # Indica ao servidor que vai sair da batalha
        self.LEAVE_BATTLE = 'leave_battle'
        # Utilizado para cancelar a entrada numa batalha.
        # Quando o jogador entra numa batalha com password e depois de tentar entrar não mete password, envia esta flag
        self.CANCEL_JOIN = 'cancel_join'
        # Flag enviada ao servidor para iniciar a batalha
        self.START_BATTLE = 'start_battle'
        # Serve para indicar ao robot que houve um problema com o comando enviado
        # Argumentos:
        # - 'not_sent': indica ao robot que por algum motivo o comando não poude ser enviado ao servidor    
        self.ERROR = 'error'
        # Serve para enviar ao robot a informação de que pode continuar quando está a utilizar 
        # os modos de execução 'block' e 'non-lock'
        self.DONE = 'done'
        # Timeout para o 'select()' do 'main_loop()'
        self.SELECT_TIMEOUT = 0
        # Intervalo em que é feito o keepalive. Em segundos.
        self.TIMER = 5
        # É enviado pelo servidor para indicar se esta pronto para aceitar comandos ou não.
        # Dá também o sinal para o inicio da batalha pela primeira vez que é colocado a True
        self.serverReadyFlag = 'server_ready'
        
        # Flag enviada ao servidor quando está pronto para iniciar a batalha
        self.playerReadyFlag = 'player_ready'
        # Flag enviada ao servidor quando está pronto para iniciar a batalha
        self.playerNotReadyFlag = 'player_not_ready'
        
        # keepalive
        self._KEEPALIVE = "hello"

        # IP do servidor do simulador de jogo
        self.serverIP = 'batonbots-ml.dyndns-server.com'
        
        # Porta do servidor
        self.serverPort = 58080
        # Tempo maximo para timeout do socket de interface
        self.INTERFACE_SOCK_TIMEOUT = 15
        # 10K
        self.BUFFER_SIZE = 10240 
        #
        self.EOL = "\r\n"

        # Host local
        self.HOST = '127.0.0.1'
        # Porta local
        self.PORT = 48080
        # Tempo maximo para timeout no socket local
        #self.LOCAL_SOCK_TIMEOUT = 5
        self.BACKLOG = 5
        # Indica em que modo o robot vai funcionar(lock mode, block mode, non-lock mode) 
        self.execMode = "lock"
        
        # Lista de comandos que estão pendentes de envio para o servidor
        self.commandStack = []
        # Número máximo de comandos que a 'self.commandStack' pode ter ao mesmo tempo
        # Convém que seja igual ao que está no servidor, caso contrário o resultado mais provável é um kick do robot
        ################### TEM DE SER IGUAL AO self.maxSize DO MODULO command_queue    ###################
        self.maxStackSize = 5
                


        # Socket para receber conexões dos robot's
        self.localSock = None
        # Socket para o servidor
        self.interfaceSock = None
        # Socket para o robot
        self.robotSock = None
        
        # Cria uma instância da sala de jogo
        self.battleRoom = BattleRoom( self.keepalive )

        # Utilizado para manter as FPS certos durante a batalh no main_loop
        self.clock = pygame.time.Clock()


        # Lista com o nome de todos os comandos considerados 'GetCommands'
        # Como o nome começado por _ são enviados pelo servidor. Os outros é pelo robô
        self._getCommands = [
                            "get_robot_position",
                            "_get_robot_position",
                            "get_bf_size",
                            "_get_bf_size",
                            "get_speed",
                            "_get_speed",
                            "get_seq_num",
                            "_get_seq_num",
                            "get_robot_dir",
                            "_get_robot_dir",
                            "get_gun_dir",
                            "_get_gun_dir",
                            "get_radar_dir",
                            "_get_radar_dir",
                            "get_exec_mode",
                            "_get_exec_mode",
                            "get_robots",
                            "_get_robots",
                            "get_alive_robots",
                            "_get_alive_robots",
                            "get_energy",
                            "_get_energy",
                            "get_damage",
                            "_get_damage",
                            "get_armor",
                            "_get_armor",
                            "get_gun_temp",
                            "_get_gun_temp",
                            "get_round",
                            "_get_round",
                            "get_round_time",
                            "_get_round_time",
                            "get_rounds_num",
                            "_get_rounds_num",
                            "get_elapsed_time",
                            "_get_elapsed_time",
                            "get_no_freeze_on",
                            "_get_no_freeze_on",
                            "get_subscribed_events",
                            "_get_subscribed_events",
                            "get_commands_queue",
                            "_get_commands_queue",
                            "ping",
                            "_ping",
                            "get_gun_lock",
                            "_get_gun_lock",
                            "get_radar_lock",
                            "_get_radar_lock"
                            ]
        
        # Queue que guarda os eventos recebidos enquanto o robô está à espera da resposta de um
        # 'GetCommand'
        self._eventsQueue = []
        # Flag que indica se o interface está a tratar de um 'GetCommand'
        self._waitingGet = False
        # Quando True indica que é para fazer o keepalive
        self._keepaliveFlag = True
        #
        self._serverTmpData = ''
        self._robotTmpData = ''
        
        # Eventos
        self._eventsBox = EventsBox()
        

        
        



    def keepalive( self ):
        retVal = self.send_to_server( self._KEEPALIVE )
        if ( retVal == -1 ):
            return False
        return True


    def shutdown(self):
        # O interface pode ser fechado sem ter iniciado os sockets
        if (self.localSock != None):
            printi("A fechar sockets...")
            try:
                self.localSock.close()
                del self.localSock
                self.localSock = None
                
                self.interfaceSock.close()
                del self.interfaceSock
                self.interfaceSock = None
                
                
                # Verifica se este socket ja foi criado
                if (self.robotSock != None):
                    self.robotSock.close()
                    del self.robotSock
                    self.robotSock = None
    
            except Exception, err:
                printe("Ocorreu um erro em 'shutdown()'.")
                printe("Descrição: " + str(err))
                return -1
    
        return 0




    def create_sockets(self):
        # Cria o socket local
        try:
            printi("A criar socket local...")
            self.localSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.localSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #self.localSock.settimeout(self.LOCAL_SOCK_TIMEOUT)
        except socket.error, err:
            printe("Erro ao criar socket local A terminar...")
            printe("Descrição: " + str(err))
            return -1

        try:
            self.localSock.bind((self.HOST, self.PORT))
            self.localSock.listen(self.BACKLOG)
            printi("Socket local a trabalhar na porta " + str(self.PORT))
        except socket.error, err:
            printe("Erro ao tentar trabalhar na porta " + str(self.PORT))
            printe("Descrição: " + str(err))
            return -1


        # Cria o socket para comunicação com o servidor
        try:
            printi("A criar socket de interface...")
            self.interfaceSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.interfaceSock.settimeout(self.INTERFACE_SOCK_TIMEOUT)
        except socket.error, err:
            printe(" ")
            printe("Erro ao criar socket de interface!")
            printe("Descrição: " + str(err))
            return -1

        printi("Sockets criados com sucesso!")
        return 0



    def accept_robot(self):
        """
            - Termina ligações e limpa registos de algum robot anterior que possa ter estado ligado.
            - Espera por uma nova conexão local do robot.
            - Depois de receber a nova ligação, actualiza a lista de socket com o novo socket.
        """
        try:
            # Procura, e se existir, retira da lista o socket antigo do robot
            #for sock in self.sockets:
            #    if (sock == self.robotSock):
            #        self.sockets.remove(self.robotSock)
                    # Fecha o socket do antigo robot
            #        self.robotSock.close()
            
            printi("À espera do robot...")
            # Recebe a nova ligação
            robot = self.localSock.accept()
            # Guarda o socket de cliente
            self.robotSock = robot[0]
            
            # Adiciona à lista o novo socket do robot
            self.sockets.append(self.robotSock)
            
        except socket.error, err:
            printe(" ")
            printe("Ocorreu um erro em 'accept_robot()'.")
            printe("!!! Descrição: " + str(err))
            return -1
        
        printi("Robot online!")
        # Informa o Servidor que o jogador está pronto.
        result = self.player_ready()
        
        if (result != 0):
            printe("Ocorreu um erro durante a actualização do estado do jogador no servidor.")
            printe("É necessario desconectar o robot do interface e voltar a conecatar.")
            
            return -1
        
        return 0



    def conn_to_srv(self):
        """
        Conecta ao servidor onde esta o simulador.
        """
        try:
            printi("A conectar ao servidor...")
            self.interfaceSock.connect((self.serverIP, self.serverPort))
            printi( "Conectado!" )
            
        except socket.error, err:
            printe("Não foi possível estabelecer uma conexão com o servidor!")
            printe("Descrição: " + str(err))
            printe("IP do servidor: " + str(self.serverIP))
            printe("Porto do servidor: " + str(self.serverPort))
            return -1
        
        except socket.timeout:
            printe("Timeout! Não foi possível estabelecer conexão com o servidor!")
            return -1

        return 0


    def send_to_server(self, data):
        try:
            self.interfaceSock.send( str(data) + self.EOL )
            return 0
        except socket.error, err:
            printe("")
            printe("Serverinterface.send_to_server  ***  A informação não foi enviada.")
            printe("Descrição: " + str(err))

            return -1


    def recv_from_server(self):
        try:
            data = self.interfaceSock.recv( self.BUFFER_SIZE )
            return data
        except socket.error, err:
            printe("")
            printe("Ocorreu um erro em 'recv_from_server()'")
            printe("Descrição: " + str(err))

            return -1


    def _send_to_client(self, data):
        try:
            self.robotSock.send( str(data) + self.EOL )
            return 0
        except socket.error, err:
            printe("")
            printe("Ocorreu um erro em '_send_to_client()'")
            printe("Descrição: " + str(err))

            return -1


    def _recv_from_client(self):
        try:
            data = self.robotSock.recv(self.BUFFER_SIZE)
            printd("Recebeu do cliente: %r" % (data + self.EOL))
            return data
        except socket.error, err:
            printe("")
            printe("Ocorreu um erro em '_recv_from_client()'")
            printe("Descrição: " + str(err))

            return -1


    def player_ready(self):
        """
        Diz ao servidor que o cliente está pronto para iniciar uma batalha.
        """
        return self.send_to_server(self.playerReadyFlag)
    
    
    def flush_socket( self ):
        try:
            inputReady, outputReady, exceptReady = select.select( [self.interfaceSock], [], [], 0 )
            printd( "Flushing..." )
            for s in inputReady:
                data = s.recv( 10240 )
                printd("lixo: " + str(data))
            return 0
        except socket.error, err:
            printe("Ocorreu um erro em 'flush_socket()'")
            printe("Descrição: " + str(err))
            return -1


    def player_not_ready(self):
        """
        Diz ao servidor que o jogador não está pronto para iniciar uma batalha.
        """
        return self.send_to_server(self.playerNotReadyFlag)


    def _profile_ok(self, profile):
        """
        Verifica se a informação enviada pelo cliente, não estão fora dos parametros.
        * O perfil tem de obedecer a (r"([a-zA-Z0-9_]{1,20})\:([a-zA-Z0-9_]{1,20})\r\n$")
        """
        r = re.compile(r"([a-zA-Z0-9_]{1,20})\r\n$")

        if (r.match(profile) != None):
            return True
        else:
            return False


    def wath_socket(self, sock):
        if (sock == self.robotSock):
            return 'clientSock'
        else:
            return 'interfaceSock'


    def event_handler(self):
        """
        Controla os eventos do pygame. 
        """
        # NO WINDOWS, SE NÃO TIVER o 'pygame.event.get()', BLOQUEIA A JANELA!!!!
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.send_to_server(self.LEAVE_BATTLE)
                self.battleRoom.alive = False
            
            # Verifica se é um 'left-click'
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
                self.battleRoom.scoreBoard.buttonStartBattle.clicked(event)
                #self.battleRoom.scoreBoard.buttonStartBattle.sensitive( False )


    def _sync_data( self, data, who ):
        if ( who == "server" ):
            _tmpData = self._serverTmpData
        if ( who == "robot" ):
            _tmpData = self._robotTmpData
            
        
        if ( (data[ -2 : ] != self.EOL) and (data != '') ):
            if ( _tmpData == '' ):
                splited = data.split( self.EOL )
                _tmpData = splited.pop()
                data = data[ :-len(_tmpData) ]
            
            else:
                splited = data.split( self.EOL )
                _tmpData += splited[0]
                data = data[ len(splited[0]): ]
                data = _tmpData + data
                
                splited = data.split( self.EOL )
                _tmpData = splited.pop()
                # Tem o IF para quando recebe o comando e só falta o '\r' e quando o recebe vem apenas o '\r' sem mais nada a seguir.
                # É pouco provável mas nunca se sabe...
                if len(_tmpData) > 0 : data = data[ :-len(_tmpData) ]
    
        else:
            if ( _tmpData != '' ):
                data = _tmpData + data
                _tmpData = ''
    
        if ( who == "server" ):
            self._serverTmpData = _tmpData
        if ( who == "robot" ):
            self._robotTmpData = _tmpData
            
        return data

    
    def _update(self):
        self.battleRoom.draw()
        # NO WINDOWS, SE NÃO TIVER o 'pygame.event.get()', BLOQUEIA A JANELA!!!!
        self.event_handler()

        # Controla a velocidade do main_loop
        self.clock.tick(self.battleRoom.fps)


    def main_loop(self):
        # Configura o eventos que devem aparecer na queue
        pygame.event.set_allowed( None )
        pygame.event.set_allowed( pygame.QUIT )
        pygame.event.set_allowed( pygame.MOUSEBUTTONDOWN )
        
        # Só configura o callback para o botão de iniciar batalha se o jogador local for o owner da batalha
        if (self.battleRoom.get_owner()):
            self.battleRoom.scoreBoard.buttonStartBattle.set_callback( self.start_battle )
        
        # Inicia o contador de tempo passado
        self.battleRoom.eTime = time()
        #
        self.commandStack = []
        
        self.sockets = [ self.localSock, self.interfaceSock ]
        self.battleRoom.alive = True
        self.tmpData = ''
        
        # keepalive
        elapsed = 0
        counter = time()
        # Faz o primeiro keepalive
        self._keepaliveFlag = True
        self.keepalive()
        
        while ( self.battleRoom.alive ):
            try:
                inputReady, outputReady, exceptReady = select.select( self.sockets, [], [], self.SELECT_TIMEOUT )                
                # Verifica se existe alguma coisa para ler
                for sock in inputReady:
                    # O "self.localSock" é o socket que recebe as conexões dos robots
                    if ( sock == self.localSock ):
                        # Recebe a nova conexão do robot
                        result = self.accept_robot()
                        if (result != 0):
                            self.battleRoom.alive = False
                            break
                        
                        # Limpa a stack de comandos porque pode ter comandos da conexão anterior
                        self.commandStack = []
                        # Faz reset ao modo de execução
                        self.execMode = "lock"

                    # Os outros sockets
                    else:
                        data = sock.recv(self.BUFFER_SIZE)
                        printd("Recebeu: %r" % data)

                        if (data != ''):
                            # Controla o socket do robot
                            if (sock == self.robotSock):
                                ######################################################
                                data = self._sync_data( data, "robot" )
                                if (data == ''):
                                    self._update()
                                    continue
                                ######################################################
                                
                                result = self.control_robot( data )
                                printd("result do control_robot: %s" % str(result))
                                if (result == -1):
                                    printw("!!! ServerInterface.control_robot() retornou algo errado.")
                                    printw("!!! Descrição: " + str(result))
                                    #self.battleRoom.alive = False
                                    # Termina a ligação com o robot
                                    self.robotSock.close()
                            
                            # Controla o socket do interface
                            elif (sock == self.interfaceSock):
                                ######################################################
                                data = self._sync_data( data, "server" )
                                if (data == ''):
                                    self._update()
                                    continue
                                ######################################################
                                self.control_server( data )
                        # Quando um dos sockets é fechado    
                        else:
                            # Quando a ligação com o robot é terminada normalmente
                            if (sock == self.robotSock):
                                printi("!!! A conexão com o Robot foi terminada.")
                                
                                # Retira o socket do robot da lista uma vez que está com problemas e vai ser fechado
                                self.sockets.remove(self.robotSock)
                                # Fecha o socket com problemas
                                self.robotSock.close()
                                # Informa o servidor que o jogador não está pronto
                                # Não controlo aqui o resultado porque se der erro ao enviar para o servidor,
                                # algo se passa, e por isso, também vai dar erro aqui no main_loop() onde é controlado. 
                                self.player_not_ready()
                            # Quando a conexao com o Servidor é terminada normalmente
                            elif (sock == self.interfaceSock):
                                # Só termina quando tiver executado o que está por executar
                                if ( self.battleRoom.changesQueue.get_size() == 0 ):
                                    printi("***   A Terminar Interface...   ***")
                                    printi("Motivo: A conexão com o Servidor foi terminada.")
                                    self.battleRoom.alive = False
                                
            except socket.error, err:
                if (sock == self.interfaceSock):
                    printe("!!! Ocorreu um erro em 'ServerInterface.main_loop()' no socket 'interfaceSock'.")
                    printe("!!! Descrição: " + str(err))
                    self.battleRoom.alive = False
                    
                elif (sock == self.robotSock):
                    printe("!!! Ocorreu um erro em 'ServerInterface.main_loop()' no socket 'clientSock'.")
                    printe("!!! Descrição: " + str(err))
                    
                    # Retira o socket do robot da lista uma vez que está com problemas e vai ser fechado
                    self.sockets.remove(self.robotSock)
                    # Fecha o socket com problemas
                    self.robotSock.close()
                    
                    # Informa o servidor que o jogador não está pronto
                    # Não controlo aqui o resultado porque se der erro ao enviar para o servidor,
                    # algo se passa, e por isso, também vai dar erro aqui no main_loop() onde é controlado.
                    result = self.player_not_ready()
                    
                else:
                    printe("\n!!! Ocorreu um erro em 'ServerInterface.main_loop()' no socket 'localSock'.")
                    printe("!!! Descrição: " + str(err))
                    #self.battleRoom.alive = False
            
            except KeyboardInterrupt, err:
                printe("***   A Terminar Interface...   ***")
                printe(">> Motivo: ^C")
                self.battleRoom.alive = False  

            # Actualiza a imagem da batalha, controla os FPS's, etc.
            self._update()
            
            # keepalive
            elapsed = time() - counter
            if ( (elapsed >= self.TIMER) and (self._keepaliveFlag) ):
                self.keepalive()
                counter = time()

        pygame.display.quit()
        pygame.quit()
        # É preciso fazer um 'reset' à 'battleRoom' porque se terminar o main_loop do pygame e o voltar a iniciar
        # sem ter criado uma nova instância da 'battleRoom', o programa é fechado.
        # Penso que seja pela classe 'ScoreBoard' derivar da 'pygame.surface.Surface'
        del self.battleRoom
        self.battleRoom = BattleRoom( self.keepalive )
        self._disconnect_robot()
        return 0


    def _disconnect_robot( self ):
        """
        Utilizado para disconecta o robot no final da batalha.
        """
        printi("A disconectar o robô.")
        if ( self.robotSock != None ):
            self.robotSock.close()
            # NÃO PRECISA SER RETIRADO AQUI PORQUE COMO É FECHADO, IRÁ SER RETIRADO NO MAIN_LOOP
            # Retira o socket do robot da lista uma vez que está com problemas e vai ser fechado
            #if ( self.robotSock in self.sockets ):
            #    self.sockets.remove(self.robotSock)


    def _is_get_command( self, command ):
        """
        Verifica se o comando passado como argumento é um 'GetCommand'
        """
        if ( command in self._getCommands ):
            return True
        return False
    

    def _handle_queued_events( self ):
        for event in self._eventsQueue:
            # event[0] = nome do evento
            # event[1] = argumentos do evento
            # Pede o evento
            ev = self._eventsBox.pull_event( event )
            if ( ev != None ):
                # Executa o evento
                ev.execute( self, event[1] )
            else:
                printe( "!!! ServerInterface._handle_queued_events  ***  Evento desconhecido." )
                printe( "Descrição: " + str(event) )


    def control_server( self, data ):
        """
        Controla a informação que o servidor envia.
        """
        ## Se por acaso se acumularem comandos por receber, é preciso separa-los e executar um a um
        # Cria uma lista com os comandos separados.
        # O ultimo valor da lista é sempre nulo
        commandList = data.split( self.EOL )
        # Como o ultimo valor da lista é sempre nulo, retira-o
        commandList.pop()
        # Interpreta comando a comando
        for command in commandList:
            # Como o 'split()' retira a terminação dos comandos (\r\n) e isso é preciso
            # para o metodo 'data_ok' e 'command_parser()', volta-se a colocar a terminação.
            command += self.EOL
            
            # Verifica se o que o servidor enviou tem um formato válido
            dataOK = self._data_ok(command)
            if (not dataOK):
                printw("!!! Comando inválido enviado pelo servidor!")
                printw("!!! Comando: " + str(command))
                
                #return -1 # Retirado porque tem de continuar para verificar os restantes comandos da lista caso existam
                continue
            
            # Separa o comando dos argumentos caso existam
            result = self.command_parser(command) 
            if (isinstance(result, tuple)):
                _command, args = result
            else:
                #return -1 # Retirado porque tem de continuar para verificar os restantes comandos da lista caso existam
                continue

            # Executa o comando ou o evento
            # Comando
            if ( dataOK == 1 ):
                self.exec_command( _command, args )
                # Sempre que recebe um comando, verifica se esse comando é um 'GetCommand'
                if ( self._is_get_command(_command) ):
                    self._handle_queued_events()
                    self._waitingGet = False
                    self._eventsQueue = []
            # Evento
            elif ( dataOK == 2 ):
                # Verifica se o ServerInterface está à espera da resposta de um 'GetCommand'
                if ( self._waitingGet ):
                    # Coloca o evento na queue 
                    self._eventsQueue.append( (_command, args) )

                    # O round_started é um evento excepção porque quando o robô envia GetCommands antes do inicio
                    # da batalha e fica à espera do inicio e ao mesmo tempo da resposta do GetCommand,
                    # Aqui verifica que a batalha iniciou, coloca o evento na queue e envia o GetCommand para
                    # o servidor para logo a seguir gerar o evento round_started.
                    if ( _command == "_round_started" ): # and (self.execMode == "block") ):
                        command = self.commandStack.pop()
                        result = self.send_to_server(command)
                        if (result != 0):
                            printe("!!! Erro ao enviar para o servidor os comandos na stack.")
                            printe("!!! Comandos: %r" % str(self.commandStack))
                            printe("!!! Descrição: %r" % str(result))
                            self._send_to_client(self.ERROR + '(' + 'not_sent' + ')')
                            self.robotSock.close()

                    continue
                # Quando não está à espera da resposta de nenhum 'GetCommand'
                else:
                    #self._eventsDic[_command](args)
                    # Pede o evento
                    ev = self._eventsBox.pull_event( _command )
                    if ( ev != None ):
                        # Executa o evento
                        ev.execute( self, args )
                    else:
                        printe( "!!! ServerInterface._handle_queued_events  ***  Evento desconhecido." )
                        printe( "Descrição: " + str(_command) )

            if (result == -1):
                printe("!!! Houve um erro ao tentar executar um comando enviado pelo servidor!")
                printe("!!! Comando: " + str(command))
                printe("!!! Descrição: " + str(result))
                continue


    def _data_ok(self, data):
        """
        Verifica se o comando enviado pelo cliente é valido. E em seguida verifica se o comando existe.
        * 'data' tem de obedecer a (r"([a-z_]{2,40}\r\n$)|[a-z_]{2,40}\([a-z0-9, ]{1,10}\)\r\n$")
        
        Retorna 1 se estiver tudo OK e se for um comando(estiver na self.commandList).
        Retorna 2 se estiver tudo OK e se for uum evento(estiver na lista self._eventsDic).
        
        Esta diferênça é utilizada no metodo 'control_server()' para saber em que lista executa o comando.
        """
        #r = re.compile(r"([a-z_]{2,40}\r\n$)|[a-z_]{2,40}\([a-zA-Z0-9, ]{1,1024}\)\r\n$")
        r = re.compile(r"([a-z_]{2,40}\r\n$)|[a-z_]{2,40}\(.{1,10240}\)\r\n$")
        if (r.match(data) != None):
            # Separa o comando dos argumentos
            command = data.strip().split("(")
            if (command[0] in self._commandsDic.keys()):
                return 1
            elif (command[0] in self._eventsBox.get_keys()):
                return 2
            else:
                printw("")
                printw("Enviado comando desconhecido")
                printw("Comando Recebido: " + str(command[0]))
                
                return False
        else:
            return False


    def command_parser(self, data):
        """
        Separa do comando dos argumentos
        """
        #r = re.compile(r"([a-z_]{2,40})\r\n$|([a-z_]{2,40})+\(([a-zA-Z0-9, ]{1,1024})\)\r\n$")
        r = re.compile(r"([a-z_]{2,40})\r\n$|([a-z_]{2,40})+\((.{1,10240})\)\r\n$")
        groups = r.match(data)
        if (groups != None):
            # Caso o comando enviado seja um comando sem argumentos tipo o 'server_state', o grupo será o numero 1.
            # Caso seja um comando com argumentos tipo o 'robot_turn_left(90)', os grupos serao o segundo e o terceiro.
            # Por isso a necessidade deste cilo IF.
            if (groups.group(1) == None):
                return (groups.group(2), groups.group(3))
            else:
                return (groups.group(1), None)
        else:
            return -1


    def exec_command( self, command, args ):
        return self._commandsDic[command]( args ) 


    def control_robot( self, data ):
        """
            Recebe comandos do robot, verifica se o comando é válido e caso seja, executa-o.
        """
        ## Se por acaso se acumularem comandos por receber, é preciso separa-los e executar um a um
        ## Por segurança, só lê ate 6 comandos. Se tiver mais, é descartado o excesso.
        # Cria uma lista com os comandos separados.
        # O ultimo valor da lista é sempre nulo
        commandList = data.split( self.EOL )
        # Como o ultimo valor da lista é sempre nulo, retira-o
        commandList.pop()
        # Interpreta comando a comando
        for command in commandList:
            # Como o 'split()' retira a terminação dos comandos (\r\n) e isso é preciso
            # para o metodo 'data_ok' e 'command_parser()', volta-se a colocar a terminação.
            command += self.EOL

            if (not self._data_ok(command)):
                continue
            
            # Separa o comando dos argumentos caso existam
            result = self.command_parser(command)
            if (isinstance(result, tuple)):
                command, args = result
            else:
                continue
            
            # Trata dos comandos de controlo
            # A explicação do que é um comando de controlo está junto à declaração da variável 'self.controlCommands'
            if (command in self.controlCommands):
                # Executa o comando enviado pelo jogador. Caso haja um problema durante a execução do mesmo,
                # envia essa informação ao jogador
                result = self.exec_command(command, args)
                if (result != 0):
                    # O comando 'exec_mode' tem um tratamento especial. Ver porquê na declaração do metodo.
                    #if (command == "exec_mode"):
                    #    self.commandStack.append(command + '(' + str(args) + ')')
                #else:
                    printw("!!! Problema ao executar um comando de controlo.")
                    printw("!!! Comando: %r(%r)" % (str(command), str(args)))
                    printw("!!! Descrição: %r" % str(result))
                    self._send_to_client(self.ERROR + '(' + 'not_sent' + ')')
                    self.robotSock.close()

            # Se não for um comando de controlo, segue o procedimento normal
            else:
                # Os comandos só podem ser enviados para o servidor quando o servidor indicar que a batalha já foi
                # iniciada
                if (self.battleRoom.started):
                    # Trata dos 'GetCommands'
                    if ( self._is_get_command(command) ):
                        retVal = self.exec_command( command, args )
                        if (retVal != 0):
                            printw("!!! Problema ao executar um comando.")
                            printw("!!! Comando: %r(%r)" % (str(command), str(args)))
                            printw("!!! Descrição: %r" % str(retVal))
                            self._send_to_client(self.ERROR + '(' + 'not_sent' + ')')
                            self.robotSock.close()
                        else:
                            print "waitingGet is set 1!"
                            print "Command:" + str( command )
                            self._waitingGet = True
                        continue

                    # No modo 'lock' a interface envia logo o comando para o servidor
                    if (self.execMode == 'lock'):
                        # Executa o comando enviado pelo jogador. Caso haja um problema durante a execução do mesmo,
                        # envia essa informação ao jogador
                        result = self.exec_command(command, args)
                        if (result != 0):
                            printw("!!! Problema ao executar um comando.")
                            printw("!!! Comando: %r(%r)" % (str(command), str(args)))
                            printw("!!! Descrição: %r" % str(result))
                            self._send_to_client(self.ERROR + '(' + 'not_sent' + ')')
                            self.robotSock.close()
                    
                    # Neste modo o interface vai acumulando comandos até o robot dar a ordem de enviar para o servidor.
                    # Quando a lista está cheia e o robot continua a enviar comandos, o primeiro valor da lista é substituido
                    # e o novo é adicionado ao final da lista
                    elif(self.execMode == 'block'):
                        if (len(self.commandStack) >= self.maxStackSize):
                            printw("O robot não pode acumular mais de %i comandos" % int(self.maxStackSize)) 
                            self.commandStack.pop(0)
                            self.commandStack.append(command + '(' + str(args) + ')')
                        
                        else:
                            self.commandStack.append(command + '(' + str(args) + ')')
                        
                        # Envia a informação ao robot que está tudo ok e que pode continuar
                        self._send_to_client(self.DONE)

                    # No modo 'non-lonk' o interface envia logo o comando para o servidor e envia uma resposta para o cliente
                    # para que não bloquei à espera do servidor
                    elif (self.execMode == 'non-lock'):
                        #result = self.send_to_server(command) # Foi comentado porque assim enviada o comando 2 vezes
                        # Executa o comando enviado pelo jogador. Caso haja um problema durante a execução do mesmo,
                        # envia essa informação ao jogador
                        result = self.exec_command(command, args)
                        if (result != 0):
                            printw("!!! Problema ao executar um comando.")
                            printw("!!! Comando: %r(%r)" % (str(command), str(args)))
                            printw("!!! Descrição: %r" % str(result))
                            self._send_to_client(self.ERROR + '(' + 'not_sent' + ')')
                            self.robotSock.close()
                        else:
                            # Envia a informação ao robot que está tudo ok e que pode continuar
                            self._send_to_client( self.DONE )

                # Quando a batalha não foi iniciada é preciso guardar os comandos que o robot envia para
                # posteriormente serem enviados para o servidor
                else:
                    # Trata dos 'GetCommands'
                    if ( self._is_get_command(command) ):
                        self.commandStack.append(command + '(' + str(args) + ')')
                        print "waitingGet is set 2!"
                        print "Command:" + str( command )
                        self._waitingGet = True
                        continue
                    
                    if (self.execMode == 'lock'):
                        if (len(self.commandStack) > 0):
                            self.commandStack.pop(0)
                            self.commandStack.append(command + '(' + str(args) + ')')
                        
                        else:
                            self.commandStack.append(command + '(' + str(args) + ')')
                    
                    elif (self.execMode == 'block'):
                        # Uma vez que o comando não pode ser enviado porque a batalha ainda não foi iniciada,
                        # guarda-o na lista para assim que poder, enviar ao servidor.
                        # Quando excede o número máximo, retira o primeiro da lista e adiciona o novo ao final.
                        if (len(self.commandStack) >= self.maxStackSize):
                            printw("O robot não pode acumular mais de %i comandos" % int(self.maxStackSize))
                            self.commandStack.pop(0)
                            self.commandStack.append(command + '(' + str(args) + ')')
                        
                        else:
                            self.commandStack.append(command + '(' + str(args) + ')')
                        
                        # Envia a informação ao robot que está tudo ok e que pode continuar
                        self._send_to_client(self.DONE)
                    
                    elif (self.execMode == 'non-lock'):
                        if (len(self.commandStack) > 0):
                            self.commandStack.pop(0)
                            self.commandStack.append(command + '(' + str(args) + ')')
                        
                        else:
                            self.commandStack.append(command + '(' + str(args) + ')')
    
                        # Envia a informação ao robot que está tudo ok e que pode continuar
                        self._send_to_client(self.DONE)
    

    def start_battle(self):
        """
        Metodo que serve de callback para o botão de iniciar a batalha.
        Dá ordem ao servidor para iniciar a batalha.
        """
        #printi("_start_battle")
        # Termina o timer do keepalive
        self._keepaliveFlag = False
        result = self.send_to_server( self.START_BATTLE )
        if (result == 0):
            printi("A iniciar a batalha...")
            # Aumenta a 'velocidade' do main loop para dar velocidade suficiente à animação
            self.battleRoom.fps = 45
            # Faz com que a animação de inicio da batalha seja mostrada
            self.battleRoom.start_animation()
        else:
            printw("Não foi possível iniciar a batalha devido a um problema local.")
            printw("Descrição: %r" % str(result))        


    def send_command_block(self):
        """
        Serve apenas para enviar todos os comandos da stack.
        """
        data = ""
        for command in self.commandStack:
            data += command + self.EOL
        if ( data != "" ):
            try:
                self.interfaceSock.send( str(data) )
                return 0
            except socket.error, err:
                printe("")
                printe("Ocorreu um erro em 'send_command_block()'")
                printe("Descrição: " + str(err))
        return -1


    ##############################################################################################################
    ###################################### Metodos para os comandos de jogo   ####################################
    ##############################################################################################################

    def _set_exec_mode(self, args=None):
        """
            Configura em que modo o robot vai funcionar
            O argumento pode ser: 'lock', 'block', 'non-lock'
            Ao alterar o  modo de execução a queue (self.commandStack) é limpa.

        Este comando é especial e quando enviado tem de ser logo executado por ter efeitos imediatos 
        na forma como os comandos seguintes são executados. 
        É tratado directamente no metodo 'control_robot'!
        Este comando é também enviado para o servidor. É um único comando de control que é enviado para o servidor.
        """
        printd("exec_mode(" + str(args) + ")")
        
        modes = [ 'lock', 'block', 'non-lock' ]
        
        # No caso de por algum motivo o robot não enviar argumento.
        if (args != None):
            mode = args.lower()
        else:
            return -1
        
        # Verifica se o modo que o robot está a tentar utilizar existe, e caso exista, configura o interface
        if (mode in modes):
            self.execMode = mode
            # Faz o reset à stack
            self.commandStack = []
            command = "exec_mode(" + str(args) + ")"
            if ( self.battleRoom.started ):
                return self.send_to_server( command )
            else:
                self.commandStack.append( command )
            return 0
        
        else:
            return -1
    

    def _execute(self, args=None):
        # Vê se existem comandos na stack para enviar ao servidor
        if (len(self.commandStack) > 0):
            # Só envia os comandos para o servidor caso a batalha já tenha sido iniciada
            if (self.battleRoom.started):
                # Envia para o servidor os comandos que o robot já tinha enviado quando se conectou ao interface
                #result = self.send_to_server( self.commandStack )
                # Envia para o servidor os comandos na stack um a um
                result = self.send_command_block()
                if (result != 0):
                    printe("\n!!! Erro ao enviar para o servidor os comandos na stack.")
                    printe("!!! Comandos: %r" % str(self.commandStack))
                    printe("!!! Descrição: %r" % str(result))
                    self._send_to_client(self.ERROR + '(' + 'not_sent' + ')')
                    self.robotSock.close()
                    return -1
                
                # Agora que já enviou os comandos, limpa a stack
                self.commandStack = []
            # Quando a batalha não iniciou ainda mas está tudo ok    
            return 0
                
        else:
            printi("execute() *** Sem comandos na stack")
            return self._send_to_client(self.DONE)   


    def _robot_move_forward(self, args=None):
        printd("robot_move_forward(" + str(args) + ")")
        command = "robot_move_forward(" + str(args) + ")"
        return self.send_to_server(command)

    def _robot_move_backward(self, args=None):
        printd("robot_move_backward(" + str(args) + ")")
        
        command = "robot_move_backward(" + str(args) + ")"
        return self.send_to_server(command)
    

    def _robot_turn_right(self, args=None):
        printd("robot_turn_right(" + str(args) + ")")
        command = "robot_turn_right(" + str(args) + ")"
        return self.send_to_server(command)

    def _robot_turn_left(self, args=None):
        printd("robot_turn_left(" + str(args) + ")")
        command = "robot_turn_left(" + str(args) + ")"
        return self.send_to_server(command)
    
    def _robot_turn_to(self, args=None):
        printd("robot_turn_to( %s )" % str(args))
        command = "robot_turn_to(" + str(args) + ")"
        return self.send_to_server(command)
    
    
    
    def _gun_turn_right( self, args=None ):
        printd("gun_turn_right(" + str(args) + ")")
        command = "gun_turn_right(" + str(args) + ")"
        return self.send_to_server( command )

    def _gun_turn_left( self, args=None ):
        printd("gun_turn_left(" + str(args) + ")")
        command = "gun_turn_left(" + str(args) + ")"
        return self.send_to_server( command )

    def _gun_turn_to( self, args=None ):
        printd("gun_turn_to( %s )" % str(args))
        command = "gun_turn_to(" + str(args) + ")"
        return self.send_to_server(command)

    def _shoot( self, args=None ):
        printd("shoot(" + str(args) + ")")
        command = "shoot"
        return self.send_to_server( command )
    
    
    
    
    
    def _radar_turn_right( self, args=None ):
        printd("radar_turn_right(" + str(args) + ")")
        command = "radar_turn_right(" + str(args) + ")"
        return self.send_to_server( command )

    def _radar_turn_left( self, args=None ):
        printd("radar_turn_left(" + str(args) + ")")
        command = "radar_turn_left(" + str(args) + ")"
        return self.send_to_server( command )

    def _radar_turn_to( self, args=None ):
        printd("radar_turn_to( %s )" % str(args))
        command = "radar_turn_to(" + str(args) + ")"
        return self.send_to_server( command )

    def _set_speed( self, args=None ):
        printd("set_speed(" + str(args) + ")")
        command = "set_speed(" + str(args) + ")"
        return self.send_to_server( command )

    def _scan( self, args=None ):
        printd("scan(" + str(args) + ")")
        command = "scan(" + str(args) + ")"
        return self.send_to_server( command )

    def _advanced_scan( self, args=None ):
        printd("advanced_scan(" + str(args) + ")")
        command = "advanced_scan(" + str(args) + ")"
        return self.send_to_server( command )
    
    def _no_freeze_on( self, args = None ):
        printd("no_freeze_on(%s)" % str(args))
        command = "no_freeze_on(" + str(args) + ")"
        return self.send_to_server( command )
    
    def _freeze_on( self, args = None ):
        printd("freeze_on(%s)" % str(args))
        command = "freeze_on(" + str(args) + ")"
        return self.send_to_server( command )

    def _subscribe_events( self, args = None ):
        printd("subscribe_events(%s)" % str(args))
        command = "subscribe_events(" + str(args) + ")"
        return self.send_to_server( command )
    
    def _unsubscribe_events( self, args = None ):
        printd("unsubscribe_events(%s)" % str(args))
        command = "unsubscribe_events(" + str(args) + ")"
        return self.send_to_server( command )
    
    def _noop( self, args = None ):
        printd("noop(%s)" % str(args))
        command = "noop"
        return self.send_to_server( command )

    def _stop( self, args = None ):
        printd("stop(%s)" % str(args))
        command = "stop"
        return self.send_to_server( command )

    def _lock_gun_on_robot( self, args = None ):
        printd("lock_gun_on_robot(%s)" % str(args))
        command = "lock_gun_on_robot(" + str(args) + ")"
        return self.send_to_server( command )

    def _lock_radar_on_robot( self, args = None ):
        printd("lock_radar_on_robot(%s)" % str(args))
        command = "lock_radar_on_robot(" + str(args) + ")"
        return self.send_to_server( command )

    def _lock_gun_on_radar( self, args = None ):
        printd("lock_gun_on_radar(%s)" % str(args))
        command = "lock_gun_on_radar(" + str(args) + ")"
        return self.send_to_server( command )

    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################









    ##############################################################################################################
    ######################################       GetCommands - Do servidor       #################################
    ##############################################################################################################

    def _get_robot_position(self, args=None):
        printd("get_robot_position()")
        self._send_to_client("get_robot_position(" + str(args) + ")")

    def _get_bf_size(self, args=None):
        printd("get_bf_size()")
        self._send_to_client("get_bf_size(" + str(args) + ")")

    def _get_speed(self, args=None):
        printd("get_speed()")
        self._send_to_client("get_speed(" + str(args) + ")")

    def _get_seq_num(self, args=None):
        printd("get_seq_num()")
        self._send_to_client("get_seq_num(" + str(args) + ")")

    def _get_robot_dir(self, args=None):
        printd("get_robot_dir()")
        self._send_to_client("get_robot_dir(" + str(args) + ")")

    def _get_gun_dir(self, args=None):
        printd("get_gun_dir()")
        self._send_to_client("get_gun_dir(" + str(args) + ")")
        
    def _get_radar_dir(self, args=None):
        printd("get_radar_dir()")
        self._send_to_client("get_radar_dir(" + str(args) + ")")

    def _get_exec_mode(self, args=None):
        printd("get_exec_mode()")
        self._send_to_client("get_exec_mode(" + str(args) + ")")

    def _get_robots(self, args=None):
        printd("get_robots()")
        self._send_to_client("get_robots(" + str(args) + ")")

    def _get_alive_robots(self, args=None):
        printd("get_alive_robots()")
        self._send_to_client("get_alive_robots(" + str(args) + ")")

    def _get_energy(self, args=None):
        printd("get_energy()")
        self._send_to_client("get_energy(" + str(args) + ")")

    def _get_damage(self, args=None):
        printd("get_damage()")
        self._send_to_client("get_damage(" + str(args) + ")")
        
    def _get_armor( self, args = None ):
        printd("get_armor()")
        self._send_to_client("get_armor(" + str(args) + ")")

    def _get_gun_temp( self, args = None ):
        printd("get_gun_temp()")
        self._send_to_client("get_gun_temp(" + str(args) + ")")

    def _get_round( self, args = None ):
        printd("get_round()")
        self._send_to_client("get_round(" + str(args) + ")")

    def _get_round_time( self, args = None ):
        printd("get_round_time()")
        self._send_to_client("get_round_time(" + str(args) + ")")

    def _get_rounds_num( self, args = None ):
        printd("get_rounds_num()")
        self._send_to_client("get_rounds_num(" + str(args) + ")")

    def _get_elapsed_time( self, args = None ):
        printd("get_elapsed_time()")
        self._send_to_client("get_elapsed_time(" + str(args) + ")")

    def _get_no_freeze_on( self, args = None ):
        printd("get_no_freeze_on()")
        self._send_to_client("get_no_freeze_on(" + str(args) + ")")

    def _get_subscribed_events( self, args = None ):
        printd("get_subscribed_events()")
        self._send_to_client("get_subscribed_events(" + str(args) + ")")

    def _get_commands_queue( self, args = None ):
        printd("get_commands_queue()")
        self._send_to_client("get_commands_queue(" + str(args) + ")")

    def _ping( self, args = None ):
        printd("ping()")
        self._send_to_client("ping(" + str(args) + ")")

    def _get_gun_lock( self, args = None ):
        printd("get_gun_lock()")
        self._send_to_client("get_gun_lock(" + str(args) + ")")

    def _get_radar_lock( self, args = None ):
        printd("get_radar_lock()")
        self._send_to_client("get_radar_lock(" + str(args) + ")")

    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################


    ##############################################################################################################
    ######################################     GetCommands - Do robot         ####################################
    ##############################################################################################################


    def get_robot_position(self, args=None):
        printd("get_robot_position()")
        command = "get_robot_position"
        return self.send_to_server(command)

    def get_bf_size(self, args=None):
        printd("get_bf_size")
        command = "get_bf_size"
        return self.send_to_server(command)

    def get_speed(self, args=None):
        printd("get_speed")
        command = "get_speed"
        return self.send_to_server(command)

    def get_seq_num(self, args=None):
        printd("get_seq_num")
        command = "get_seq_num"
        return self.send_to_server(command)

    def get_robot_dir(self, args=None):
        printd("get_robot_dir")
        command = "get_robot_dir"
        return self.send_to_server(command)

    def get_gun_dir(self, args=None):
        printd("get_gun_dir")
        command = "get_gun_dir"
        return self.send_to_server(command)

    def get_radar_dir(self, args=None):
        printd("get_radar_dir")
        command = "get_radar_dir"
        return self.send_to_server(command)

    def get_exec_mode(self, args=None):
        printd("get_exec_mode")
        command = "get_exec_mode"
        return self.send_to_server(command)
    
    def get_robots( self, args = None ):
        printd( "get_robots" )
        command = "get_robots"
        return self.send_to_server( command )

    def get_alive_robots( self, args = None ):
        printd( "get_alive_robots" )
        command = "get_alive_robots"
        return self.send_to_server( command )

    def get_energy( self, args = None ):
        printd( "get_energy" )
        command = "get_energy"
        return self.send_to_server( command )
    
    def get_damage( self, args = None ):
        printd( "get_damage" )
        command = "get_damage"
        return self.send_to_server( command )    
    
    def get_armor( self, args = None ):
        printd( "get_armor" )
        command = "get_armor"
        return self.send_to_server( command )

    def get_gun_temp( self, args = None ):
        printd( "get_gun_temp" )
        command = "get_gun_temp"
        return self.send_to_server( command )

    def get_round( self, args = None ):
        printd( "get_round" )
        command = "get_round"
        return self.send_to_server( command )

    def get_round_time( self, args = None ):
        printd( "get_round_time" )
        command = "get_round_time"
        return self.send_to_server( command )

    def get_rounds_num( self, args = None ):
        printd( "get_rounds_num" )
        command = "get_rounds_num"
        return self.send_to_server( command )

    def get_elapsed_time( self, args = None ):
        printd( "get_elapsed_time" )
        command = "get_elapsed_time"
        return self.send_to_server( command )

    def get_no_freeze_on( self, args = None ):
        printd( "get_no_freeze_on" )
        command = "get_no_freeze_on"
        return self.send_to_server( command )

    def get_subscribed_events( self, args = None ):
        printd( "get_subscribed_events" )
        command = "get_subscribed_events"
        return self.send_to_server( command )

    def get_commands_queue( self, args = None ):
        printd( "get_commands_queue" )
        command = "get_commands_queue"
        return self.send_to_server( command )

    def ping( self, args = None ):
        printd( "ping" )
        command = "ping"
        return self.send_to_server( command )

    def get_gun_lock( self, args = None ):
        printd( "get_gun_lock" )
        command = "get_gun_lock"
        return self.send_to_server( command )

    def get_radar_lock( self, args = None ):
        printd( "get_radar_lock" )
        command = "get_radar_lock"
        return self.send_to_server( command )
    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################



    ##############################################################################################################
    ###################################### Metodos para o controlo do servidor   #################################
    ##############################################################################################################

    def _term_battle_room(self, args = None):
        """
        Recebido quando a sala de jogo é fechada.
        
        args - string 'none'
        """
        printd("_term_battle_room(" + str(args) + ')')
        # Para quando a batalha não está iniciada tem de terminar a sala de jogo com o comando directo em vez do encapsolado
        if ( not self.battleRoom.started ):
            self.battleRoom.alive = False
            # Reset ao contador de rounds
            self.battleRoom.round = 0
            # Volta a indicar que a batalha não está iniciada
            self.battleRoom.started = False
            # Limpa todos os objectos
            self.battleRoom.objectsGroup = []
        elif ( self.battleRoom.started ):
            self.battleRoom.changesQueue.enqueue( [[ ["_term_battle_room", None] ]] )

        retVal = 0
        # Quando nao tem nenhum robot conectado
        if ( self.robotSock != None ):
            retVal = self._send_to_client("term_battle_room")
            self.battleRoom.scoreBoard.set_score_state( self.battleRoom._playerName, "player_not_ready" )
        
        self._keepaliveFlag = True
        
        return retVal

    
    def _term_battle(self, args = None):
        """
        Recebido quando a batalha termina mas a sala continua aberta.
        
        args - string 'none'
        """
        printd("_term_battle(" + str(args) + ')')
        retVal = 0
        # Quando nao tem nenhum robot conectado
        retVal = self._send_to_client("term_battle")
        self.battleRoom.scoreBoard.set_score_state( self.battleRoom._playerName, "player_not_ready" )
        
        self._keepaliveFlag = True
        
        return retVal
    

    def _kicked_player( self, args = None ):
        """
        - args: robotName
        """
        printd("_kicked_player(" + str(args) + ')')
        # Se a batalha estiver iniciada o evento encapsulado é que remove o score
        if ( not self.battleRoom.started ):
            self.battleRoom._remove_player_score( args )
            # Só faz sentido enviar o evento quando a batalha está a decorrer...

        # Verifica se há jogadores suficientes para iniciarem a batalha e se estão todos prontos
        # com o objectivo de habilitar ou desabilitar o botão de iniciar batalha
        self.battleRoom.check_ready_for_battle()


    def _joined_player(self, args=None):
        #printd("_joined_player(" + str(args) + ')')
        playerList = []
        # Converte a lista numa string
        player = eval(args)
        printi( "O jogador " + str(player[0]) + " entrou na batalha" )
        # Este passo é preciso porque o metodo 'add_players' está preparado para receber uma lista com varios jogadores
        # Para mais pormenores, ver o metodo
        playerList.append(player)
        self.battleRoom.add_players(playerList)
        # Verifica se há jogadores suficientes para iniciarem a batalha e se estão todos prontos
        # com o objectivo de abilitar ou desabilitar o botão de iniciar batalha
        self.battleRoom.check_ready_for_battle()
    
    
    def _join_fail(self, args=None):
        """
            Indica que não foi possível entrar na batalha porque já esta numa batalha
        """
        printd("_join_fail(" + str(args) + ')')


    def _set_player_status(self, args=None):
        """
            Actualiza o estado do jogador ('player_ready' ou 'player_not_ready').
            Recebe uma lista com o nome do jogador e o seu estado.
            Serve para actualiza o ScoreBoard.
        """
        #printi("_refresh_player_status(" + str(args) + ')')
        playerName, state = eval(args)
        printi( "O jogador " + str(playerName) + " alterou o estado para " + str(state) )
        # Actualiza o estado do jogador no Score Board
        self.battleRoom.scoreBoard.set_score_state(playerName, state)
        
        # Verifica se há jogadores suficientes para iniciarem a batalha e se estão todos prontos
        # com o objectivo de abilitar ou desabilitar o botão de iniciar batalha
        self.battleRoom.check_ready_for_battle()
        

    def _players_list( self, args = None ):
        """
        Falg que indica que está a ser enviada uma lista com o perfil dos jogadores que estão
        na batalha onde o jogador entrou.
        """
        printd("_players_list(" + str(args) + ')')
    

    def _full_battle( self, args = None ):
        """
        É invocado quando o jogador tenta entrar numa sala que está cheia.
        """
        printd("_full_room(" + str(args) + ')')

    def _repeated_battle_name( self, args = None ):
        """
        É invocado quando o tenta criar uma batalha com um nome que já existe
        """
        printd("_repeated_battle_name(" + str(args) + ')')

    def _battle_doesnt_exist( self, args = None ):
        """
        É invocado quando o o jogador tenta entrar numa batalha que já não existe
        """
        printd("_battle_doesnt_exist(" + str(args) + ')')

    def _battles_list( self, args = None ):
        """
        É invocado logo a seguir ao jogador se autenticar. O servidor envia uma lista com
        as salas de batalha dispiníveis.
        
        Formato do 'args':
        [battleName, maxPlayers, minPlayers, battleType, cycleDuration, commandsPerCycle]
        """
        printd("_battles_list(" + str(args) + ')')


    def _refresh_battle_picture( self, args = None ):
        """
        Invocado a cada ciclo pelo servidor. Traz no argumento as alterações do campo de batalha.
        
         - 'args' - Alterações do campo de batalha.
         
         "_refresh_battle_picture([['Mr. Smith', (245, 520), -5], ['Mr. Anderson', (410, 452), 12]])\r\n"
        """
        printd("_refresh_battle_picture(" + str(args) + ')')
                
        # Descomprime a informação
        print "######################################"
        print str(args)
        decompressed = zlib.decompress(base64.b64decode(str(args)))
        print "######################################"
        
        # Transforma a string numa lista
        changesList = eval(decompressed)
        printd("-------------------_refresh_battle_picture--------------------")
        printd("ChangesList Length")
        printd(len(changesList))
        
        self.battleRoom.changesQueue.enqueue(changesList)
        
        printd("ChangesQueue:")
        printd(self.battleRoom.changesQueue.changesList)
        printd("-------------------------------------------------------")
        

    def _sov( self, args = None ):
        """
        É recebido quando o robot excede o número máximo de comandos por segundo.
        Não é enviado para o robô. Serve apenas como debug.
        """
        printw( "!!! Foi excedido o número máximo(20) de comandos permitidos por segundo!" )


    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################
