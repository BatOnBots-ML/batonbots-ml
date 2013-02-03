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

from log.logging_mod import Logging
log = Logging()
printd = log.debug
printi = log.info
printe = log.error
printw = log.warning


class Package():
        pass



class EventsBox():
    """
    """
    def __init__( self ):
        # Dicionario com todos os eventos(e o metodo correspondente) que são enviados para o robô
        # Todos os restantes eventos como por exemplo o '_player_kicked' ficam no 'self.commandsDic'
        self._eventsDic = {
                            # Indica que o round foi iniciado
                            # No argumento traz as posições iniciais e o número do round na primeira posição
                            '_round_started': self.round_started,
                            #
                            #'_round_ended': self._round_ended,
                            # Informa o jogador que foi kickado do servidor por inactividade
                            # Apenas para debug
                            '_kicked_by_inactivity': self.kicked_by_inactivity,
                            # Indica ao jogador que já executou todos os comandos
                            '_done': self.done,
                            # Informa que o comando enviado não foi processado devido a congestionamento no servidor
                            '_command_dropped': self.command_dropped,
                            # Informa o jogador que enviou um comando com um argumento inválido
                            # recebe _invalid_arg_inf(command, arg) onde 'command' e 'arg' é o comando e o respectivo 
                            # argumento inválido.
                            '_invalid_arg_inf': self.invalid_arg_inf,
                            # Informa o jogador que vai ser expulso da batalha porque excedeu o limite máximo de 
                            # comandos seguidos com argumentos inválidos.
                            # recebe _invalid_arg_max(command, arg) onde 'command' e 'arg' é o comando e o respectivo 
                            # argumento inválido.
                            '_invalid_arg_max': self.invalid_arg_max,
                            # Quando o servidor não recenhece o comando que foi enviado ou ocorreu algum problema
                            # na sua verificação
                            # Este evento não é enviado para o robot
                            '_invalid_command': self.invalid_command,
                            # Eventos relacionados com as colisões
                            '_destroyed': self.destroyed,
                            '_robot_destroyed': self.robot_destroyed,
                            '_kicked_robot': self.kicked_robot,
                            '_on_hit_wall': self.on_hit_wall,
                            '_on_hit_robot': self.on_hit_robot,
                            '_on_hit_by_bullet': self.on_hit_by_bullet, # Quando o robot é atingido por uma bala
                            '_on_bullet_hit': self.on_bullet_hit,
                             
                            # Eventos de jogo
                            '_gun_overheat': self.gun_overheat,
                            '_out_of_energy': self.out_of_energy,
                            '_event_not_subscribed': self.event_not_subscribed,
                            
                            # Radar
                            '_scan_event': self.scan_event
                        }

    def pull_event( self, event ):
        """
        Retorna o evento e todas as dependencias caso tenha na forma de um objecto
        OU
        'None' se o evento não existir. Este último caso não deve acontecer...
        """
        if ( event in self._eventsDic.keys() ):
            return self._eventsDic[ event ]()
        else:
            return None

    def get_keys( self ):
        return self._eventsDic.keys()











    ########################################################################################################
    #############################################    EVENTOS   #############################################
    ########################################################################################################
    def round_started( self ):
        package = Package()
        package.execute = self._round_started
        return package
    
    def _round_started( self, mainClass, args = None ):
        """
        É invocado no inicio de cada round.
        
        'args' - Vem com o numero do round e todos os jogadores na batalha e as duas posições iniciais.
        """
        #printi("_round_started(" + args + ')')
        # Altera o estado da batalha para batalha iniciada
        mainClass.battleRoom.started = True
        # Volta a repor o modo de execução
        mainClass.execMode = "lock"

        # Só o para uma vez...
        if ( not mainClass.battleRoom.started ):
            # Termina o timer do keepalive
            mainClass._keepaliveFlag = False
            
        # Limpa o grupo de robots
        args = eval(args)
        
        printi( "Iniciou a ronda " + str(args[1][0]) )
        
        roundNum = args[ 1 ][ 0 ]
        
        # Quando o round não é o primeiro é preciso informar o robot que se vai iniciar um novo round
        if (roundNum != 1):
            mainClass._send_to_client( "round_started(" + str(roundNum) + ")" )
    

        
        # Vê se existem comandos na stack para enviar para o servidor
        if ( len(mainClass.commandStack) > 0 ):
            # Verifica se está à espera da resposta de um 'GetCommand'.
            # Se estiver significa que o ultimo comando da self.commandStack é o 'GetCommand'
            # No caso de estar à espera da resposta de um 'GetCommand' só ha diferença no cado do modo
            # de execução ser o 'block' porque no meio do block pode estar um 'GetCommand'. E com
            # esta excepção evita-se que os comandos até ao 'GetCommand' sejam enviados e os
            # seguintes não. E assim só são enviados quando recebido o 'execute()
            if ( (mainClass._waitingGet) and (mainClass.execMode == "block") ):
                command = mainClass.commandStack.pop()
                result = mainClass.send_to_server( command )
                if (result != 0):
                    printe( "!!! Erro ao enviar para o servidor os comandos na stack." )
                    printe( "!!! Comandos: %r" % str(mainClass.commandStack) )
                    printe( "!!! Descrição: %r" % str(result) )
                    mainClass._send_to_client( mainClass.ERROR + '(' + 'not_sent' + ')' )
                    mainClass.robotSock.close()
                    
            # Quando não está à espera da resposta de um 'GetCommand'
            else:
                # Envia para o servidor os comandos na stack um a um
                result = mainClass.send_command_block()
                if (result != 0):
                    printe( "\n!!! Erro ao enviar para o servidor os comandos na stack." )
                    printe( "!!! Comandos: %r" % str(mainClass.commandStack) )
                    printe( "!!! Descrição: %r" % str(result) )
                    mainClass._send_to_client( mainClass.ERROR + '(' + 'not_sent' + ')' )
                    mainClass.robotSock.close()
            
                else:
                    # Agora que já enviou os comandos, limpa a stack
                    mainClass.commandStack = []

        mainClass.battleRoom.changesQueue.enqueue( [[args]] )
        
        
    def kicked_by_inactivity( self ):
        package = Package()
        package.execute = self._kicked_by_inactivity
        return package

    def _kicked_by_inactivity( self, mainClass, args = None ):
        """
        Informa o jogador de que foi kickado por inactividade.
        
        arg - None
        """
        printw( "_kicked_by_inactivity()" )
        printw( "Acabaste de ser expulso da batalha por inactividade!" )

    
    def done( self ):
        package = Package()
        package.execute = self._done
        return package
    
    def _done( self, mainClass, args = None ):
        """
        Informa o jogador que o servidor já executou todos os seu comandos.
        """
        mainClass._send_to_client( "done(%s)" % args )


    def command_dropped( self ):
        package = Package()
        package.execute = self._command_dropped
        return package

    def _command_dropped( self, mainClass, args = None ):
        """
        Esta flag indica que o comando enviado pelo robot não foi processado devido a congestionamento no servidor.
        """
        printw("_command_dropped(" + str(args) + ')')
        mainClass._send_to_client( "command_dropped(" + str(args) + ")" )
        
    
    def invalid_arg_inf( self ):
        package = Package()
        package.execute = self._invalid_arg_inf
        return package
    
    def _invalid_arg_inf(self, mainClass, args=None):
        """
        Informa o jogador que enviou um comando com um argumento inválido
        
        arg - tupla (command, arg) onde 'command' e 'arg' é o comando e o respectivo argumento inválido.
        """
        printw("_invalid_arg_inf(" + str(args) + ')')
        mainClass._send_to_client( "invalid_arg_inf(" + str(args) + ")" )

    
    def invalid_arg_max( self ):
        package = Package()
        package.execute = self._invalid_arg_max
        return package
    
    def _invalid_arg_max( self, mainClass, args = None ):
        """
        Informa o jogador que vai ser expulso da batalha porque excedeu o limite máximo de comandos seguidos 
        com argumentos inválidos.
        
        arg - tupla (command, arg) onde 'command' e 'arg' é o comando e o respectivo argumento inválido.
        """
        printw("_invalid_arg_max(" + str(args) + ')')
        mainClass._send_to_client( "invalid_arg_max(" + str(args) + ")" )


    def invalid_command( self ):
        package = Package()
        package.execute = self._invalid_command
        return package

    def _invalid_command( self, mainClass, args = None ):
        """
        Informa o jogador que vai ser expulso da batalha porque o comando que enviou é desconhecido.
        
        arg - Comando que foi enviado com problemas.
        """
        printw("_invalid_command(" + str(args) + ')')


    def destroyed( self ):
        package = Package()
        package.execute = self._destroyed
        return package

    def _destroyed( self, mainClass, args = None ):
        """
        Quando o nosso robot é destruido.
        - args : Nome do jogador que nos destruído ou None quando é contra uma parede.
        """
        mainClass._send_to_client( "destroyed(" + str(args) + ")" )


    def robot_destroyed( self ):
        package = Package()
        package.execute = self._robot_destroyed
        return package

    def _robot_destroyed( self, mainClass, args = None ):
        """
        Quando um robot na batalha é destruido
        - args : Nome do robot que foi destruído.
        """
        mainClass._send_to_client( "robot_destroyed(" + str(args) + ")" )
        

    def kicked_robot( self ):
        package = Package()
        package.execute = self._kicked_robot
        return package

    def _kicked_robot( self, mainClass, args = None ):
        mainClass._send_to_client( "kicked_robot(" + str(args) + ")" )
        

    def on_hit_wall( self ):
        package = Package()
        package.execute = self._on_hit_wall
        return package

    def _on_hit_wall( self, mainClass, args = None ):
        """
        Quando o robot embate numa parede.
        
        - args - Parede onde embateu. top | right | bottom | left
        """
        printd("on_hit_wall()")
        mainClass._send_to_client( "on_hit_wall(" + str(args) + ")" )


    def on_hit_robot( self ):
        package = Package()
        package.execute = self._on_hit_robot
        return package

    def _on_hit_robot( self, mainClass, args = None ):
        """
        Quando um robot embate noutro robot.
        - args - Informações sobre o robot em que embateu. robotName, robotDirection, robotPosition
                              O robotDirection não é para onde o robot está virado mas sim o angulo em que ele está
                              em relação ao nosso robot.
        """
        printd("on_hit_robot()")
        mainClass._send_to_client( "on_hit_robot(" + str(args) + ")" )


    def on_hit_by_bullet( self ):
        package = Package()
        package.execute = self._on_hit_by_bullet
        return package

    def _on_hit_by_bullet( self, mainClass, args = None ):
        printd("on_hit_by_bullet(" + str(args) + ")")
        mainClass._send_to_client("on_hit_by_bullet(" + str(args) + ")") 


    def on_bullet_hit( self ):
        package = Package()
        package.execute = self._on_bullet_hit
        return package

    def _on_bullet_hit( self, mainClass, args = None ):
        printd("_on_bullet_hit(" + str(args) + ")")
        mainClass._send_to_client("on_bullet_hit(" + str(args) + ")") 


    def gun_overheat( self ):
        package = Package()
        package.execute = self._gun_overheat
        return package

    def _gun_overheat( self, mainClass, args = None ):
        printd("gun_overheat(" + str(args) + ")")
        mainClass._send_to_client("gun_overheat(" + str(args) + ")") 


    def out_of_energy( self ):
        package = Package()
        package.execute = self._out_of_energy
        return package

    def _out_of_energy( self, mainClass, args = None ):
        printd("out_of_energy(" + str(args) + ")")
        mainClass._send_to_client("out_of_energy(" + str(args) + ")")
    
    
    def event_not_subscribed( self ):
        package = Package()
        package.execute = self._event_not_subscribed
        return package
    
    def _event_not_subscribed( self, mainClass, args = None ):
        """
        Quando o robot envia um comando que gera eventos e esses eventos não estão subscritods.
        Um exemplo desses comandos é o 'scan'.
        """
        printw( "O evento '" + str(args) + "' foi gerado e não está subscrito!" )
        

    def scan_event( self ):
        package = Package()
        package.execute = self._scan_event
        return package

    def _scan_event( self, mainClass, args = None ):
        printd("scan_event(" + str(args) + ")")
        mainClass._send_to_client("scan_event(" + str(args) + ")") 
        

        