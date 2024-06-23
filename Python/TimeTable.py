# This code is used to create a timetable for a week using the data from a CSV file.
# The CSV file contains the following columns: Name, Option, Day, Start Time, Duration, Location

import csv
from math import floor
from ics import Calendar, Event
import arrow
from datetime import datetime, timedelta
import requests

def day2num(day):
    if day == "Monday":
        return 0
    elif day == "Tuesday":
        return 1
    elif day == "Wednesday":
        return 2
    elif day == "Thursday":
        return 3
    elif day == "Friday":
        return 4
    elif day == "Saturday":
        return 5
    elif day == "Sunday":
        return 6

def sum_totals(totals, name, duration):
    if name in totals:
        totals[name] += duration
    else:
        totals[name] = duration

def create_event(calender, name, type, date_time, duration_hours, location):
    event = Event()
    # Set the name of the event
    event.name = name + "-" + type
    # Set date  and time of event from next Monday
    event.begin = date_time
    # Set the end time of the event
    event.end = event.begin.shift(hours=duration_hours)
    # Set the location of the event
    event.location = location
    # Add the event to the calendar
    calender.events.add(event)

def is_time_slot_available(calender, date_time: arrow):
    for event in calender.events:
        if(event.begin - date_time).days == 0:
            if(event.begin - date_time).days == 0 and date_time.hour >= event.begin.hour and date_time.hour < event.end.hour:
                return False
    # no event at that time
    return True

def get_my_timetable(start_year: int, start_month: int, start_day: int, weeks_duration: int, calender_url: str):
    # Dictionary to store the total duration of each subject
    totals = {}

    # Get the current date and time
    now = arrow.now('+12:00').replace(hour=0, minute=0, second=0, microsecond=0)

    firstDay = arrow.get(datetime(start_year, start_month, start_day, hour=0, minute=0, second=0, microsecond=0), tzinfo='+12:00')
    lastDay = firstDay.shift(weeks=+weeks_duration)

    cal_url = Calendar(requests.get(calender_url).text)

    # create second calender for self study
    cal_self = Calendar()

    cal_timetable = Calendar()

        # Read the data from the Cal url
    for event in cal_url.events:
        if event.begin < firstDay or event.begin > lastDay:
            continue
        else:
            event_time = event.begin.shift(hours=+12)
            create_event(cal_timetable, event.name.split('/')[0], event.description[event.description.find("ActivityType Description: ")+len("ActivityType Description: "):].split("\nLocation")[0].strip(), event_time, event.duration.seconds//3600, event.location)
            sum_totals(totals, event.name.split('/')[0].strip(), event.duration.seconds//3600)

    # for event in cal_timetable.events:
        # print(event.name, event.begin, event.end, event.location)

    # Print the total duration of each subject
    for key, value in totals.items():
        print(key, value, "hours")

    print("\n")

    # Create self-study events
    # Calculate which subject has the least total duration
    event_exists = False
    next_hour_unavailable = False
    last_subject = ""

    end_week = (lastDay - firstDay).days//7
    # Create self-study events
    for week in range(0, end_week):
        for week_day in range(0, 5):
            break_taken = False
            for hour in range(9, 17):
                date = firstDay.shift(weeks=+week, days=+week_day, hours=+hour)

                is_available = is_time_slot_available(cal_timetable, date)

                if hour >= 12 and not break_taken and is_available:
                    create_event(cal_self, "BREAK TIME", "NA", date, 1, "anywhere")
                    break_taken = True
                    continue

                min_subject = min(totals, key=totals.get)
                if last_subject == min_subject:
                    min_subject = sorted(totals, key=totals.get)[1]
                
                if is_available:
                    create_event(cal_self, min_subject, "Self-Study", date, 1, "anywhere")
                    last_subject = min_subject
                    sum_totals(totals, min_subject, 1)

    # Save the calendar to a file
    with open('Timetable.ics', 'w') as my_file:
        my_file.writelines(cal_timetable)

    with open('SelfStudy.ics', 'w') as my_file:
        my_file.writelines(cal_self)

    # Print the total duration of each subject
    print("\n\nTotal hours over", end_week, "weeks")
    for key, value in totals.items():
        print(key, value, "hours")

    print("\nAvg weekly hours over", end_week, "weeks")
    for key, value in totals.items():
        print(key, value/end_week, "hours")




# for alex in 2024 sem 2
# get_my_timetable(2024, 7, 15, 6, "https://cyon-syd-v4-api-d4-01.azurewebsites.net//api/ical/9918847d-0e11-4f16-9354-2df982b9374d/28a887ff-0b5a-16ee-05f1-eac61d9b129c/timetable.ics")