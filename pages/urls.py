from django.urls import path
from . import views
from .views import blog_category, gallery, Photo
from .feeds import LatestPostsFeed
from marketing.views import email_list_signup

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    #path('category/<str:cats>/', CategoryView, name= 'category'),
    path("category/<slug:category_slug>/", views.blog_category, name='categories'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('gallery/', views.gallery, name='gallery'),
    path('post_list/', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>',views.post_list, name='post_list_by_tag'),
    #path('post_list/',views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
    path('subscribe/', email_list_signup, name="subscribe"),
    path('feed/',LatestPostsFeed(),name='post_feed'),
    #path('about', views.about, name='about'),
    #path('services', views.services, name='services'),
    #path('contact', views.contact, name='contact'),
]
