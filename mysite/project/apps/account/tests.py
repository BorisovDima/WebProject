from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class TestProfile(StaticLiveServerTestCase):

    def test_upload_photo(self):
        pass