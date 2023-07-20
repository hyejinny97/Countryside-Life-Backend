from django.db.models.query import prefetch_related_objects
from django.db.models import Count
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer, LikeSerializer, serializers
from .pagination import PageNation
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView


# 게시물 생성/조회/수정/삭제
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    pagination_class = PageNation
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'title']
    # ordering_fields = ['likes', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # 요청에서 필터링 매개변수 가져오기
        category = self.request.query_params.get('category', None)
        # search = self.request.query_params.get('search', None)
        region = self.request.query_params.get('region', None)
        
        # 필터링 적용
        if category and category != '전체':
            queryset = queryset.filter(category=category)
        # elif search:
        #     queryset = queryset.filter(content__icontains=search)
        #     queryset = queryset.filter(title__icontains=search)

        if region and region != '전체':
            queryset = queryset.filter(region=region)
        
        # 정렬 적용
        ordering = self.request.query_params.get('ordering', 'created_at')
        if ordering == 'created_at':
            queryset = queryset.order_by('-created_at', '-id')
        if ordering == 'likes':
            queryset = queryset.annotate(likes_count=Count('like_users')).order_by('-likes_count')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.user != request.user: raise serializers.ValidationError('게시글 작성자만 수정 가능합니다.')

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user: raise serializers.ValidationError('게시글 작성자만 삭제 가능합니다.')

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# 댓글 생성/조회/수정/삭제
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, kwargs['article_id'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, article_id):
        article = Article.objects.get(id=article_id)
        serializer.save(user=self.request.user, article=article)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.user != request.user: raise serializers.ValidationError('댓글 작성자만 수정 가능합니다.')

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user: raise serializers.ValidationError('댓글 작성자만 삭제 가능합니다.')

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# 좋아요/좋아요 취소
class LikeView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.like_users.all():
            article.like_users.remove(request.user) 
        else:
            article.like_users.add(request.user)

        serializer = self.get_serializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 특정 user가 작성한 모든 게시글 조회
class UserArticlesView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = PageNation

    def list(self, request, *args, **kwargs):
        queryset = request.user.article_set.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 특정 user가 작성한 모든 댓글 조회
class UserCommentsView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = PageNation

    def list(self, request, *args, **kwargs):
        queryset = Article.objects.filter(comments__user_id=request.user.pk).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

# 특정 user가 좋아요한 모든 게시글 조회
class UserLikeArticlesView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = PageNation

    def list(self, request, *args, **kwargs):
        queryset = Article.objects.filter(like_users=request.user).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
