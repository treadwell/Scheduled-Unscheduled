# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import re
import os
import csv
import sqlite3
from datetime import datetime
from re import sub

# <codecell>

### Processing Layer ###

class Facility(object):
    def __init__(self, date, location, new, sched,
                 unsched, ship, susp, old, future, hold):
        
        # properties:
        # location: Gahanna, Ashland, or Groveport
        # date
        # new: new_orders
        # sched: scheduled orders
        # unsched: unscheduled orders
        # ship: ship confirms
        # susp: suspended orders
        # old: old in process
        # future: future orders
        # hold: hold or problem orders

        # can do arbitrary things with the input, like any fn
        # print date
        # date = datetime.datetime(date)
        
        # this is a schema

        self.date = date
        #  assert location in ('Gahanna', 'Ashland', 'Groveport')
        self.location = location
        self.new = new
        self.sched = sched
        self.unsched = unsched
        self.ship = ship
        self.susp = susp
        self.old = old
        self.future = future
        self.hold = hold
    
    def __repr__(self):
        return str(self.__dict__)

    # __str__ = __repr__ ## uncomment this if printing doesn't work well
        
### Open questions
	# 1. How can I write to and call from a db?
		# easiest option: sqlite
		# if you want to use something else: pyodbc
	# 2. for the application layer -
		#### encapsulate input & output in functions
		# script structure:
		## bunch of definitions
		## small loop or script that does stuff, inside "if __name__ == '__main__':"
		### don't worry about this immediately - just have a short script at the end

# <codecell>

### Input Layer ###


#filename ='CDC0089 01-09-14.TXT'
#path = '.'

#files = os.listdir(os.getcwd())




#filename ='CDC0089 01-10-14.TXT'

#files = os.listdir(path)

facility_data = {}
def read_file(path, filename):
	
    with open(path + filename) as f:
        # alternative: pull things directly by line number
        lines = list(f)

    assert "TOTAL NEW ORDERS" in lines[11]
    assert "TOTAL SCHEDULED ORDERS" in lines[36]
    assert "TOTAL UNSCHEDULED ORDERS" in lines[49]
    assert "TOTAL SHIPMENT CONFIRM" in lines[60]
    assert "SUSPENDED SHIPMENTS" in lines[63]
    assert "OLD INPROCESS (INP)" in lines[66]
    assert "FUTURE DATED" in lines[67]
    assert "HOLDS / ERRORS" in lines[68]


    order_types = {'new':11,
                   'sched':36,
                   'unsched':49,
                   'ship':60,
                   'susp':63,
                   'old':66,
                   'future':67,
                   'hold':68}


    order_type_names = ['new', 'sched',
                         'unsched', 'ship', 'susp', 'old', 'future', 'hold']

    L_names = {'GAH':[52,60],
               'ASH':[90,96],
               'GRO':[126,132]} # location_names

    date = str([word for word in lines[1].split() if '/' in word]).strip("[]\'")
    date = datetime.strptime(date, '%m/%d/%y')
    date = date.strftime('%Y-%m-%d')
    

    for L in L_names.keys():  # cycle through the locations, sequence doesn't matter
        order_type_data = []
        order_type_data_1 = []

        for o in order_type_names:  # cycle through order_types.  Sequence matters, necessitating a separate list
            order_type_data.append(lines[order_types[o]][L_names[L][0]:L_names[L][1]].replace(' ', ''))
	    
        for d in order_type_data:
            if d == '':
                order_type_data_1.append(0)
            else:
                order_type_data_1.append(int(sub(r'[^\d.]', '', d)))

        facility_data[(L,date)] = Facility(date, L, *order_type_data_1)

    return date, facility_data

#date, facility_data = read_file(path, filename)

print "------------ START OF DIRECTORY PROCESSING ------------"
def read_dir(path):
    files = os.listdir(path)
    data_files = [file for file in files if 'CDC0089' in file]
    for file in data_files:
        read_file(path, file)
	
def get_facility_db(path):  # complete this once database output is working.
    facility_data_1 = {}
    name = "facility_data.db"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
    for f, facility in [("Gahanna", "GAH"), ("Ashland", "ASH"), ("Groveport", "GRO")]:
        c.execute("Select * from " + f)
        ### check that the headers in the table match what you're expecting
        data = c.fetchall()
        for d in data:
            d_key = (facility, str(d[0])) # turn d[0] directly into a datetime object
            d_value = Facility(str(d[0]), facility, *d[1:]) #d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            ### check that d is being unpacked correctly
            facility_data_1[d_key] = d_value
    #print "facility_data_1:", facility_data_1
    print "number objects:", len(facility_data_1.keys())
    return
    
print "----------------- END OF INPUT LAYER ------------------"

# <codecell>

### Output Layer ###


def cvs_fac(facility,date):
    f = facility_data[(facility, date)]
    return [f.new, f.sched, f.unsched, f.ship, f.susp, f.old, f.future, f.hold]

def display_fac(facility,date):
    return '\t'.join(cvs_fac(facility, date))


def fac_to_screen(date): 
	print date, display_fac('GAH', date), display_fac('ASH', date), display_fac('GRO', date)

# fac_to_screen(date)  # this needs to be driven by filename

def fac_to_csv(date):  # what is the input here?  The objects by name?
	save_filename = 'Scheduled Unscheduled.csv'
	csvRow = [date] + cvs_fac('GAH', date) + cvs_fac('ASH', date) + cvs_fac('GRO', date)
	myfile = open(path + save_filename,'a')
	writer = csv.writer(myfile)
	writer.writerow(csvRow)
	myfile.close()
	print date, "data saved to file:", save_filename

# <codecell>

def fac_to_db(facility, date):
    name = "facility_data.db"
    path = "/users/kbrooks/Documents/MH/Projects/Metrics/Distribution/Scheduled Unscheduled (CDC0089-1)/"
    schema = "(date integer, new integer, sched integer, unsched integer, ship integer, susp integer, old integer, future integer, hold integer)"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
	    
    if facility == "GAH":
        table = "Gahanna"
    elif facility == "ASH":
        table = "Ashland"
    elif facility == "GRO":
        table = "Groveport"
    else:
        raise UnsupportedFacility
        # exceptions should end with Exception or Error - UnsupportedFacilityException

    ## this should be a dictionary
        

        
    # create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS ''' + table + schema)
    
    c.execute("INSERT INTO " + table + " VALUES " + str(insert_tuple(facility,date)))
    conn.commit()
    conn.close()
    return

def insert_tuple(facility,date):
    ### fix this
    return (facility_data[(facility,date)].date, facility_data[(facility,date)].new, \
            facility_data[(facility,date)].sched, facility_data[(facility,date)].unsched, \
            facility_data[(facility,date)].ship, facility_data[(facility,date)].susp, \
            facility_data[(facility,date)].old, facility_data[(facility,date)].future, \
            facility_data[(facility,date)].hold)

# fac_to_db("GAH", "12/12/13")

# <codecell>

# populate the database
def populate_database():
    dates = sorted(list(set([date for facility, date in facility_data.keys()])))
    locations = sorted(list(set([facility for facility, date in facility_data.keys()])))
    for date in dates:
        for location in locations:
            fac_to_db(location, date)    
    print "database update completed"

# <codecell>

def wipe_tables():
    name = "facility_data.db"
    path = "/users/kbrooks/Documents/MH/Projects/Metrics/Distribution/Scheduled Unscheduled (CDC0089-1)/"
    conn = sqlite3.connect(path + name)
    c = conn.cursor()
	    
    for table in ["Gahanna", "Ashland", "Groveport"]:
        print "deleting:", table
        c.execute('''DROP table ''' + table)
        # create the table afterwards
        
    conn.commit()
    conn.close()



### the control script

if __name__ == "__main__":
    #wipe_tables()
    # really good testing tool: http://docs.python.org/2/library/doctest.html

    #  update data from directory
    path = '/users/kbrooks/Documents/MH/Projects/Metrics/Distribution/Scheduled Unscheduled (CDC0089-1)/'
    #wipe_tables()
    read_dir(path)

    graceful_failing_in_get_facility_db = False
    if graceful_failing_in_get_facility_db:
        get_facility_db(path)
    ## this should fail gracefully (i.e. return no answer for the facility in
    ## question) if a given table isn't there
    # one option: print a warning like "<<facility>> not found, list of all tables: xyz"

    populate_database()


