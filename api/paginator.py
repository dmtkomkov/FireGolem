from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        if self.request.version == 'v1':
            return Response({
                'count': self.page.paginator.count,
                'page_size': self.page_size,
                'page_number': self.page.number,
                'page_count': self.page.paginator.num_pages,
                'results': data
            })
        return super(CustomPagination, self).get_paginated_response(data)