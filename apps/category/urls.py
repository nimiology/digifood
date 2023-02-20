from django.urls import path

from apps.category.views import CategoryAPIView, CategoryListAPIView

app_name = 'category'
urlpatterns = [
    path('', CategoryListAPIView.as_view(), name='category'),
    path('<pk>/', CategoryAPIView.as_view(), name='category'),
]