# coding=utf-8

import requests
import json
import pprint

APIKEY = '98b287dc820ee3913a9c9082ed2f79db'

def get_weather_info():

    # http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID={APIKEY}

    # id = 7284829  (Budapest XIV- ker)
    # jelenlegi időjárás
    # api_url = 'http://api.openweathermap.org/data/2.5/weather?id=7284829&units=metric&lang=hu&APPID={}'.format(APIKEY)

    # előrejelzés
    api_url = 'http://api.openweathermap.org/data/2.5/forecast?id=7284829&units=metric&lang=hu&APPID={}'.format(APIKEY)

    response = requests.get(api_url)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise requests.exceptions.ConnectionError('Az adatok lekérése sikertelen...')
        #raise ConnectionError('Az adatok lekérése sikertelen...')

def  display_weather_info(weather_info):
    # pprint.pprint(data)
    city= weather_info['city']['name']
    date =  weather_info['list'][0]['dt_txt']
    max_T = weather_info['list'][0]['main']['temp_max']
    min_T = weather_info['list'][0]['main']['temp_min']
    pressure =  weather_info['list'][0]['main']['pressure']
    humidity = weather_info['list'][0]['main']['humidity']
    wind =  weather_info['list'][0]['wind']['speed']
    description = weather_info['list'][0]['weather'][0]['description']
    print(f'Település: {city}') # hely neve
    # a legkorábbi előrejelzés

    print(f'Dátum: {date}')  # az 1. előrejelzés
    print(f'Maximum hőmérséklet: {max_T} °C')  # max hőmérséklet
    print(f'Minimum hőmérséklet: {min_T} °C')  # min hőmérséklet
    print(f'Légnyomás: {pressure} hPa')  # légnyomás
    print(f'Páratartalom: {humidity} %')  # légnedvesség
    print(f'Szélsebesség: {wind} km/h')  # szélsebesség
    print(f'Leírás: {description}')  #leírás

    # az utolsó előrejezlés kiírása
    # print(len(weather_info['list']))
    # print(weather_info['list'][len(weather_info['list'])-1]['dt_txt'])  # az 1. előrejelzés
    # print(weather_info['list'][0]['main']['temp_max'])  # max hőmérséklet
    # print(weather_info['list'][0]['main']['temp_min'])  # min hőmérséklet
    # print(weather_info['list'][0]['main']['pressure'])  # légnyomás
    # print(weather_info['list'][0]['main']['humidity'])  # légnedvesség
    # print(weather_info['list'][0]['wind']['speed'])  # szélsebesség
    # print(weather_info['list'][0]['weather'][0]['description'])  # leírás


if __name__ == "__main__":

    try:
        weather_info = get_weather_info()
        display_weather_info(weather_info)
    except requests.exceptions.ConnectionError:
        print('Az adatok lekérése sikertelen, próbálja meg később!')

