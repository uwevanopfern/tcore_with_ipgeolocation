from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    region_iso_code = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=100)
    country_is_eu = models.BooleanField(blank=True, null=True)
    continent = models.CharField(max_length=100)
    continent_code = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=100)

    def __str__(self):
        return self.country


class Holiday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_local = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    date = models.DateField()
    week_day = models.CharField(max_length=100)

    def __str__(self):
        return self.date


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    like_count = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"
