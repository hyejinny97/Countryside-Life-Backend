from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article, ArticleImage, Comment


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['id', 'nickname', 'image']
        read_only_fields = ['id']


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['image']


# 댓글 생성/조회/수정/삭제
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user', 
            'article',
            'content',
            'created_at', 
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at', 
            'updated_at',
        ]
        extra_kwargs = {
            'article': {'required': False},
        }


# 게시물 생성/조회/수정/삭제
class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    article_images = ArticleImageSerializer(many=True, partial=True, required=False)
    comments = CommentSerializer(many=True, partial=True, required=False)
    comments_cnt = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 
            'user', 
            'category', 
            'region', 
            'title', 
            'content', 
            'article_images', 
            'like_users',
            'comments',
            'comments_cnt',
            'created_at', 
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'comments',
            'comments_cnt',
            'like_users',
            'created_at', 
            'updated_at',
        ]
        extra_kwargs = {
            'article_images': {'required': False},
            'like_users': {'required': False},
            'comments': {'required': False},
        }
        # depth = 1

    def get_comments_cnt(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        article = Article.objects.create(**validated_data)

        article_images_data = validated_data.get('article_images', [])
        for image in article_images_data:
            ArticleImage.objects.create(article=article, image=image)

        return article


# 좋아요/좋아요 취소
class LikeSerializer(serializers.ModelSerializer):
    like_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = [
            'id', 
            'like_users',
        ]
