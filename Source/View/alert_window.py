#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Sep 27 23:59:56 EDT 2012
# 
# 

"""
    Kinda like the JavaScript alert function. It's just in charge of saying something to the user.
"""

import pygtk
pygtk.require('2.0')
import gtk

import glade_window

class AlertWindow(glade_window.GladeWindow):
    """
        The window used for displaying errors and other warnings.
    """
    def __init__(self, alert_string = 'Sorry!\nAn Unknown Error Has Occured.'):
        glade_window.GladeWindow.__init__(self, 'AlertWindow.glade')

        # Get the widgets
        self.window = self.connect_widget_by_name('wdwAlert', 'destroy', self.quit_this_window)
        self.btn_quit = self.connect_widget_by_name('btnOkay', 'clicked', self.quit_this_window)
        self.label = self.wTree.get_widget('lblAlertText')

        # Set attributes of the widgets
        self.window.set_resizable(False)
        self.window.set_title('Error...')    
        self.label.set_text(alert_string)

    def quit_this_window(self, sender):
        """
            Handles exiting the window
        """
        self.window.hide()
        gtk.main_quit()
