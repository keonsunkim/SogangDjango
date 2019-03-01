from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .managers import FollowManager

User = settings.AUTH_USER_MODEL


class FollowModel(models.Model):
    follower = models.ForeignKey(
        User, related_name="follower", db_index=True, 
        on_delete=models.CASCADE
        )
    following = models.ForeignKey(
        User, related_name="following", db_index=True, 
        on_delete=models.CASCADE
        )
    following_since = models.DateTimeField(
        auto_now_add=True)

    follow_shortcuts = FollowManager()

    objects = models.Manager()

    class Meta:
        unique_together = (("follower", "following"))

    def __str__(self):
        return f'{self.follower.email} ===> {self.following.email}'

    def save(self, *args, **kwargs):
        if self.follower == self.following:
            raise ValueError('You cannot follow yourself')
        else:
            super(FollowModel, self).save(*args, **kwargs)