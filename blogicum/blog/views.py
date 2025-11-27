from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from blog.models import Post, Category


def index(request):
    template_name = 'blog/index.html'
    posts = Post.objects.select_related(
        'author',
        'category',
        'location'
    ).filter(
        Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=timezone.now())
    ).order_by(
        '-pub_date'
    )[:5]
    context = {'post_list': posts}
    return render(request, template_name, context)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'author',
            'category',
            'location'
        ).filter(
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=timezone.now())

        ),
        pk=id
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
    post_list = Post.objects.select_related(
        'author',
        'category',
        'location'
    ).filter(
        Q(is_published=True)
        & Q(category=category)
        & Q(pub_date__lte=timezone.now())
    )
    context = {
        'post_list': post_list,
        'category': category
    }
    return render(request, template_name, context)
