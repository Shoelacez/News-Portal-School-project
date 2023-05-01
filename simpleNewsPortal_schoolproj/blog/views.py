from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Comment
from django.http import HttpResponseRedirect
from .forms import CommentForm, ReplyForm
from django.db.models import Count


# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-date_created')
    context = {'posts': posts}
    return render(request, 'blog/home.html', context)


def category_detail(request, category_id):
    # Get the category object based on the slug
    category = get_object_or_404(Category, id=category_id)
    # Get all the posts that belong to the category
    posts = Post.objects.filter(category=category)
    context = {'category': category, 'posts': posts}
    # Render the template with the category and its posts
    return render(request, 'blog/category_detail.html', context)


class PostListview(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewType>.html
    context_object_name = 'posts'
    ordering = ['-date_created']


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked

        # add comment count to context
        context['comment_count'] = stuff.comments_counted()

        stuff.reads += 1  # increment reads count
        stuff.save()  # save updated Post object
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'image', 'video']

    def form_valid(self, form):
        form.instance.author = self.request.user
        image = self.request.FILES.get('image')
        video = self.request.FILES.get('video')
        if image:
            form.instance.image = image
        if video:
            form.instance.video = video
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'categories', 'image', 'video']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required()
def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        # if the user has already liked, clicking again means disliking
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post_detail', kwargs={"pk": pk}))


@login_required
def comment_to_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)

    context = {"form": form}
    return render(request, 'blog/comment_form.html', context)


@login_required()
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    form = ReplyForm()

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            return redirect('post_detail', pk=comment.post.id)

    context = {'form': form}
    return render(request, 'add_reply.html', context)

#
# @login_required()
# def search(request):
#     query = request.GET.get('query')
#     category = request.GET.get('category')
#
#     if query and category:
#         # Filter posts by category and search query
#         posts = Post.objects.filter(category__name__icontains=category, title__icontains=query)
#     elif query:
#         # Filter posts by search query only
#         posts = Post.objects.filter(title__icontains=query)
#     elif category:
#         # Filter posts by category only
#         posts = Post.objects.filter(category__name__icontains=category)
#     else:
#         # No search query or category selected, return all posts
#         posts = Post.objects.all()
#
#     context = {
#         'posts': posts,
#         'query': query,
#         'category': category,
#     }
#     return render(request, 'blog/search_results.html', context)

@login_required()
def search(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    num_views = request.GET.get('num_views')
    num_likes = request.GET.get('num_likes')
    print(num_likes)

    if query and category:
        # Filter posts by category and search query
        posts = Post.objects.filter(category__name__icontains=category, title__icontains=query)
    elif query:
        # Filter posts by search query only
        posts = Post.objects.filter(title__icontains=query)
    elif category:
        # Filter posts by category only
        posts = Post.objects.filter(category__name__icontains=category)
    else:
        # No search query or category selected, return all posts
        posts = Post.objects.all()

    if num_views:
        # Filter posts by number of reads
        posts = posts.filter(reads=num_views)

    if num_likes:
        # Filter posts by number of likes
        # posts = posts.filter(likes=num_likes)
        posts = posts.annotate(num_likes=Count('likes')).filter(num_likes=num_likes)

    context = {
        'posts': posts,
        'query': query,
        'category': category,
        'num_views': num_views,
        'num_likes': num_likes,
    }
    return render(request, 'blog/search_results.html', context)

def about(request):
    return render(request, 'blog/about.html')
