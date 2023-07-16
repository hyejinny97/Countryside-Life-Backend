from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet, LikeView, UserArticlesView

article_router = DefaultRouter()
article_router.register(r'', ArticleViewSet)

comment_router = DefaultRouter()
comment_router.register(r'', CommentViewSet)


urlpatterns = [
    path('', include(article_router.urls), name='community_articles'),
    path('<int:article_id>/comments/', include(comment_router.urls), name='community_comments'),
    path('<int:article_id>/likes/', LikeView.as_view(), name='community_articles_likes'),
    path('user/', UserArticlesView.as_view(), name='user_community_articles'),
]
