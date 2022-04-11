from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    username = models.CharField(max_length=100, default=None, blank=True, null=True)
    pending_state = models.CharField(max_length=100, default=None, blank=True, null=True)
    chat_id = models.CharField(max_length=20)


class UserWallet(models.Model):
    user = models.ForeignKey('temple_island_bot.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default=None, blank=True, null=True)
    address = models.CharField(max_length=100, default=None, blank=True, null=True)
    image_url = models.CharField(max_length=100, default=None, blank=True, null=True)

    def get_user_name(self):
        return self.user.first_name