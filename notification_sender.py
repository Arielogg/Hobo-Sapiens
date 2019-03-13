import logging
from os import environ
from telegram import InputMediaPhoto
from telegram.ext import Updater

from crawler_utils.utils import chunks, nofail


class Notification(object):

    def __init__(self, price=None, location=None, area=None, url=None, pics_urls=None, id=None, source=None, ) -> None:
        super().__init__()
        self.id = id
        self.source = source
        self.price = price
        self.location = location
        self.area = area
        self.url = url
        self.pics_urls = pics_urls

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Notification) and o.id == self.id


class NotificationSender:

    def __init__(self) -> None:
        super().__init__()
        self.updater = Updater(token=environ.get('AF_TELEGRAM_BOT_TOKEN'),
                               request_kwargs={"connect_timeout": 60., "read_timeout": 60.})

    def send_to_chat(self, notif: Notification):
        desc = f'ID: {notif.id}\nPrice: {notif.price}\nArea: {notif.area}\nWhere: {notif.location}\nURL: {notif.url} '
        try:
            # chat_id = '-1001121437337'
            # chat_id = '73115329'
            chat_id = environ.get('AF_TELEGRAM_CHAT_ID')
            if notif.pics_urls:
                for c in chunks(notif.pics_urls, 10):
                    self._send_pics(c, chat_id, desc)
            self._send_message(chat_id, desc)
        except Exception as e:
            logging.error(e)

    @nofail(retries=20)
    def _send_message(self, chat_id, desc):
        self.updater.bot.send_message(chat_id, desc, timeout=20 * 60, disable_web_page_preview=True)

    @nofail(retries=20)
    def _send_pics(self, c, chat_id, desc):
        self.updater.bot.send_media_group(chat_id, [InputMediaPhoto(i, caption=desc) for i in c],
                                          timeout=20 * 60, disable_notification=True)


if __name__ == '__main__':
    NotificationSender().send_to_chat(
        Notification("SL", 1200, "75003", 30, "http://ya.ru",
                     ["https://www.python-course.eu/images/venitian_masks.png",
                      "https://cache.lovethispic.com/uploaded_images/thumbs/220227-Keep-Calm-And-Pass-Your-Exams.jpg",
                      "https://poster.keepcalmandposters.com/default/5997547_no_dp_because_exam_chaling.png"]))
