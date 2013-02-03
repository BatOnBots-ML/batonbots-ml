#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Paredes

Percorre o campo de batalha encostado às paredes no sentido dos ponteiros do relógio.
"""
from port_module import Robot
from time import sleep

class Paredes( Robot ):
    def __init__( self ):
        Robot.__init__( self )
        self._alive = True
        # Inicia o robot
        self.init()



    def round_started( self, roundNum ):
        print "round_started( " + str( roundNum ) + ' )'
        self.subscribe_events( "[out_of_energy]" )
        


    def out_of_energy( self ):
        """
        Quando fica sem energia espera um segundo para recarregar e reduz a velocidade para reduzir o consumo.
        """
        print "out_of_energy()"
        # Faz uma pausa para recarregar as baterias ate conseguir andar novamente
        sleep( 1 )
        # Reduz a velocidade para reduzir o consumo de energia
        self.set_speed( 2 )


    
    def start( self ):
        direction = 0
        while ( self._alive ):
            self.robot_move_forward( 1000 )
            self.robot_turn_to( direction )
            direction += 90
            if ( direction == 360 ): 
                direction = 0

            


if ( __name__ == "__main__" ):
    robot = Paredes()
    robot.start()