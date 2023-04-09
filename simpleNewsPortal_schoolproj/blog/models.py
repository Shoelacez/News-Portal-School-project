from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    reads = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    # Allowing users to upload pictures and images
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    # comment_and_reply_count
    def comments_counted(self):
        return Comment.objects.filter(post=self).count() + Reply.objects.filter(comment__post=self).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.content}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.post.comments_count = self.post.comments_counted()
            self.post.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.post.comments_count = self.post.comments_counted()
        self.post.save()


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_replied = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f"{self.content}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.comment.post.comments_count = self.comment.post.comments_counted()
            self.comment.post.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.comment.post.comments_count = self.comment.post.comments_counted()
        self.comment.post.save()

