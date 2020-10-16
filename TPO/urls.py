from django.urls import path
from . import views
from .views import NewsListView, NewsDetailView , CompanyDetailView , CompanyQueryListView , QueryCreateView , QueryDeleteView , QueryDeleteView , QueryUpdateView

urlpatterns = [
    path('',views.dashboard , name = 'TPO-dashboard'),
    path('home/', NewsListView.as_view() , name = 'TPO-home'),
    path('about/', views.about, name = 'TPO-about'),
    path('analytics/', views.analytics, name = 'TPO-analytics'),
    path('news/<int:pk>/', NewsDetailView.as_view() , name = 'news-detail'),
    path('company/<int:pk>/', CompanyDetailView.as_view() , name = 'company-detail'),
    path('company/<str:title>', CompanyQueryListView.as_view() , name = 'company-queries'),
    path('query/<str:title>/new/', QueryCreateView.as_view() , name = 'query-create'),
    path('query/<int:pk>/update/', QueryUpdateView.as_view() , name = 'query-update'),
    path('query/<int:pk>/delete/', QueryDeleteView.as_view() , name = 'query-delete'),
]
