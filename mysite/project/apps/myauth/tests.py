from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from project.apps.account.models import BlogUser, Profile
from django.urls import reverse

test_user = "test_0"
test_pass = '19960213Z26a'
domain = 'localhost'




class UserAuth():
    def user_auth(self, w, data):
        w.get('%s' % (self.live_server_url))
        login = w.find_element_by_id('login_username')
        login.send_keys(data[0])
        password = w.find_element_by_id('id_password')
        password.send_keys(data[1])
        w.find_element_by_id('button_login').click()



class MyAuthTest(StaticLiveServerTestCase):
    #fixtures = ['user_auth.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = BlogUser.objects.create_user(username=test_user, is_verified=True)
        cls.user.set_password(test_pass)
        cls.user.save()
        cls.driver = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_login(self):
        url = self.live_server_url + reverse('account:profile', kwargs={'login': test_user})
        self.driver.get('%s' % (self.live_server_url))
        login = self.driver.find_element_by_id('login_username')
        login.send_keys(test_user)
        password = self.driver.find_element_by_id('id_password')
        password.send_keys(test_pass)
        self.driver.find_element_by_id('button_login').click()
        assert self.driver.current_url == url

    def test_registr(self):
        pass

