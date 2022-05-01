import requests, csv, os
from bs4 import BeautifulSoup
from PIL import Image


def fetch():
    response = requests.get('http://www.soundofindia.com/raagas.asp').text
    soup = BeautifulSoup(response, 'lxml')

    ragas = []
    ragas_links = []
    thaats = []

    main_table = [tag for tag in soup.body.table.tbody.contents[5].contents[3].table.contents[7].table.contents[3::] if tag != '\n']
    for row in main_table:
        data = row.contents
        ragas.append(data[1].text[3:-1])
        ragas_links.append(data[1].a['href'])
        if data[3].text[3:-2] != '':
            thaats.append(data[3].text[3:-2])
        else:
            thaats.append('None')
        
    with open('icm.csv', 'w', newline='') as icm:
        writer = csv.writer(icm)
        writer.writerow(['ragas', 'ragasLinks', 'Thaats'])
        for row in range(len(ragas)):
            writer.writerow((ragas[row], ragas_links[row], thaats[row]))

def get_thaats():
    with open('icm.csv') as data:
        reader = csv.reader(data)       
        thaats = {thaat[2] for thaat in list(reader)[1::]}
    return list(thaats)


def search_raga(name):
    with open('icm.csv') as data:
        reader = csv.reader(data)
        results = [row for row in reader if name in row[0]]
    return results

def search_thaat(name):
    with open('icm.csv') as data:
        results = []
        reader = csv.reader(data)
        results = [row for row in reader if name == row[2]]
    return results

def raga_data(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    file = soup.source['src']
    raga_url = 'http://www.soundofindia.com/' + file
    raga_site = requests.get(raga_url)

    if not os.path.exists('soundfiles'):
        os.makedirs('soundfiles', 0o777)
    with open(file, 'wb') as raga:
        raga.write(raga_site.content)

    labelled_data = soup.body.table.tbody.contents[5].contents[3].table.contents[7].table.find_all("td")

    result = {'mp3': file, 'Thaat': labelled_data[1].text, 'Prahar': labelled_data[5].text, 'Jaati': labelled_data[21].text, 
    'Bhaav': labelled_data[11].text}

    new_values = map(lambda value: value if value != '' else 'None', result.values())
    result = {k: v for k, v in zip(result.keys(), new_values)}

    return result

def image_download():
    image_url = 'https://t3.ftcdn.net/jpg/02/47/71/54/360_F_247715478_GUT14S7J2ieTPLGZBREoSSKbPNf7aklh.jpg'
    response = requests.get(image_url)
    if not os.path.exists('images'):
        os.makedirs('images', 0o777)
    with open('images/banner.jpg', 'wb') as file:
        file.write(response.content)
    img = Image.open('images/banner.jpg')
    img.save('images/banner.gif')
    
