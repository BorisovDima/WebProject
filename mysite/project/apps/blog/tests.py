from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from .models import Article
from .forms import UpdatePostForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from project.apps.myauth.tests import UserAuth
from project.apps.account.models import Profile
from selenium.webdriver.support.wait import WebDriverWait
import time



test_pass = '19960213Z26a'
test_user = 'author'

class TestBlogNotLive(TestCase):
    fixtures = ['location-data.json']

    def setUp(self):
        super().setUp()
        self.author = get_user_model().objects.create_user(is_verified=True, username=test_user)
        self.author.set_password(test_pass)
        self.author.save()

    def test_not_post_after_24_hours(self):
        post = Article.objects.create(text="TEST TEXT", author=self.author)
        form = UpdatePostForm({'text': 'TEST TEXT FORM'}, instance=post)
        form.is_valid()
        self.assertIsNone(form.errors.get('create_data'), 'Post was created now, but cant update')

        post = Article.objects.create(text="TEST TEXT", author=self.author,
                                      create_data=timezone.now() - timezone.timedelta(hours=23))
        form = UpdatePostForm({'text': 'TEST TEXT FORM'}, instance=post)
        form.is_valid()
        self.assertIsNone(form.errors.get('create_data'), 'Post was created 23 hours ago, but cant update')

        post = Article.objects.create(text="TEST TEXT", author=self.author,
                                      create_data=timezone.now() - timezone.timedelta(hours=25))
        form = UpdatePostForm({'text': 'TEST TEXT FORM'}, instance=post)
        form.is_valid()
        self.assertEqual(form.errors.get('__all__')[0], 'Time expired',  'Post was created 24 hours ago, but can update')


from uuid import uuid4


class TestBlogPost(UserAuth, StaticLiveServerTestCase):
    fixtures = ['user_data.json', 'profile_data.json', 'location-data.json']


    def setUp(self):
        self.author = get_user_model().objects.create_user(username=test_user, is_verified=True)
        self.author.set_password(test_pass)
        self.author.save()
        self.driver = WebDriver()
        self.user_auth(self.driver, (test_user, test_pass))

    def tearDown(self):
        self.driver.close()

    def test_post_not_in_user_page(self):
        self.driver.find_element_by_id('link_to_main-page').click()
        self.driver.find_element_by_xpath(
            './/div[@id="navbarToggler"]//button[@data-target="#Create-post"]').click()
        text = self.driver.find_element_by_id('navbar-create_post_form')
        key = str(uuid4())
        text.send_keys(key)
        self.driver.find_element_by_id('send-form-post').click()

        self.assertFalse(self.get_post(key), 'Post posted on public page')

        post = Article.objects.filter(text=key)
        self.assertTrue(post.count() == True)



    def test_post_in_user_page(self):
        self.driver.find_element_by_xpath(
            './/div[@id="navbarToggler"]//button[@data-target="#Create-post"]').click()
        text = self.driver.find_element_by_id('navbar-create_post_form')
        key = str(uuid4())
        text.send_keys(key)
        self.driver.find_element_by_id('send-form-post').click()

        self.assertTrue(self.get_post(key), 'Post wasnt posted on user page')

        post = Article.objects.filter(text=key)
        self.assertTrue(post.count() == True)

    def test_update_post(self):
        self.driver.find_element_by_xpath(
            './/div[@id="navbarToggler"]//button[@data-target="#Create-post"]').click()
        text = self.driver.find_element_by_id('navbar-create_post_form')
        text.send_keys('TEXT BEFORE UPDATE')
        self.driver.find_element_by_id('send-form-post').click()
        time.sleep(2)

        self.assertTrue(Article.objects.filter(text='TEXT BEFORE UPDATE').count() == True, )

        self.driver.find_element_by_xpath('//div[@id="add-loader"]//a[@data-toggle="dropdown"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//a[@data-action="update_object"]').click()
        time.sleep(1)
        self.driver.find_element_by_id('update-post-text').clear()
        self.driver.find_element_by_id('update-post-text').send_keys('TEXT AFTER UPDATE')
        self.driver.find_element_by_xpath('//a[@data-action="save_update"]').click()

        self.assertTrue(self.get_post('TEXT AFTER UPDATE'), 'Post wasnt updated')
        self.assertTrue(Article.objects.filter(text='TEXT AFTER UPDATE').count() == True)


    def test_post_views(self):
        Article.objects.create(text='TEST VIEWS', author=self.author)
        users = get_user_model().objects.filter(username__startswith='test_')[:100]
        count_view = 0
        self.driver.delete_all_cookies()
        for user in users:
            try:
                self.user_auth(self.driver, (user.username, '19960213Z26a'))
            except Exception as a:
                print(a)
                continue
            self.driver.find_element_by_id('link_to_main-page').click()
            WebDriverWait(self.driver, 30).until(lambda element: self.driver.find_element_by_xpath('//div[@data-action="detail-post"]'))
            self.driver.find_element_by_xpath('//div[@data-action="detail-post"]').click()
            time.sleep(1)
            count_view += 1
            self.driver.delete_all_cookies()
        self.user_auth(self.driver, (test_user, test_pass))
        count = self.driver.find_element_by_xpath('//div[@id="add-loader"]//span[@data-type="counter-views-footer-post"]').text
        self.assertTrue(int(count) == count_view)


    def get_post(self, text):
        try:
             WebDriverWait(self.driver, 20).\
                    until(lambda element: self.driver.find_element_by_xpath(
                    '//div[@id="add-loader"]//h6[contains(text(), "%s")]' % text))
             return True
        except Exception as e:
             return False




