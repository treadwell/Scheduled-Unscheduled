from AAA_sched_unsched import *

path = "/users/kbrooks/Documents/MH/Projects/Metrics/Distribution/Scheduled Unscheduled (CDC0089-1)/"

print "Pre-update records"
print count_db_records(path)

incr_db_update(path)

print "Post-update records"
print count_db_records(path)

# add more data types (orders, lines, units)
