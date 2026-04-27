# course_app/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except Exception:
            raise NotFound("Bunday sahifa mavjud emas!")  # ← o'zbek tilida

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'pages': self.page.paginator.num_pages,
            'current': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })