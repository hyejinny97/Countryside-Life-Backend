from django.db import models
from django.contrib.auth import get_user_model

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('텃밭', '텃밭'),
        ('화단', '화단'),
        ('한달살기', '한달살기'),
        ('댕댕이', '댕댕이'),
        ('냥냥이', '냥냥이'),
        ('귀촌', '귀촌'),
        ('풍경','풍경'),
        ('축제','축제'),
        ('명소','명소'),
        ('자유','자유'),
    ]

    REGION_CHOICES = [
        ('강원도', '강원도'),
        ('경기도', '경기도'),
        ('경상남도', '경상남도'),
        ('경상북도', '경상북도'),
        ('광주광역시', '광주광역시'),
        ('대구광역시', '대구광역시'),
        ('대전광역시', '대전광역시'),
        ('부산광역시', '부산광역시'),
        ('서울특별시', '서울특별시'),
        ('세종특별자치시', '세종특별자치시'),
        ('울산광역시', '울산광역시'),
        ('인천광역시', '인천광역시'),
        ('전라남도', '전라남도'),
        ('전라북도', '전라북도'),
        ('제주특별자치도', '제주특별자치도'),
        ('충청남도', '충청남도'),
        ('충청북도', '충청북도'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like_users = models.ManyToManyField(get_user_model(), related_name='like_articles')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=5000)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ArticleImage(models.Model):
    def article_image_path(instance, filename):
        # MEDIA_ROOT/article_image/<filename> 경로로 업로드
        return f'article_image/{filename}'

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_images')
    image = models.ImageField(upload_to=article_image_path, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)