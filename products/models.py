from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from users.models import Profile
# Create your models here.


class Product(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, related_name='owner')
    name = models.ForeignKey('SingleProduct', default=uuid.uuid4, on_delete=models.CASCADE, null=True, related_name = 'product')
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    quantity = models.PositiveIntegerField(null=True, blank=True, default=0)
    location = models.CharField(max_length=100, null=True, blank=True)
    payments = models.ManyToManyField('Payment', blank=True, default="In Hand")
    instock = models.BooleanField(blank=True, null=True, default=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=True)

    def __str__(self):
        return self.name.name

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', '-created']

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

class SingleProduct(models.Model):

    name = models.CharField(max_length=200, null=True, blank=True, default="Ibirayi")
    price = models.PositiveIntegerField(null=True, blank=True, default=0)
    unity = models.CharField(max_length=200, null=True, blank=True, default="Kilogram")
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Category"

class Order(models.Model):
    STATUS = (
        ('Confirmed','Confirmed'),
        ('Delivered','Delivered'),
        ( 'Declined','Declined'),
        ( 'Pending','Pending'),
    )
    seller = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="seller")
    buyer = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="buyer")
        
    productName = models.CharField(max_length=200, null=True, blank=True)
    price = models.PositiveIntegerField( null=True, blank=True, verbose_name="Initial Price")
    status = models.CharField(max_length=200, choices=STATUS, default="Pending", null=True, blank=True)
    unity = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Quantity Purchased")
    location = models.CharField(max_length=200, null=True, blank=True)
    request = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    ProductId = models.CharField(blank=True, null= True, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.productName
    def line_total(self):
        return self.quantity * self.price



