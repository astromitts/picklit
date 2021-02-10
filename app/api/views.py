from rest_framework.response import Response
from rest_framework.views import APIView

from app.views import ProjectView

from app.api.serializers import FeatureSerializer, ScenarioSerializer


class ScenarioDashboard(APIView, ProjectView):
	def get(self, request, *args, **kwargs):
		serializer = ScenarioSerializer(self.scenario)
		return Response(serializer.data)

	def patch(self, request, *args, **kwargs):
		serializer = ScenarioSerializer(self.scenario, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(data=serializer.data)
		else:
			data = {
				'status': 'error',
				'message': 'requested patch fields invalid'
			}
			return Response(data=data, code=400)

	def delete(self, request, *args, **kwargs):
		serializer = ScenarioSerializer(self.delete)
		return Response(serializer.data)


class FeatureDashboard(APIView, ProjectView):
	def get(self, request, *args, **kwargs):
		serializer = FeatureSerializer(self.feature)
		return Response(serializer.data)
