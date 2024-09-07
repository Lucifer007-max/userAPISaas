from django.urls import include, path
from api.views import Auth
from rest_framework.routers import DefaultRouter

app_name = 'api'
router = DefaultRouter()

urlpatterns = [
    path('signup', Auth.as_view({'post': 'create'}), name='register-list'),
    path('verify', Auth.as_view({'post': 'userExist'}), name='verify'),
    path('delete', Auth.as_view({'delete': 'delete'}), name='delete'),
    path('authenticate', Auth.as_view({'post': 'authenticate'}), name='authenticate'),
    path('validatePassword', Auth.as_view({'post': 'validatePassword'}), name='validatePassword'),
    path('logout', Auth.as_view({'put': 'logout'}), name='logout'),
    path('<int:user_id>', Auth.as_view({'get': 'getUserById'}), name='get-user-by-id'),
    path('update/<int:user_id>',  Auth.as_view({'put': 'updateUser'}), name='user-update'),
    path('cartgetId/<int:user_id>', Auth.as_view({'get': 'getCartDataById'}), name='get-cart-by-id'),
    path('cart/<int:user_id>', Auth.as_view({'put': 'updateCart'}), name='updateCart'),
]
