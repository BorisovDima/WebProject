from django.apps import AppConfig


class EventHandlerConfig(AppConfig):
    name = 'project.apps.event_handler'

    def ready(self):
        import project.apps.event_handler.signals