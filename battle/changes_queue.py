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



class ChangesQueue(object):
    """ 
    Descrição: Queue do tipo FIFO que guarda todas as alterações que forem feitas à 'imagem' da batalha.
               Isto é util para armazenar as alterações da 'imagem' durante o delay.
               Esta lista não tem ligação com a 'commands_queue'. Esta é utilizada para guardar as alterações
               da batalha para os jogadores.

        # Contém uma lista com 3 níveis.
        # - Nível 1: Nível principal. Cada campo deste nível equivale a um periodo completo. Um periodo completo
        #            equivale a n segundos. n é defenido pelo servidor. Por defeito = 1 segundo
        # - Nível 2: Cada campo deste nível equivale a um ciclo.
        # - Nível 3: São as movimentações de cada robot e os eventos da batalha.
        #
        #           |------------------------------------------------  Nível 1 ----------------------------------------------------|
        #                |--------------------  Nível 2 ------------------|
        #                   |----- Nível 3 -----|
        # Formato:  [    [  [robotName, pos, dir], [robotName, pos, dir]  ],  [  [eventName, val], [robotName, pos, dir]  ]    ]

    Incluida em:
        - BattleRoom
        
        
    Nota: Este modulo não é igual ao do servidor, principalmente no metodo 'dequeue'.
    """
    
    #firstChanges = property( get_first_changes, None, "Retorna a primeira lista com alterações" )
    
    def __init__(self):
        # Tamanho da Queue
        self.size = 0
        # Contém uma lista com 3 níveis.
        # - Nível 1: Nível principal. Cada campo deste nível equivale a um periodo completo. Um periodo completo
        #            equivale a n segundos. n é defenido pelo servidor. Por defeito = 1 segundo
        # - Nível 2: Cada campo deste nível equivale a um ciclo.
        # - Nível 3: São as movimentações de cada robot e os eventos da batalha.
        #
        #           |------------------------------------------------  Nível 1 ----------------------------------------------------|
        #                |--------------------  Nível 2 ------------------|
        #                   |----- Nível 3 -----|
        # Formato:  [    [  [robotName, pos, dir], [robotName, pos, dir]  ],  [  [eventName, val], [robotName, pos, dir]  ]    ]
        self.changesList = []
    
    
    def __iter__( self ):
        return self
    
    def __len__( self ):
        return self.size
    
    
    def next(self):
        if ( self.get_size() > 0 ):
            retVal = self.changesList.pop(0)
            self.size = len(self.changesList)
            return retVal
        else:
            raise StopIteration

    
    def enqueue(self, command_set):
        """
        Adiciona um comando à lista
        'command_set' - é uma lista com uma lista do comando e o argumento, e quem enviou esse 
              comando [[command, args], playerName]
        """
        self.changesList.append(command_set)
        self.size = len(self.changesList)
    

    def dequeue(self):
        """
        Retorna o primeiro campo do nível 3( alterações e eventos por ciclo )
        Se estiver vazia retorna []
        """
        tmpList = self.changesList[ : ]
        
        for changesPerPeriod in tmpList:
            for changesPerCycle in changesPerPeriod:
                self.changesList[0].pop( 0 )
                if ( len(self.changesList[0]) == 0 ):
                    self.changesList.pop( 0 )
                    self.size = len(self.changesList)
                    
                return changesPerCycle
            
            self.changesList.pop( 0 )
            self.size = len(self.changesList)
        
        return []
                

    def get_size(self):
        """
        Retorna o tamanho da Queue
        """
        return self.size
    

    def get_position(self, command_set):
        """
        Retorna a posição de um conjunto dentro da lista
        
        'command_set' - [[command, args], playerName]
        
        Retorna o index se encontrar.
        Retorna 'None' se não encontrar.
        """
        try:
            index = self.changesList.index(command_set)
            return index
        except ValueError, err:
            printe("")
            printe( "CommandQueue/get_position() *** O conjunto não existe na lista." )
            printe( "Descrição: " + str(err) )
            return None


    def refresh(self):
        self.size = len(self.changesList)


    def reset(self):
        self.changesList = []
        self.size = 0

    
