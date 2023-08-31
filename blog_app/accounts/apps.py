from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_app.accounts'

    def ready(self):
        import blog_app.accounts.signals