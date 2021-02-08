"""pickleit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('project/', app_views.ListProjects.as_view(), name='project_list'),
    path('project/new/', app_views.CreateProject.as_view(), name='project_create'),
    path('persona/new/', app_views.CreatePersona.as_view(), name='persona_create'),
    path('project/<str:project_pk>/', app_views.ProjectDetail.as_view(), name='project_detail'),
    path('project/<str:project_pk>/tabledef/', app_views.ListTableDefinition.as_view(), name='table_def_list'),
    path('project/<str:project_pk>/tabledef/new/', app_views.EditTableDefinition.as_view(), name='table_def_create'),
    path('project/<str:project_pk>/tabledef/<str:table_pk>/', app_views.EditTableDefinition.as_view(), name='table_def_edit'),
    path('project/<str:project_pk>/feature/new/', app_views.CreateFeature.as_view(), name='feature_create'),
  	path(
    	'project/<str:project_pk>/feature/<str:feature_pk>/',
    	app_views.FeatureDetail.as_view(),
    	name='feature_detail'
    ),
  	path(
    	'project/<str:project_pk>/feature/<str:feature_pk>/scenario/<str:scenario_pk>/edit/',
    	app_views.ScenarioEdit.as_view(),
    	name='scenario_edit'
    ),
    path(
    	'project/<str:project_pk>/feature/<str:feature_pk>/scenario/new/',
    	app_views.CreateScenario.as_view(),
    	name='create_scenario'
    ),
    path(
    	'project/<str:project_pk>/feature/<str:feature_pk>/scenario/<str:scenario_pk>/step/new/',
    	app_views.CreateStep.as_view(),
    	name='create_step'
    ),
    path(
        'project/<str:project_pk>/feature/<str:feature_pk>/scenario/<str:scenario_pk>/step/<str:step_pk>/shift/<str:direction>/',
        app_views.ShiftStep.as_view(),
        name='shift_step'
    ),
    path(
        'project/<str:project_pk>/feature/<str:feature_pk>/scenario/<str:scenario_pk>/step/<str:step_pk>/edit/',
        app_views.EditStep.as_view(),
        name='edit_step'
    ),
    path(
    	'project/<str:project_pk>/delete/<str:itemtype>/',
    	app_views.DeleteItem.as_view(),
    	name='delete_item'
    ),
]
