#!/usr/bin/env python2

import cx_Oracle
import sys
try:
	username = sys.argv[1]
	password = sys.argv[2]

	host = sys.argv[3]
	port = sys.argv[4]
	inst = sys.argv[5]

	tbn = host+':'+port+'/'+inst

#print tbn

	con = cx_Oracle.connect(username, password, tbn)
	cursor = con.cursor()

	cursor.execute("""select TIME, trunc("CPU"/60) as "CPU", trunc("Concurrency"/60) as "Concurrency", trunc("System I/O"/60) as "System I/O", trunc("User I/O"/60) as "User I/O", trunc("Administrative"/60) as "Administrative", trunc("Configuration"/60) as "Configuration", trunc("Application"/60) as "Application", trunc("Network"/60) as "Network", trunc("Commit"/60) as "Commit", trunc("Scheduler"/60) as "Scheduler", trunc("Cluster"/60) as "Cluster", trunc("Queueing"/60) as "Queueing", trunc("Other"/60) as "Other" from (select nvl(wait_class,'CPU')  activity, trunc(sample_time,'MI') time from v$active_session_history) v pivot ( count(*) for activity in ( 'CPU' as "CPU", 'Concurrency' as "Concurrency", 'System I/O' as "System I/O", 'User I/O' as "User I/O", 'Administrative' as "Administrative", 'Configuration' as "Configuration", 'Application' as "Application", 'Network' as "Network", 'Commit' as "Commit", 'Scheduler' as "Scheduler", 'Cluster' as "Cluster", 'Queueing' as "Queueing", 'Other' as "Other")) where time > sysdate - interval '1'  minute""")
	cur = cursor.fetchone()

	cursor.close()
	con.close()
#print "DONE"
	print "CPU:%s Concurrency:%s sysio:%s userio:%s Administrative:%s Configuration:%s Application:%s Network:%s Commit:%s Scheduler:%s Cluster:%s Queueing:%s Other:%s" % cur[1:]
#except cx_Oracle.DatabaseError:
#	print "ERROR: Cannot connect to database!\n"
except IndexError:
	print "Usage: %s username password host port instance_name" % sys.argv[0]
#except:
#	print "ERROR: Unexcepted!"
