from django.test import TestCase
from project.apps.blog.models import Article
from project.apps.account.models import BlogUser


class TestLoader(TestCase):
    def setUp(self):
        user = BlogUser.objects.create_user(username='test', password='1996')
        user.save()
        for i in range(102):
            Article.objects.create(title=str(i), text='test', author=user)


    def test_uniq_articles(self):
        resp = self.client.get('/api/load/articles/')
        print(resp)