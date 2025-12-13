# posts/pagination.py
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    # Defines the query parameter name for the page size (e.g., ?page_size=10)
    page_size_query_param = 'page_size' 
    # Sets the default number of items per page
    page_size = 10 
    # Allows a user to set a maximum page size (e.g., max 50 items)
    max_page_size = 50