from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include(('splash.urls', 'splash'), namespace='splash')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('campaign/', include(('campaign.urls', 'campaign'), namespace='campaign')),
]
