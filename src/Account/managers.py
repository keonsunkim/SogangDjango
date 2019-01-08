from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):

    def create_user(self, email, slug_name_for_url, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            slug_name_for_url=slug_name_for_url,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, slug_name_for_url, user_type, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            slug_name_for_url=slug_name_for_url,
        )
        user.user_type = user_type
        user.save(using=self._db)
        return user

    def create_superuser(self, email, slug_name_for_url, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            slug_name_for_url=slug_name_for_url,
        )
        user.user_type = 50
        user.admin = True
        user.active = True
        user.save(using=self._db)
        return user
