#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Sun Jul 29 14:56:22 EDT 2012
# 
# 

import sys, Views, gtk, pygtk
window = Views.SelectIdWindow('Semester')
sys.path.append('../Controller')
import Queries
table_data = Queries.SelectQuery().GetAllDataFromTable('Semester')

window.AddTableData(table_data)

window.Window.show_all()

gtk.main()


print window.Highlighted
