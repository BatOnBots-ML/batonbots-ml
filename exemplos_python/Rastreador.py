#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rastreador

Rastreia o campo de batalha em busca dos robôs inimigos e ataca o último que encontrar.
"""
from port_module import Robot

class Rastreador( Robot ):
    def __init__( self ):
        Robot.__init__( self )
        self._alive = True
        # Inicia o robot
        self.init()
    

    def round_started( self, roundNum ):
        print "\nround_started( " + str( roundNum ) + ' )'
        # Configura o modo de execução. Neste caso não é obrigatório porque este é o modo por defeito
        self.exec_mode( "lock" )
        self.subscribe_events( "[scan_event]" )
    
    
    
    def scan_event( self, event ):
        counter = 0
        print "#################################"
        for obj in event.objsList:
            print "- Alvo %d:" % counter
            print obj.objName
            print obj.objEnergy
            print obj.objDamage
            print obj.objArmor
            print obj.objPosition
            print obj.objDirection
            print obj.objRelativeDirection
            print obj.objSpeed
            print obj.objDistance
            counter += 1
            print "---------------------------"
        if ( event.found() ):
            self.gun_turn_to( event.objsList[0].objRelativeDirection )
            self.shoot()
        print "#################################"





    def start( self ):
        while( self._alive ):
            self.scan()






if ( __name__ == '__main__' ):
    robot = Rastreador()
    robot.start()
            
                


