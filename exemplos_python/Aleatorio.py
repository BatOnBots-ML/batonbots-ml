#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Robot: Aleatorio

Movimenta-se aleatóriamente pelo campo de batalha.
"""
from port_module import Robot


class Aleatorio( Robot ):
    def __init__( self ):
        Robot.__init__( self )
        # Enquanto True o robô continua a funcionar
        self._alive = True
        # Controla a direcção do movimento do robô
        self._drection = 1
        # Inicia o robot
        self.init()
    


    def round_started( self, roundNum ):
        print "\nround_started( " + str( roundNum ) + ' )'
        self._direction = 1
        self.exec_mode("block")
        self.subscribe_events( "[on_hit_robot, on_hit_wall]" )
    
    
    
    def on_hit_wall( self, wall ):
        print "on_hit_wall( " + wall + " )"
        self._direction *= -1
    
    def on_hit_robot( self, event ):
        print "#################################"
        print "on_hit_robot()"
        print event.robotName
        print event.robotDamage
        print event.robotArmor
        print event.relativeDirection
        print "#################################"
        self._direction *= -1



    def start( self ):
        while( self._alive ):
            self.robot_move_forward( 300 * self._direction )
            self.robot_turn_right( 90 )
            self.execute()







if __name__ == '__main__':
    robot = Aleatorio()
    robot.start()


