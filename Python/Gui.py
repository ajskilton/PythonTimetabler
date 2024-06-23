import PySimpleGUI as sg
from TimeTable   import get_my_timetable
import arrow

layout = [
   [sg.T('Enter your calender link')],      
   [sg.Input(default_text=' ', key='-INPUT-')], 
   [sg.T('Enter the date you want to start from:')],
   [sg.Input(default_text='YYYY-M-D HH:mm:ss', key='-DATE_INPUT-')],
   [sg.CalendarButton('Choose Date', target="-DATE_INPUT-", key='-CALENDAR-')],
   [sg.Button(button_text="Generate", key='-GENERATE-')]
   ]

# Create the window
window = sg.Window('ORIGINAL', layout)

# Create an event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "-GENERATE-":
      print("GENERATING")
      date = arrow.get(values['-DATE_INPUT-'], 'YYYY-M-D HH:mm:ss').replace(hour=0, minute=0, second=0, microsecond=0, tzinfo='+12:00') 
      get_my_timetable(date.year, date.month, date.day, 6, values['-INPUT-'])
    

window.close()