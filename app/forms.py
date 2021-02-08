from django.forms import (
	Form,
	ModelForm,
	HiddenInput,
	CharField,
)

from app.models import (
    DataTableDefinition,
	Feature,
	Persona,
	Project,
	Scenario,
	Step
)


class AbstractModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbstractModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class DataTableDefinitionForm(AbstractModelForm):
    class Meta:
        model = DataTableDefinition
        fields = [
            'project',
            'name',
            'header',
            'rows',
        ]

        help_texts = {
            'name': 'must be unique for this project',
            'header': 'e.g. "[\'id\', \'name\', \'description\']"',
            'rows': 'e.g. "[ [\'d\', \'e\', \'f\'], [\'apples\', \'bananas\',\'pears\',], [4, 5, 6] ]"'
        }

        widgets = {
            'project': HiddenInput()
        }


class ProjectForm(AbstractModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
        ]


class PersonaForm(AbstractModelForm):
    class Meta:
        model = Persona
        fields = [
            'name',
            'description'
        ]


class FeatureForm(AbstractModelForm):
    class Meta:
        model = Feature
        fields = [
            'name',
            'description',
            'project',
        ]

        widgets = {
        	'project': HiddenInput()
        }


class ScenarioForm(AbstractModelForm):
    class Meta:
        model = Scenario
        fields = [
        	'feature',
            'persona',
            'description',
            'title',
        ]

        widgets = {
        	'feature': HiddenInput()
        }


class StepForm(AbstractModelForm):
    class Meta:
        model = Step
        fields = [
            'starter',
            'action',
            'body',
            'scenario',
            'table',
        ]

        widgets = {
        	'scenario': HiddenInput()
        }


class DeleteItemForm(Form):
    pk = CharField(widget=HiddenInput())
