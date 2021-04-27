from django.contrib import admin
from .models import Team, Post, Comment, Category, CategoryPhoto, Photo
from django.utils.html import format_html

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px" />'.format(object.photo.url))

    thumbnail.short_description = 'Photo'

    list_display = ('id', 'thumbnail', 'first_name', 'designation', 'created_date')
    list_display_links = ('id','thumbnail', 'first_name')
    search_fields = ('first_name', 'last_name', 'designation')
    list_filter = ('designation', )

admin.site.register(Team, TeamAdmin)
admin.site.register(CategoryPhoto)
admin.site.register(Photo)
@admin.register(Category)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','is_active', 'is_selected')
    list_filter = ('is_selected','title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status','publish')
