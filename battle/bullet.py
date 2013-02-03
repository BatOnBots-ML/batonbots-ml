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


class Bullet( object ):
    """
    Metodos comuns dos objectos que são desenhados na batalha:
        - update()
        - blit()
        - get_name()
    
    Atributos comuns:
        - Não há

    Nota: Caso haja dúvidas, seguir o atributo "objectsGroup" da classe BattleRoom.
    """
    def __init__(self, bulletID, owner, bulletPosition, screen, bulletImage):
        self._id = bulletID
        self._owner = owner
        self._position = bulletPosition
        self._screen = screen
        self._image = bulletImage
        self._rect = self._image.get_rect()


    def get_name( self ):
        return self._id
    
    def get_owner( self ):
        return self._owner
    
    def blit( self ):
        self._screen.blit( self._image, self._rect )

    def update( self, x, y ):
        self._rect.center = (x, y)
