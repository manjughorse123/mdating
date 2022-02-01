from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView, TokenObtainPairView, \
#     TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('account/', include('account.urls')),
    path('post/api/', include('post.urls')),
    path('media/api/', include('usermedia.urls')),
    path('likeuser/', include('likeuser.urls')),
    path('friend/', include('friend.urls')),
    path('matchprofile/', include('matchprofile.urls')),
    path('verify/', include('userverify.urls')),

    # path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    # path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

