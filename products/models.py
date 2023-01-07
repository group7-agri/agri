from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from users.models import Profile
# Create your models here.


class Product(models.Model):
    PRODUCT_TYPE = (
        ('Tea','Icyayi'),
        ( 'Coffee','Ikawa'),
        ('Cassava','Imyumbati'),
        ( 'Sweet Potato','Ibijumba'),
        ( 'Irish Potato','Ibirayi'),
        ('Maize','Ibigori'),
        ( 'Beans','Ibishyimbo'),
    ) 
    UNITY_TYPE = (
        ('Kg','Kilograms'),
        ( 'Lt','Litres'),
        ('Tray','Trays'),
        ( 'Species','Species'),
    )
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, choices=PRODUCT_TYPE, default="Ibirayi")
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    quantity = models.IntegerField(null=True, blank=True, default=0)
    unity = models.CharField(null=True,max_length=200, choices=UNITY_TYPE,blank=True, default="Kg")
    price = models.IntegerField(null=True, blank=True, default=0)
    location = models.CharField(max_length=100, null=True, blank=True)
    payments = models.ManyToManyField('Payment', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'product']]

    def __str__(self):
        return self.value


class Payment(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
