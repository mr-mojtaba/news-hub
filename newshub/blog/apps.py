from django.apps import AppConfig


# This class configures the 'blog' application.
class BlogConfig(AppConfig):
    # Sets the default auto field type for models in this application.
    default_auto_field = 'django.db.models.BigAutoField'

    # The name of the application used in Django settings.
    name = 'blog'

    # A human-readable name for the application that appears in the Django admin panel.
    verbose_name = "وبلاگ"
