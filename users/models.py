from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Profile(models.Model):


    ACCOUNT_TYPE = (
        ('Farmer','Farmer'),
        ('Rancher','Rancher'),
        ( 'Trader','Trader'),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    # short_intro = models.CharField(max_length=200, blank=True, null=True)
    account = models.CharField(max_length=200, choices=ACCOUNT_TYPE, default="Farmer")
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url


class Training(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    trainer = models.CharField(max_length=200, blank=True, null=True)
    certificate = models.ImageField(
        null=True, blank=True, upload_to='certificates/')
    completed = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.trainer)
    
    class Meta:
        ordering = ['completed']

    @property
    def imageURL(self):
        try:
            url = self.certificate.url
        except:
            url = ''
        return url



class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    attachment = models.ImageField(
        null=True, blank=True, upload_to='Messages/')
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
    
    @property
    def imageURL(self):
        try:
            url = self.attachment.url
        except:
            url = ''
        return url

class Inquiry(models.Model):
    STATUS = (
        ('Solved', 'Solved'),
        ('Unsolved', 'Not Solved'),
    )
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    attachment = models.ImageField(
        null=True, blank=True, upload_to='Inquiry/')
    is_read = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=200, choices=STATUS, default="Unsolved", null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-status', '-created']
    
    @property
    def imageURL(self):
        try:
            url = self.attachment.url
        except:
            url = ''
        return url
