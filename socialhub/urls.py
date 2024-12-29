from django.urls import path
from . import views

app_name = "socialhub"

urlpatterns = [
    # Main feed and post views
    path('', views.home_view, name='home'),
    path('p/<slug:slug>/', views.post_detail_view, name='post-detail'),
    
    # Post CRUD operations
    path('post/new/', views.post_create_view, name='post-create'),
    path('post/<int:pk>/update/', views.post_update_view, name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete_view, name='post-delete'),
    
    # Search functionality
    path('search/', views.search_view, name='search'),
    
    # Post interactions
    path('post/like/', views.like_view, name='like'),
    path('post/report/', views.post_report_view, name='report-user'),
    
    # Notifications
    path('<str:username>/notifications/',views.notifications_view,name='notifications'),
    path('<str:username>/notifications/update/',views.notifications_update_view,name='notifications-update'),
    path('<str:username>/notifications/count/',views.notifications_unread_count_view,name='notifications-count'),


    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow-unfollow/<int:pk>/',views.userFollowUnfollow,name="follow-unfollow"),
]