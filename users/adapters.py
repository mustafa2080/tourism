from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.translation import gettext_lazy as _

class CustomAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        """Generate a username from email"""
        email = user.email
        if email:
            username = email.split('@')[0]
            user.username = username

    def save_user(self, request, user, form):
        """Save user and ensure username is set"""
        user = super().save_user(request, user, form)
        if not user.username:
            user.username = user.email.split('@')[0]
            user.save()
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_username(self, request, sociallogin):
        """Generate a username from email for social accounts"""
        email = sociallogin.account.extra_data.get('email')
        if email:
            username = email.split('@')[0]
            sociallogin.user.username = username

    def save_user(self, request, sociallogin, form=None):
        """Save social user and ensure username is set"""
        user = super().save_user(request, sociallogin, form)
        if not user.username:
            user.username = user.email.split('@')[0]
            user.save()
        return user
