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

meeting1=list(rrule(DAILY, count=7,
           dtstart=parse("20151214T090000"))) 


meeting2 = list(rrule(DAILY, count=7,
           dtstart = parse("20151214T103000")))

event1 = list(rrule(DAILY, count=3, 
           dtstart = parse("20151211T130000")))


calendar.extend(meeting1)
calendar.extend(meeting2)
calendar.extend(event1)


#so long as entries in workout are not in the list foo
    #    check to see if there is room to place [not a time set]the items from 
    #    into the list foo



#set two exercises, each with their own time interval in seconds 


squats = list(rrule(SECONDLY, interval=30, count = 1))

bench_press = list(rrule(SECONDLY, interval = 45, count=1))


