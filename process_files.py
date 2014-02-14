import AAA_sched_unsched

#  update data from directory
path = '/users/kbrooks/Documents/MH/Projects/Metrics/Distribution/Scheduled Unscheduled (CDC0089-1)/'
#wipe_tables()
get_facility_db(path)
read_dir(path)
populate_database()
print len(set(facility_data.keys())-set(facility_data_db.keys())), "records updated"
