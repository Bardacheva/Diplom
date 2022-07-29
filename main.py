from random import randrange
import requests
from tokens import user_token

from urllib.parse import urlparse, urlencode

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

APP_ID = 8187574
USER_ID = 107469728
VERIFY = True
TIMEOUT = 2
protocol_version = '5.81'

''' Авторизация пользователя'''

class VK:
    scope = 'photos, wall, pages, messages, offline'
    protocol_version = '5.81'

    _URL_AUTHORIZE = 'https://oauth.vk.com/authorize'#для авторизации
    _URL_METHOD = 'https://api.vk.com/method'#куда посылаем запрос
    _URL_REDIRECT = 'https://oauth.vk.com/blank.html'#для авторизации
    PARAMS_COMMON = {
        'access_token': user_token,
        'v': protocol_version,
        'code': ''
    }

    def __init__(self, token: str, user_id: int):
        self.user_token = token
        self.user_id = user_id
        self.PARAMS_COMMON.update({'access_token':token})

    def _get_url(self, params):
        return '/'.join(self._URL_METHOD, params)

    def _get_user_token(self, auth_params):
        print('Нажмите на ссылку ниже и следуйте инструкции на сайте VK')
        url = '?'.join((self._URL_AUTHORIZE, urlencode(auth_params)))
        print(f'====> {url} <====')
        print('')
        return input('Вставьте сюда ссылку из браузера ====>')

    def get_new_user_token(self, app_id, scope=scope):
        _auth_params = {
            'client_id': app_id,
            'redirect_url': self._URL_REDIRECT,
            'display': 'page',
            'response_type': 'token'
        }
        raw_url = self._get_user_token(_auth_params)
        try:
            parse_temp = urlparse(raw_url)
            print(parse_temp)

        except ValueError:
            print('Неверная ссылка')

vk = VK('', USER_ID)
vk.get_new_user_token(APP_ID)


'''Взаимодействие пользователя с программой '''

vk = vk_api.VkApi(token=user_token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Привет, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "До встречи!")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")

def get_user_info(self, user_id):
    info = self.vk.users.get(user_ids=(user_id),
                             fields=('first_name', 'last_name',
                                    'age', 'city', 'martial_status', 'sex'))
    return info[0]



''' Поиск по условиям'''
def search_users(sex, age, martial_status, city):
    all_persons = []
    link_profile = 'https://vk.com/id'
    vk_ = vk_api.VkApi(token=user_token)
    response = vk_.method('users.search',
                          {'sort': 1,
                           'sex': sex,
                           'age': age,
                           'city': city,
                           'martial_status': martial_status,
                           })
    for element in response['items']:
        person = [
            element['first_name'],
            element['last_name'],
            link_profile + str(element['id']),
            element['id']
        ]
        all_persons.append(person)
    return all_persons

''' Поиск фотографий'''
def get_photo(user_owner_id):
    vk = vk_api.VkApi(token=user_token)
    try:
        response = vk.method('photos.get',
                              {
                                  'access_token': user_token,
                                  'v': protocol_version,
                                  'owner_id': user_owner_id,
                                  'album_id': 'profile',
                                  'count': 3,
                                  'extended': 1,
                                  'photo_sizes': 1,
                              })
    except ApiError:
        return 'Фото отсутствуют'
    users_photos = []
    for i in range(3):
        try:
            users_photos.append(
                [response['items'][i]['likes']['count'],
                 'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id'])])
        except IndexError:
            users_photos.append(['нет фото.'])
    return users_photos


'''Загрузка изображений в сообщения'''
def photo_messages(self, users_photos, peer_id=None):
    url = self.vk.photos.getMessagesUploadServer(peer_id=peer_id)['upload_url']
    with get_photo(users_photos) as photo_files:
        response = self.http.post(url, files=photo_files)
    return self.vk.photos.saveMessagesPhoto(**response.json())