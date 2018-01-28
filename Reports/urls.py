from django.urls import path
# from Product.views import ProductDetail, ProductList
from .views import SearchProductView, AdvancedSearch

app_name = 'Search'

urlpatterns = [
    path('', SearchProductView.as_view(),name = 'Result'),
    path('advanced/', AdvancedSearch.as_view(), name = 'Advanced'),
    # path('single/<slug:slug>/', ProductDetail.as_view(),name = 'Single'),


]
