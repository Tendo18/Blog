from django.urls import path
from . import views

urlpatterns = [
    path('promotions/', views.PromotionListView.as_view(), name='promotion-list'),
    path('promotions/create/', views.PromotionCreateView.as_view(), name='promotion-create'),
    path('promotions/<slug:slug>/', views.PromotionDetailView.as_view(), name='promotion-detail'),
    path('promotions/<int:pk>/update/', views.PromotionUpdateView.as_view(), name='promotion-update'),
    path('promotions/<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion-delete'),
] 