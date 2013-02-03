# -*- coding: utf-8 -*-
'''
Created on 2010/02/24

@author: NuGuN


Modulo de portabilidade para outras linguagens de programação.
'''
import socket
import re
from time import time



class OnHitRobotEvent():
    """
    Evento 'on_hit_robot'.
    
    Quando um robot embate noutro robot.
    
    - robotName: Nome do robot em que embateu.
    - robotDamage: Estragods do robot em que embateu.
    - robotArmor: lista com o estado da armadura do robot em que embateu.
    - relativeDirection: Direcção em que o robô adversário embateu relativamente 
                         à direcção do nosso robô. Na prática este valor é útil 
                         para virar o robô, arma ou radar na direcção do robô em 
                         que se embateu utilizando o comando “robot_turn_to()”, 
                         “gun_turn_to()” ou “radar_turn_to()”.
    """
    def __init__( self, robotName, robotDamage, robotArmor, relativeDirection ):
        self.robotName = robotName
        self.robotDamage = robotDamage
        self.robotArmor = robotArmor
        self.relativeDirection = relativeDirection


class OnHitByBulletEvent():
    """
    Evento 'on_hit_by_bullet'.

    Quando o robot é atingido por uma bala.
    
    - robotName: Nome do robot que disparou a bala.
    - relativeDirection: Direcção do robô que disparou a bala relativamente ao nosso robô.
    """
    def __init__( self, robotName, relativeDirection ):
        self.robotName = robotName
        self.relativeDirection = relativeDirection


class OnBulletHitEvent():
    """
    Evento 'on_bullet_hit'.
    
    Quando uma das nossas balas atinge outro robô.
    
    - robotName: Nome do robot que foi atingido.
    - robotDamage: Estragos do robot que foi atingido.
    - robotArmor: lista com o estado da armadura do robot que foi atingido.
    - relativeDirection: Direcção do robot que foi atingido relativamente ao nosso robô no momento da colisão.
    - robotDistance: Distância entre o robô atingido e o nosso.
    """
    def __init__( self, robotName, robotDamage, robotArmor, relativeDirection, robotDistance ):
        self.robotName = robotName
        self.robotDamage = robotDamage
        self.robotArmor = robotArmor
        self.relativeDirection = relativeDirection
        self.robotDistance = robotDistance


class ScanEvent():
    """
    Evento 'scan_event'.
    
    - objName: Nome do objecto que foi encontrado.
    - objEnergy: Energia do objecto que foi encontrado.
    - objDamage: Estragos do objecto que foi encontrado.
    - objArmor: Armadura do objecto que foi encontrado.
    - objPosition: Posição [x, y] do objecto que foi encontrado arredondado às centesimas.
    - objDirection: Direcção em graus do objectos que foi encontrado.
    - objRelativeDirection: Posição do objecto que foi encontrado relativamente à direcção do nosso robô.
    - objSpeed: Velocidade a que o bjecto que foi encontrado se move.
    - objDistance: Distancia do objecto encontrado em relação ao nosso robô.
    """
    def __init__( self, objList ):
        # Lista com os objectos encontrados
        self.objsList = []
        for obj in objList:
            self.objsList.append( ObjClass(*obj) )

    def found( self ):
        """
        Retorna 'True' quando foram encontrados objectos, ou 'Flase' quando não foram encontrados objectos.
        """
        if ( len(self.objsList) > 0 ):
            return True
        return False
    
    def pop( self ):
        """
        O robô pode utilizar este metodo para retirar um a um como numa stack os objectos encontrados.
        Quando fica sem objectos retorna 0 (zero).
        Outra forma do robô vir buscar os objectos encontrados é directamente à lista.
        Ex.: obj = event.objsList[ 0 ]
        Para copiar todos os objectos de uma só vez:
        Ex.: objects = event.objsList[ : ]
        """
        try:
            return self.objsList.pop( 0 )
        
        except IndexError:
            return 0
    
    def count( self ):
        """
        Retorna o número de objectos encontrados.
        """
        return len( self.objsList )



class ObjClass():
    def __init__(self, objName, objEnergy, objDamage, objArmor, objPosition, objDirection, objRelativeDirection, objSpeed, objDistance):
        self.objName = objName
        self.objEnergy = objEnergy
        self.objDamage = objDamage
        self.objArmor = objArmor
        self.objPosition = objPosition
        self.objDirection = objDirection
        self.objRelativeDirection = objRelativeDirection
        self.objSpeed = objSpeed
        self.objDistance = objDistance






class Robot():
    def __init__(self):
        # Dicionario de comandos recebidos
        self.commandsList = {
                            # Indica que o comando foi executado  e que pode continuar a enviar comandos.
                            'done': self._done,
                            # Indica que o round começou e que pode começar a enviar comandos
                            'round_started': self._round_started,
                            # Quando a sala de jogo foi fechada
                            'term_battle_room': self._term_battle_room,
                            # Quando a batalha termina
                            'term_battle': self._term_battle,
                            # Quando um comando válido é descartado pelo servidor
                            'command_dropped': self._command_dropped,
                            # Quando um comando é enviado com um argumento inválido
                            'invalid_arg_inf': self._invalid_arg,
                            # Quando o robô excede o número máximo de comandos inválidos
                            'invalid_arg_max': self._invalid_arg_max,
                            # Indica que foi destruido =/
                            'destroyed': self._destroyed,
                            # Quando um robot é retirado da batalha
                            'kicked_robot': self._kicked_robot,
                            # Recebido quando um dos outros robots é destruido
                            'robot_destroyed': self._robot_destroyed,
                            # Quando embate numa parede
                            'on_hit_wall': self._on_hit_wall,
                            # quando embate noutro robot
                            'on_hit_robot': self._on_hit_robot,
                            # Quando é atingido por uma bala
                            'on_hit_by_bullet': self._on_hit_by_bullet,
                            # Quando uma das nossas balas atinge um robot
                            'on_bullet_hit': self._on_bullet_hit,
                            # Quando a arma sobreaquece
                            'gun_overheat': self._gun_overheat,
                            # Quando o robot fica sem energia
                            'out_of_energy': self._out_of_energy,
                            # Quando um scan é terminado ou encontra algum objecto
                            'scan_event': self._scan_event,
                            #
                            'error': self._error,
                            
                            # GetCommands
                            'get_robot_position': self._get_robot_position,
                            'get_bf_size': self._get_bf_size,
                            'get_speed': self._get_speed,
                            'get_seq_num': self._get_seq_num,
                            'get_robot_dir': self._get_robot_dir,
                            'get_gun_dir': self._get_gun_dir,
                            'get_radar_dir': self._get_radar_dir,
                            'get_exec_mode': self._get_exec_mode,
                            'get_robots': self._get_robots,
                            'get_alive_robots': self._get_alive_robots,
                            'get_energy': self._get_energy,
                            'get_damage': self._get_damage,
                            'get_armor': self._get_armor,
                            'get_gun_temp': self._get_gun_temp,
                            'get_round': self._get_round,
                            'get_round_time': self._get_round_time,
                            'get_rounds_num': self._get_rounds_num,
                            'get_elapsed_time': self._get_elapsed_time,
                            'get_no_freeze_on': self._get_no_freeze_on,
                            'get_subscribed_events': self._get_subscribed_events,
                            'get_commands_queue': self._get_commands_queue,
                            'ping': self._ping,
                            'get_gun_lock': self._get_gun_lock,
                            'get_radar_lock': self._get_radar_lock,
                            None: None
                            }
        # Socket utilizado na comunicação com o interface
        self.sock = None
        # Buffer para o recv() do socket
        self.BUFFER_SIZE = 1024
        # Time-out para o socket
        # Não está a ser utilizado neste momento
        self.TIMEOUT = 30
        # IP da interface loopback para estabelecer conexão com o interface. 
        # Isto se o localhost estiver configurado com '127.0.0.1'
        self.LOCALHOST = 'localhost'  
        # Porta da interface
        self.PORT = 48080
        #
        self.EOL = "\r\n"
        #
        self.tmpData = ""




    def _shutdown(self):
        """
            Termina a conexão com o interface.
        """
        try:
            self.sock.close()
        except socket.error, err:
            print "\n!!! Erro em '_shutdown()'"
            print "!!! Descrição: " + str(err)


    def finish(self):
        exit( 0 )


        
    def init(self):
        """
        Primeiro metodo a ser invocado depois de ser criada a instancia da classe.
        """
        # Cria o socket
        if (self._create_socket() != 0):
            return -1
        
        # Estabelece ligação à Interface
        if (self._connect() != 0 ):
            return -1
        
        return self._wait_for_server()



    def _create_socket(self):
        """
        Cria o socket para a ligação à Interface.
        """
        try:
            print "\n>> A criar socket..."
            self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            #self.sock.settimeout( self.TIMEOUT )
            print ">> Socket criado!"
        
        except socket.error, err:
            print "!!! Ocorreu um erro ao criar o socket!"
            print "!!! Descrição: %s" % str(err)
            return -1
        
        return 0



    def _connect(self):
        """
        Estabelece a ligação à interface.
        """
        try:
            print ">> A estabelecer ligação com o Interface..."
            self.sock.connect((self.LOCALHOST, self.PORT))
            print ">> Conexão estabelecida com sucesso!"
            print ">> Robô Online!"
        
        except socket.error, err:
            print "!!! Ocorreu um erro ao tentar estabelecer ligação com o Interface!"
            print "!!! Descrição: %s" % str(err)
            return -1
        
        return 0  



    def _recv_from_server(self):
        try:
            data = self.sock.recv(self.BUFFER_SIZE)
            #print "Recebeu:"
            #print r"%s" % data
            return data
        except socket.error, err:
            print "!!! Ocorreu um erro em '_recv_from_server()'"
            print "!!! Descrição: " + str(err)

            return -1



    def _send_to_server(self, data):
        try:
            #print "%s ** Enviou:" % str(time())
            #print r"%s" % data
            self.sock.send(str(data) + self.EOL)
            return 0
        except socket.error, err:
            print "!!! Ocorreu um erro em '_send_to_server()'"
            print "!!! Descrição: " + str(err)

            return -1







    def _command_parser(self, data):
        """
        Separa do comando os argumentos
        """
        data += self.EOL
        r = re.compile(r"([a-zA-Z_]{2,40})\r\n$|([a-zA-Z_]{2,40})+\((.{1,1024})\)\r\n$")
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
            print "!!! Comando com um formato incorrecto."
            print "!!! Descrição: %s" % str( data )
            return (None, None)





    def _sync_data( self, data ):
        if ( (data[ -2 : ] != self.EOL) and (data != '') ):
            if ( self.tmpData == '' ):
                splited = data.split( self.EOL )
                self.tmpData = splited.pop()
                data = data[ :-len(self.tmpData) ]
            
            else:
                splited = data.split( self.EOL )
                self.tmpData += splited[0]
                data = data[ len(splited[0]): ]
                data = self.tmpData + data
                
                splited = data.split( self.EOL )
                self.tmpData = splited.pop()
                # Tem o IF para quando recebe o comando e só falta o '\n' e quando o recebe vem apenas o '\n' sem mais nada a seguir.
                # É pouco provável mas nunca se sabe...
                if len(self.tmpData) > 0 : data = data[ :-len(self.tmpData) ]
    
        else:
            if ( self.tmpData != '' ):
                data = self.tmpData + data
                self.tmpData = ''
    
        return data


    
    def _wait_for_server(self):
        retVal = 0
        data = self._recv_from_server()
        if ( (data == -1) or (data == "") ):
            self._shutdown()
            self.finish()
            return None
        
        # Sincroniza a informação recebida
        data = self._sync_data( data )
        while ( data == "" ):
            data = self._sync_data( data )
    
        # Separa os comandos no caso de ter recebido mais que um
        commands = data.split( self.EOL )
        # Retira o ultimo que está vazio
        commands.pop()
        for command in commands:
            com, args = self._command_parser( command )
            retVal = self.commandsList[ com ]( args )
        return retVal
    
    
                        













































    ##############################################################################################
    ####################################    Comandos do Robô    ##################################
    ##############################################################################################



    def robot_move_forward( self, val ):
        """
        Move o robot para a frente.
        """
        self._send_to_server( "robot_move_forward(" + str(val) + ")" )
        return self._wait_for_server()    
        
    def robot_move_backward( self, val ):
        """
        Move o robot para trás.
        """
        self._send_to_server( "robot_move_backward(" + str(val) + ")" )
        return self._wait_for_server()
    
    
    
    def robot_turn_right( self, val ):
        """
        Vira o robot para a direita se 'val' for positivo e para a esquerda se for negativo. 
        """
        self._send_to_server( "robot_turn_right(" + str(val) + ")" )
        return self._wait_for_server()


    def robot_turn_left( self, val ):
        """
        Vira o robot para a esquerda se 'val' for positivo e para a direita se for negativo.
        """
        self._send_to_server( "robot_turn_left(" + str(val) + ")" )
        return self._wait_for_server()


    def robot_turn_to( self, val ):
        """
        Vira o robot para uma direcção especifica.
        """
        self._send_to_server( "robot_turn_to(" + str(val) + ")" )
        return self._wait_for_server()







    def gun_turn_right( self, val ):
        """
        Vira a arma para a direita se 'val' for positivo e para a esquerda se for negativo.
        """
        self._send_to_server( "gun_turn_right(" + str(val) + ")" )
        return self._wait_for_server()


    def gun_turn_left( self, val ):
        """
        Vira a arma para a esquerda se 'val' for positivo e para a direita se for negativo.
        """
        self._send_to_server( "gun_turn_left(" + str(val) + ")" )
        return self._wait_for_server()
    

    def gun_turn_to( self, val ):
        """
        Vira a arma para uma direcção especifica.
        """
        self._send_to_server( "gun_turn_to(" + str(val) + ")" )
        return self._wait_for_server()

    
    def shoot( self ):
        """
        Dispara.
        """
        self._send_to_server( "shoot" )
        return self._wait_for_server()
    
    

    


    def radar_turn_right( self, val ):
        """
        Vira o radar para a direita se 'val' for positivo e para a esquerda se for negativo. 
        """
        self._send_to_server( "radar_turn_right(" + str(val) + ")" )
        return self._wait_for_server()


    def radar_turn_left( self, val ):
        """
        Vira o radar para a esquerda se 'val' for positivo e para a direita se for negativo.
        """
        self._send_to_server( "radar_turn_left(" + str(val) + ")" )
        return self._wait_for_server()


    def radar_turn_to( self, val ):
        """
        Vira o radar para uma direcção especifica.
        """
        self._send_to_server( "radar_turn_to(" + str(val) + ")" )
        return self._wait_for_server()


    def set_speed( self, val ):
        """
        Configura a velocidade a que o robot se movimenta para a frente ou para trás.
        Aceita apenas valores inteiros de 1 a 4 onde 1 é a velocidade mínima e  a velocidade máxima e por defeito.
        """
        self._send_to_server( "set_speed(" + str(val) + ")" )
        return self._wait_for_server()
        


    def scan( self, val = "right" ):
        """
        Faz um scan em busca de objectos no campo de batalha. Neste caso, robots adeversarios.
         - Aceita como argumentos(capitalização ignorada):
             - 'right' - No fundo não faz nada porque é o mesmo que sem argumento(sentido dos ponteiros do relógio).
             - 'left' - Inverte o sentido do scan, sendo iniciado para a esquerda(sentido inverso ao dos ponteiros do relógio).
             - 'here' - Faz um scan apenas na direcção para onde o radar está virado.
        
        Quando é dado sem argumento, utiliza o 'right'.
        """
        self._send_to_server( "scan(" + str(val) + ")" )
        return self._wait_for_server()

    
    
    def advanced_scan( self, val = "on" ):
        """
        Altera o modo de funcionamento do scan.
         - Aceita como argumentos(capitalização ignorada):
             - 'off' - Valor por defeito. Faz com que o radar gere o evento scan_event e pare o robot ao primeiro
                       objecto identificado.
             - 'on' - Activa o modo avançado do scan. Neste modo o scan só termina quando dá uma volta de 360º
                      e sempre que são encontrados objectos é gerado o evento 'scan_event'.
        
        Quando é dado sem argumento, utiliza o 'on'.
        """
        self._send_to_server( "advanced_scan(" + str(val) + ")" )
        return self._wait_for_server()
        




    def no_freeze_on( self, events ):
        """
        Serve para fazer com que determinados eventos não imobilizem o robô.
        Como argumento recebe uma string:
            - "all": Nenhum evento imobiliza o robô. Com a excepção de eventos como o 'out_of_energy', 'hit_on_wall',
                     'hit_on_robot'. Os dois ultimos só param movimentos como o 'robot_move_X' ou 'robot_turn_Y'.
        Exemplo de argumento:
            - "['on_hit_by_bullet', 'gun_overheat']"
        IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas. 
                      Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
        """
        self._send_to_server( "no_freeze_on(" + str(events) + ")" )
        return self._wait_for_server()

    def freeze_on( self, events ):
        """
        Serve para fazer com que determinados eventos imobilizem o robô.
        Por defeito todos imobilizam o robô.
        Como argumento recebe uma string:
            - "all": Todos os eventos imobilizam o robô.
            - "['on_hit_by_bullet', 'gun_overheat']"
        IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas. 
                      Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
        """
        self._send_to_server( "freeze_on(" + str(events) + ")" )
        return self._wait_for_server()
    
    def subscribe_events( self, events ):
        """
        Serve para configurar os eventos que o robô quer receber.
        Como argumento recebe uma string:
            - "all": subscreve todos os eventos.
            - "['on_hit_by_bullet', 'gun_overheat']"
        IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas. 
                      Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
        """
        self._send_to_server( "subscribe_events(" + str(events) + ")" )
        return self._wait_for_server()

    def unsubscribe_events( self, events ):
        """
        Serve para configurar os eventos que o robô não quer receber.
        Como argumento recebe uma string:
            - "all": Não recebe nenhum evento que seja configurável.
            - "['on_hit_by_bullet', 'gun_overheat']"
        IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas. 
                      Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
        """
        self._send_to_server( "unsubscribe_events(" + str(events) + ")" )
        return self._wait_for_server()

    def noop( self ):
        """
        Faz reset ao contador de inactividade do robô.
        noop -> No Operation
        """
        self._send_to_server( "noop" )
        return self._wait_for_server()

    def stop( self ):
        """
        Imobiliza o robô
        """
        self._send_to_server( "stop" )
        return self._wait_for_server()

    def lock_gun_on_robot( self, flag ):
        """
        Faz com que a arma vire junto ao robô e vice-versa.
        """
        self._send_to_server( "lock_gun_on_robot(" + str(flag) + ")" )
        return self._wait_for_server()

    def lock_radar_on_robot( self, flag ):
        """
        Faz com que o radar vire junto ao robô e vice-versa.
        """
        self._send_to_server( "lock_radar_on_robot(" + str(flag) + ")" )
        return self._wait_for_server()

    def lock_gun_on_radar( self, flag ):
        """
        Faz com que a arma vire junto ao radar e vice-versa.
        """
        self._send_to_server( "lock_gun_on_radar(" + str(flag) + ")" )
        return self._wait_for_server()

    ##############################################################################################
    ##############################################################################################
    







    

    ####################################### Comandos de Controlo ############################################
    
    def exec_mode(self, val):
        """
        Configura o modo de execução.
        """
        result = self._send_to_server( "exec_mode(" + str(val) + ")" )
        if ( result == -1 ):
            self._shutdown()
            self.finish()
            return result
        
        return self._wait_for_server()




    def execute(self):
        """
        Comando que dá a ordem para executar os comandos na stack, quando se está a utilizar o modo 'block'.
        """
        result = self._send_to_server( "execute" )
        if ( result == -1 ):
            self._shutdown()
            self.finish()
            return result
        
        return self._wait_for_server()


    ##############################################################################################
    ##############################################################################################    
    
    
    
    ##############################################################################################
    ################################      Eventos     ############################################
    ##############################################################################################
    


    
    def _done(self, args = None):
        """
        - args : Recebido pelo robot quando um comando ou um bloco de comandos é executado na totalidade. 
                 O seu argumento (seqNum) representa a sequencia de comandos quando enviado pelo servidor,
                 'None' quando o 'done' é enviado pelo ServerInterfacee neste caso pode ser ignorado. Pode ainda
                 ser 'invalid_arg' ou 'command_dropped'.
                 No fundo serve para saber a que comando(s) pertence o 'done' recebido. 
                 Bastante útil no modo 'non-lock' e em casos especificod do 'block'.
                 É incrementado a cada comando aceite pelo servidor. O que é recebido no 'done' representa o 
                 último comando que terminou a sua execução.
                     
                 - FARÁ SENTIDO O 'port_module' FAZER O CONTROLO DESTA SEQUENCIA OU SERÁ MELHOR SER O ROBOT A 
                 IMPLEMENTAR ESSA FUNCIONALIDADE..?
        """
        self.done( args )
        return "done"
    
    def done( self, arg ):
        pass
    
    
    def _round_started( self, args = None ):
        """
        Invocado quando um novo round é iniciado.
        
        - args : Número do round que acabou de iniciar.
        """
        self.round_started( int(args) )
        return "round_started"
        
    def round_started( self, roundNum ):
        pass
        




    def _term_battle_room( self, args = None ):
        """
        Invocado quando a sala de jogo é terminada.
        
        - args : None.
        """
        self.term_battle_room()
        return "term_battle_room"
        
    def term_battle_room( self ):
        print "\nterm_battle_room()"
        exit( 0 )



    def _term_battle( self, args = None ):
        """
        Invocado quando a sala de jogo é terminada.
        
        - args : Nome da batalha.
        """
        self.term_battle()
        return "term_battle"
        
    def term_battle( self ):
        print "\nterm_battle()"
        exit( 0 )



    ######################################################################################################
    ####################################### Eventos da Batalha ###########################################
    ######################################################################################################
    def _command_dropped( self, args = None ):
        """
        Quando um comando válido é descartado pelo servidor.
         - args:
             - lista com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
        """
        arg = eval(args)
        self.command_dropped( arg )
        return "command_dropped"
        
    def command_dropped( self, command ):
        pass
    
    
    def _invalid_arg( self, args = None ):
        """
        Recebido quando um dos comandos enviados tem um argumento inválido.
         - args:
             - lista com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
        """
        arg = eval( args )
        self.invalid_arg( arg )
        return "invalid_arg"
        
    def invalid_arg( self, command ):
        pass


    def _invalid_arg_max( self, args = None ):
        """
        Recebido quando o robô envia mais de X comandos seguidos com o argumento inválido.
         - args:
             - lista com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
        """
        arg = eval( args )
        self.invalid_arg_max( arg )
        return "invalid_arg_max"
        
    def invalid_arg_max( self, command ):
        pass


    
    def _destroyed( self, args = None ):
        """
        Recebido quando o nosso robot é destruído.
        
        - args : Nome do robot que destruío o nosso robot OU 'None' se o robot for destruido por embater numa parede.
        """
        self.destroyed( args )
        # Neste cado, uma vez que não pode enviar comandos porque o robot foi destuído, vai aguardar o inicio 
        # do novo ciclo
        return  self._wait_for_server()
         
    def destroyed( self, args ):
        pass
    




    def _kicked_robot( self, args = None ):
        """
        Recebido quando um robot é retirado da batalha.
        Só é recebido quando a batalha está a decorrer.
        
        - args: Nome do robô que foi retirado.
        """
        self.kicked_robot( str(args) )
        return "kicked_robot"
    
    def kicked_robot( self, robotName ):
        pass




    def _robot_destroyed( self, args = None ):
        """
        Recebido quando um dos outros robots é destruido.
        
        - args : Nome do robot que foi destruído.
        """
        self.robot_destroyed( args )
        return "robot_destroyed"

    def robot_destroyed( self, args ):
        pass





    def _on_hit_wall( self, args = None ):
        """
        Quando o nosso robot embate numa parede.
        
        - args : Parede onde embateu. top | right | bottom | left
        """
        self.on_hit_wall( args )
        return "on_hit_wall"

    def on_hit_wall( self, args = None ):
        pass




    def _on_hit_robot( self, args = None ):
        """
        Quando um robot embate noutro robot.
        
        - robotName: Nome do robot em que embateu.
        - robotDamage: Estragods do robot em que embateu.
        - robotArmor: lista com o estado da armadura do robot em que embateu.
        - relativeDirection: Direcção em que o robô adversário embateu relativamente 
                             à direcção do nosso robô. Na prática este valor é útil 
                             para virar o robô, arma ou radar na direcção do robô em 
                             que se embateu utilizando o comando “robot_turn_to()”, 
                             “gun_turn_to()” ou “radar_turn_to()”.
        """
        args = eval( args )
        robotName = args[ 0 ]
        robotDamage = args[ 1 ]
        robotArmor = args[ 2 ]
        relativeDirection = args[ 3 ]

        event = OnHitRobotEvent( robotName, robotDamage, robotArmor, relativeDirection )
        self.on_hit_robot( event )
        return "on_hit_robot"
        
    def on_hit_robot( self, event ):
        pass
    
    
    
    def _on_hit_by_bullet( self, args = None ):
        """
        Quando o robot é atingido por uma bala.
        
        - robotName: Nome do robot que disparou a bala.
        - relativeDirection: Direcção do robô que disparou a bala relativamente ao nosso robô.
        """
        args = eval( args )
        robotName = args[ 0 ]
        relativeDirection = args[ 1 ]

        event = OnHitByBulletEvent( robotName, relativeDirection )
        self.on_hit_by_bullet( event )
        return "on_hit_by_bullet"

    def on_hit_by_bullet( self, event ):
        pass



    def _on_bullet_hit( self, args = None ):
        """
        Quando uma das nossas balas atinge outro robot.
        
        args( robotName, robotArmor, robotDamage, robotEnergy, relativeDirection )
        
        - robotName: Nome do robot que foi atingido.
        - robotDamage: Estragos do robot que foi atingido.
        - robotArmor: lista com o estado da armadura do robot que foi atingido.
        - robotRelativeDirection: Direcção do robot que foi atingido relativamente ao nosso robô no momento da colisão.
        - robotDistance: Distância entre o robô atingido e o nosso.
        """
        args = eval( args )
        robotName = args[ 0 ]
        robotDamage = args[ 1 ]
        robotArmor = args[ 2 ]
        robotRelativeDirection = args[ 3 ]
        robotDistance = args[ 4 ]

        event = OnBulletHitEvent( robotName, robotDamage, robotArmor, robotRelativeDirection, robotDistance )
        self.on_bullet_hit( event )
        return "on_bullet_hit"

    def on_bullet_hit( self, event ):
        pass


    def _gun_overheat( self, args = None ):
        self.gun_overheat()
        return "gun_overheat"
    def gun_overheat( self ):
        #print "-gun_overheat( )"
        pass


    def _out_of_energy( self, args = None ):
        self.out_of_energy()
        return "out_of_energy"
    def out_of_energy( self ):
        #print "-out_of_energy( )"
        pass


    def _scan_event( self, args = None ):
        """
        args = [   [ objName, objEnergy, objDamage, objArmor, objPosition, objDirection, objRelativeDirection, objSpeed, objDistance ]   ]
        - objName: Nome do objecto que foi encontrado.
        - objEnergy: Energia do objecto que ofi encontrado.
        - objDamage: Estragos do objecto que foi encontrado.
        - objArmor: Armadura do objecto que foi encontrado.
        - objPosition: Posição (x, y) do objecto que foi encontrado arredondado às centesimas.
        - objDirection: Direcção em graus do objectos que foi encontrado.
        - objRelativeDirection: Posição do objecto que foi encontrado relativamente à direcção do nosso robot.
        - objSpeed: Velocidade a que o bjecto que foi encontrado se move.
        - objDistance: Distancia do objecto encontrado em relação ao nosso robot.
        """
        args = eval( args )
        objList = []
        for obj in args:
            objName = args[ 0 ][ 0 ]
            objEnergy = args[ 0 ][ 1 ]
            objDamage = args[ 0 ][ 2 ]
            objArmor = args[ 0 ][ 3 ]
            objPosition = args[ 0 ][ 4 ]
            objDirection = args[ 0 ][ 5 ]
            objRelativeDirection = args[ 0 ][ 6 ]
            objSpeed = args[ 0 ][ 7 ]
            objDistance = args[ 0 ][ 8 ]
            
            objList.append( [objName, objEnergy, objDamage, objArmor, objPosition, objDirection, objRelativeDirection, objSpeed, objDistance] )
        
        event = ScanEvent( objList )
        self.scan_event( event )
        return "scan_event"
        
    def scan_event( self, event ):
        pass
    
    
    
    def _error( self, args = None ):
        """
        Recebido quando alguma coisa corre mal no ServerInterface.
        
        args - String com a indicação do problema.
        """
        self.error( args )
        return "error"
        
    def error( self, err ):
        pass




    #####################################   GetCommands   #########################################
    
    def get_robot_position( self ):
        self._send_to_server( "get_robot_position" )
        return self._wait_for_server()
    
    def _get_robot_position( self, args = None ):
        """
        Resposta do servidor.
        """
        position = eval( args )
        return position
    



    def get_bf_size( self ):
        self._send_to_server( "get_bf_size" )
        return self._wait_for_server()
    
    def _get_bf_size( self, args = None ):
        """
        Resposta do servidor.
        """
        size = eval( args )
        return size


    def get_speed( self ):
        self._send_to_server( "get_speed" )
        return self._wait_for_server()
    
    def _get_speed( self, args = None ):
        """
        Resposta do servidor.
        """
        speed = int( args )
        return speed


    def get_seq_num( self ):
        self._send_to_server( "get_seq_num" )
        return self._wait_for_server()
    
    def _get_seq_num( self, args = None ):
        """
        Resposta do servidor.
        """
        seqNum = int( args )
        return seqNum


    def get_robot_dir( self ):
        self._send_to_server( "get_robot_dir" )
        return self._wait_for_server()
        
    def _get_robot_dir( self, args = None ):
        """
        Resposta do servidor.
        """
        dir = round( float(args), 2 )
        return dir


    def get_gun_dir(self):
        self._send_to_server("get_gun_dir")
        return self._wait_for_server()
        
    def _get_gun_dir( self, args = None ):
        """
        Resposta do servidor.
        """
        dir = round( float(args), 2 )
        return dir



    def get_radar_dir(self):
        self._send_to_server("get_radar_dir")
        return self._wait_for_server()
        
    def _get_radar_dir( self, args = None ):
        """
        Resposta do servidor.
        """
        dir = round( float(args), 2 )
        return dir


    def get_exec_mode(self):
        self._send_to_server("get_exec_mode")
        return self._wait_for_server()
        
    def _get_exec_mode( self, args = None ):
        """
        Resposta do servidor.
        """
        mode = str( args )
        return mode


    def get_robots(self):
        self._send_to_server("get_robots")
        return self._wait_for_server()
        
    def _get_robots( self, args = None ):
        """
        Resposta do servidor.
        """
        robots = eval( args )
        return robots


    def get_alive_robots(self):
        self._send_to_server("get_alive_robots")
        return self._wait_for_server()
        
    def _get_alive_robots( self, args = None ):
        """
        Resposta do servidor.
        """
        robots = eval( args )
        return robots

    
    def get_energy(self):
        self._send_to_server("get_energy")
        return self._wait_for_server()
        
    def _get_energy( self, args = None ):
        """
        Resposta do servidor.
        """
        energy = round( float(args), 1 )
        return energy
    

    def get_damage(self):
        self._send_to_server("get_damage")
        return self._wait_for_server()
        
    def _get_damage( self, args = None ):
        """
        Resposta do servidor.
        """
        damage = int( args )
        return damage


    def get_armor(self):
        self._send_to_server("get_armor")
        return self._wait_for_server()
        
    def _get_armor( self, args = None ):
        """
        Resposta do servidor.
        """
        armor = eval( args )
        return armor


    def get_gun_temp(self):
        self._send_to_server("get_gun_temp")
        return self._wait_for_server()
        
    def _get_gun_temp( self, args = None ):
        """
        Resposta do servidor.
        """
        temp = round( float(args), 1 )
        return temp


    def get_round(self):
        self._send_to_server("get_round")
        return self._wait_for_server()
        
    def _get_round( self, args = None ):
        """
        Resposta do servidor.
        """
        round = int( args )
        return round


    def get_round_time(self):
        self._send_to_server("get_round_time")
        return self._wait_for_server()
        
    def _get_round_time( self, args = None ):
        """
        Resposta do servidor.
        """
        roundT = int( args )
        return roundT


    def get_rounds_num(self):
        self._send_to_server("get_rounds_num")
        return self._wait_for_server()
        
    def _get_rounds_num( self, args = None ):
        """
        Resposta do servidor.
        """
        roundNum = int( args )
        return roundNum


    def get_elapsed_time( self ):
        self._send_to_server("get_elapsed_time")
        return self._wait_for_server()
        
    def _get_elapsed_time( self, args = None ):
        """
        Resposta do servidor.
        """
        elapsedTime = round( float(args), 2 )
        return elapsedTime


    def get_no_freeze_on( self ):
        self._send_to_server("get_no_freeze_on")
        return self._wait_for_server()
        
    def _get_no_freeze_on( self, args = None ):
        """
        Resposta do servidor.
        """
        freezeOn = eval( args )
        return freezeOn


    def get_subscribed_events( self ):
        self._send_to_server("get_subscribed_events")
        return self._wait_for_server()
        
    def _get_subscribed_events( self, args = None ):
        """
        Resposta do servidor.
        """
        freezeOn = eval( args )
        return freezeOn


    def get_commands_queue( self ):
        self._send_to_server("get_commands_queue")
        return self._wait_for_server()
        
    def _get_commands_queue( self, args = None ):
        """
        Resposta do servidor.
        """
        freezeOn = eval( args )
        return freezeOn


    def ping( self ):
        """
        Calcula o tempo que os pedidos demoram entre o cliente e o servidor MAIS o tempo que o servidor demora a processar o comando.
        O valor retornado é metado do resultado para que conte apenas um dos sentidos(cliente->servidor), logo,
        este valor passa a ver um genero de estimativa.
        Em segundos.
        """
        initTime = time()
        self._send_to_server( "ping" )
        retVal = self._wait_for_server()
        delay = round( ((time() - initTime) / 2), 3 )
        return delay

    def _ping( self, args = None ):
        """
        Resposta do servidor.
        """
        return None


    def get_gun_lock( self ):
        self._send_to_server("get_gun_lock")
        return self._wait_for_server()
        
    def _get_gun_lock( self, args = None ):
        """
        Resposta do servidor.
        """
        lock = str( args )
        return lock


    def get_radar_lock( self ):
        self._send_to_server("get_radar_lock")
        return self._wait_for_server()
        
    def _get_radar_lock( self, args = None ):
        """
        Resposta do servidor.
        """
        lock = str( args )
        return lock
    ##############################################################################################
    ##############################################################################################  
