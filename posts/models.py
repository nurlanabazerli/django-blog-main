from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Kateqoriya Adı')
    slug = models.SlugField(unique=True, help_text='dəyiştirmə')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Teq Adı')
    slug = models.SlugField(unique=True, help_text='dəyiştirmə.')

    def __str__(self):
        return self.name


class HitCount(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='teqs')
    views = models.ManyToManyField(HitCount, related_name='post_views', blank=True)
    title = models.CharField(max_length=75, verbose_name='Başlıq')
    slug = models.SlugField(unique=True, help_text='dəyiştirmə')
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', verbose_name='şəkil')
    content = RichTextField(verbose_name='Məzmun')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')
    available = models.BooleanField(default=True, verbose_name='Aktif/Pasif')

    def __str__(self):
        return self.title

    def getHitCount(self):
        return self.views.count()

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Şərh')
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True, verbose_name='Aktif/Pasif')

    class Meta:
        ordering = ['-created']  ## Post şərhlərini təzədən köhnəyə sıralama

    def __str__(self):
        return self.author.username+' | '+ self.post.title