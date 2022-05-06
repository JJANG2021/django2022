import re
from django.db import models
from acc.models import User

# Create your models here.
class Board(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")   # User 의 DB를 바라봄
    content = models.TextField()
    pubdate = models.DateTimeField()    # 최신글이 맨위로 올라오기 위해
    likey = models.ManyToManyField(User, blank=True, related_name="likey")    # N 대 N 관계

    def __str__(self):
        return self.subject
    
    def summary(self):
        if len(self.content) > 40:
            return f"{self.content[:40]}..."
        return self.content
    
    def hot(self):
        if self.likey.count() >= 2:
            return True
        return False


class Reply(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    replyer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.board}_{self.replyer}"