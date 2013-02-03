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


import socket
from hashlib import sha512


class CAuth( object ):
    def __init__( self, sock, callback, mode = "gui" ):
        self._callback = callback
        self._mode = mode

        self._sock = sock
        # Pode ser uma instancia de dois objectos. Ou do AuthGUI ou do AuthCLI.
        self._interface = None
        # Bytes
        self._BUFFER = 100
        #self._HASH_REPTS = 10000

    def _clean_up( self ):
        self._sock.close()
        self._interface.destroy()





    def _send_to_server( self, data ):
        EOL = "\r\n"
        try:
            self._sock.send( data + EOL )
            return True

        except socket.error, err:
            print "\n!!! Erro no envio da informação!"
            print "!!! Descrição: %s" % str(err)
            return False



    def _recv_from_server( self ):
        data = ''
        try:
            data = self._sock.recv( self._BUFFER )
            return data

        except socket.error, err:
            print "\n!!! Não foi possível receber informação do servidor!"
            print "!!! Descrição: %s" % str(err)
            return data          







    def _check_response( self, data):
        if ( data == 'dupip' ):
            self._clean_up()
            self._interface.pop_up( "Já existe um utilizador ligado com este IP." )
            self._callback( False )
        elif ( data == 'comerr' ):
            self._clean_up()
            self._interface.pop_up( "A ligação foi terminada inesperadamente." )
            self._callback( False )
        elif ( data == 'alrauth' ):
            self._clean_up()
            self._interface.pop_up( "Esta conta já se encontra autenticada." )
            self._callback( False )
        elif ( data == 'authfail' ):
            self._clean_up()
            self._interface.pop_up( "Autenticação terminada sem sucesso." )
            self._callback( False )
        elif ( data[ : 7 ] == 'invcred' ):
            self._interface.pop_up( "Credenciais Inválidas. Tente Novamente." )
            self._interface.restart( data[ -( len(data) - 7): ] )
        elif ( data[ : 6 ] == 'authok' ):
            self._callback( data[ -( len(data) - 7): ] )
            self._interface.destroy()
        else:
            self._clean_up()
            self._interface.pop_up( "Não foi possível terminar a autenticação devido a um erro desconhecido." )
            self._callback( False )
    


    def _hash_password( self, password ):
        hash = sha512()
        hash.update(password)
        #for i in xrange(self._HASH_REPTS):
        #    hash.update(hash.digest())
        return str(hash.hexdigest())



    def _control( self, data ):
        """
        Troca informação com o servidor.
        """
        userName = data[ 0 ]
        password = self._hash_password( data[ 1 ] )
        str_ = userName + ":" + password
        self._send_to_server( str_ )

        data = self._recv_from_server()
        if ( data == '' ):
            self._check_response( "comerr" )
            #self._clean_up()
            #self._callback( False )
            return

        retVal = self._check_response( data.strip() )



    def _cb( self, widget, event, value = None, data = None ):
        if ( value == 'cancel' ):
            self._clean_up()
            self._callback( False )
        elif ( value == 'ok' ):
            self._control( data )


    def _start_gui( self ):
        from auth_gui import AuthGUI
        self._interface = AuthGUI( self._cb )
        self._interface.create_w( )


    def _start_cli( self ):
        """
        Não implementado.
        """
        #from auth_cli import authCLI
        #self._interface = AuthCLI( self._cb )
        pass



    



    def start( self ):
        if ( self._mode.lower() == "gui" ):
            self._start_gui()
        elif ( self._mode.lower() == "cli" ):
            self._start_cli()
            return "Não Implementado"
        

        self._interface.start()
        


























############################################################################
############################################################################
############################################################################

if __name__ == "__main__":
    import gtk

    host = "127.0.0.1"
    port = 28080


    def create_socket():
        global sock
        try:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            return True

        except socket.error, err:
            print "\n!!! Erro na criação do socket!"
            print "!!! Descrição: %s" % str(err)
            return False



    def connect():
        """
        - addr - Tupla com o host e a porta do servidor.
        """
        global host
        global port
        try:
            sock.connect( (host, port) )
            return True

        except socket.error, err:
            print "\n!!! Não foi possível estabelecer a ligação com o servidor!"
            print "!!! Descrição: %s" % str(err)
            return False




    def callback( value ):
        print "Callback: %s" % str(value)
        if ( value != False ):
            print ">> Auntenticação efectuada com sucesso!"

        else:
            print "!!! Autenticação efectuada sem sucesso..."

        gtk.main_quit()




    if ( create_socket() ):
        if ( connect() ):    
            auth = CAuth( sock, callback )
            auth.start()

            gtk.main()
