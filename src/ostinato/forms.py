from django import forms
from django.contrib.auth.models import User

from ostinato.models import ContentItem


class ContentItemForm(forms.ModelForm):
	class Meta:
		model = ContentItem
		exclude = ('order', 'content_type', 'object_id', '_sm_state')
        # TODO: A developer should be able to further customize the exclude
        # list on a per-project basis, by editing the project settings
        # This can allow them to hide even more fields that may not be
        # required in their specific project

	def __init__(self, *args, **kwargs):
            super(ContentItemForm, self).__init__(*args, **kwargs)

            # Setup the State field so that it's clear what it does
            actions = (('', '-- %s --' % self.instance.sm_state),)
            for action in self.instance.sm_state_actions():
                actions += ((action, action),)
            self.fields['_sm_action'] = forms.ChoiceField(
                choices=actions, label="State", required=False)

            # Set up any filters for contributors and authors
            if 'allowed_authors' in kwargs:
                users = User.objects.filter(**allowed_authors)
            else:
                users = User.objects.filter(is_staff=True)
            choices = []
            for user in users:
                choices.append((user.id, user.username))
            self.fields['authors'].widget.choices = choices

            if 'allowed_contributors' in kwargs:
                user = User.objects.filter(**allowed_contributors)
            else:
                user = User.objects.filter(is_staff=True)
            choices = []
            for user in users:
                choices.append((user.id, user.username))
            self.fields['contributors'].widget.choices = choices

        def save(self, *args, **kwargs):
            """
            Override the save method so that we can take any required actions
            and move to the next state.
            """
            action = self.cleaned_data['_sm_action']
            if action:
	            self.instance.sm_take_action(action)
            return super(ContentItemForm, self).save(*args, **kwargs)