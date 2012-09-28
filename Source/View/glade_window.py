#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Sep 27 22:43:01 EDT 2012
# 
# 

"""
    In charge of handling those features that will probably be present in all views that are 
derived from Glade. Adding this slight bit of complexity should greatly reduce overall view
complexity.
"""

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

class GladeWindow:
    """
        The parent class for many windows, handling the glade views
    """
    def __init__(self, glade_file):
        self.glade_file = glade_file
        self.wTree = gtk.glade.XML(self.glade_file)

    def connect_widget_by_name(self, name, event, function, *args):
        """
            Connects a passed widget, specified by name to the passed function and then
            returns the widget with the name of name.
        """
        widget = self.wTree.get_widget(name)
        widget.connect(event, function, *args)
        return widget

    def connect_new_button(self, name, function, *args):
        """
            Creates a new button, connects it and returns it
        """
        widget = gtk.Button(name)
        widget.connect('clicked', function, *args)
        return widget


