#!/usr/bin/env python
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

import pygtk
pygtk.require('2.0')
import re
from time import sleep

# Estes estão aqui misturados porque dá erro se o gui for importado depois do pygame!
# ISTO ACONTECE QUANDO INSTALEI O PYGTK ALL IN ONE NO WINDOWS
from ui.gui import *
import pygame

from auth.cauth_mod import CAuth
from interface.ServerInterface import ServerInterface
from log.logging_mod import Logging
log = Logging()
printd = log.debug
printi = log.info
printe = log.error
printw = log.warning


#
gtk.gdk.threads_init()



# Indica se o jogador esta ou não autenticado
autenticated = False
# Nome de utilizador com que o jogador se autenticou
playerName = ""
#
playersList = []
# Intervalo em que é feito o keepalive. Em segundos.
TIMER = 5
# ID do timer do keepalive
timerID = -1
# Instância da classe Interface
interface = ServerInterface()
#
EOL = "\r\n"







def auth_callback(value):
    """
    Callback utilizada para a autenticação dos jogadores.
    Quando um jogador termina a autenticação com ou sem sucesso, esta função é invocada.
    """
    global autenticated
    global playerName
    global interface
    global TIMER
    global timerID
    
    if (value != False):
        autenticated = True
        playerName = value
        # Actualiza o estado a barra de estado
        gobject.idle_add(gui.set_status_bar, 'Ligado! Sessão Iniciada Como ' + str(playerName))
        # Depois de estar autenticado, o jogador já pode pedir a lista das batalhas.
        gobject.idle_add(gui.buttonRefresh.set_sensitive, True)
        gobject.idle_add(gui.buttonCreate.set_sensitive, True)
        gobject.idle_add(gui.menuBarLogin.set_sensitive, True)
        # Por razões de compatibilidade com o python 2.6 é utilizado o metodo 'get_child()'
        gobject.idle_add(gui.menuBarLogin.get_child().set_label, 'Terminar Sessão')
        # Inicia o keepalive
        timerID = gobject.timeout_add_seconds( TIMER, interface.keepalive )
        return
        
    interface.shutdown()
    gobject.idle_add(gui.menuBarLogin.set_sensitive, True)
    gobject.idle_add(gui.set_status_bar, 'Desconectado...')



def exit_callback():
    global interface
    global exit
    # Indica que é mesmo para terminar o programa
    exit = 1
    interface.shutdown()
    gtk.main_quit()


def login_callback(widget=None):
    """
    Callback para o botão de login.
    """
    global interface
    global gui
    result = interface.create_sockets()
    # Caso não tenha criado os sockets
    if (result != 0):
        gobject.idle_add(gui.set_status_bar, 'Desconectado...')
        gobject.idle_add(gui.menuBarLogin.set_sensitive, True)
        return
    
    # Actualiza o estado a barra de estado
    gobject.idle_add(gui.set_status_bar, 'A Conectar ao Servidor...')

    # Conecta ao servidor
    result = interface.conn_to_srv()
    if (result != 0):
        interface.shutdown()
        # Actualiza o estado a barra de estado
        gobject.idle_add(gui.set_status_bar, 'Desconectado...')
        gobject.idle_add(gui.menuBarLogin.set_sensitive, True)
        
    else:
        # Actualiza o estado da barra de estado
        gobject.idle_add(gui.set_status_bar, 'Conectado ao Servidor! Inserir Credenciais...')
        # Client Authetication Module
        cam = CAuth(interface.interfaceSock, auth_callback)
        gobject.idle_add(cam.start)
    

def logout_callback(widget=None):
    global interface
    global gui
    global playerName
    playerName = ""
    # Actualiza o estado a barra de estado
    gobject.idle_add(gui.set_status_bar, 'Desconectado...')
    gobject.idle_add(gui.menuBarLogin.set_sensitive, True)
    gobject.idle_add(gui.buttonRefresh.set_sensitive , False)
    gobject.idle_add(gui.buttonCreate.set_sensitive, False)
    # Por razões de compatibilidade com o python 2.6 é utilizado o metodo 'get_child()'
    gobject.idle_add(gui.menuBarLogin.get_child().set_label, 'Iniciar Sessão')
    gobject.idle_add(gui.lsBattlesList.clear)
    interface.shutdown()


def parse_battles_list(data):
    """
    Recebe uma string com a lista das batalhas, separa essa lista do comando que a precede, e,
    converte numa 'list'
    """
    r = re.compile(r"(\[\])$|(_battles_list\()+(.{1,1024})\)\r\n$")
    
    groups = r.match(data)
    if (groups != None):
        # Caso o comando enviado seja um comando sem argumentos tipo o 'server_state', o grupo será o numero 1.
        # Caso seja um comando com argumentos tipo o 'robot_turn_left(90)', os grupos serao o segundo e o terceiro.
        # Por isso a necessidade deste cilo IF.
        if (groups.group(1) == None):
            return eval(groups.group(3))
        else:
            return []
        
    else:
        return []


def _con_fail():
    global gui

    gtk.gdk.threads_enter()
    md = GenericMessageDialog(gui, 'A ligação ao servidor foi terminada inesperadamente.', gtk.MESSAGE_ERROR)
    gtk.gdk.threads_leave()
    gobject.idle_add(md.show_it)
    logout_callback()


def get_battles_list_callback():
    """
    - Faz o pedido da lista das batalhas ao servidor.
    - Recebe a lista.
    - Actualiza a lista na GUI.
    """
    global interface
    global gui
    global EOL
    
    # Actualiza o estado a barra de estado
    gobject.idle_add(gui.set_status_bar, 'A Pedir Lista de Batalhas ao Servidor...')    

    # Pede ao servidor a lista das salas disponíveis
    retVal = interface.send_to_server("get_battles_list")
    if ( retVal == -1 ):
        _con_fail()
        return False
    
    # Provoca um atraso de 2 segundos para que o jogador não comece a clicar muitas vezes seguidas
    # E a segunda função deste sleep é esperar um pouco pela resposta do servidor (ANTES do sock.rec())
    # Para o caso de já ter qualquer coisa no buffer, não retornar logo o que está no buffer e nem esperar pela
    # resposta com a lista da batalhas
    sleep(0.5)
    
    data = interface.recv_from_server()
    
    # Quando há erro no socket
    if (data != -1):
        # Retira o último "" para não ficar um campo em branco na lista do 'split'
        data = data.strip( EOL )
        splitedData = data.split( EOL )
        for data in splitedData:
            data += EOL
            result = command_parser(data)
            if (result != -1):
                command, args = result
                # Verifica se é mesmo uma lista de batalhas, porque podem ficar comandos acumulados no buffer
                if (command == '_battles_list'):
                    # Separa a lista das batalhas do comando
                    #_battles_list([['Sample Battle 1', 1, 1, 2, 10, 'NuGuN', False]])
                    data = parse_battles_list(data)
                    break
            
            data = []
    # Como quando há erros no socket, é retornado '-1' e o 'parse_battles_list' só aceita strings ou buffers
    else:
        data = []

    # Actualiza a GUI com a lista das batalhas
    gobject.idle_add( gui.create_list, data )

    # Actualiza o estado da barra de estado
    gobject.idle_add( gui.set_status_bar, 'Ligado!' )
    gobject.idle_add( gui.buttonRefresh.set_sensitive, True )



####################################################################################

def has_password_callback(password):
    global interface
    command = 'battle_password'
    # Quando a password é '-1' é porque o jogador cancelou a entrada na batalha
    if (password == -1):
        interface.send_to_server(interface.CANCEL_JOIN)
    else:
        interface.send_to_server(command + '(' + password + ')')


def repeated_battle_name(arg=None):
    global gui
    printi("repeated_battle_name")
    gtk.gdk.threads_enter()
    md = GenericMessageDialog(gui, 'Já existe uma batalha com um nome igual!', gtk.MESSAGE_ERROR)
    gtk.gdk.threads_leave()
    gobject.idle_add(md.show_it)


def full_battle(args=None):
    global gui
    printi("full_battle")
    gtk.gdk.threads_enter()
    md = GenericMessageDialog(gui, 'A batalha na qual está a tentar entrar está cheia!', gtk.MESSAGE_ERROR)
    gtk.gdk.threads_leave()
    gobject.idle_add(md.show_it)
    

def join_fail(args=None):
    global gui
    printi("join_fail")
    gtk.gdk.threads_enter()
    md = GenericMessageDialog(gui, 'Não foi possível entrar na batalha.', gtk.MESSAGE_ERROR)
    gtk.gdk.threads_leave()
    gobject.idle_add(md.show_it)
    

def battle_doesnt_exist(args=None):
    global gui
    printi("battle_doesnt_exist")
    gtk.gdk.threads_enter()
    md = GenericMessageDialog(gui, 'A batalha em que está a tentar entrar não existe.', gtk.MESSAGE_ERROR)
    gtk.gdk.threads_leave()
    gobject.idle_add(md.show_it)


def battle_already_start(args=None):
    global gui
    printi("battle_already_start")
    gtk.gdk.threads_enter()
    md = GenericMessageDialog(gui, 'A batalha na qual está a tentar entrar já foi iniciada.', gtk.MESSAGE_ERROR)
    gtk.gdk.threads_leave()
    gobject.idle_add(md.show_it)


def has_password(arg=None):
    """
    É invocada quando o jogador está a tentar entrar numa batalha com password.
    """
    global gui
    global askDialog
    printi("has_password")
    
    gtk.gdk.threads_enter()
    askDialog = AskForPassword(has_password_callback, gui)
    gtk.gdk.threads_leave()
    gobject.idle_add(askDialog.get_password)


def players_list(list):
    """
    Quando o jogador entra numa batalha e receba lista de jogadores.
    Termina o 'mainloop' do pygtk e inicia a sala de batalha.
    
    'list' - Lista com os jogadores na batalha
    """
    global gui
    global playersList
    printi("players_list(" + str(list) + ")")
    
    # Converte a lista numa string
    playersList = eval(list)

    gobject.idle_add(gui.hide_all)
    #gobject.idle_add( gui.destroy )
    gobject.idle_add(gtk.main_quit)
    

def command_parser(data):
    """
    Separa o comando dos argumentos.
    """
    #r = re.compile(r"([a-z_]{2,40})\r\n$|([a-z_]{2,40})+\(([a-zA-Z0-9, ]{1,1024})\)\r\n$")
    r = re.compile(r"([a-z_]{2,40})\r\n$|([a-z_]{2,40})+\((.{1,1024})\)\r\n$")
    groups = r.match(str(data))
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



def create_battle_callback( battleConf ):
    global interface
    global playerName
    commandsDict = {
                    '_repeated_battle_name': repeated_battle_name,
                    '_join_fail': join_fail,
                    '_players_list': players_list
                    }
    # Limpa alguma informação que tenha ficado por ler de uma batalha anterior
    # Serve para evitar o problema de quando a janela é fechada durante uma batalha e em seguida se tenta criar outra batalha
    # e existe um _term_battle_room esquecido
    interface.flush_socket()
    # Cria uma batalha e automaticamente entra nela
    command = 'create_battle' + str( battleConf )
    # Envia para o servidor a informação para criar uma nova batalha
    interface.send_to_server( command )
    # Configura já o nome da batalha onde o jogador está a tentar entrar
    battleName = battleConf[ 0 ]
    interface.battleRoom.set_battle_name( battleName )
    # Configura a duração de cada round.
    # É utilizado para mostrar no titulo da janela o tempo a passar.
    interface.battleRoom.set_time( battleConf[5] )
    # Escreve o titulo
    #interface.battleRoom.set_title()
    # Configura a flag que indica que o jogador local é o owner da batalha
    interface.battleRoom.set_owner( True )
    # Carrega o nome do jogador local
    # É utilizado para actualizar o estado do robot (player_ready ou player_not_ready)
    interface.battleRoom.set_player_name( playerName )
    # Respostas possíveis:
    #  * '' - Servidor desconectou
    #  * '_repeated_battle_name' - O nome da batalha que se está a tentar criar já existe
    #  * '_join_fail' - Quando por algum motivo a batalha é criada mas não é possível colocar o jogadpr dentro da mesma
    #  * '_players_list' - Indica que a batalha foi criada e que o jogador entrou na mesma.
    data = interface.recv_from_server()
    # Por ser o fecho da conexão com o servidor, tem um tratamento diferente
    if (data == '' or data == -1):
        global gui
        printw("A conexão ao servidor foi terminada inesperadamente.")
        gtk.gdk.threads_enter()
        md = GenericMessageDialog(gui, 'A conexão ao servidor foi terminada inesperadamente!', gtk.MESSAGE_ERROR)
        gtk.gdk.threads_leave()
        gobject.idle_add(md.show_it)
        # Faz logout uma vez que a conexão foi a baixo
        logout_callback()
    # Verifica se é um comando válido e caso seja, separa o comando dos argumentos caso tenha argumentos
    result = command_parser(data)
    if (result != -1):
        command, args = result
        # Verifica se o comando é um comando esperado
        if (command in commandsDict.keys()):
            commandsDict[ command ](args)
        # Quando é um comando inesperado
        else:
            printw("O comando recebido não é um comando esperado.")
            printw("Descrição: " + str(command))
            return -1            
    # Quando a informação recebida não é um comando válido
    else:
        printw("A informação enviada pelo servidor é inválida.")
        printw("Descrição: " + str(data))
        return -1


def join_battle_callback(battleName):
    global interface
    global playerName
    global EOL
    commandsDict = {
                    '_full_battle': full_battle,
                    '_join_fail': join_fail,
                    '_battle_doesnt_exist': battle_doesnt_exist,
                    '_battle_already_start': battle_already_start,
                    '_has_password': has_password,
                    '_players_list': players_list
                    }
    # Limpa alguma informação que tenha ficado por ler de uma batalha anterior
    # Serve para evitar o problema de quando a janela é fechada durante uma batalha e em seguida se tenta criar outra batalha
    # e existe um _term_battle_room esquecido
    interface.flush_socket()
    # Cria uma batalha e automaticamente entra nela
    command = 'join_battle(' + str(battleName) + ')'
    # Envia para o servidor a informação para criar uma nova batalha
    interface.send_to_server(command)
    # Configura já o nome da batalha onde o jogador está a tentar entrar
    interface.battleRoom.set_battle_name(battleName)
    # Escreve o titulo
    interface.battleRoom.set_title()
    
    # Configura a flag que indica que o jogador local é o owner da batalha
    interface.battleRoom.set_owner(False)
    # Carrega o nome do jogador local
    # É utilizado para actualizar o estado do robot (player_ready ou player_not_ready)
    interface.battleRoom.set_player_name( playerName )
    
    while (1):
        # Respostas possíveis:
        #  * '' - Servidor desconectou
        #  * '_full_battle' - Indica que a batalha está cheia.
        #  * '_join_fail' - Quando por algum motivo a batalha é criada mas não é possível colocar o jogadpr dentro da mesma
        #  * '_has_password' - Indica que a batalha tem password e é preciso envia-la ao servidor
        #  * '_players_list' - Indica que a batalha foi criada e que o jogador entrou na mesma.
        interface.interfaceSock.settimeout( 60 )
        data = interface.recv_from_server()
        interface.interfaceSock.settimeout( interface.INTERFACE_SOCK_TIMEOUT )

        # Por ser o fecho da conexão com o servidor, tem um tratamento diferente
        if (data != '' and data != -1):
            # Retira o último "\r\n" para não ficar um campo em branco na lista do 'split'
            data = data.strip( EOL )
            splitedData = data.split( EOL )
            for data in splitedData:
                # Para não ter de alterar o metodo 'command_parser', porque ele está à espera que os comandos
                # enviados tenham todos essa terminação. Caso contrário são descartados 
                data += EOL
                # Verifica se é um comando válido e caso seja, separa o comando dos argumentos caso tenha argumentos
                result = command_parser(data)
                if (result != -1):
                    command, args = result
                    # Verifica se o comando é um comando esperado
                    if (command in commandsDict.keys()):
                        # Executa a função correspondente ao comando recebido
                        commandsDict[ command ](args)
                        if (command != '_has_password'):
                            return
                    # Quando é um comando inesperado
                    else:
                        printw("O comando recebido não é um comando esperado.")
                        printw("Descrição: " + str(command))
                        return        
                # Quando a informação recebida não é um comando válido
                else:
                    printw("A informação enviada pelo servidor é inválida.")
                    printw("Descrição: " + str(data))
                    return
        else:
            global gui
            global askDialog
            printw("Não foi recebida resposta do servidor ou ocorreu um erro na ligação!")
            gtk.gdk.threads_enter()
            md = GenericMessageDialog(gui, 'Não foi recebida resposta do servidor ou ocorreu um erro na ligação!', gtk.MESSAGE_ERROR)
            gtk.gdk.threads_leave()
            gobject.idle_add(md.show_it)
            try:
                gobject.idle_add(askDialog.dialog.destroy)
            except:
                pass
            
            has_password_callback( -1 )
            # Apenas para receber o '_join_fail' que o servidor vai enviar como resposta ao 'cancel_join'.
            # Para já fica assim... Para ficar como deve ser é preciso um 'main_loop', porque assim, mesmo com
            # o 'for' para ler vários comandos no buffer não é suficiente uma vez que os comandos chegam atrasados
            # e já não são apanhados na leitura do buffer. É preciso estar constantemente a ler o buffer...
            interface.interfaceSock.settimeout(5)
            interface.recv_from_server()
            interface.interfaceSock.settimeout(interface.INTERFACE_SOCK_TIMEOUT)
            break
    ####################################################################################
















if __name__ == '__main__' :
    
    exit = 0
    gui = BattlesListGUI(exit_callback, login_callback, logout_callback, get_battles_list_callback, create_battle_callback, join_battle_callback)
    gui.create_w()
    while (not exit):
        gui.show_all()
        gui.lsBattlesList.clear()
        
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
        # termina o timer
        if ( timerID != -1 ):
            gobject.source_remove( timerID )
            
        if (exit == 0):
            # Inicia os modulos necessários manualmente
            # Se utilizar pygame.init(), em Gentoo o pygame.quit() bloqueia porque um dos 6 modulos que é iniciado
            # não é terminado, o que faz com que a janela de jogo não seja fechada...
            pygame.display.init()
            pygame.font.init()
            result = interface.battleRoom.create()
            # Caso haja problemas ao criar a janela de jogo, volta à lista de batalhas
            if (result != -1):
                interface.battleRoom.add_players(playersList)
                interface.battleRoom.draw()
                exit = interface.main_loop()
                if ( exit == 0 ):
                    timerID = gobject.timeout_add_seconds( TIMER, interface.keepalive )
                    interface.keepalive()
            
            else:
                pygame.quit()
                
                # É preciso fazer um 'reset' à 'battleRoom' porque se terminar o main_loop do pygame e o voltar a iniciar
                # sem ter criado uma nova instância da 'battleRoom', o programa é fechado.
                # Penso que seja pela classe 'ScoreBoard' derivar da 'pygame.surface.Surface'
                del interface.battleRoom
                interface.battleRoom = BattleRoom()
                interface.send_to_server(interface.LEAVE_BATTLE)
    

