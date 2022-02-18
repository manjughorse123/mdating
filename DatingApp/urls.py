from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView, TokenObtainPairView, \
#     TokenRefreshView, TokenVerifyView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Dating App",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
admin.site.site_title= "Dating App"
admin.site.site_header = "Admin Deshboard"
urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('account/', include('account.urls')),
    path('post/api/', include('post.urls')),
    path('usermedia/api/', include('usermedia.urls')),
    path('likeuser/', include('likeuser.urls')),
    path('friend/', include('friend.urls')),
    path('matchprofile/', include('matchprofile.urls')),

    # path('', include('masterapp.urls')),
    # path('verify/', include('userverification.urls')),
    # path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    # path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

