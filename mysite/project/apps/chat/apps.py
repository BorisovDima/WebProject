from django.apps import AppConfig


class ChatConfig(AppConfig):
    name = 'project.apps.chat'

    def ready(self):
        import project.apps.chat.signals




