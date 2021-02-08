from django import template

from app.forms import DeleteItemForm, StepForm

register = template.Library()


@register.filter
def pdb(item):
    """ Helper for dropping into PDB from a template
    """
    import pdb  # noqa
    pdb.set_trace()  # noqa


@register.filter
def get_step_form(scenario):
	return StepForm(initial={'scenario': scenario})


@register.filter
def get_step_edit_form(step):
	return StepForm(instance=step)


@register.filter
def get_delete_item_form(item):
	return DeleteItemForm(initial={'pk': item.pk})
