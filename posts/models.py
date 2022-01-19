from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

    @property
    def likes(self):
        likes = PostLike.objects.filter(post=self)
        return likes.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} made a like on post #{self.post.pk}.'
