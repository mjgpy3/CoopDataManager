#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Sep 27 23:52:17 EDT 2012
# 
# 

import pygtk
pygtk.require('2.0')
import gtk

import glade_window
import actions

class ReportsWindow(glade_window.GladeWindow):
    """
        A window which allows the user to select known reports and generate them.
    """
    def __init__(self, reports):
        # Non-widget data
        self.highlighted = None
        self.reports = reports
        self.current_action = actions.table['None']

        glade_window.GladeWindow.__init__(self, 'ReportsWindow.glade')

        # Get the widgets
        self.window = self.connect_widget_by_name('wdwReports', 'destroy', self.quit_this_window)
        self.btn_generate = self.connect_widget_by_name('btnGenerate', 'clicked', lambda x: gtk.main_quit())
        self.btn_cancel = self.connect_widget_by_name('btnCancel', 'clicked', self.quit_this_window)
        self.cmb_select_reports = self.connect_widget_by_name('cmbSelectReports', \
                                                              'changed', self.set_different_report)

        # Set the combobox's entires
        for report in reports:
            self.cmb_select_reports.append_text(report.name + ' - ' + report.output_format)
        self.window.set_title('Reports')
        self.cmb_select_reports.set_active(0)
        self.cmb_select_reports.set_visible(True)

    def set_different_report(self, sender):
        """
            Sets the current report if the user changed it to a valid option
        """
        if self.cmb_select_reports.get_active() != 0:
            self.highlighted = self.reports[self.cmb_select_reports.get_active() - 1]
            self.current_action = actions.table['Reports']
        else:
            self.current_action = actions.table['Quit']

    def quit_this_window(self, sender):
        """
            Handles quitting the window
        """
        self.current_action = actions.table['Quit']
        gtk.main_quit()
