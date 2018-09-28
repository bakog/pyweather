# coding=utf-8

import requests
import json
import pprint

APIKEY = '98b287dc820ee3913a9c9082ed2f79db'

def call():

    # http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID={APIKEY}

    # id = 7284829  (Budapest XIV- ker)
    # jelenlegi időjárás
    # api_url = 'http://api.openweathermap.org/data/2.5/weather?id=7284829&units=metric&lang=hu&APPID={}'.format(APIKEY)

    # előrejelzés
    api_url = 'http://api.openweathermap.org/data/2.5/forecast?id=7284829&units=metric&lang=hu&APPID={}'.format(APIKEY)

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return "HIBA"


if __name__ == "__main__":

    data = call()
    # pprint.pprint(data)
    print("Település: ", data['city']['name'])  # hely neve
    # a legkorábbi előrejelzés kiiratása

    print('Dátum: ', data['list'][0]['dt_txt'])  # az 1. előrejelzés
    print('Maximum hőmérséklet: ', data['list'][0]['main']['temp_max'], ' °C')  # max hőmérséklet
    print('Minimum hőmérséklet: ', data['list'][0]['main']['temp_min'], ' °C')  # min hőmérséklet
    print('Légnyomás: ',  data['list'][0]['main']['pressure'])  # légnyomás
    print('Páratartalom:', data['list'][0]['main']['humidity'])  # légnedvesség
    print('Szélsebesség: ', data['list'][0]['wind']['speed'])  # szélsebesség
    print('Leírás: ', data['list'][0]['weather'][0]['description'])  #leírás

    # az utolsó előrejezlés kiírása
    # print(len(data['list']))
    # print(data['list'][len(data['list'])-1]['dt_txt'])  # az 1. előrejelzés
    # print(data['list'][0]['main']['temp_max'])  # max hőmérséklet
    # print(data['list'][0]['main']['temp_min'])  # min hőmérséklet
    # print(data['list'][0]['main']['pressure'])  # légnyomás
    # print(data['list'][0]['main']['humidity'])  # légnedvesség
    # print(data['list'][0]['wind']['speed'])  # szélsebesség
    # print(data['list'][0]['weather'][0]['description'])  # leírás
