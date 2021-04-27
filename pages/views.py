from django.shortcuts import render, get_object_or_404
from .models import Team, Post,Comment, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from taggit.models import Tag
from django.db.models import Count
from marketing.forms import EmailSignupForm
from .models import Photo, CategoryPhoto
# Create your views here.


def gallery(request):
    teams = Team.objects.all()
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = CategoryPhoto.objects.all()
    context = {'teams':teams,'categories': categories, 'photos': photos}
    return render(request, 'blogpost/gallery.html', context)


def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    teams = Team.objects.all()
    return render(request, 'blogpost/photo.html', {'photo': photo, 'teams': teams})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blogpost/list.html'

def blog_category(request, category_slug):
    teams = Team.objects.all()
    categories = Category.objects.all()
    posts = Post.published.filter(status='published')
    if category_slug:
        category = get_object_or_404(Category, slug= category_slug)
        posts = Post.published.filter(category=category)
   
    context = {
        "categories": categories,
        "posts": posts,
        "category": category,
        "teams": teams,
    }
    
    return render(request, "blogpost/categories.html", context)


def home(request, tag_slug=None):
    featured_posts =Post.objects.order_by('-created').filter(is_featured=True)
    teams = Team.objects.all()
    object_list = Post.published.all()
    posts = Post.published.all()
    categories = Category.objects.filter(is_active=True)
    forms = EmailSignupForm()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
        
    paginator = Paginator(object_list,4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    #all_cars = Car.objects.order_by('-created_date')
    #model_search = Car.objects.values_list('model', flat=True).distinct()
    #city_search = Car.objects.values_list('city', flat=True).distinct()
    #year_search = Car.objects.values_list('year', flat=True).distinct()
    #body_style_search = Car.objects.values_list('body_style', flat=True).distinct()

    # search_fields = Car.objects.values('model', 'city', 'year', 'body_style')

    template = 'blogpost/home.html'

    data = {
        'teams' : teams,
        'posts' : posts,
        'page' : page,
        'tag' : tag,
        'featured_posts' : featured_posts,
        'categories': categories,
        'forms': forms,
        
        #'featured_cars' : featured_cars,
        #'all_cars' : all_cars,
        #'model_search' : model_search,
        #'city_search' : city_search,
        #'year_search' : year_search,
        #'body_style_search' : body_style_search,
        #'search_fields': search_fields,
    }

    return render(request, template, data)


def post_list(request, tag_slug=None):
    teams = Team.objects.all()
    posts = Post.published.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        
    paginator = Paginator(posts,4)# 3 posts at single page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    template = 'blogpost/list.html'
    
    context = {
        'page': page,
        'posts': posts,
        'teams': teams,
        'tag': tag,
    }
    
    return render(request, template, context)


#To display a single post
def post_detail(request, year, month, day, post):
    teams = Team.objects.all()
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
        # list of active parent comments
    comments = post.comments.filter(active=True, parent__isnull=True)

    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post = post
            # save
            new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:2]
    
    template = 'blogpost/detail.html'

    data = {
        'post': post,
        'teams' : teams,
        'comments': comments,
        'comment_form': comment_form,
        'post_tags_ids': post_tags_ids,
        'similar_posts': similar_posts,
    }

    return render(request, template, data)

def post_share(request, post_id):
    teams = Team.objects.all()
    post =  get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #  ... send data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,'sewemallonline@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    template = 'blogpost/share.html'
    
    context = {
        'post' : post,
        'form' : form,
        'sent' : sent,
        'teams': teams,
    }
    
    return render(request, template, context)
