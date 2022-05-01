import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED
import pygame, os
import data
from pygame import mixer

gui.SetOptions(background_color='#404040',
    font=("Verdana", 15),
    input_elements_background_color='#e8e7ca',
    button_color=('white','#046b20'),
    text_element_background_color='#404040')

data.fetch()

def create_window():
    layout = [
        [gui.Text(text="Welcome to my RagaPedia", justification='center', expand_x=True, font=("Segoe UI Black", 25))],
        [gui.Button('Quit', size=29), gui.Button('Reset', size=29)], 
        [gui.Text(text="Choose the way you wish to search for Raga \t:"), gui.Combo(["Thaat", "Raga"], expand_x=True, key='category')],
        [gui.Text(text="Enter Search Term if searching by Raga \t\t:"), gui.Input(key='raga')],
        [gui.Text(text="Select Thaat if searching by Thaat \t\t:"), gui.Combo(data.get_thaats(), expand_x=True, key='thaat')],
        [gui.Button('Search', size=100)]
        ]

    return gui.Window("RagaPedia", layout, size=(800, 800))

window = create_window()


def play(result):
    mixer.init()
    mixer.music.load(result['mp3'])
    mixer.music.play()

while True:
    event, values = window.read()

    if event == 'Quit' or event == WINDOW_CLOSED:
        try:
            mixer.music.stop()
            mixer.quit()
        except pygame.error:
            pass
        for file in os.listdir('soundfiles'):
            os.remove(os.path.join('soundfiles', file))
        os.remove('icm.csv')
        for file in os.listdir('images'):
            os.remove(os.path.join('images', file))
        break

    if event == 'Search':
        if values['category'] == 'Raga':
            search_results = data.search_raga(values['raga'])
        elif values['category'] == 'Thaat':
            search_results = data.search_thaat(values['thaat'])
        names = [raga[0] for raga in search_results]
        
        added_rows = [
            [gui.Text(text="Select your search result \t:"), gui.Combo(names, expand_x=True, key='search_result')],
            [gui.Button('Submit', size=100)]
        ]
        
        window.extend_layout(window, added_rows)

    if event == 'Submit':
        url = 'http://www.soundofindia.com/' + list(filter(lambda row: values['search_result'] == row[0], search_results))[0][1]

        data.image_download()
        
        result = data.raga_data(url)
        added_rows = [
            [gui.Image('images/banner.gif', key='Banner', size=(1000, 250))],
            [gui.Button('Play', size=14 ), gui.Button('Pause', size=14), gui.Button('Resume', size=14), gui.Button('Stop', size=14)],
            [gui.Table(values=[['Thaat', result['Thaat']], ['Prahar', result['Prahar']], ['Jaati', result['Jaati']], ['Bhaav', result['Bhaav']]], 
            headings=['Label', 'Value'], expand_x=True, hide_vertical_scroll=True, justification='center', num_rows=4,
            background_color='#475841')] 
        ]   

        window.extend_layout(window, added_rows) 

    if event == 'Play':
        play(result)

    if event == 'Pause':

        try:
            mixer.music.pause()
        except pygame.error:
            pass
    
    if event == 'Resume':

        try:
            mixer.music.unpause()
        except pygame.error:
            pass
    
    if event == 'Stop':

        try:
            mixer.music.stop()
            mixer.quit()
        except pygame.error:
            pass

    if event == 'Reset':
        window.close(); del window

        try:
            mixer.music.stop()
            mixer.quit()
        except pygame.error:
            pass
        
        window = create_window()