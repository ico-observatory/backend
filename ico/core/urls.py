"""
Django URL settings for JEMS project.
"""


from django.urls import include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views

from .views import (QueryView, VersionView, WorkerView, ListQueryByVersionView, AliveView, QueryFile, HandleVersionExecution)

urlpatterns = [
    # re_path(r'api/home/', LoginApiView.as_view(), name='user_home'),
    re_path('api/token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    re_path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    re_path(r'^api/worker/user/(?P<user_id>[0-9]+)/$', WorkerView.as_view(), name='get_worker'),
    re_path(r'^api/worker/(?P<worker_id>[0-9]+)/$', WorkerView.as_view(), name='put_worker'),
    re_path('api/worker/', WorkerView.as_view(), name='post_worker'),
    re_path(r'^api/alive/(?P<pk>[0-9]+)/$', AliveView.as_view(), name='alive'),
    re_path('api/version/', VersionView.as_view(), name='version'),
    re_path(r'^api/handle_version/(?P<version_id>[0-9]+)/(?P<worker_id>[0-9]+)/$', HandleVersionExecution.as_view(), name='handle_version'),
    # re_path('api/query/', QueryView.as_view(), name='query'),
    re_path('api/query_file/', QueryFile.as_view(), name='query_file'),
    # re_path(r'^api/query_by_version/(?P<version_id>[0-9]+)/$', ListQueryByVersionView.as_view(), name='list_query_by_version'),
]
urlpatterns = format_suffix_patterns(urlpatterns)