"""URL route definitions for the application."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import RedirectView, TemplateView

from archeion.index.views import ArtifactDetailView, HomepageView, LinkDetailView

urlpatterns = [
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # path("accounts/login/", RedirectView.as_view(url="/admin/login/")),
    # path("accounts/logout/", RedirectView.as_view(url="/admin/logout/")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    # User management
    path("users/", include("archeion.users.urls", namespace="users")),
    # path('robots.txt', static.serve,
    #    {'document_root': settings.STATICFILES_DIRS[0], 'path': 'robots.txt'}),
    # re_path(r'^favicon\.ico$', RedirectView.as_view(url=static('favicons/favicon.ico'), permanent=True)),
    path("archive/", RedirectView.as_view(url="/")),
    path("archive/<str:pk>", LinkDetailView.as_view(), name="link-detail"),
    path("archive/<str:link_id>/<str:slug>", ArtifactDetailView.as_view(), name="artifact-detail"),
    path("index.html", RedirectView.as_view(url="/")),
    path("", HomepageView.as_view(), name="Home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
