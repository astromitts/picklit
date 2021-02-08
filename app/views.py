import json
from copy import copy

from django.contrib import messages
from django.db import IntegrityError
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.utils.safestring import mark_safe

from app.forms import (
	DataTableDefinitionForm,
	FeatureForm,
	PersonaForm,
	ProjectForm,
	ScenarioForm,
	StepForm,
)
from app.models import (
	DataTableDefinition,
	Feature,
	Persona,
	Project,
	Scenario,
	Step,
)


def _print_form_error(request, message, form):
	if form.errors.get('__all__'):
		message = '{}: {}'.format(message, form.errors['__all__'])
	messages.error(request, message)


class ProjectView(View):
	def setup(self, request, *args, **kwargs):
		super(ProjectView, self).setup(request, *args, **kwargs)
		self.project = None
		self.feature = None
		self.scenario = None
		self.step = None

		self.project_url = None
		self.feature_url = None
		self.scenario_url = None
		self.step_url = None

		url_kwargs = {}

		breadcrumbs = []

		if 'project_pk' in kwargs:
			self.project = Project.objects.get(pk=kwargs['project_pk'])
			url_kwargs.update({'project_pk': self.project.pk})
			self.project_url = reverse('project_detail', kwargs=url_kwargs)
			breadcrumbs.append(('Project: {}'.format(self.project.name), self.project_url))

			self.data_table_list_url = reverse('table_def_list', kwargs=url_kwargs)

			if 'table_pk' in kwargs:
				breadcrumbs.append(('Data Tables', self.data_table_list_url))
				self.data_table = self.project.datatabledefinition_set.get(pk=kwargs['table_pk'])
				url_kwargs.update({'table_pk': self.data_table.pk})
				self.table_url = reverse('table_def_edit', kwargs=url_kwargs)
				breadcrumbs.append(('Data Table: {}'.format(self.data_table.name), self.table_url))

			if 'feature_pk' in kwargs:
				self.feature = self.project.feature_set.get(pk=kwargs['feature_pk'])
				url_kwargs.update({'feature_pk': self.feature.pk})
				self.feature_url = reverse('feature_detail', kwargs=url_kwargs)
				breadcrumbs.append(('Feature: {}'.format(self.feature.name), self.feature_url))


				if 'scenario_pk' in kwargs:
					self.scenario = self.feature.scenario_set.get(pk=kwargs['scenario_pk'])
					url_kwargs.update({'scenario_pk': self.scenario.pk})

					self.scenario_url = reverse('scenario_edit', kwargs=url_kwargs)
					breadcrumbs.append(
						('Scenario: {} {}'.format(self.scenario.persona, self.scenario.title), self.scenario_url)
					)

					if 'step_pk' in kwargs:
						self.step = self.scenario.step_set.get(pk=kwargs['step_pk'])
						url_kwargs.update({'step_pk': self.step.pk})

		self.url_kwargs = url_kwargs
		self.context = {
			'project': self.project,
			'feature': self.feature,
			'scenario': self.scenario,
			'project_url': self.project_url,
			'feature_url': self.feature_url,
			'scenario_url': self.scenario_url,
			'step': self.step,
			'breadcrumbs': breadcrumbs
		}



class ListProjects(View):
	def get(self, request, *args, **kwargs):
		template = loader.get_template('pickleit/pages/project_list.html')
		context = {
			'projects': Project.objects.all(),
			'personas': Persona.objects.all(),
			'project_form': ProjectForm(),
			'persona_form': PersonaForm()
		}
		return HttpResponse(template.render(context, request))


class ProjectDetail(ProjectView):
	def get(self, request, *args, **kwargs):
		template = loader.get_template('pickleit/pages/project_detail.html')
		self.context.update({
			'form': FeatureForm(initial={'project': self.project})
		})
		return HttpResponse(template.render(self.context, request))



class CreateProject(View):
	def post(self, request, *args, **kwargs):
		form = ProjectForm(data=request.POST)
		if form.is_valid():
			new_project = Project(name=request.POST['name'])
			new_project.save()
		else:
			_print_form_error(request, 'Could not create new project', form)
		return redirect(reverse('project_list'))


class CreatePersona(View):
	def post(self, request, *args, **kwargs):
		form = PersonaForm(data=request.POST)
		if form.is_valid():
			new_persona = Persona(
				name=request.POST['name'],
				description=request.POST['description']
			)
			new_persona.save()
		else:
			_print_form_error(request, 'Could not create new persona', form)
		return redirect(reverse('project_list'))


class ListTableDefinition(ProjectView):
	def get(self, request, *args, **kwargs):
		self.context['breadcrumbs'].append(('Data Tables', self.data_table_list_url))
		self.template = loader.get_template('pickleit/pages/list_table_defs.html')
		return HttpResponse(self.template.render(self.context, request))


class EditTableDefinition(ProjectView):
	def setup(self, request, *args, **kwargs):
		super(EditTableDefinition, self).setup(request, *args, **kwargs)
		self.form = DataTableDefinitionForm
		self.template = loader.get_template('pickleit/pages/create_table_def.html')
		self.edit = False

		if kwargs.get('table_pk'):
			self.edit = True
		else:
			self.context['breadcrumbs'].append(('Data Tables', self.data_table_list_url))
			self.context['breadcrumbs'].append(('Create Data Table', self.request.path))
			self.data_table = DataTableDefinition()

	def get(self, request, *args, **kwargs):
		if self.edit:
			form = self.form(instance=self.data_table)
		else:
			form = self.form(initial={'project': self.project})
		self.context.update(
			{
				'form': form,
				'edit': self.edit,
				'create': not self.edit,
			}
		)
		return HttpResponse(self.template.render(self.context, request))

	def post(self, request, *args, **kwargs):
		post_data = copy(request.POST)
		errors = []
		try:
			post_data['header'] = json.loads(post_data['header'])
		except json.JSONDecodeError:
			errors.append('<li>Header: invalid JSON list</li>')

		try:
			post_data['rows'] = json.loads(post_data['rows'])
		except json.JSONDecodeError:
			errors.append('<li>Rows: invalid JSON list</li>')

		if errors:
			message = 'Could not process form data: <ul>{}</ul>'.format(''.join(errors))
			messages.error(request, message)
			self.context.update({'form': self.form(data=request.POST)})
			return HttpResponse(self.template.render(self.context, request))
		else:
			try:
				self.data_table.name = post_data['name']
				self.data_table.header = post_data['header']
				self.data_table.rows = post_data['rows']
				self.data_table.project = self.project

				self.data_table.save()

				self.url_kwargs.update({'table_pk': self.data_table.pk})
				self.table_url = reverse('table_def_edit', kwargs=self.url_kwargs)
				return redirect(self.table_url)
			except IntegrityError:
				message = 'A data table with this name already exists for project.'
				messages.error(request, message)
				self.context.update({'form': self.form(data=request.POST)})
				return HttpResponse(self.template.render(self.context, request))


class FeatureDetail(ProjectView):
	def get(self, request, *args, **kwargs):
		template = loader.get_template('pickleit/pages/feature_detail.html')
		self.context.update({
			'form': ScenarioForm(initial={'feature': self.feature})
		})
		return HttpResponse(template.render(self.context, request))


class ScenarioEdit(ProjectView):
	def get(self, request, *args, **kwargs):
		template = loader.get_template('pickleit/pages/feature_edit.html')
		self.context.update({
			'form': FeatureForm(instance=self.feature),
			'edit_form': ScenarioForm(instance=self.scenario),
			'scenario_form': ScenarioForm(initial={'feature': self.feature}),
		})
		return HttpResponse(template.render(self.context, request))

	def post(self, request, *args, **kwargs):
		form = ScenarioForm(data=request.POST)
		if form.is_valid():
			self.scenario.persona = Persona.objects.get(pk=request.POST['persona'])
			self.scenario.description = request.POST['description']
			self.scenario.title = request.POST['title']
			self.scenario.save()
		else:
			_print_form_error(request, 'Could not update scenario', form)
		return redirect(request.path)


class CreateFeature(ProjectView):
	def post(self, request, *args, **kwargs):
		form = FeatureForm(data=request.POST)
		if form.is_valid():
			new_feature = Feature(
				name=request.POST['name'],
				description=request.POST['description'],
				project=self.project,
			)
			new_feature.save()

			self.url_kwargs.update({'feature_pk': new_feature.pk})
			return redirect(reverse('feature_detail', kwargs=self.url_kwargs))
		else:
			_print_form_error(request, 'Could not create new feature', form)
		return redirect(self.project_url)


class CreateScenario(ProjectView):
	def post(self, request, *args, **kwargs):
		form = ScenarioForm(data=request.POST)
		if form.is_valid():
			new_scenario = Scenario(
				persona_id=request.POST['persona'],
				description=request.POST['description'],
				title=request.POST['title'],
				feature=self.feature,
			)
			new_scenario.save()
			self.url_kwargs.update({'scenario_pk': new_scenario.pk})
			return redirect(reverse('scenario_edit', kwargs=self.url_kwargs))
		else:
			_print_form_error(request, 'Could not create new scenario', form)
			return redirect(self.feature_url)


class CreateStep(ProjectView):
	def post(self, request, *args, **kwargs):
		form = StepForm(data=request.POST)
		if form.is_valid():
			new_step = Step(
				scenario_id=request.POST['scenario'],
				starter=request.POST['starter'],
				action_id=request.POST['action'],
				body=request.POST['body'],
				table_id=request.POST.get('table')
			)
			new_step.save()
		else:
			_print_form_error(request, 'Could not create new step', form)
		return redirect(self.scenario_url)


class ShiftStep(ProjectView):
	def post(self, request, *args, **kwargs):
		direction = kwargs['direction']
		if direction == 'up':
			self.step.shift_up()
		else:
			self.step.shift_down()
		return redirect(self.scenario_url)


class EditStep(ProjectView):
	def post(self, request, *args, **kwargs):
		form = StepForm(data=request.POST)
		if form.is_valid():
			self.step.starter = request.POST['starter']
			self.step.body = request.POST['body']
			self.step.action_id = request.POST['action']
			self.step.table_id=request.POST.get('table')
			self.step.save()
		else:
			_print_form_error(request, 'Could not edit step', form)
		return redirect(self.scenario_url)


class DeleteItem(View):
	def post(self, request, *args, **kwargs):
		itemtype = kwargs['itemtype']
		if itemtype == 'persona':
			model = Persona
		elif itemtype == 'project':
			model = Project
		elif itemtype == 'scenario':
			model = Scenario
		elif itemtype == 'step':
			model = Step
		elif itemtype == 'feature':
			model = Feature
		elif itemtype == 'table':
			model = DataTableDefinition
		else:
			raise Exception('Item type {} not recognized'.format(itemtype))
		target_item = model.objects.get(pk=request.POST['itempk'])
		target_item.delete()

		return redirect(request.GET['returnurl'])
