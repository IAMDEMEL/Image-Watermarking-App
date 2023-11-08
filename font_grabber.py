import requests
import pandas as pd
from bs4 import BeautifulSoup

font_dic = {}


def grab_windows_default_truetypefonts():
    """Gets list of True Type Fonts from Microsoft website"""
    global font_dic
    names = []
    files = []
    website = 'https://learn.microsoft.com/en-us/typography/fonts/windows_10_font_list'

    response = requests.get(website)
    soup = BeautifulSoup(response.text, 'html.parser')
    unfiltered_list = soup.find('table').find_all('tr')
    unfiltered_list.pop(0)

    for data in unfiltered_list:
        unfiltered_font_list = data.find_all('td')
        names.append(unfiltered_font_list[1].text)
        files.append(unfiltered_font_list[2].text.lower())

    font_dic = {font_name: file_file for font_name, file_file in zip(names, files)}
    store_new_fonts()


def store_new_fonts():
    """Stores fonts into a CSV file for later use"""
    storable_dict = {
        'Name': font_dic.keys(),
        'File Name': font_dic.values()
    }

    dict_dataframe = pd.DataFrame(storable_dict)
    dict_dataframe.to_csv('Fonts/fonts.csv', mode='a', index=False)


def get_fonts():
    """Returns a Dictionary and True Type Fonts and File Names."""
    global font_dic
    readable_data = pd.read_csv('Fonts/fonts.csv')
    font_dic = {font_name: file_file for font_name, file_file in zip(readable_data['Name'].values,
                                                                     readable_data['File Name'].values)}
    # print(font_dic)
    return font_dic
