from django.core.management.base import BaseCommand
from django.utils import timezone
from ... import models
import random
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

# cities = None
# all_cities = []
# with open('cities.json', encoding='utf-8') as file:
#     cities = json.load(file)
# count = 1
# for city in cities:
#     citi = {
#         'id': count,
#         'name': city['name']
#     }
#     all_cities.append(citi)
#     if count == 1001:
#         break
#     count += 1
#
# data = models.Citi.objects.get()
# data.data = all_cities
# data.save()
# print(data.data)
# # data.save


token = 'vk1.a.spx6PyqlNUTXe67P7GSGQCR7bCyzWdOIsixvpKOmUEsrSmZ4EkSGGkhotXlVVbPkOesdn8u9bdSft0HeyAcwh1hP594VhHpycSPeT0_9EwMLqy46x67iiRohQJxRCGUlGDNGL_lCpvwrjD183t9lT5Qortl4Mef2BeaWEjza7DgiUI8aFuBLUAwHESx5xBV1_34AOFGpFDpojEJFgPRvsw'
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)


cities_data = models.Citi.objects.get()
cities_data = cities_data.data
cities = []
for citi in cities_data:
    cities.append(citi['name'].lower())


def check_word(cities, used_citi, text):
    last_word = ''
    if text.lower()[-1] == 'ь' or text.lower()[-1] == 'ъ' or text.lower()[-1] == 'й' or text.lower()[-1] == 'ы':
        last_word = text.lower()[-2]
    else:
        last_word = text.lower()[-1]
    answer_cities = []
    for citi in cities:
        if citi.lower()[0] == last_word and citi not in used_citi:
            answer_cities.append(citi)
    if answer_cities == []:
        return True
    else:
        return False


def get_stage(text):
    return models.Stages.objects.filter(current_stage=f'{text}').get()


def send_message(user_id, message):
    kb = VkKeyboard(one_time=False)
    kb.add_button('Старт', color=VkKeyboardColor.POSITIVE)
    kb.add_button('Стоп', color=VkKeyboardColor.NEGATIVE)

    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id(), 'keyboard': kb.get_keyboard()})


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                data_user = vk_session.method("users.get", {"user_ids": event.user_id})
                username = data_user[0]['first_name']
                user, created = models.User.objects.get_or_create(vk_uid=event.user_id, name=username)
                used_citi = user.used_citi.split(',')

                if event.text.lower() == 'старт':
                    user.stage = 'game'
                    user.save()
                    random_citi = random.choice(cities)
                    last_word = ''
                    if random_citi.lower()[-1] == 'ь' or random_citi.lower()[-1] == 'ъ' or random_citi.lower()[-1] == 'й' or random_citi.lower()[-1] == 'ы':
                        last_word = random_citi.lower()[-2]
                    else:
                        last_word = random_citi.lower()[-1]
                    send_message(user.vk_uid,
                                 'Правила игры: нужно написать название РУССКОГО города, первая буква которого начинается на последнюю букву предыдущего города')
                    send_message(user.vk_uid,
                                 f'Я начну {random_citi.capitalize()}\nВведите название города, начинающегося с буквы "{last_word.upper()}"')
                    user.used_citi = f"{random_citi}"
                    user.save()
                    used_citi = user.used_citi.split(',')


                elif event.text.lower() == 'стоп':
                    user.stage = 'menu'
                    user.save()
                    send_message(user.vk_uid, 'Игра завершена')

                else:
                    if user.stage == 'game':
                        if event.text.lower() in cities:
                            if event.text.lower() in used_citi:
                                send_message(event.user_id, 'Такой город уже был!\nВведите другой')
                            else:
                                last_word = ''
                                if used_citi[-1].lower()[-1] == 'ь' or used_citi[-1].lower()[-1] == 'ъ' or \
                                        used_citi[-1].lower()[-1] == 'й' or used_citi[-1].lower()[-1] == 'ы':
                                    last_word = used_citi[-1].lower()[-2]
                                else:
                                    last_word = used_citi[-1].lower()[-1]

                                if event.text.lower()[0] != last_word:
                                    send_message(event.user_id, f'Город должен начинаться с буквы "{last_word}"')
                                else:
                                    user.used_citi += f',{event.text.lower()}'
                                    user.save()
                                    used_citi = user.used_citi.split(',')
                                    if check_word(cities, used_citi, event.text):
                                        send_message(event.user_id, 'Боту нечем ответить\nВы победили!')
                                        user.stage = 'menu'
                                        user.save()
                                    elif len(cities) == len(used_citi):
                                        send_message(event.user_id, 'Слова закончились!\nВы победили!')
                                        user.stage = 'menu'
                                        user.save()
                                    else:
                                        last_word = ''
                                        if used_citi[-1].lower()[-1] == 'ь' or used_citi[-1].lower()[-1] == 'ъ' or \
                                                used_citi[-1].lower()[-1] == 'й' or used_citi[-1].lower()[-1] == 'ы':
                                            last_word = used_citi[-1].lower()[-2]
                                        else:
                                            last_word = used_citi[-1].lower()[-1]
                                        answer_cities = []
                                        for citi in cities:
                                            if citi[0] == last_word and citi not in used_citi:
                                                answer_cities.append(citi)

                                        random_citi = random.choice(answer_cities)
                                        last_last_word = ''
                                        if random_citi.lower()[-1] == 'ь' or random_citi.lower()[-1] == 'ъ' or \
                                                random_citi.lower()[-1] == 'й' or random_citi.lower()[-1] == 'ы':
                                            last_last_word = random_citi.lower()[-2]
                                        else:
                                            last_last_word = random_citi.lower()[-1]

                                        user.used_citi += f",{random_citi.lower()}"
                                        user.save()
                                        used_citi = user.used_citi.split(',')

                                        if check_word(cities, used_citi, used_citi[-1]):
                                            send_message(event.user_id, f'К сожалению слова на букву "{last_last_word.upper()}" больше нет\nВы Проиграли!!')
                                            user.stage = 'menu'
                                            user.save()
                                        elif len(cities) == len(used_citi):
                                            send_message(event.user_id, 'Слова закончились!\nВы Проиграли!!')
                                            user.stage = 'menu'
                                            user.save()
                                        else:
                                            send_message(event.user_id,
                                                         f'{random_citi.capitalize()}\nВам на букву "{last_last_word.upper()}"')

                        else:
                            send_message(event.user_id, 'Такого города не существует')
                    else:
                        send_message(user.vk_uid, 'Напишите "Старт" для начала игры')

