#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Aug 23 21:32:56 EDT 2012
# 
# 

import queries
from datetime import datetime
import sys
sys.path.append('../Model')
import model_abstraction

def get_current_reports():
    reports = []
    get_all_in_html = Report('Get all data', 'HTML', make_html_page_of_model)
    reports.append(get_all_in_html)
    return reports


class Report:
    def __init__(self, name, output_format, generator):
        self.name = name
        self.output_format = output_format
        self.generator = generator


def make_html_page_of_model():
    now = str(datetime.now())
    now_string = now[:now.index('.')].replace(':', '_').replace(' ', '_')
    file_name = 'AllModelData-' + now_string + '.html'
    model = model_abstraction.ModelStructure()
    model.build_from_schema()
    select = queries.SelectQuery(model)

    with open(file_name, 'w') as f:
        f.write('<html>\n  <head>\n  </head>\n  <body>\n')
        for table in model.tables + model.transaction_tables:
            table_data = select.get_all_data_from_table(table.name)
            f.write('      <h1>%s</h1>\n' % table.name)
            f.write('        <table border="1">\n')
            f.write('          <tr><th>' + '</th><th>'.join([str(i) for i in table_data.header]) + '</th></tr>\n')
            for line in table_data.data:
                   f.write('          <tr><td>' + '</td><td>'.join([str(i) for i in line]) + '</td></tr>\n')
            f.write('        </table>\n')
        f.write('  </body>\n</html>')

