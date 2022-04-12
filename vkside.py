from urllib.request import urlretrieve

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from tgside import send_message, send_photo, send_doc
from yamlparser import VKTOKEN, CHATS_ID
from logger import logger


class VkBot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=VKTOKEN)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, 208821694)
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                chat_id = event.message['peer_id']
                user_id = event.message['from_id']
                user_info = self.vk_session.method("users.get", {"user_ids": user_id})[0]
                user_firstname = user_info['first_name']
                user_lastname = user_info['last_name']
                try:
                    tg_chat_id = CHATS_ID[chat_id]
                except KeyError:
                    logger.exception(f'Unexpected msg from {chat_id}')
                    continue
                if event.message['text']:
                    logger.info(f"Message from {user_firstname} {user_lastname} from {chat_id}")
                    send_message(f"*{user_firstname} {user_lastname}*:\n{event.message['text']}",
                                 tg_chat_id)
                if event.message['attachments']:
                    for j in event.message['attachments']:
                        doc_type = j['type']
                        if doc_type == 'photo':
                            logger.info(f"Photo from {user_firstname} {user_lastname} from {chat_id}")
                            self.send_photo(j['photo']['sizes'], chat_id)
                        elif doc_type == 'doc':
                            logger.info(f"Doc from {user_info['first_name']} {user_info['last_name']}")
                            self.send_doc(j, event.message['peer_id'])
                        elif doc_type == 'sticker':
                            logger.info(f"Sticker from {user_firstname} {user_lastname} from {chat_id}")
                            sticker_url = j['sticker']['images'][1]['url']
                            self.send_sticker(user_firstname, user_lastname, sticker_url, tg_chat_id)
                        elif doc_type == 'poll':
                            logger.info(f"Poll from {user_firstname} {user_lastname} from {chat_id}")
                            self.react_to_poll(chat_id)
                        else:
                            logger.info(
                                f"{doc_type} from {user_info['first_name']} {user_info['last_name']} from {chat_id}")
                            self.unknown_file(tg_chat_id)

    @staticmethod
    def send_photo(event_message: list, chat_id):
        send_photo(event_message[-1]['url'], CHATS_ID[chat_id])

    @staticmethod
    def send_doc(event_message, chat_id):
        url = event_message['doc']['url']
        doc_name = f"{event_message['doc']['title']}"
        urlretrieve(url, doc_name)
        send_doc(doc_name, CHATS_ID[chat_id])

    @staticmethod
    def send_sticker(fname, lname, sticker_url, chat_id):
        send_message(f"*{fname} {lname}*:", chat_id)
        send_photo(sticker_url, chat_id)

    @staticmethod
    def unknown_file(chat_id):
        send_message('_Был прислан какой-то файлик, но не могу его переслать. Придётся всё таки в вк зайти..._',
                     chat_id)

    @staticmethod
    def react_to_poll(chat_id):
        send_message('_В вк какой-то опрос организовали, стоит проголосовать_',chat_id)


VkBot()
