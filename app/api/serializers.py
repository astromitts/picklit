from rest_framework import serializers

from app.models import DataTableDefinition, Scenario, Step, Feature


class DataTableDefinitionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DataTableDefinition
		fields = [
			'pk',
			'header',
			'rows'
		]

class StepSerializer(serializers.HyperlinkedModelSerializer):
	data_table = DataTableDefinitionSerializer(
		read_only=True, source='table'
	)

	class Meta:
		model = Step
		fields = [
			'pk',
			'starter',
			'action_display',
			'body',
			'order',
			'data_table',
		]


class ScenarioSerializer(serializers.HyperlinkedModelSerializer):
	steps = StepSerializer(many=True, read_only=True, source='step_set')

	class Meta:
		model = Scenario
		fields = [
			'pk',
			'api_path',
			'edit_path',
			'persona_display',
			'title',
			'description',
			'steps',
		]


class ScenarioSerializerSmall(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Scenario
		fields = [
			'pk',
			'api_path',
			'edit_path',
			'title',
			'description',
		]


class FeatureSerializer(serializers.HyperlinkedModelSerializer):
	scenarios = ScenarioSerializerSmall(many=True, read_only=True, source='scenario_set')

	class Meta:
		model = Feature
		fields = [
			'pk',
			'api_path',
			'name',
			'description',
			'scenarios',
		]
