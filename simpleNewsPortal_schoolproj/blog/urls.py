from django.urls import path
from .views import PostListview, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    # path("", PostListview.as_view(), name="blog_home"),
    path("", views.home, name="blog_home"),
    path("about/", views.about, name="blog_about"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("like_post/<int:pk>", views.like_view, name="like_post"),
    path("post/<int:pk>/comment/", views.comment_to_post, name="comment"),
    path("post/<int:comment_id>/reply/", views.add_reply, name="add_reply"),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),

]
