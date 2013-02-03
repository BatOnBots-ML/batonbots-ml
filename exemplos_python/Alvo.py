#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Robot: Alvo

Permanece imóvel no campo de batalha. Útil como alvo para testes.
"""
from port_module import Robot
from time import sleep

class Alvo( Robot ):
    def __init__( self ):
        Robot.__init__( self )
        self._alive = True
        # Inicia o robot
        self.init()

    def start( self ):
        while ( self._alive ):
            sleep( 2 )
            self.noop()



if ( __name__ == "__main__" ):
    robot = Alvo()
    robot.start()