#!/usr/bin/python

import atom
import datetime
import getpass

import gdata.calendar.service

BadAuthentication = gdata.service.BadAuthentication

class UTC(datetime.tzinfo):
    def utcoffset(self, date):
        return datetime.timedelta()
    def dst(self, date):
        return datetime.timedelta()
    def tzname(self, date):
        return "UTC"

class LOCAL(datetime.tzinfo):
    timediff = datetime.datetime.now().replace(second=0,microsecond=0) - \
               datetime.datetime.utcnow().replace(second=0,microsecond=0)
    def utcoffset(self, date):
        return self.timediff
    def dst(self, date):
        return datetime.timedelta()
    def tzname(self, date):
        return "localtime"

def fixNaiveDatetime(dt):
    '''If dt is a naive datetime, add our best guess of local timezone'''
    if dt.utcoffset() is None:
        return dt.replace(tzinfo=LOCAL())

class GoogleCalendar():
    def __init__(self, user, passwd,
                 calendarpath='/calendar/feeds/default/private/full'):
        self.user = user
        self.calendarpath = calendarpath
        self.service = gdata.calendar.service.CalendarService()
        self.service.ssl = True
        self.service.ClientLogin(user,passwd)

    def _doInsertEvent(self, title, when, content, where):
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        if content:
            event.content = atom.Content(text=content)
        if where:
            event.where = gdata.calendar.Where(where)
        event.when.append(when)
        return self.service.InsertEvent(event, self.calendarpath)
        
    def insertAllDayEvent(self, title, date, content=None, where=None):
        when = gdata.calendar.When(
            start_time = date.strftime('%F'),
            end_time = (date+datetime.timedelta(days=1)).strftime('%F')
        )
        return self._doInsertEvent(title, when, content, where)

    def insertEvent(self, title, start, end=None, duration=None,
                    content=None, where=None):
        if not (end or duration):
            raise ValueError("must specify end time or duration")
        if not end:
            end = start + duration
        when = gdata.calendar.When(
            start_time = fixNaiveDatetime(start).isoformat(),
            end_time = fixNaiveDatetime(end).isoformat()
        )
        return self._doInsertEvent(title, when, content, where)
