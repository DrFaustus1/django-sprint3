from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category

POSTS_LIMIT = 5


def index(request):
    template_name = 'blog/index.html'
    posts = Post.objects.select_related(
        'author',
        'category',
        'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by(
        '-pub_date'
    )[:POSTS_LIMIT]
    context = {'post_list': posts}
    return render(request, template_name, context)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'author',
            'category',
            'location'
        ),
        pk=id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )

    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = category.posts.select_related(
        'author',
        'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {
        'post_list': post_list,
        'category': category
    }
    return render(request, template_name, context)
