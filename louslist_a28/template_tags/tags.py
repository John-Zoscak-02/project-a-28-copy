from django import template
register = template.Library()


from datetime import datetime
from datetime import timedelta
import pytz

@register.filter(name='get_events')
def get_events(value):
    events = []

    switcher = {
    "Su" : 0,
    "Mo" : 1,
    "Tu" : 2,
    "We" : 3,
    "Th" : 4,
    "Fr" : 5,
    "Sa" : 6 }

    for class_event in value:
        days_str = class_event.days
        days = [days_str[i:i+2] for i in range(0, len(days_str), 2)]

        today = datetime.now().astimezone(pytz.timezone('America/New_York')).date()
        sunday = today - timedelta(days=(today.weekday()+1)%7)
        sunday_anchor = datetime(sunday.year, sunday.month, sunday.day)
        #print("anchor: ", sunday_anchor)
        if class_event.start_time and class_event.end_time:
            for day in days:
                starttime_delta = timedelta(days=switcher.get(day, 0), hours=int(class_event.start_time[:2]), minutes=int(class_event.start_time[3:5]))
                endtime_delta = timedelta(days=switcher.get(day, 0), hours=int(class_event.end_time[:2]), minutes=int(class_event.end_time[3:5]))
                
                start = sunday_anchor + starttime_delta
                end = sunday_anchor + endtime_delta
                summary = "%s: %s" % (class_event.course.department.subject, class_event.course.catalog_number)
                description = class_event.course.description
                location = class_event.facility_description
                print(start.strftime("%Y-%m-%dT%H:%M:00.00Z"), end.strftime("%Y-%m-%dT%H:%M:00.00Z"))
            
                events.append({
                    'summary': summary,
                    'description': description,
                    'location': location, 
                    'start': {
                        'datetime': start.strftime("%Y-%m-%dT%H:%M:00.00Z"),
                        'timeZone': 'America/New_York',
                    },
                    'end': {
                        'datetime': end.strftime("%Y-%m-%dT%H:%M:00.00Z"),
                        'timeZone': 'America/New_York',
                    },
                })
    return events

@register.filter(name='intersect')
def intersect(value, id):
    ct=0
    for friend in value.friends: 
        for cls in friend.schedule.classes:
            ct += value.schedule.get(id=id).intersect(cls)
    return ct
