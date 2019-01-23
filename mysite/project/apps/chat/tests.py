from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from project.apps.account.models import BlogUser, Profile
from django.urls import reverse
import logging, time
logger = logging.getLogger()

user_data = (('test_chat_1', '19960213'), ('test_chat_2', '19960213'), ('test_chat_3', '19960213'))


class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True  # emulate StaticLiveServerTestCase


    def create_user(self):
        self.user1 = BlogUser.objects.create_user(username='test_chat_1', is_verified=True)
        self.user2 = BlogUser.objects.create_user(username='test_chat_2', is_verified=True)
        self.user3 = BlogUser.objects.create_user(username='test_chat_3', is_verified=True)
        self.user1.set_password('19960213'), self.user2.set_password('19960213'), self.user3.set_password('19960213')
        self.user1.save(), self.user2.save(), self.user3.save()


    def setUp(self):
        super().setUp()
        self.create_user()

        self.w1 = webdriver.Firefox()
        self.w2 = webdriver.Firefox()


    def tearDown(self):
        self.w1.quit()
        self.w2.quit()
        try:
            self.w3.quit()
        except Exception:
            pass
        super().tearDown()


    def user_auth(self, n, w):
        w.get('%s' % (self.live_server_url))
        login = w.find_element_by_id('login_username')
        login.send_keys(user_data[n][0])
        password = w.find_element_by_id('id_password')
        password.send_keys(user_data[n][1])
        w.find_element_by_id('button_login').click()

    def test_when_message_send_user_in_the_different_dialog(self):

        self.w3 = webdriver.Firefox()

        for n, w in enumerate((self.w1, self.w2, self.w3)):
            self.user_auth(n, w)

        self._init_dialog(self.w1, self.user2, 'Guten Tag!')
        # первый юзер отправялет  диалог через send message в профиле второго

        self._init_dialog(self.w2, self.user3, 'Czesc')
        # второй юзер начинает диалог с третьим юзером

        self._enter_dialog(self.w3, self.user2, check=True, f='Czesc')
        # третий юзер заходит в новый диалог и смотрит пришло ли сообщение

        self.assertFalse(self._check_message(self.w1, 'Czesc'), 'Message came in another dialogue')
        # первый проверяет, что ему ничего не пришло

        ##########################################################

        self._send_message(self.w2, 'Zdravo')
        # второй отправялет сообщение

        self.assertTrue(self._check_message(self.w3, 'Zdravo'),'Message did not come')
        # третий проверяет

        self.assertFalse(self._check_message(self.w1, 'Zdravo'), 'Message came in another dialogue')
        # первый проверяет, что ему ничего не пришло

        ##########################################################

        self._send_message(self.w3, 'Szia')
        # третий отправялет сообщение

        self.assertTrue(self._check_message(self.w2, 'Szia'), 'Message did not come')
        # второй проверяет

        self.assertFalse(self._check_message(self.w1, 'Szia'), 'Message came in another dialogue')
        # первый проверяет, что ему ничего не пришло

        ##########################################################

        self._send_message(self.w1, 'Hola')
        # первый отправялет сообщение

        self.assertFalse(self._check_message(self.w2, 'Hola'), 'Message came in another dialogue')
        # второй проверяет, что ему ничего не пришло

        self.assertFalse(self._check_message(self.w3, 'Hola'), 'Message came in another dialogue')
    # третий проверяет, что ему ничего не пришло


    def test_when_message_send_user_in_the_same_dialog(self):

        for n, w in enumerate((self.w1, self.w2)):
            self.user_auth(n, w)

        self._init_dialog(self.w1, self.user2, 'Guten Tag!')
        # первый юзер отправялет  диалог через send message в профиле второго

        self._enter_dialog(self.w2, self.user1, check=True, f='Guten Tag!')
        # второй юзер заходит в новый диалог и смотрит пришло ли сообщение


    ################################################

        self._send_message(self.w1, 'Ahoj')
        #первый отправялет сообщение в real time

        self.assertTrue(self._check_message(self.w2, 'Ahoj'), 'Message did not come')
        #второй проверяет

    ################################################

        self._send_message(self.w2, 'Hello')
        # второй отправялет сообщение

        self.assertTrue(self._check_message(self.w1, 'Hello'), 'Message did not come')
        #первый проверяет
        print('------------------------')
    ################################################

        self._send_message(self.w1, 'Konnichiwa')
        #первый отправялет

        self.assertTrue(self._check_message(self.w2, 'Konnichiwa'), 'Message did not come')
        #второй проверяет

    ################################################

        self._send_message(self.w2, 'Hey')
        # второй отправялет сообщение

        self.assertTrue(self._check_message(self.w1, 'Hey'), 'Message did not come')
        # первый проверяет

    ###############################################



    # === Utility ===

    def _check_message(self, w, msg):
        try:
             WebDriverWait(w, 15).until(lambda element:
                   w.find_element_by_xpath('.//div[@id="message-list"]//h6[contains(text(), "%s")]' %  msg))
             return True
        except Exception:
            return False


    def _send_message(self, w, msg):
        dialog = w.find_element_by_id('id_text_dialog')
        dialog.send_keys(msg)
        w.find_element_by_id('send-message').click()  # отправил сообщение
        self.assertTrue(self._check_message(w, msg), 'Message did not come')


    def _init_dialog(self, w, user, msg):
        w.get(self.live_server_url + reverse('account:profile', kwargs={'login': user.username}))
        w.find_element_by_id('send_message_profile_user').click()
        dialog = w.find_element_by_id('id_text_dialog')
        dialog.send_keys(msg)
        w.find_element_by_id('send-message').click() # отправил сообщение
        self.assertTrue(self._check_message(w, msg), 'Message did not come')

    def _enter_dialog(self, w, user, check=False, f=None):
        w.get(self.live_server_url + reverse('account:profile', kwargs={'login': user.username}))
        w.find_element_by_id('send_message_profile_user').click()
        if check:
            w.find_element_by_xpath('.//div[@id="message-list"]//h6[contains(text(), "%s")]' % f)
