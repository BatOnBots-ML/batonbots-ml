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

import gtk


class AboutDialog(): 
    def __init__( self ):
        self._license = open( "LICENSE", "r" ).read()


    def showAbout( self, widget ):
        about = gtk.AboutDialog()
        about.set_program_name("BatOnBots-ML")
        about.set_version("Pre Alpha 0.1")
        about.set_copyright("Copyright 2013 BatOnBots-ML")
        about.set_authors( ["Cláudio Prates a.k.a. NuGuN"] )
        about.set_comments("Batalha Online de Robots - Multi-Linguagem")
        about.set_website("http://www.batonbots-ml.net/")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("ui/about_img.png"))
        about.set_license( self._license )
        about.run()
        about.destroy()
