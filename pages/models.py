from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField


class Item(models.Model):
    video = EmbedVideoField()  # same like models.URLField()
    item_snippet = models.CharField(max_length=250, default="click to read the blog post ")

class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='photos/Category/', blank=True , null=True)
    is_active = models.BooleanField(default=True)
    is_selected = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        """ Meta for the naming in the django admin that
            describes a model if the object is singular or
            plural
        """
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    
    def get_absolute_url(self):
        return reverse("home:categories", args=[ self.slug ])

# Create your models here.
class Team(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    bio = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    user_name = models.CharField(max_length=255)
    number = PhoneNumberField(blank=True)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/team/', blank=True, null=True)
    facebook_link = models.URLField(max_length=130)
    instagram_link = models.URLField(max_length=130)
    youtube_link = models.URLField(max_length=130, blank=True, null=True)
    twitter_link = models.URLField(max_length=130, blank=True, null=True)
    google_plus_link = models.URLField(max_length=130, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES= ( ('draft','Draft'),('published','Published'),
                      )
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='blog_posts')
    #category = models.CharField(max_length=250, default="Others")
    snippet = models.CharField(max_length=250, default="click to read the blog post ")
    blog_photo = models.ImageField(upload_to='photos/blogs/', blank=True , null=True)
    blog_photo_1 = models.ImageField(upload_to='photos/blogs/', blank=True , null=True)
    blog_photo_2 = models.ImageField(upload_to='photos/blogs/', blank=True , null=True)
    blog_photo_3 = models.ImageField(upload_to='photos/blogs/', blank=True , null=True)
    post_video = EmbedVideoField()  # same like models.URLField()
    youtube_link = models.URLField(max_length=130, blank=True, null=True)
    url_link = models.URLField(max_length=130, blank=True, null=True)
    body = RichTextField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    is_featured = models.BooleanField(default=False)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('home:post_detail',
                    args=[self.publish.year,
                          self.publish.month,
                          self.publish.day,
                          self.slug])
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # manually deactivate inappropriate comments from admin site
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        # sort comments in chronological order by default
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
class CategoryPhoto(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Photo(models.Model):
    category = models.ForeignKey(
        CategoryPhoto, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    youtube_link = models.URLField(max_length=130, blank=True, null=True)
    url_link = models.URLField(max_length=130, blank=True, null=True)
    description = models.TextField()
    

    def __str__(self):
        return self.description