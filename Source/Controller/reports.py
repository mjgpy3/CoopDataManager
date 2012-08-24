#!/usr/bin/env python

# Created by Michael Gilliland
# Date: Thu Aug 23 21:32:56 EDT 2012

"""
    Contains a function to return all reports (get_current_reports), the Report class is used to set a standard for what reports
    should look like, and any additional functions generate reports and should be added in get_current_reports
"""

import queries
from datetime import datetime
import sys
sys.path.append('../Model')
import model_abstraction

def get_current_reports():
    """
        Used for adding reports to the reports view. All reports must have a name, format (e.g. html, csv, excel) and a generator function.
    """
    reports = []
    get_all_in_html = Report('Get all data', 'HTML', make_html_page_of_model)
    reports.append(get_all_in_html)
    get_all_in_excel = Report('Get all data', 'Excel', make_csv_page_of_model)
    reports.append(get_all_in_excel)
    return reports


class Report:
    """
        Represents a report
    """
    def __init__(self, name, output_format, generator):
        self.name = name
        self.output_format = output_format
        self.generator = generator


def make_html_page_of_model():
    """
        Makes an html file with a timestamp, showing all data currently in the model
    """
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

def make_csv_page_of_model():
    """
        Makes a csv file with a timestamp, showing all data currently in the model
    """
    now = str(datetime.now())
    now_string = now[:now.index('.')].replace(':', '_').replace(' ', '_')
    file_name = 'AllModelData-' + now_string + '.csv'
    model = model_abstraction.ModelStructure()
    model.build_from_schema()
    select = queries.SelectQuery(model)

    with open(file_name, 'w') as f:
        for table in model.tables + model.transaction_tables:
            table_data = select.get_all_data_from_table(table.name)
            f.write('%s\n' % table.name)
            f.write(','.join([str(i) for i in table_data.header]) + ',\n')
            for line in table_data.data:
                   f.write(','.join([str(i) for i in line]) + ',\n')
            f.write('\n')

