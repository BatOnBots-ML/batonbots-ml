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

import logging
from sys import stdout



class Logging( object ):
    '''
    Controla a informação que é passada para a consola.
    '''
    def __init__( self, level = "info", format = "[ %(asctime)s *** %(levelname)s ] >> %(message)s", logTo = "console" ):
        self._levels = {
                  "debug": logging.DEBUG,
                  "info": logging.INFO,
                  "warning": logging.WARNING,
                  "error": logging.ERROR,
                  "critical": logging.CRITICAL
                 }

        self._logger = logging.getLogger()
        formatter = logging.Formatter( format.lower(), datefmt='%m-%d-%Y, %H:%M:%S' )
        #self._logger.setLevel( logging.DEBUG )
        self._logger.setLevel( self._levels[ level ] )
        
        # Evita que sejam adicionados mais handlers
        if ( len(self._logger.handlers) > 0 ):
            return
        
        if ( logTo == "console" ):
            strm_out = logging.StreamHandler( stdout )
            strm_out.setFormatter( formatter )
            self._logger.addHandler( strm_out )
            
        elif ( logTo == "file" ):
            hdlr = logging.FileHandler( "log.log" )
            hdlr.setFormatter( formatter )
            self._logger.addHandler( hdlr )
        
        print self._logger.handlers
        # sistema antigo...
        #logging.basicConfig( format = format.lower(), level = self._levels[level.lower()], datefmt='%m-%d-%Y, %H:%M:%S' )
        
    
    def debug(self, msg):
        """
        Debug Level
        """
        self._logger.debug( unicode(str(msg), encoding = "utf-8", errors = "replace") )

    def info(self, msg):
        """
        Info Level
        """
        self._logger.info( unicode(str(msg), encoding = "utf-8", errors = "replace") )

    def warning(self, msg):
        """
        Warning Level
        """
        self._logger.warning( unicode(str(msg), encoding = "utf-8", errors = "replace") )

    def error(self, msg):
        """
        Error Level
        """
        self._logger.error( unicode(str(msg), encoding = "utf-8", errors = "replace") )
        
    def critical(self, msg):
        """
        Critical Level
        """
        self._logger.critical( unicode(str(msg), encoding = "utf-8", errors = "replace") )






if ( __name__ == "__main__" ):
    log = Logging(level = "debug")
    log.debug( "Debug. atão" )
    log.info( "Info." )
    log.warning( "Warning." )
    log.error( "Error." )
    log.critical( "Critical." )


