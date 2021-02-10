from django.urls import path

from app.api import views

urlpatterns = [

  	path(
    	'api/project/<str:project_pk>/feature/<str:feature_pk>/',
    	views.FeatureDashboard.as_view(),
    	name='api_feature_dashboard'
    ),
  	path(
    	'api/project/<str:project_pk>/feature/<str:feature_pk>/scenario/<str:scenario_pk>/',
    	views.ScenarioDashboard.as_view(),
    	name='api_scenario_dashboard'
    ),
]
