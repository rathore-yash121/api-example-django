from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth.views import logout

import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),

    url(r'^dashboard/$',  'drchrono.views.dashboard', name='dashboard'),

    url(r'^logout/$', logout, {'next_page': 'index'}, name='logout'),

]
