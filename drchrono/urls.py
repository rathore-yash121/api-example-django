from django.conf.urls import include, url
from django.views.generic import TemplateView

import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # url(r'^home/$',  'drchrono.views.home', name='home'),

    url(r'^dashboard/$',  'drchrono.views.dashboard', name='dashboard'),

    # url(r'^createEmail/$',  'drchrono.views.createEmail', name='createEmail'),

]
