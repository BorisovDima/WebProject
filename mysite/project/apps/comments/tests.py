from django.contrib.auth import get_user_model
from channels.testing import ChannelsLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from project.apps.blog.models import Article
from project.apps.myauth.tests import UserAuth
from project.apps.account.models import Profile
from selenium.webdriver.support.wait import WebDriverWait
from django.urls import reverse


test_pass = '19960213Z26a'
test_user = 'comment-test1'

test_user2 = 'comment-test2'

class TestComment(UserAuth, ChannelsLiveServerTestCase):


    def setUp(self):
        self.user1 = get_user_model().objects.create_user(is_verified=True, username=test_user)
        self.user2 = get_user_model().objects.create_user(is_verified=True, username=test_user2)
        self.user1.set_password(test_pass), self.user2.set_password(test_pass),
        self.user1.save(), self.user2.save()

        Profile.objects.create(name=self.user1.username, bloguser=self.user1)
        Profile.objects.create(name=self.user2.username, bloguser=self.user2)

        Article.objects.create(text='TEST COMMENT POST', author=self.user1)
        Article.objects.create(text='TEST COMMENT POST #2', author=self.user1)
        self.w1 = WebDriver()
        self.w2 = WebDriver()
        self.user_auth(self.w1, (test_user, test_pass))
        self.user_auth(self.w2, (test_user2, test_pass))

    def tearDown(self):
        self.w1.close()
        self.w2.close()

    def test_comment_send(self):
        self.w2.get(self.live_server_url + reverse('account:profile', kwargs={'login': self.user1.username}))

        WebDriverWait(self.w2, 10).until(lambda el: self.w2.find_element_by_xpath('//div[@id="add-loader"]//div[@data-id="2"]'))
        self.w2.find_element_by_xpath('//div[@id="add-loader"]//div[@data-id="2"]').click()

        WebDriverWait(self.w1, 10).until(lambda el: self.w1.find_element_by_xpath('//div[@id="add-loader"]//div[@data-id="2"]'))
        self.w1.find_element_by_xpath('//div[@id="add-loader"]//div[@data-id="2"]').click()


        self.send_comment(self.w1, 'TEST COMMENT #1')

        self.assertTrue(self.check_comment(self.w2, 'TEST COMMENT #1'))

        self.send_comment(self.w2, 'TEST COMMENT #2')

        self.assertTrue(self.check_comment(self.w1, 'TEST COMMENT #2'))

    def test_different_comment_send(self):


        self.w2.get(self.live_server_url + reverse('account:profile', kwargs={'login': self.user1.username}))

        WebDriverWait(self.w2, 10).until(lambda el: self.w2.find_element_by_xpath('//div[@id="add-loader"]//div[@data-id="2"]'))
        self.w2.find_element_by_xpath('//div[@id="add-loader"]//div[@data-id="2"]').click()

        WebDriverWait(self.w1, 10).until(lambda el: self.w1.find_element_by_xpath('//div[@id="add-loader"]//div[@data-id="1"]'))
        self.w1.find_element_by_xpath('//div[@id="add-loader"]//div[@data-id="1"]').click()


        self.send_comment(self.w1, 'TEST COMMENT #1')

        self.assertFalse(self.check_comment(self.w2, 'TEST COMMENT #1'))

        self.send_comment(self.w2, 'TEST COMMENT #2')

        self.assertFalse(self.check_comment(self.w1, 'TEST COMMENT #2'))


    def send_comment(self, w, msg):
        w.find_element_by_xpath('//textarea[@data-type="data-form"]').send_keys(msg)
        w.find_element_by_xpath('//input[@data-action="comment-send"]').click()
        self.check_comment(w, msg)

    def check_comment(self, w, msg):
        try:
            WebDriverWait(w, 30).\
                until(lambda el: w.find_element_by_xpath('.//div[@id="container-comments"]//h6[contains(text(), "%s")]' % msg))
            return True
        except Exception:
            return False

