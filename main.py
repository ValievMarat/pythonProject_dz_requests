import requests
import os
import time

# Задание 1, superhero

def get_id_superhero(name_list):
    # я воспользовался другим api: https://akabab.github.io/superhero-api/api/
    # можно было бы получить всю информацию через метод /all.json, но решил через него
    # отдельно получать список id, а потом другим методом получать уже нужные параметры,
    # чтобы было подобно оригинальному api
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    resp = requests.get(url)
    list_all = resp.json()

    result_list = []
    for dict_hero in list_all:
        if dict_hero['name'] in name_list:
            result_list.append({'id': dict_hero['id'], 'name': dict_hero['name']})

    return result_list


def get_intelligence_by_id_list(id_list):
    url = 'https://akabab.github.io/superhero-api/api/id/'
    for superhero in id_list:
        resp = requests.get(f'{url}{superhero["id"]}.json')
        dict_hero = resp.json()
        superhero['intelligence'] = dict_hero['powerstats']['intelligence']

def task_1():
    list_name = ['Hulk', 'Captain America', 'Thanos']
    list_id_superhero = get_id_superhero(list_name)
    get_intelligence_by_id_list(list_id_superhero)

    max_intelligence = 0
    name_max_superhero = ''
    for superhero in list_id_superhero:
        if max_intelligence < superhero['intelligence']:
            max_intelligence = superhero['intelligence']
            name_max_superhero = superhero['name']

    print('Самый умный супергерой:', name_max_superhero)
    print('Ум:', max_intelligence)

#Задание 2, yandex disk

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        name_file = os.path.basename(file_path)
        headers = {'Authorization': f'OAuth {self.token}', 'Content-Type': 'Application/json'}
        params = {'path': name_file, 'overwrite': True}
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code == 200:
            href = resp.json()['href']
            with open(file_path, 'rb') as file:
                resp = requests.put(href, files={'file': file})
                print(f'Статус: {resp.status_code}')

        else:
            print(f'Ошибка 1 {resp.status_code}: {resp.json()["message"]}')


def task_2():
    Token = 'AQAAAAAL5KijAADLWwkHJVFYQU1sjc2zKhiutN0'

    file_path = 'C:\example_file\Пример файла.txt'

    Yandex_loader = YaUploader(Token)
    Yandex_loader.upload(file_path)

# Задание 3, stackoverflow

def get_list_questions_stackoverflow():
    url = 'https://api.stackexchange.com/2.3/questions'
    current_date = int(time.time())
    last_date = current_date - 2 * 86400

    params = {'fromdate': last_date, 'todate': current_date,
              'order': 'desc', 'sort': 'activity', 'tagged': 'Python', 'site': 'stackoverflow'}

    list_questions = []
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        dict = resp.json()
        for question in dict['items']:
            list_questions.append(question['title'])
    else:
        print(f'Ошибка, статус {resp.status_code}')

    return list_questions

def task_3():
    # https: // api.stackexchange.com / 2.3 / questions?fromdate = 1656374400 & todate = 1656460800 & order = desc & sort = activity & tagged = Python & site = stackoverflow
    list_questions = get_list_questions_stackoverflow()
    print(f'Всего вопросов: {len(list_questions)}')
    for title in list_questions:
        print(title)

if __name__ == '__main__':
    # task_1()

    # task_2()

    task_3()



