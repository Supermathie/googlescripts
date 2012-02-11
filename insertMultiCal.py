#!/usr/bin/python

from __future__ import print_function

import datetime
import getpass
import sys

import GoogleCalendar

print('Google Username: ', end='')
user = sys.stdin.readline().strip()
passwd = getpass.getpass('Password for {0}: '.format(user))

try:
    calendar = GoogleCalendar.GoogleCalendar(user, passwd)
except GoogleCalendar.BadAuthentication as e:
    print(e, file=sys.stderr)
    sys.exit(1)


# ---------------------------------
# Edit this section to correspond to your list of events
mainEventDate = datetime.datetime(2012, 03, 01)

events = (
#( DayOffset, 'Event Title', 'Event Location', 'Event Content'),
 (  0, 'Main Event', 'Australia', "We're finally in Australia!"),
 ( -1, 'Plane Trip', None, "Don't forget to catch your flight"),
 ( -2, 'Book your taxi for Australia', None, None),
 ( -3, 'Find your passport', None, "It's probably in the dresser"),
 (  7, 'Recovery from vacation', 'Home', None),
)

# ---------------------------------

for event in events:
    calendar.insertAllDayEvent(
        date = primaryEventDate + datetime.timedelta(days=event[0]),
        title = event[1],
        where = event[2],
        content = event[3]
    )
