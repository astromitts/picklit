from copy import copy
from django.db import models
from django.urls import reverse


class Project(models.Model):
	name = models.CharField(max_length=250, unique=True)


class Feature(models.Model):
	name = models.CharField(max_length=250)
	description = models.TextField(max_length=250, blank=True, null=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)

	class Meta:
		unique_together = ['project', 'name']

	@property
	def api_path(self):
		return reverse(
			'api_feature_dashboard', kwargs={
				'project_pk': self.project.pk,
				'feature_pk': self.pk,
			}
		)


class Persona(models.Model):
	name = models.CharField(max_length=250, unique=True)
	description = models.TextField(max_length=250)

	def __str__(self):
		return self.name

	@classmethod
	def get_or_create(cls, name, description):
		qs = cls.objects.filter(name=name)
		if qs.exists():
			instance = qs.first()
		else:
			instance = cls(name=name)
		instance.description = description
		instance.save()
		return instance


class Scenario(models.Model):
	title = models.CharField(max_length=250)
	description = models.TextField(blank=True, null=True)
	feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
	persona = models.ForeignKey(Persona, null=True, on_delete=models.SET_NULL)

	@property
	def persona_display(self):
		return self.persona.name

	@property
	def api_path(self):
		return reverse(
			'api_scenario_dashboard', kwargs={
				'project_pk': self.feature.project.pk,
				'feature_pk': self.feature.pk,
				'scenario_pk': self.pk,
			}
		)

	@property
	def edit_path(self):
		return reverse(
			'scenario_edit', kwargs={
				'project_pk': self.feature.project.pk,
				'feature_pk': self.feature.pk,
				'scenario_pk': self.pk,
			}
		)


class ActionDefinition(models.Model):
	action = models.CharField(max_length=25, unique=True)

	def __str__(self):
		return self.action

	@classmethod
	def get_or_create(cls, action):
		qs = cls.objects.filter(action=action)
		if qs.exists():
			return qs.first()
		new_instance = cls(action=action)
		new_instance.save()
		return new_instance


class DataTableDefinition(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=250)
	header = models.JSONField(default=list)
	rows = models.JSONField(default=list)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = ['project', 'name']


class Step(models.Model):
	scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
	starter = models.CharField(
		max_length=10,
		choices=(
			('When', 'When'),
			('Then', 'Then'),
			('And', 'And'),
		)
	)
	action = models.ForeignKey(ActionDefinition, null=True, on_delete=models.SET_NULL)
	body = models.CharField(max_length=500)
	order = models.IntegerField(null=True)
	table = models.ForeignKey(DataTableDefinition, null=True, blank=True, on_delete=models.SET_NULL)

	class Meta:
		ordering = ['order']
		unique_together = ['scenario', 'order']

	@property
	def action_display(self):
		return self.action.action

	def shift_up(self):
		original_order = copy(self.order)
		self.order = None
		self.save()
		next_step = self.scenario.step_set.filter(order__lt=original_order).order_by('-order').first()
		next_step.order = original_order
		next_step.save()

		self.order = original_order - 10
		self.save()

	def shift_down(self):
		original_order = copy(self.order)
		self.order = None
		self.save()

		next_step = self.scenario.step_set.filter(order__gt=original_order).first()
		next_step.order = original_order
		next_step.save()

		self.order = original_order + 10
		self.save()

	def save(self, *args, **kwargs):
		if not self.pk:
			max_order = self.scenario.step_set.order_by('-order').first()
			if max_order:
				next_order = max_order.order + 10
				self.order = next_order
			else:
				self.order = 10
		super(Step, self).save(*args, **kwargs)

