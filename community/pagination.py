from rest_framework.pagination import PageNumberPagination

class PageNation(PageNumberPagination):
    page_size = 10