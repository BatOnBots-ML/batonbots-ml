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


import pygtk
pygtk.require('2.0')
import gtk
import gobject

from threading import Thread




class GenericMessageDialog():
    def __init__(self, parent, text, type):
        self.md = gtk.MessageDialog( parent, 
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                type,
                                gtk.BUTTONS_OK, 
                                str(text)
                               )
        self.md.connect( 'response', self.destroy )


    def destroy(self, widget, response):
        self.md.destroy()


    def show_it(self):
        self.md.show_all()








class AuthGUI( gtk.Window ):
    def __init__( self, callback ):
        self._callback = callback


    def _exec( self, widget  ):
        userName = self._entryUser.get_text()
        password = self._entryPassword.get_text()
        self.hide()
        
        self._callback( None, None, 'ok', (userName, password) )








    def pop_up( self, text):
        md = GenericMessageDialog( self, text, gtk.MESSAGE_ERROR )
        md.show_it()

    

    def _check_len( self, widget = None ):
        """
        Verifica se o username e a password estão dentro dos parametros
        Tamanho minimo de 7 caracteres e maximo de 20 para a password e
        minimo de 3 caracteres e maximo de 20 o username.
        """
        userNameMinL = 3
        userNameMaxL = 20
        passMinL = 7
        passMaxL = 20

        if ( ((len(self._entryUser.get_text()) >= userNameMinL) and (len(self._entryUser.get_text()) <= userNameMaxL)) &
             ((len(self._entryPassword.get_text()) >= passMinL) )and (len(self._entryPassword.get_text()) <= passMaxL)):
            gobject.idle_add( self._buttonOK.set_sensitive, True )
            return True

        else:
            gobject.idle_add( self._buttonOK.set_sensitive, False )
            return False


    def create_w( self ):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title("Iniciar Sessão")
        self.connect("delete_event", self._callback, 'cancel')
        self.set_border_width(10)
        self.set_resizable(False)
        self.set_position(gtk.WIN_POS_CENTER)
        #self.set_modal( True )

        main_vbox = gtk.VBox(False, 0)
        self.add(main_vbox)

        #### Labels ####
        hbox = gtk.HBox(False, 0)
        main_vbox.pack_start(hbox, False, False, 0)

        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 0)

        label = gtk.Label("Utilizador")
        vbox.pack_start(label, True, False, 6)

        label = gtk.Label("Palavra-Chave")
        vbox.pack_start(label, True, False, 6)




        ##### Caixas de texto #####
        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, True, True, 3)


        self._entryUser = gtk.Entry(20)
        #self.entryUtilizador.set_text("")
        self._entryUser.connect("changed", self._check_len)
        vbox.pack_start(self._entryUser, True, True, 0)

        self._entryPassword = gtk.Entry(20)
        #self.entryChave.set_text("")
        self._entryPassword.set_visibility(False)
        self._entryPassword.connect("changed", self._check_len)
        self._entryPassword.connect( "activate", self._exec )
        vbox.pack_start(self._entryPassword, True, True, 5)


        self._labelAttempts = gtk.Label("Tentativas Restantes: 3")
        main_vbox.pack_start(self._labelAttempts, False, False, 0)

        # Separador
        separador = gtk.HSeparator()
        main_vbox.pack_start(separador, True, True, 5)


        #### Butões ####
        hbox = gtk.HBox(True, 0)
        main_vbox.pack_start(hbox, True, False, 0)

        self._buttonCancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        #self._buttonCancel.connect_object("clicked", gtk.Widget.destroy, self)
        self._buttonCancel.connect( "clicked", self._callback, None, 'cancel' )
        hbox.pack_start(self._buttonCancel, True, True, 5)

        self._buttonOK = gtk.Button(stock=gtk.STOCK_OK)
        self._buttonOK.connect( "clicked", self._exec )
        self._buttonOK.set_sensitive( False )
        hbox.pack_start(self._buttonOK, True, True, 5)


        #self.show_all()



    def restart( self, attempts ):
        self._entryUser.set_text( "" )
        self._entryPassword.set_text( "" )
        self._buttonOK.set_sensitive( False )
        self._labelAttempts.set_text( "Tentativas Restantes: %s" % str(attempts) )
        self.set_focus( self._entryUser )
        self.start()


    def start( self ):
        self.show_all()




