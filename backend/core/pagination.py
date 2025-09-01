from rest_framework.pagination import PageNumberPagination

class BlogPagination(PageNumberPagination):
    page_size = 10  # default
    page_size_query_param = 'page_size'  # user can change
    max_page_size = 50  # max that user can change(page_size_query_param)
