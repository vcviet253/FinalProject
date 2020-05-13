

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from django.forms import formset_factory
from django.utils import timezone

from app.models import Ballot, AddressBallotRegister


class UserRegisterForm(UserCreationForm):
    """
    Form for user register to website
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OptionForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Option name'}))

OptionFormSet = formset_factory(OptionForm, can_delete=True, extra=2)


class BallotForm(forms.Form):
    ballot_name = forms.CharField(required=False)
    ballot_end_date = forms.DateTimeField(widget=forms.SelectDateWidget(empty_label=("Year", "Month", "Day"),attrs={'style': 'display: inline-block; width: 33%;'}), required=False)
    max_vote = forms.CharField(required=False)
    file = forms.FileField(required=False,
                           help_text='Upload csv file with each line containing an email address.<br/>For example:<br/>johndoe@example.com<br/>nicholas@example.com<br/>...')

    def clean(self):
        cleaned_data = super(BallotForm, self).clean()

        ballot_name = cleaned_data.get('ballot_name')
        ballot_end_date = cleaned_data.get('ballot_end_date')
        max_vote = cleaned_data.get('max_vote')
        file = cleaned_data.get('file')
        print(file)
        print(ballot_end_date)
        print(cleaned_data)

        if ballot_name.strip() == '':
            self.add_error('ballot_name', 'This field is required')
        elif Ballot.objects.filter(ballot_name=ballot_name.strip()).exists():
            self.add_error('ballot_name', 'Ballot name existed. Choose another name')
        if ballot_end_date == None:
            self.add_error('ballot_end_date', 'This field is required')
        elif ballot_end_date <= timezone.now():
            # raise forms.ValidationError("Invalid date. End date must be at least one day from today")
            self.add_error('ballot_end_date', 'Invalid date. End date must be at least one day from today')
        if max_vote == '' or max_vote ==None:
            self.add_error('max_vote', 'This field is required')
        elif not max_vote.isdigit():
            self.add_error('max_vote', 'Please enter a positive integer')
        elif int(max_vote) < 1:
            self.add_error('max_vote', 'Max votes allowed must be greater than 1')
        if file == None:
            self.add_error('file', 'This field is required')
        elif not file.name.endswith('.csv'):
            self.add_error('file', 'Only csv file allowed')

        return cleaned_data


class AddressBallotRegisterForm(forms.ModelForm):
    class meta:
        model = AddressBallotRegister
        fields = '__all__'
