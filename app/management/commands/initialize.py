from django.core.management.base import BaseCommand

from app.models import ActionDefinition, Persona

DEFAULT_ACTION_DEFINITIONS = [
	'I am on',
	'I click',
	'I fill in the form field',
	'I select',
	'I have the following data',
	'I enter the following data',
	'I see'
]

DEFAULT_PERSONAS = [
	('Product Owner', 'Manages products, prioritizes features, and creates requests'),
	('UX Designer', 'Does UX research, creates wireframes and mocks, and ensures product meets PO\'s requests'),
	('Software Engineer', 'Implements features and UX designs across products'),
]


class Command(BaseCommand):
	help = 'Initialized some required data'

	def handle(self, *args, **options):
		self.stdout.write('Creating action defintions...')
		for action in DEFAULT_ACTION_DEFINITIONS:
			ActionDefinition.get_or_create(action)

		self.stdout.write('Creating personas...')
		for persona in DEFAULT_PERSONAS:
			name = persona[0]
			description = persona[1]
			Persona.get_or_create(name, description)

		self.stdout.write('Done.')
