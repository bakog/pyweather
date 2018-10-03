# coding=utf-8

import tkinter as tk
from tkinter import ttk, Menu
import json
import collections
import requests
import time
import pprint

APIKEY = '98b287dc820ee3913a9c9082ed2f79db'
#APIKEY = '493d738091d8a1a591bb85ccf1b0c32c'

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        countries = list()
        cities = list()
        City = collections.namedtuple('City', 'id, name, countrycode')

        with open('city.list.json') as in_file:
            cities_data = json.load(in_file)

        for city in cities_data:
            if city['country']:
                cities.append(City(id=city['id'], name=city['name'], countrycode=city['country']))

        with open('country_data_json.json', 'r') as country_file:
            countries_data = json.load(country_file)

        for country in countries_data:
            countries.append(country['Name']+" - (" +country['Code']+(')'))

        countries = sorted(countries, key=lambda x: x[0])
        cities_list= sorted(cities, key=lambda x: x.name)

        mainframe = ttk.Frame(self)
        mainframe.pack(fill='both', expand=True)

        mainmenu = Menu(self)
        self.config(menu=mainmenu)
        self.config(padx=3, pady=3)

        def quit():
            self.destroy()

        def get_weather_info(city, units):
            print(city.id)
            api_url = 'http://api.openweathermap.org/data/2.5/forecast?id={}&units={}&lang=hu&APPID={}'.format(city.id, units, APIKEY)
            #print(api_url)
            response = requests.get(api_url)

            if response.status_code == 200:
                #print(json.loads(response.content.decode('utf-8')))
                return json.loads(response.content.decode('utf-8'))
            else:
                return "HIBA"


        def get_current_weather_info(city, units):
            print(city.id)
            api_url = 'http://api.openweathermap.org/data/2.5/weather?id={}&units={}&lang=hu&APPID={}'.format(city.id, units, APIKEY)
            #print(api_url)

            response = requests.get(api_url)

            if response.status_code == 200:
                # print(json.loads(response.content.decode('utf-8')))
                return json.loads(response.content.decode('utf-8'))
            else:
                return "HIBA"


        def detail():
            '''
            Előrejelzési adatok megjelenítés tizesével
            :return:
            '''
            city = varosok.get()
            filtered_city = list(filter(lambda x: x.name == city, cities))
            city = filtered_city[0]
            unit = metric_list.get()
            if unit=='SI':
                units = 'metric'
            else:
                units = 'imperial'
            try:
                forecast_weather_info = get_weather_info(city, units)
                detail_win = Elorejelzes(forecast_weather_info, units)
                detail_win.title("Előrejelzés")
                detail_win.wm_minsize(500, 400)
                detail_win.mainloop()

            except requests.exceptions.ConnectionError:
                btn_detail.grid_forget()
                status_label.configure(text='Az adatok lekérése sikertelen, próbálja meg később!')  # hiba
                #print('Az adatok lekérése sikertelen, próbálja meg később!')

        def select_country():
            country = orszagok.get().split('(')[1].rstrip(')')
            #print(country)
            cities_list = sorted([x.name for x in cities if x.countrycode == country])
            varosok.configure(values=cities_list)
            #print(cities_list)

        def data_search():
            city = varosok.get()
            filtered_city = list(filter(lambda x: x.name == city, cities))
            city = filtered_city[0]
            #print(city)
            unit = metric_list.get()
            if unit == 'SI':
                units = 'metric'
            else:
                units = 'imperial'

            def display_weather_info(weather_info, units):

                if units == 'metric':
                    temp = "°C"
                    speed = 'km/h'
                else:
                    temp = '°F'
                    speed = "m/h"

                # a legleső adatsor megjelenítése

                #pprint.pprint(weather_info)
                city = weather_info['name']
                #date = weather_info['dt_txt']
                max_T = weather_info['main']['temp_max']
                min_T = weather_info['main']['temp_min']
                pressure = weather_info['main']['pressure']
                humidity = weather_info['main']['humidity']
                wind = weather_info['wind']['speed']
                description = weather_info['weather'][0]['description']
                #print(f'Település: {city}')  # hely neve
                # a legkorábbi előrejelzés

                label_datum = ttk.Label(mainframe, text=f'Jelenlegi időjárás')  # az 1. előrejelzés
                label_datum.grid(row=5, column=0, columnspan=2)

                label_max = ttk.Label(mainframe, text=f'Maximum hőmérséklet: {max_T} {temp}')  # max hőmérséklet
                label_max.grid(row=6, column=0, columnspan=2)

                label_min = ttk.Label(mainframe, text=f'Minimum hőmérséklet: {min_T}  {temp}')  # min hőmérséklet
                label_min.grid(row=7, column=0, columnspan=2)

                label_pressure = ttk.Label(mainframe, text=f'Légnyomás: {pressure} hPa')  # légnyomás
                label_pressure.grid(row=8, column=0, columnspan=2)

                label_humidity = ttk.Label(mainframe, text=f'Páratartalom: {humidity} %')  # légnedvesség
                label_humidity.grid(row=9, column=0, columnspan=2)

                label_wind = ttk.Label(mainframe, text=f'Szélsebesség: {wind} {speed}')  # szélsebesség
                label_wind.grid(row=10, column=0, columnspan=2)

                label_description = ttk.Label(mainframe, text=f'Leírás: {description}')  # leírás
                label_description.grid(row=11, column=0, columnspan=2)

                # státuszsor
                status_label.configure(text='')  # hiba

            try:
                print("most kéne csatlakozni...")
                #weather_info = get_weather_info(city)
                weather_info = get_current_weather_info(city, units)
                display_weather_info(weather_info, units)

            except requests.exceptions.ConnectionError:
                btn_detail.grid_forget()
                status_label.configure(text='Az adatok lekérése sikertelen, próbálja meg később!')  # hiba
                #print('Az adatok lekérése sikertelen, próbálja meg később!')

        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label='Quit', command=quit)
        mainmenu.add_cascade(label='File', menu=filemenu)

        orszagok_label = ttk.Label(mainframe, text="Válassz az országok kódjai közül! ")
        orszagok_label.grid(row=0, column=0, pady=10)
        orszagok = ttk.Combobox(mainframe, values=countries, state='readonly', height=10)
        orszagok.grid(row=0, column=1)
        orszagok.bind('<<ComboboxSelected>>', lambda w: select_country())

        varosok_label = ttk.Label(mainframe, text="Válassz a városok közül! ")
        varosok_label.grid(row=1, column=0, pady=10)
        varosok = ttk.Combobox(mainframe, values=cities_list, state='readonly', height=10)
        varosok.grid(row=1, column=1)
        #varosok.bind('<<ComboboxSelected>>', lambda x: data_search())

        metric_label = ttk.Label(mainframe, text="Mértékegység")
        metric_label.grid(row=2, column=0)
        metric_list = ttk.Combobox(mainframe, values=['SI', 'Imperial'],state='readonly', height=2)
        metric_list.grid(row=3, column=1)
        metric_list.bind('<<ComboboxSelected>>', lambda x: data_search())


        btn_detail = ttk.Button(mainframe, text="Előrejelzés")
        btn_detail.bind('<Button-1>', lambda x: detail())
        btn_detail.grid(row=4, column=1, columnspan=2)

        status_row = ttk.Frame(self)
        status_row.pack(fill='x', padx=2, pady=5)
        status_label = ttk.Label(status_row, text="", foreground='red')
        status_label.pack(side="left", fill='x')

class Elorejelzes(tk.Toplevel):
    def __init__(self, weather_info, units):
        tk.Toplevel.__init__(self)

        self.start = 0
        self.stop = 10
        self.weather_info = weather_info
        self.data_labels= []
        self.units = units

        self.mainframe = tk.Frame(self)
        self.mainframe.pack(fill="both", expand=True)

        self.tableframe = ttk.Frame(self.mainframe)
        self.tableframe.pack(fill="both", expand=True)

        l_date = ttk.Label(self.tableframe, text="Dátum")
        l_date.grid(row=0, column=1, padx=10, pady=5)
        l_max = ttk.Label(self.tableframe, text="Maximum hőmérséklet")
        l_max.grid(row=0, column=2, padx=10)
        l_min = ttk.Label(self.tableframe, text="Minimum hőmérséklet")
        l_min.grid(row=0, column=3, padx=10)
        l_pressure = ttk.Label(self.tableframe, text="Légnyomás")
        l_pressure.grid(row=0, column=4, padx=10)
        l_humidity = ttk.Label(self.tableframe, text="Páratartalom")
        l_humidity.grid(row=0, column=5, padx=10)
        l_wind = ttk.Label(self.tableframe, text="Szél")
        l_wind.grid(row=0, column=6, padx=10)
        l_description = ttk.Label(self.tableframe, text="Leírás")
        l_description.grid(row=0, column=7, padx=10)

        def clean_labels():
            for d in self.data_labels:
                d.configure(text='')

        def next():
            clean_labels()

            #print(len(weather_info['list']),'---', self.start, self.stop)
            self.start = self.stop
            if len(weather_info['list'])>=self.stop+10:
                self.stop += 10
            else:
                self.stop = len(weather_info['list'])
            if self.stop==len(weather_info['list']):
                btn_next.grid_forget()
            if self.start>=10:
                btn_prev.grid(row=20, column=1)
            self.show_data(self.weather_info, self.start, self.stop)

        def prev():
            clean_labels()

            #print(len(weather_info['list']),'---', self.start, self.stop)
            self.stop = self.start
            if self.start-10>=0:
                self.start -= 10
            else:
                self.start = 0
            if self.start<10:
                btn_prev.grid_forget()
            if self.stop<len(weather_info['list']):
                btn_next.grid(row=20, column=2)

            self.show_data(self.weather_info, self.start, self.stop)

        btn_prev = ttk.Button(self.tableframe, text="Előző adatok")
        #btn_prev.grid(row=20, column=0)
        btn_prev.bind('<Button-1>', lambda w: prev())
        btn_next = ttk.Button(self.tableframe, text="További adatok")
        btn_next.grid(row=20, column=2)
        btn_next.bind('<Button-1>', lambda w: next())


        self.show_data(self.weather_info, self.start, self.stop)

    def show_data(self,  weather_info, start, stop):
        row = 1

        if self.units == 'metric':
            temp = "°C"
            speed = 'km/h'
        else:
            temp = '°F'
            speed = "m/h"

        for data in weather_info['list'][start:stop]:
            date = data['dt_txt']
            max_T = data['main']['temp_max']
            min_T = data['main']['temp_min']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            description = data['weather'][0]['description']

            data_label_date = ttk.Label(self.tableframe, text=date)
            data_label_date.grid(row=row, column=1)
            data_label_max = ttk.Label(self.tableframe, text=f'{max_T} {temp}')
            data_label_max.grid(row=row, column=2)
            data_label_min = ttk.Label(self.tableframe, text=f'{min_T} {temp}')
            data_label_min.grid(row=row, column=3)
            data_label_pressure = ttk.Label(self.tableframe, text=pressure)
            data_label_pressure.grid(row=row, column=4)
            data_label_humidity = ttk.Label(self.tableframe, text=humidity)
            data_label_humidity.grid(row=row, column=5)
            data_label_wind = ttk.Label(self.tableframe, text=f'{wind} {speed}')
            data_label_wind.grid(row=row, column=6, padx=10)
            data_label_description = ttk.Label(self.tableframe, text=description)
            data_label_description.grid(row=row, column=7)

            self.data_labels.append(data_label_date)
            self.data_labels.append(data_label_max)
            self.data_labels.append(data_label_min)
            self.data_labels.append(data_label_pressure)
            self.data_labels.append(data_label_humidity)
            self.data_labels.append(data_label_wind)
            self.data_labels.append(data_label_description)

            row += 1




if __name__ == '__main__':
    app = App()
    app.title('Időjárás előrejelzés')
    app.wm_minsize(400, 300)
    app.mainloop()