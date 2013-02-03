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


from about_dialog import AboutDialog





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








class BattlesListGUI(gtk.Window):
    def __init__(self, exitCallback, loginCallback, logout_callback, refreshCallback, createCallback, joinCallback ):
        '''
        Constructor
        '''
        # Callback para o exit
        self.exitCallback = exitCallback
        # Callback para o logout
        self.logoutCallback = logout_callback
        # Callback para o botão de login
        self.loginCallback = loginCallback
        # Callback para o botão 'buttonRefresh'
        self.refreshCallback = refreshCallback
        # Callback para o botão 'buttonRefresh'
        self.createCallback = createCallback
        # Callback para o botão 'buttonJoin'
        self.joinCallback = joinCallback
        
        self.transDict = {
                      'title': 'BatOnBots-ML  -  Lista de Batalhas',
                      ### Menus
                      'menuBarFile': 'Ficheiro',
                      'menuBarLogin': 'Iniciar Sessão',
                      'menuBarExit': 'Sair',
                      'menuBarHelp': 'Ajuda',
                      'menuBarTutorials': 'Tutoriais',
                      'menuBarCheckUpdates': 'Procurar Actualizações',
                      'menuBarAbout': 'Sobre',
                      ###
                      ### Titulo das colunas da lista das batalhas ###
                      'column0': 'Batalha',
                      'column1': 'Tipo',
                      'column2': 'Jogadores',
                      'column3': 'Rondas',
                      'column4': 'Admin',
                      'column5': 'Palavra-Chave',
                      ###
                      ### Butões ###
                      'buttonCreate': 'Criar Batalha',
                      'buttonJoin': 'Entrar',
                      'buttonRefresh': 'Actualizar',
                      'buttonExit': 'Sair',
                      ###
                      ### Status
                      'status0': 'Desconectado...',
                      ###
                      ### Tipo de batalha
                      '1': 'Oficial',
                      '2': 'Treino'
                     }



    def destroy(self, widget = None):
        """
        Este metodo está connectado ao evento 'destroy' da janela, e, é também invocado no modulo 'ServerInterface'
        quando é para fechar esta janela e mostrar a sala de jogo.
        """
        # Como este metodo também é invocado no modulo 'ServerInterface' quando é para fechar esta janela e mostrar 
        # a sala de jogo, é preciso fazer a distinção porque o 'exitCallback' invoca o metodo 'shutdown' da classe
        # 'ServerInterface' e isso não pode acontecer quando é para passar para a sala de jogo.
        if ( widget != None ):
            self.exitCallback()

    
    def exit(self, widget = None):
        self.destroy('False')


    def menuBarLogin_active(self, widget = None):
        """
        Invocado quando o menu 'Iniciar Sessão' é activado.
        
        Inicia o processo de autenticação do jogador no servidor.
        """
        # Por razões de compatibilidade com o python 2.6 é utilizado o metodo 'get_child()'
        if ( self.menuBarLogin.get_child().get_label() == 'Iniciar Sessão' ):
            thread = Thread( target = self.loginCallback )
            thread.start()
            
        else:
            thread = Thread( target = self.logoutCallback )
            thread.start()
        
        self.menuBarLogin.set_sensitive( False )


    def buttonRefresh_clicked(self, widget = None):
        """
        Invocado quando o botão 'buttonRefresh' é clicado.
        """
        self.buttonRefresh.set_sensitive( False ) 
        thread = Thread( target = self.refreshCallback )
        thread.start()

    def buttonCreate_clicked(self, widget = None):
        """
        Invocado quando o botão 'buttonRefresh' é clicado.
        """ 
        createBattleForm = CreateBattle( self, self.buttonCreate, self.createCallback )
        createBattleForm.create_w()
        self.buttonCreate.set_sensitive( False )

    def buttonJoin_clicked(self, widget = None):
        """
        Invocado quando o botão 'buttonJoin' é clicado.
        """ 
        treeSelection = self.treeViewRobotLS.get_selection()
        listStore, iter = treeSelection.get_selected()
        
        # O 0(zero) é porque o nome da batalha está na coluna 0(zero)
        battleName = listStore.get_value( iter, 0 )
        
        self.buttonJoin.set_sensitive( False ) 
        thread = Thread( target = self.joinCallback, args = [battleName] )
        thread.start()        

    ################################################################################################
    def treeView_clicked(self, widget = None, event = None):
        """
        Invocado quando a 'treeViewRobotLS' é 'clicada'.
        """
        widget.get_selection().connect('changed', self.treeView_selection_changed)


    def treeView_selection_changed(self, treeViewSelection):
        """
        Serve para activar ou desactivar o botão 'buttonJoin' quando há uma batalha seleccionada ou não.
        """
        if ( treeViewSelection.count_selected_rows() == 0 ):
            self.buttonJoin.set_sensitive( False )
        
        else:
            self.buttonJoin.set_sensitive( True )


    def treeView_activated(self, widget = None, row = None, col = None):
        """
        É invocado quando é feito double click/Enter/SpaceBar numa linha da lista.
        """
        model = widget.get_model()
        battleName = model[row][0]
        
        self.buttonJoin.set_sensitive( False )
        
        self.buttonJoin.set_sensitive( False ) 
        thread = Thread( target = self.joinCallback, args = [battleName] )
        thread.start()        

    ################################################################################################



    def create_w(self):
        gtk.Window.__init__( self, gtk.WINDOW_TOPLEVEL )
        self.set_title( self.transDict[ 'title' ] )
        self.connect( 'destroy', self.exit )
        self.set_size_request( 500, 300 )
        self.set_position( gtk.WIN_POS_CENTER )
        
        main_vbox = gtk.VBox( False, 0 )
        
        ### Menus
        mb = gtk.MenuBar()

        menu = gtk.Menu()
        menuBarFile = gtk.MenuItem( self.transDict[ 'menuBarFile' ] )
        menuBarFile.set_submenu(menu)
       
        self.menuBarLogin = gtk.MenuItem( self.transDict[ 'menuBarLogin' ] )
        self.menuBarLogin.connect( 'activate', self.menuBarLogin_active )
        menu.append( self.menuBarLogin )
        
        separator = gtk.SeparatorMenuItem()
        menu.append( separator )
        
        exit = gtk.MenuItem( self.transDict[ 'menuBarExit' ] )
        exit.connect("activate", self.exit)
        menu.append( exit )

        mb.append( menuBarFile )
        
        
 
        menu = gtk.Menu()
        menuBarHelp = gtk.MenuItem( self.transDict[ 'menuBarHelp' ] )
        menuBarHelp.set_submenu( menu )
        
        self.menuBarTutorials = gtk.MenuItem( self.transDict[ 'menuBarTutorials' ] )
        menu.append( self.menuBarTutorials )
        
        self.menuBarCheckUpdates = gtk.MenuItem( self.transDict[ 'menuBarCheckUpdates' ] )
        menu.append( self.menuBarCheckUpdates )
        
        separator = gtk.SeparatorMenuItem()
        menu.append( separator )
        
        self.menuBarAbout = gtk.MenuItem( self.transDict[ 'menuBarAbout' ] )
        self.menuBarAbout.connect( "activate", AboutDialog().showAbout )
        menu.append( self.menuBarAbout )
        
        mb.append( menuBarHelp )
  
        main_vbox.pack_start(mb, False, False, 0)

        ###
        
        
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type( gtk.SHADOW_ETCHED_IN )
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        main_vbox.pack_start(sw, True, True, 0)

        self.lsBattlesList = self._create_model()

        self.treeViewRobotLS = gtk.TreeView(self.lsBattlesList)
        self.treeViewRobotLS.connect("row-activated", self.treeView_activated)
        #self.treeViewRobotLS.connect( 'cursor-changed', self.treeView_cursor_changed )
        # Invoca o metodo quando uma linha é clicada
        self.treeViewRobotLS.add_events(gtk.gdk.BUTTON_PRESS_MASK )
        self.treeViewRobotLS.connect('button_press_event', self.treeView_clicked)
        self.treeViewRobotLS.set_rules_hint(True)
        sw.add(self.treeViewRobotLS)

        self._create_columns(self.treeViewRobotLS)
    

        ### Butões
        
        self.buttonExit = gtk.Button( label=self.transDict['buttonExit'] )
        self.buttonExit.connect( 'clicked', self.exit)
        hbox = gtk.HBox( False, 0 )
        hbox.pack_end(self.buttonExit, False, False, 4)
        
        self.buttonRefresh = gtk.Button( label=self.transDict['buttonRefresh'] )
        self.buttonRefresh.set_sensitive( False )
        self.buttonRefresh.connect( 'clicked', self.buttonRefresh_clicked )
        hbox.pack_end(self.buttonRefresh, False, False, 4)

        self.buttonJoin = gtk.Button( label=self.transDict['buttonJoin'] )
        self.buttonJoin.set_sensitive( False )
        self.buttonJoin.connect( 'clicked', self.buttonJoin_clicked )
        hbox.pack_end(self.buttonJoin, False, False, 4)
        
        self.buttonCreate = gtk.Button( self.transDict[ 'buttonCreate' ] )
        self.buttonCreate.set_sensitive( False )
        self.buttonCreate.connect( 'clicked', self.buttonCreate_clicked )
        hbox.pack_end( self.buttonCreate, False, False, 4 )
        
        main_vbox.pack_start(hbox, False, False, 5)
        ###
        

        ### Status-Bar
        self.statusBar = gtk.Statusbar()
        self.statusBar.push( 0, self.transDict[ 'status0' ] )
        
        main_vbox.pack_start( self.statusBar, False, False, 0 )

        self.add( main_vbox )
        self.show_all()


        self.menuBarLogin_active()

        


    def _create_model(self):
        store = gtk.ListStore(str, str, str, str, str, bool)

        return store
    
    
    def _create_columns(self, treeView):
        rendererText = gtk.CellRendererText()
        rendererText.set_property( 'xalign', 0.5 )
        column = gtk.TreeViewColumn( self.transDict['column0'], rendererText, text=0 )
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        
        # Tipo
        rendererText = gtk.CellRendererText()
        rendererText.set_property( 'xalign', 0.5 )
        column = gtk.TreeViewColumn( self.transDict['column1'], rendererText, text=1 )
        column.set_sort_column_id(1)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        rendererText.set_property( 'xalign', 0.5 )
        column = gtk.TreeViewColumn( self.transDict['column2'], rendererText, text=2 )
        column.set_sort_column_id(2)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        rendererText.set_property( 'xalign', 0.5 )
        column = gtk.TreeViewColumn( self.transDict['column3'], rendererText, text=3 )
        column.set_sort_column_id(3)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        rendererText.set_property( 'xalign', 0.5 )
        column = gtk.TreeViewColumn( self.transDict['column4'], rendererText, text=4 )
        column.set_sort_column_id(4)
        treeView.append_column(column)
        
        rendererToggle = gtk.CellRendererToggle()
        #rendererToggle.set_property( 'activatable', False )
        column = gtk.TreeViewColumn( self.transDict['column5'], rendererToggle, active=5)
        column.set_sort_column_id(5)
        treeView.append_column(column)
        
        
        
    def create_list(self, list):
        """
        Recebe uma lista com as batalhas e actualiza a GUI.
        
        'list' - [['Sample Battle 1', 1, 1, 2, 10, 'NuGuN', False]]
        """
        self.lsBattlesList.clear()
        for battle in list:
            battle[1] = self.transDict[ str(battle[1]) ]
            totalPlayers = battle[2]
            maxPlayers = battle[3]
            battle.pop(2)
            battle.pop(2)
            battle.insert( 2, str(totalPlayers) + '/' + str(maxPlayers) )
            self.lsBattlesList.append( battle )

    def set_status_bar(self, status):
        """
        Actualiza a barra de estado.
        
        Está a ser invocada na classe 'ServerInterface'.
        """
        self.statusBar.push( 0, status ) 







class CreateBattle( gtk.Window ):
    """
    Tem o formulario utilizado para criar uma batalha.
    """
    
    def __init__(self, parent, copyButtonCreate, createCallback):
        """
        'copyButtonCreate' - cópia do botão 'buttonCreate' da janela principal.
                                 É preciso para alterar a propriedade 'sensitive' do mesmo.
        """
        self.transDict = {
                      'title': 'BatOnBots-ML  -  Criar Batalha',
                      ###
                      'column0': "Robôs Disponíveis",
                      'column1': "Robôs Sel.",
                      ###
                      'name': 'Nome da Batalha:',
                      'maxPlayers': 'Nº Max. de Jogadores:',
                      'type': 'Tipo de Batalha:',
                      #'team-deathmatch': 'Com Equipas',
                      #'free-for-all': 'Sem Equipas',
                      'official': 'Oficial',
                      'not-official': 'Treino',
                      'nRounds': 'Nº de Rondas:',
                      'roundsDuration': 'Duração de Cada Ronda:',
                      'password': 'Palavra-Chave:',
                      'checkButtonPassword': 'Ocultar Palavra-Chave',
                      ###
                      ### Butões
                      'buttonCreate': 'Criar Batalha',
                      'buttonCancel': 'Cancelar'
                      ###
                     }
        
        self.virtualRobotsDict = {
                                  0 : "Alvo",
                                  1 : "Suicida",
                                  2 : "Paredes",
                                  3 : "Aleatorio",
                                  4 : "Rastreador"
                                  }
        
        # Copia do botão para criar batalha da janela principal
        self.copyButtonCreate = copyButtonCreate
        # Callback para o botão 'buttonCreate'
        self.createCallback = createCallback
        # Parent desta janela
        self.parent_ = parent

        

    def checkButtonPassword_toggled(self, widget = None):
        if ( self.checkButtonPassword.get_active() ):
            self.entryPassword.set_visibility( False )
            
        else:
            self.entryPassword.set_visibility( True )
    
    
    def buttonCreate_clicked(self, widget = None):
        self.create_battle()
        self.copyButtonCreate.set_sensitive( True )
    
    
    def buttonCancel_clicked(self, widget = None):
        self.delete_event()
    
    
    def delete_event(self, widget = None, event = None):
        self.copyButtonCreate.set_sensitive( True )
        self.destroy()












    ################################################################################################

    def treeViewLS_activated(self, widget = None, row = None, col = None):
        """
        É invocado quando é feito double click/Enter/SpaceBar numa linha da lista.
        """
        try:
            val = int( self.entryMaxPlayers.get_text() ) - 1
        except:
            val = 0
            
        if ( len(self.selectedRobots) < val ):
            model = widget.get_model()
            selectedRobot = model[row][0]
            self.selectedRobots.append( [selectedRobot] )
            # Coloca automaticamente o tipo de batalha para testes
            self.radioButtonType.set_active( True )
            # Desabilita esta opção porque com robots virtuais uma batalha só pode ser de testes
            self.radioButtonType2.set_sensitive( False )


    def treeViewSelected_activated(self, widget = None, row = None, col = None):
        """
        É invocado quando é feito double click/Enter/SpaceBar numa linha da lista.
        """
        model = widget.get_model()
        iter = model.get_iter( row )
        model.remove( iter )
        # Volta a activar a opção se não houver robots virtuais seleccionados
        if ( len(self.selectedRobots) == 0 ):
            self.radioButtonType2.set_sensitive( True )
        
    ################################################################################################
















    def _create_model(self):
        store = gtk.ListStore( str )
        return store
    
    def _create_columns_ls(self, treeView):
        rendererText = gtk.CellRendererText()
        rendererText.set_property( 'xalign', 0.5 )
        column = gtk.TreeViewColumn( self.transDict['column0'], rendererText, text=0 )
        column.set_sort_column_id(0)    
        treeView.append_column(column)

    def _create_columns_selected(self, treeView):
        rendererText = gtk.CellRendererText()
        rendererText.set_property( 'xalign', 0.5 )
        column = gtk.TreeViewColumn( self.transDict['column1'], rendererText, text=0 )
        column.set_sort_column_id(0)    
        treeView.append_column(column)





    def create_w(self):
        gtk.Window.__init__( self, gtk.WINDOW_TOPLEVEL )
        self.set_title( self.transDict[ 'title' ] )
        self.set_border_width( 5 )
        self.set_position( gtk.WIN_POS_CENTER )
        self.set_size_request( 680, -1 )
        self.set_resizable( True )
        self.connect('delete_event', self.delete_event)
        self.set_transient_for( self.parent_ )
        self.set_modal( True )
        
        
        
        main_vbox = gtk.VBox(False, 0)
        main_hbox = gtk.HBox(False, 0)
        
        sec_vbox = gtk.VBox(False, 0)
        
        ##############################################################
        hbox = gtk.HBox( False, 0 )
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        label = gtk.Label( self.transDict[ 'name' ] )
        hAlign.add( label )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        
        hAlign = gtk.Alignment( 0, 1, 1, 0 )
        self.entryName = gtk.Entry( 50 )
        hbox.pack_start( self.entryName )
        hAlign.add( hbox )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        ##############################################################

        # Cria um espaço entre os diferentes campos
        hbox = gtk.HBox( False, 0 )
        sec_vbox.pack_start( hbox, False, False, 5 )

        ##############################################################
        hbox = gtk.HBox( False, 0 )
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        label = gtk.Label( self.transDict[ 'maxPlayers' ] )
        hAlign.add( label )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        self.entryMaxPlayers = gtk.Entry( 1 )
        self.entryMaxPlayers.set_alignment( 0.5 )
        self.entryMaxPlayers.set_text( '4' )
        self.entryMaxPlayers.set_size_request(30, -1)
        hbox.pack_start( self.entryMaxPlayers )
        hAlign.add( hbox )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        ##############################################################
        
        
        # Cria um espaço entre os diferentes campos
        hbox = gtk.HBox( False, 0 )
        sec_vbox.pack_start( hbox, False, False, 5 )
        
        ##############################################################
        hbox = gtk.HBox( False, 0 )
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        label = gtk.Label( self.transDict[ 'type' ] )
        hAlign.add( label )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        self.radioButtonType = gtk.RadioButton( None, label = self.transDict['not-official'])
        hbox.pack_start( self.radioButtonType )
        hAlign.add( hbox )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        
        hbox = gtk.HBox( False, 0 )
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        self.radioButtonType2 = gtk.RadioButton(  self.radioButtonType, label = self.transDict['official'] )
        hbox.pack_start( self.radioButtonType2 )
        hAlign.add( hbox )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        ##############################################################
        
        # Cria um espaço entre os diferentes campos
        hbox = gtk.HBox( False, 0 )
        sec_vbox.pack_start( hbox, False, False, 5 )
        
        #############################################################
        hbox = gtk.HBox( False, 0 )
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        label = gtk.Label( self.transDict[ 'nRounds' ] )
        hAlign.add( label )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        self.entryNRounds = gtk.Entry( 2 )
        self.entryNRounds.set_alignment( 0.5 )
        self.entryNRounds.set_text( '3' )
        self.entryNRounds.set_size_request(30, -1)
        hbox.pack_start( self.entryNRounds )
        hAlign.add( hbox )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        ##############################################################
        
        
        # Cria um espaço entre os diferentes campos
        hbox = gtk.HBox( False, 0 )
        sec_vbox.pack_start( hbox, False, False, 5 )
        
        
        ##############################################################    
        hbox = gtk.HBox( False, 0 )
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        label = gtk.Label( self.transDict[ 'roundsDuration' ] )
        hAlign.add( label )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        self.entryRoundsDuration = gtk.Entry( 3 )
        self.entryRoundsDuration.set_alignment( 0.5 )
        self.entryRoundsDuration.set_text( '120' )
        self.entryRoundsDuration.set_size_request(45, -1)
        hbox.pack_start( self.entryRoundsDuration )
        hAlign.add( hbox )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        ##############################################################
        
    
        # Cria um espaço entre os diferentes campos
        hbox = gtk.HBox( False, 0 )
        sec_vbox.pack_start( hbox, False, False, 5 )
        
    
        ##############################################################
        hbox = gtk.HBox( False, 0 )
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        label = gtk.Label( self.transDict[ 'password' ] )
        hAlign.add( label )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        self.entryPassword = gtk.Entry( 15 )
        self.entryPassword.set_visibility( False )
        #self.entryPassword.set_size_request(45, -1)
        hbox.pack_start( self.entryPassword )
        hAlign.add( hbox )
        sec_vbox.pack_start( hAlign, False, False, 0 )
        
        hAlign = gtk.Alignment( 0, 1, 0, 0 )
        self.checkButtonPassword = gtk.CheckButton( self.transDict['checkButtonPassword']  )
        self.checkButtonPassword.set_active( True )
        self.checkButtonPassword.connect( 'toggled', self.checkButtonPassword_toggled )
        hAlign.add( self.checkButtonPassword)
        sec_vbox.pack_start( hAlign, False, False, 0 )
        ##############################################################
        
        
        
        frame = gtk.Frame()
        frame.add( sec_vbox )
        main_hbox.pack_start( frame, True, True, 5 )






        ########################################################################
        ##################### Listas dos robots ############################
        ########################################################################
        hbox = gtk.HBox( True, 5 )
        
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type( gtk.SHADOW_ETCHED_IN )
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.lsRobots = self._create_model()

        self.treeViewRobotLS = gtk.TreeView(self.lsRobots)
        self.treeViewRobotLS.connect("row-activated", self.treeViewLS_activated)
        #self.treeViewRobotLS.connect( 'cursor-changed', self.treeViewLS_cursor_changed )
        # Invoca o metodo quando uma linha é clicada
        #self.treeViewRobotLS.add_events(gtk.gdk.BUTTON_PRESS_MASK )
        #self.treeViewRobotLS.connect('button_press_event', self.treeView_clicked)
        self.treeViewRobotLS.set_rules_hint(True)
        sw.add(self.treeViewRobotLS)

        self._create_columns_ls(self.treeViewRobotLS)

        
        hbox.pack_start( sw, True, True, 5 )
        
        ###
        ###
        
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type( gtk.SHADOW_ETCHED_IN )
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.selectedRobots = self._create_model()

        self.treeViewRobotSelected = gtk.TreeView(self.selectedRobots)
        self.treeViewRobotSelected.connect("row-activated", self.treeViewSelected_activated)
        #self.treeViewRobotLS.connect( 'cursor-changed', self.treeView_cursor_changed )
        # Invoca o metodo quando uma linha é clicada
        #self.treeViewRobotSelected.add_events(gtk.gdk.BUTTON_PRESS_MASK )
        #self.treeViewRobotSelected.connect('button_press_event', self.treeViewSelected_clicked)
        self.treeViewRobotSelected.set_rules_hint(True)
        sw.add(self.treeViewRobotSelected)

        self._create_columns_selected(self.treeViewRobotSelected)
        
        hbox.pack_start( sw, True, True, 5 )
        ###
        ###
        
        frame = gtk.Frame()
        frame.add( hbox )
        ########################################################################
        ########################################################################
        ########################################################################
        

        main_hbox.pack_start( frame, True, True, 5 )

        
        ## Adiciona todo o conjunto menos os botões
        main_vbox.pack_start( main_hbox, True, True, 5 )

        
        ### Adiciona os botões
        ##############################################################
        hAlign = gtk.Alignment( 0, 1, 1, 0 )
        hbox = gtk.HBox( False, 0 )

        self.buttonCancel = gtk.Button( self.transDict['buttonCancel'] )
        self.buttonCancel.connect( 'clicked', self.buttonCancel_clicked )
        hbox.pack_end( self.buttonCancel, False, False, 0 )


        self.buttonCreate = gtk.Button( self.transDict['buttonCreate'] )
        self.buttonCreate.connect( 'clicked', self.buttonCreate_clicked )
        hbox.pack_end( self.buttonCreate, False, False, 5 )
        
        
        hAlign.add( hbox )
        main_vbox.pack_start( hAlign, False, False, 5 ) 
        ##############################################################

        # Robots virtuais disponíveis
        # PARA ALTERAR!!!
        for robot in self.virtualRobotsDict.keys():
            self.lsRobots.append( [self.virtualRobotsDict[robot]] )
        
        
        
        self.add( main_vbox )
        self.show_all()
        



    def to_int(self, val):
        """
        Alguns valores de configuração da batalha têm de ser valores do tipo interiro. Este metodo serve para
        fazer essa convesão. Não é utilizado apenas o metodo built-in 'int()' porque se o utilizador inserir
        uma letra ele dá erro. E para não estar a meter um 'try' em todos, invoca-se este metodo.
        Os valores de configuração que precisam disto são:
         - maxPlayers
         - battleType
         - commandsPerCycle
         - rounds
         - round_duration
         
        Se o jogador tiver inserido um valor do tipo inteiro, faz a conversão. Se não retorna como string.
        """
        try:
            return int(val)
        
        except ValueError:
            return val


    def check_battle_conf(self):
        """
        Verifica se os valores que o jogador inseriu no formulário.

        battleName - Nome da batalha. Pode ter um minimo de 3 caracteres e um máximo de 50 caracteres.
        maxPlayers - Número máximo de jogadores que a batalha pode ter. Valor interiro que pode ir de 2 a 4.
        battleType - Tipo de batalha. Pode ser para pontuação ou não. Valor inteiro 1 ou 2.
        commandsPerCycle - Número maximo de comandos que um jogador pode enviar durante um só ciclo.
                           Por defeito são 20 comandos por ciclo. Este número ainda é experimental.
                           Minimo 1 comando por ciclo e maximo 20.
        'rounds' - Número de rounds que a batalha vai ter. Valor inteiro Min. 1. Max. 15. Por defeito 5.
        'round_duration' - Duração máxima em segundos que cada round pode ter. Valor inteiro Min. 10. Max. 300
        'password' - Palacra-Chave de acesso à batalh. Pode ter um minimo de 3 caracteres e um máximo de 15 caracteres.
        'selectedRobotsNum' - Número de robots virtuais que estão seleccionados
        'selectedRobots' - Lista com a referencia dos robots virtuais que estão seleccionados 
        
        Quando os valores estão todos correctos, retorna uma lista com os valores.
        """
        # Nome
        battleName = self.entryName.get_text()
        # Número máximo de jogadores que a batalha pode ter
        maxPlayers = self.to_int( self.entryMaxPlayers.get_text() )
        # Tipo da batalha: 1 - Com pontuação; 2 - Sem pontuação
        if ( self.radioButtonType.get_active() ):
            battleType = 2
        else:
            battleType = 1
        # Número máximo de comandos por ciclo. Para já este valor não deve ser alterado
        # Min. 1 - Max. 20
        commandsPerCycle = 20
        # Número de Rounds que a batalha vai ter
        nRounds = self.to_int( self.entryNRounds.get_text() ) 
        # Duração máxima em segundos que cada round pode ter
        roundsDuration = self.to_int( self.entryRoundsDuration.get_text() )
        # Password de acesso à batalha. Se não tiver password, o valor enviao é 'None'
        password = self.entryPassword.get_text()
        # Número de robots virtuais seleccionados
        selectedRobotsNum = len(self.selectedRobots)


        if ((len(battleName) < 3) or (len(battleName) > 50)):
            self.set_focus( self.entryName )
            return "Nome da batalha. Pode ter um minimo de 3 caracteres e um máximo de 50 caracteres.\n'battleName': " + str(battleName)


        if ((maxPlayers < 2) or (maxPlayers > 4)):
            self.set_focus( self.entryMaxPlayers )
            return "Número máximo de jogadores que a batalha pode ter. Valor inteiro que pode ir de 2 a 4.\n'maxPlayers': " + str(maxPlayers)

        if ((battleType != 1) and (battleType != 2)):
            return "Tipo de batalha. Pode ser para pontuação ou para testes. Valor inteiro 1 ou 2.\n'battleType': " + str(battleType)

        if ((commandsPerCycle < 1) or (commandsPerCycle > 20)):
            return "Número maximo de comandos que um jogador pode enviar durante um só ciclo. Valor inteiro Min. 1 e Max. 10.\n'commandsPerCycle': " + str(commandsPerCycle)

        if ((nRounds < 1) or (nRounds > 15)):
            self.set_focus( self.entryNRounds )
            return "Número máximo de rounds. Valor inteiro Min. 1. Max. 15. Por defeito 5.\n'rounds': " + str(nRounds)

        if ((roundsDuration < 10) or (roundsDuration > 300)):
            self.set_focus( self.entryRoundsDuration )
            return "Duração máxima em segundos que cada round pode ter. Valor inteiro Min. 10. Max. 300.\n'round_duration': " + str(roundsDuration)
        

        # Quando a batalha não tem password
        if ( password == '' ):
            password = 'None'
            
        elif ((len(password) < 3) or (len(password) > 15)):
            self.set_focus( self.entryPassword )
            return "Palacra-Chave de acesso à batalh. Pode ter um minimo de 3 caracteres e um máximo de 15 caracteres.\n'password': " + str(password)
    
    
        # Verifica se foram seleccionados mais robots viratais do que o número máximo de jogadores
        try:
            val = int( self.entryMaxPlayers.get_text() ) - 1
        except:
            val = 0    
        if ( selectedRobotsNum > val ):
            return "O número de robôs virtuais excede o número máximo de jogadores que a batalha pode ter.\n'maxPlayers': " + str(maxPlayers) + "\n'selectedRobots': " + str( selectedRobotsNum )
        
        
        
        # Carrega a lista das referencias dos robots virtuais seleccionados
        selectedRobots = []
        row = self.selectedRobots.get_iter_first()
        while ( row != None ):
            vRobot = self.selectedRobots.get_value( row, 0 )
            selectedRobots.append( self.virtualRobotsDict.values().index(vRobot) )
            row = self.selectedRobots.iter_next(row)

        
        
        return (battleName, maxPlayers, battleType, commandsPerCycle, nRounds, roundsDuration, password, selectedRobots)


        
        
    def create_battle(self):
        """
        
        """
        # (battleName, maxPlayers, battleType, commandsPerCycle, nRounds, roundsDuration, password)
        battleConf = self.check_battle_conf()
        
        if ( isinstance(battleConf, tuple) ):        
            thread = Thread( target = self.createCallback, args = [battleConf] )
            thread.start()
            self.destroy()
        
        else:
            text = "Um parâmetro inserido é inválido.\n\nDescrição: " + str(battleConf)
            md = GenericMessageDialog( None, text, gtk.MESSAGE_ERROR )
            md.show_it()
            


class AskForPassword():
    """
    Janela para pedir a password quando uma batalha tem password.
    """
    
    def __init__(self, callback, parent = None):
        """
        'callback' - metodo que é invocado quando o jogador pressiona um botão ou dá 'enter' na caixa de texto.
        'parent' - 'Parent' para a janela.
        """
        self.parent = parent
        self.callback = callback
        
        self.transDict = {
                      'title': 'Inserir Password',
                      'text': 'Password: ',
                      'checkButtonVisibility': 'Ocultar Palavra-Chave'
                     }


    def _make_callback(self, password):
        thread = Thread( target = self.callback, args = [password] )
        thread.start()



    def _give_password(self, widget = None, response = -1):
        """
        Verifica se a password inserida no 'entryPassword' está conforme as regras:
            - Min. - 3 caracteres
            - Max. - 15 caracteres
            
        Se estiver conforme as regras, invoca o metodo que foi passado à classe (callback) e envia como argumento 
        a password.
        """
        if ( response == gtk.RESPONSE_OK ):
            password = self.entryPassword.get_text()
            if ( password != '' ):
                # Verifica se está conforme as regras
                if ( (len(password) >= 3) and (len(password) < 15) ):
                    self._make_callback( password )
                    self.dialog.destroy()
                

            self.dialog.set_focus( self.entryPassword )

        elif ( response == gtk.RESPONSE_CANCEL ):
            self._make_callback( -1 )
            self.dialog.destroy()
        
        elif ( response == gtk.RESPONSE_DELETE_EVENT):
            self._make_callback( -1 )
            self.dialog.destroy()
            





    def _entryPassword_activate(self, entry):
        """
        Metodo que é invocado aquando do evento 'activate' do objecto 'entryPassword'
        """
        #self.dialog.response( gtk.RESPONSE_OK )
        self._give_password( response = gtk.RESPONSE_OK )



    def _checkButtonVisibility_toggled(self, checkButton):
        """
        Metodo que é invocado aquando do evento 'toggled' do objecto 'checkButtonVisibility'
        """
        if ( checkButton.get_active() == False ):
            self.entryPassword.set_visibility( True )
        
        else:
            self.entryPassword.set_visibility( False )
            


    def _create_w(self):
        self.dialog = gtk.MessageDialog(
                                    self.parent,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_OTHER,
                                    gtk.BUTTONS_OK_CANCEL,
                                    None)
        self.dialog.connect( 'response', self._give_password )
        self.dialog.set_title( self.transDict[ 'title' ] )
        
        
        #########################################################################################
        main_vbox = gtk.VBox(False, 0)
        
        
        #########################################################################################
        self.entryPassword = gtk.Entry(15)
        self.entryPassword.set_visibility( False )
        self.entryPassword.connect("activate", self._entryPassword_activate)
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label(self.transDict[ 'text' ]), False, 0, 0)
        hbox.pack_end(self.entryPassword)
        main_vbox.pack_start( hbox, False, False, 0)
        
        
        #########################################################################################
        checkButtonVisibility = gtk.CheckButton( self.transDict[ 'checkButtonVisibility' ] )
        checkButtonVisibility.set_active( True )
        checkButtonVisibility.connect( 'toggled', self._checkButtonVisibility_toggled )
        hbox = gtk.HBox(False, 0)
        hbox.pack_start( checkButtonVisibility, False, False, 0 )
        main_vbox.pack_start( hbox, False, False, 5 )
        
        
        #########################################################################################
        self.dialog.vbox.pack_start(main_vbox, True, True, 0)
        self.dialog.show_all()
        


    def get_password(self):
        """
        Metodo a ser invocado para iniciar o processo.
        """
        self._create_w()
        
        












def callback( response ):
    print "Password:"
    print response
    #gtk.mainquit()
    

"""
if __name__ == '__main__':
    a = GenericMessageDialog( 'testeeee', gtk.MESSAGE_ERROR )
"""
"""
if __name__ == '__main__':
    
    gtk.gdk.threads_init()
    
    a = AskForPassword( callback )
    a.get_password()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    







if ( __name__ == '__main__' ):
    a = BattlesListGUI()
    a.create_w()
    gtk.main()
"""


    