"""hypernews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from news.views import NewsPageView, NewsMainView, CreateNewsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/news/')),
    path('news/<int:id>/', NewsPageView.as_view()),
    path('news/create/', CreateNewsView.as_view()),
    path('news/', NewsMainView.as_view()),
]

urlpatterns += static(settings.STATIC_URL)
