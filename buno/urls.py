from django.urls import path
from . import views

app_name = 'buno'

urlpatterns = [
    # Cafe URLs
    path('cafes/', views.CafeListView.as_view(), name='cafe_list'),
    path('cafes/<int:pk>/', views.CafeDetailView.as_view(), name='cafe_detail'),
    path('cafes/my/', views.user_cafes, name='user_cafes'),
    
    # Cafe Menu URLs
    path('cafes/<int:cafe_id>/menu/', views.CafeMenuView.as_view(), name='cafe_menu'),
    path('cafes/<int:cafe_id>/menu/<int:pk>/', views.CafeMenuDetailView.as_view(), name='cafe_menu_detail'),
    
    # Like URLs
    path('cafes/<int:cafe_id>/likes/', views.LikeView.as_view(), name='cafe_likes'),
    path('cafes/<int:cafe_id>/unlike/', views.unlike_cafe, name='unlike_cafe'),
    
    # Comment URLs
    path('cafes/<int:cafe_id>/comments/', views.CommentView.as_view(), name='cafe_comments'),
    path('cafes/<int:cafe_id>/comments/<int:pk>/', views.CommentDetailView.as_view(), name='cafe_comment_detail'),
    
    # Search and Recommendation URLs
    path('search/', views.search_cafes, name='search_cafes'),
    path('recommendations/', views.recommend_cafes, name='recommend_cafes'),
]
