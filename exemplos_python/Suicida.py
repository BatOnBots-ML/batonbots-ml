#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Suicida


Procura inimigos com o radar e vai contra o primeiro que encontrar ate não ter energia.
'''
from port_module import Robot
from time import sleep

class Suicida( Robot ):
    def __init__( self ):
        Robot.__init__( self )
        self._alive = True
        self._hitWall = False
        # Lista com os objectos encontrados no rastreio
        self._targets = []
        # Inicia o robot
        self.init()


    def round_started( self, roundNum ):
        print "round_started( " + str( roundNum ) + " )"
        self.exec_mode("block")
        self.subscribe_events( "[on_hit_wall, out_of_energy, scan_event]" )



    def on_hit_wall( self, wall ):
        print "on_hit_wall( " + wall + " )"
        self._hitWall = True


    def out_of_energy( self ):
        print "out_of_energy()"
        # Faz uma pausa para recarregar as baterias ate conseguir andar novamente
        sleep( 2 )
        # Reduz a velocidade para reduzir o consumo de energia
        self.set_speed( 2 )
        self.execute()


    def scan_event( self, event ):
        self._targets = []
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
            self._targets.append( obj )
            counter += 1
            print "---------------------------"
        print "#################################"





    def start( self ):
        while ( self._alive ):
            # Faz o rastreio
            self.scan()
            self.execute()
            if ( self._targets != [] ):
                target = self._targets[ 0 ]
                # Direcciona-se parar o inimigo
                self.robot_turn_to( target.objRelativeDirection )
                # Vai-se aproximando gradualmente
                halfDist = int( target.objDistance / 2 )
                # Se estiver a bater numa parede não anda para a frente
                if ( self._hitWall ):
                    self._hitWall = False
                    self.robot_move_backward( halfDist )
                else:
                    self.robot_move_forward( halfDist )
                self.execute()
            

    
if ( __name__ == "__main__" ):
    robot = Suicida()
    robot.start()