from django.db import models
from django.db.models import Q


class FollowManager(models.Manager):
	def get_follower_list(self, user_id):
		follower_list = super(FollowManager, self).filter(
			following_id=user_id)
		return follower_list

	def get_following_list(self, user_id):
		following_list = super(FollowManager, self).filter(
			follower_id=user_id)
		return following_list

	def get_follow_relation(self, user_id_1, user_id_2):
		follow_relation = super(FollowManager, self).filter(
			follower_id=user_id_1,
			following_id=user_id_2
			)
		return follow_relation