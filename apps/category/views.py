from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAdminUser

from apps.category.models import Category
from apps.category.serializers import CategorySerializer


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = {
        'title': ['contains'],
    }

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(CategoryListAPIView, self).post(request, *args, **kwargs)


class CategoryAPIView(RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(CategoryAPIView, self).delete(request, *args, **kwargs)
