# coding=utf-8

import tkinter as tk
from tkinter import ttk, Menu, Listbox
import json
import collections
import requests

APIKEY = '98b287dc820ee3913a9c9082ed2f79db'

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        cities = list()
        City = collections.namedtuple('City', 'id, name, countrycode')
        with open('city.list.json') as in_file:
            data = json.load(in_file)

        for city in data:
            cities.append(City(id=city['id'], name=city['name'], countrycode=city['country']))

        #print (cities[0:5])
        mainframe = ttk.Frame(self)
        mainframe.pack(fill='both', expand=True)

        mainmenu = Menu(self)
        self.config(menu=mainmenu)
        self.config(padx=3, pady=3)

        def quit():
            self.destroy()

        def data_search():
            city = varosok.get()
            id  = city['id']
            name = city['name']
            api_url = 'http://api.openweathermap.org/data/2.5/forecast?id=7284829&units=metric&lang=hu&APPID={}'.format(
                APIKEY)

            response = requests.get(api_url)

            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            else:
                return "HIBA"

        filemenu = Menu(mainmenu, tearoff=0)
        #filemenu.add_command(label="Search", command=search)
        filemenu.add_command(label='Quit', command=quit)
        mainmenu.add_cascade(label='File', menu=filemenu)

        varosok_label = ttk.Label(mainframe, text="Válassz a városok közül! ")
        varosok_label.grid(row=0, column=0)
        # varosok = Listbox(mainframe)
        # varosok.grid(row=0, column=1)
        # for item in cities[:5]:
        #     varosok.insert('end', item)
        varosok = ttk.Combobox(mainframe, values= cities[:5], state='readonly', height=4)
        varosok.grid(row=0, column=1)
        varosok.bind('<Button-1>', lambda w: data_search())




if __name__ == '__main__':
    app = App()
    app.title('Időjárás előrejelzés')
    app.wm_minsize(400, 300)
    app.mainloop()