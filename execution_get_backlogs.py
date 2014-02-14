from AAA_sched_unsched import *

# Calculate facility backlogs
path = '/users/kbrooks/Documents/MH/Projects/Metrics/Distribution/Scheduled Unscheduled (CDC0089-1)/'
get_facility_db(path)
#print facility_data_db


print calc_facility_backlog("GAH")
print calc_facility_backlog("ASH")
print calc_facility_backlog("GRO")

# Other things to look at:
#  ratio of unscheduled to scheduled (is work being pulled fast enough to keep up with backlog)
#  instantaneous backlog
#  smoothed backlog (more responsive than MA10). Use Loess?
#  trend in shipping, backlog, in process, new