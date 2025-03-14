from django import forms
from django.contrib.auth.models import User

from .models import Inscription, Ticket, Critique, TicketFeedback


#  INSCRIPTION FORM

class InscriptionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput,
                                       label="Confirmer mot de pass")

    class Meta:
        model = Inscription
        fields = ['username', 'email', 'password']

    # validator password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'book_title', 'author', 'review_content', 'image']


# CRITIQUE PART


class CritiqueForm(forms.ModelForm):
    class Meta:
        model = Critique
        fields = ['title', 'description', 'image']


class CritiqueFeedbackForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        label="Note"
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Votre commentaire"}),
        label="Commentaire"
    )


# FOLLOW USERS AND LOGIN


class FollowUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")


# TICKET FEEDBACK
class TicketFeedbackForm(forms.ModelForm):
    class Meta:
        model = TicketFeedback
        fields = ['rating', 'comment']

    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        label="Note"
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Votre commentaire"}),
        label="Commentaire"
    )


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = TicketFeedback
        fields = ['rating', 'comment']
