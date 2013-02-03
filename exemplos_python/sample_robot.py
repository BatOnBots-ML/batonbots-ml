# -*- coding:utf-8 -*-
'''
Created on 13 de Dez de 2010

@author: nugun
'''

from port_module import Robot
from time import sleep
import time


def round_started( roundNum ):
    print "round_started( " + str( roundNum ) + ' )'
    global alive
    alive = 0


def term_battle_room():
    print "term_battle_room()"

def term_battle():
    print "term_battle()"

def destroyed( robotName ):
    print "Destroyed( " + str( robotName ) + ' )'

def kicked_robot( robotName ):
    print "kicked_robot( " + str( robotName ) + ' )'

def robot_destroyed( robotName ):
    print "robot_destroyed( %s )" % str(robotName)


def on_hit_wall( event ):
    print "\non_hit_wall( %s )\n" % event.side


def on_hit_robot( event ):
    print "on_hit_robot()"
    print event.robotName
    print event.robotDamage
    print event.robotArmor
    print event.robotRelativeDirection


def on_hit_by_bullet( event ):
    print "on_hit_by_bullet()"
    print event.robotName
    print event.relativeDirection


def on_bullet_hit( event ):
    print "on_bullet_hit()"
    print event.robotName
    print event.robotDamage
    print event.robotArmor
    print event.robotRelativeDirection
    print event.robotDistance


def gun_overheat():
    print "Evento - gun_overheat()"


def out_of_energy():
    print "Evento - out_of_energy()"
    #time.sleep( 10 )


def scan_event( event ):
    for obj in event.objsList:
        print "**********************************"
        print obj.objName
        print obj.objEnergy
        print obj.objDamage
        print obj.objArmor
        print obj.objPosition
        print obj.objDirection
        print obj.objRelativeDirection
        print obj.objSpeed
        print obj.objDistance
    

def invalid_arg( command ):
    print "invalid_arg(%s)" % str(command)

def invalid_arg_max( command ):
    print "invalid_arg_max(%s)" % str(command)
    
def dropped_command( command ):
    print "dropped_command(%s)" % str(command)




def get_input():
    input = raw_input(">>Comando: ")
    splited = input.split( " " )
    if ( len(splited) == 1 ):
        splited.append( 90 )
    return splited



if __name__ == '__main__':

    #time.sleep(0.0098)

    moving = "forward"
    alive = 1
    # cria um robot
    robot = Robot()

    

    robot.round_started = round_started
    robot.term_battle_room = term_battle_room
    robot.term_battle = term_battle
    robot.destroyed = destroyed
    robot.kicked_robot = kicked_robot
    robot.robot_destroyed = robot_destroyed
    robot.on_hit_wall = on_hit_wall
    robot.on_hit_robot = on_hit_robot
    robot.on_hit_by_bullet = on_hit_by_bullet
    robot.gun_overheat = gun_overheat
    robot.out_of_energy = out_of_energy
    robot.on_bullet_hit = on_bullet_hit
    robot.scan_event = scan_event
    robot.invalid_arg = invalid_arg
    robot.invalid_arg_max = invalid_arg_max
    robot.dropped_command = dropped_command
    
    # Inicia o robot
    result = robot.init()
    # Nota Importante!!!!! 
    # No tutorial deve-se insitar a utilizar este comando mesmo que se esteja a utilizar o valor por defeito(lock)
    # porque se o jogador está a utilizar por exemplo o 'block', desconectar o robot mas não termina o Interface,
    # então o interface vai continuar com o 'block' e quando o jogador inicia o robot e não volta a colocar o 'lock'
    # o robot vai entrar em loop porque vai estar a constantemente a enviar comandos 
    #robot.exec_mode('lock')
    #robot.execute()
    
    while(1):
        alive = 1
        print "\n>> Iniciou o while\n"
        #robot.radar_turn_left( 300 )
        #robot.execute()
        #robot.shoot()
        #robot.execute()
        while (alive):
            print "\n>> executou o comando.\n"
            input = get_input()
            #input = ['', '']
            if ( input[0] == 'left' ):
                robot.robot_turn_left( input[1] )
                #robot.execute()
            elif ( input[0] == 'right' ):
                print "turn_right: %s" % str( robot.robot_turn_right( input[1] ) )
                #robot.execute()
            elif ( input[0] == 'turnto' ):
                robot.robot_turn_to( input[1] )
                #robot.execute()
            elif ( input[0] == 'forward' ):
                robot.robot_move_forward( input[1] )
                #robot.execute()
            elif ( input[0] == 'backward' ):
                robot.robot_move_backward( input[1] )
                #robot.execute()
            elif ( input[0] == 'gunright' ):
                robot.gun_turn_right( input[1] )
                robot.execute()
            elif ( input[0] == 'gunleft' ):
                robot.gun_turn_left( input[1] )
                robot.execute()
            elif ( input[0] == 'gunturnto' ):
                robot.gun_turn_to( input[1] )
                robot.execute()
            elif ( input[0] == 'radarright' ):
                robot.radar_turn_right( input[1] )
                robot.execute()
            elif ( input[0] == 'radarleft' ):
                robot.radar_turn_left( input[1] )
                robot.execute()
            elif ( input[0] == 'radarturnto' ):
                robot.radar_turn_to( input[1] )
                robot.execute()
            elif ( input[0] == 'shoot' ):
                robot.shoot()
                #robot.execute()
            elif ( input[0] == 'scan' ):
                robot.scan( "here" )
                #robot.execute()
            elif ( input[0] == 'speed' ):
                robot.set_speed( input[1] )
            elif ( input[0] == 'subscribe_events' ):
                robot.subscribe_events( "[" + input[1] + "]" )
            elif ( input[0] == 'unsubscribe_events' ):
                robot.unsubscribe_events( "[" + input[1] + "]" )
            elif ( input[0] == 'no_freeze_on' ):
                robot.no_freeze_on( "[" + input[1] + "]" )
            elif ( input[0] == 'freeze_on' ):
                robot.freeze_on( "[" + input[1] + "]" )
            elif ( input[0] == 'advanced_scan' ):
                robot.advanced_scan( input[1] )
            elif ( input[0] == 'exec' ):
                robot.execute()
            elif ( input[0] == 'exec_mode' ):
                robot.exec_mode( input[1] )

            elif ( input[0] == 'get_robot_position' ):
                print "::%s" % str(robot.get_robot_position())
            elif ( input[0] == 'get_bf_size' ):
                print "::%s" % str(robot.get_bf_size())
            elif ( input[0] == 'get_speed' ):
                print "::%s" % robot.get_speed()
            elif ( input[0] == 'get_seq_num' ):
                print "::%s" % robot.get_seq_num()
            elif ( input[0] == 'get_robot_dir' ):
                print "::%s" % robot.get_robot_dir()
            elif ( input[0] == 'get_gun_dir' ):
                print "::%s" % robot.get_gun_dir()
            elif ( input[0] == 'get_radar_dir' ):
                print "::%s" % robot.get_radar_dir()
            elif ( input[0] == 'get_exec_mode' ):
                print "::%s" % robot.get_exec_mode()
            elif ( input[0] == 'get_robots' ):
                print "::%s" % str(robot.get_robots())
            elif ( input[0] == 'get_alive_robots' ):
                print "::%s" % str(robot.get_alive_robots())
            elif ( input[0] == 'get_energy' ):
                print "::%s" % robot.get_energy()
            elif ( input[0] == 'get_damage' ):
                print "::%s" % robot.get_damage()
            elif ( input[0] == 'get_armor' ):
                print "::%s" % robot.get_armor()
            elif ( input[0] == 'get_gun_temp' ):
                print "::%s" % robot.get_gun_temp()
            elif ( input[0] == 'get_round' ):
                print "::%s" % robot.get_round()
            elif ( input[0] == 'get_round_time' ):
                print "::%s" % robot.get_round_time()
            elif ( input[0] == 'get_rounds_num' ):
                print "::%s" % robot.get_rounds_num()
            elif ( input[0] == 'get_elapsed_time' ):
                print "::%s" % robot.get_elapsed_time()
            elif ( input[0] == 'get_no_freeze_on' ):
                print "::%s" % str(robot.get_no_freeze_on())
            elif ( input[0] == 'get_subscribed_events' ):
                print "::%s" % str(robot.get_subscribed_events())
            elif ( input[0] == 'get_commands_queue' ):
                print "::%s" % str(robot.get_commands_queue())
            elif ( input[0] == 'ping' ):
                print "::%s" % robot.ping()
            elif ( input[0] == 'get_gun_lock' ):
                print "::%s" % str(robot.get_gun_lock())
            elif ( input[0] == 'get_radar_lock' ):
                print "::%s" % str(robot.get_radar_lock())
                
            elif ( input[0] == 'stop' ):
                print "::%s" % robot.stop()
            elif ( input[0] == 'lock_gun_on_robot' ):
                print "::%s" % robot.lock_gun_on_robot( input[1] )
            elif ( input[0] == 'lock_radar_on_robot' ):
                print "::%s" % robot.lock_radar_on_robot( input[1] )
            elif ( input[0] == 'lock_gun_on_radar' ):
                print "::%s" % robot.lock_gun_on_radar( input[1] )
                
                

            elif ( input[0] == 'teste' ):
                robot.robot_turn_to( robot.get_gun_dir() )
            elif ( input[0] == 'teste2' ):
                robot.robot_turn_to(180)
                robot.gun_turn_to(180)
            elif ( input[0] == 'teste3' ):
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.execute()
            elif ( input[0] == 'teste4' ):
                robot.robot_move_forward( 1000 )
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.execute()
            elif ( input[0] == 'teste5' ):
                robot.robot_move_forward( 100 )
                robot.shoot()
                robot.execute()
            elif ( input[0] == 'teste6' ):
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.execute()
            elif ( input[0] == 'teste7' ):
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.robot_move_forward( 100000 )
                robot.execute()
            elif ( input[0] == 'teste8' ):
                robot.robot_move_forward( 100000 )
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.execute()
            elif ( input[0] == 'teste9' ):
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.robot_move_forward( 100000 )
                robot.shoot()
                robot.execute()
            elif ( input[0] == 'teste10' ):
                robot.robot_move_forward( 1000 )
                robot.shoot()
                robot.shoot()
                robot.get_robot_dir()
                robot.execute()
            elif ( input[0] == 'teste11' ):
                robot.shoot()
                robot.shoot()
                robot.shoot()
                robot.get_robot_position()
                robot.robot_move_forward( 100000 )
                robot.shoot()
                robot.execute()
























    print "fim..."
    

