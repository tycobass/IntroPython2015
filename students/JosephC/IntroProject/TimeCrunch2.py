#TimeCrunch

from datetime import *
from dateutil.rrule import *
from dateutil.parser import *

''' 
As there is only so much time in the day, we have to fit our workouts in somehow.  TimeCrunch looks at the calendar on your phone and suggests workouts, 
big and small, that appear to fit your schedule.  

TimeCrunch is for those trying to develop good fitness habits, rather than more experienced and dedicated individuals who already have established workout 
plans.  The latter folks make time to get fit.  TimeCrunch is for those who perpetually complain about lack of time to work out.  If your calendar is accurate,
then TimeCrunch will find time for you to develop good habits.  
'''

#   create a calendar and a list of meetings and events
calendar = []


meeting1 = list(rrule(DAILY, count=7,
                dtstart=parse("20151214T090000"))) 


meeting2 = list(rrule(DAILY, count=7,
                dtstart = parse("20151214T103000")))

event1 = list(rrule(DAILY, count=3, 
              dtstart = parse("20151211T130000")))

squats = list(rrule(SECONDLY, interval=30, count = 1)) 

chair_squats = list(rrule(SECONDLY, interval = 30, count = 1))

pushups = list(rrule(SECONDLY, interval = 45, count=1))

crunches = list(rrule(SECONDLY, interval = 14, count = 1))

arm_circles = list(rrule(SECONDLY, interval = 12, count = 1))

leg_curl = list(rrule(SECONDLY, interval = 24, count = 1))



your_events = [meeting1, meeting2, event1, squats, chair_squats, pushups, crunches, arm_circles, leg_curl]

for d in your_events:
    #print(d)
    calendar.extend(d)

sorted(calendar)
"""
time_format = "%a %b %d %H:%M:%S %Y"
for i in calendar:
    if i in calendar:
        print("You have time to time to do {}!".format(today.strftime(time_format)))
"""
 
if squats in your_events: print("You have space to do a set of squats (it'll only take you 30 seconds!).")
if chair_squats in your_events: print("You have space to a set of squats from your chair (it'll only take you 30 seconds!).")
if pushups in your_events: print("You have space to do a set of pushups (it'll only take you 45 seconds!).")
if crunches in your_events: print("You have space to do a set of crunches (it'll only take 14 seconds!).")
if arm_circles in your_events: print("You have space to a round of arm circles (it'll only take 12 seconds1).")
if leg_curl in your_events: print("You have space to do a set of leg curls (it'll only take 24 seconds per leg!).")

#Offer the use ability to look through their calendar, converting the wierd datetime format to something more human-readable


