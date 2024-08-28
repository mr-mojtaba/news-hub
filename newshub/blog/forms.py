from django import forms
from .models import Comment, Post


class TicketForm(forms.Form):
    """
    Form for creating and handling ticket submissions.
    """

    # Choices for the subject field in the ticket form.
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )

    # Form fields for the ticket.
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        """
        Validates that the phone number contains only numeric characters.
        """
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن عددی نیست!')
            else:
                return phone


class CommentForm(forms.ModelForm):
    """
    Form for creating and handling comments on posts.
    """

    def clean_name(self):
        """
        Validates the name field to ensure it is at least 3 characters long.
        """
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("نام کوتاه است!")
            else:
                return name

    class Meta:
        """
        Metadata for the CommentForm.
        Specifies the model and fields to include in the form.
        """

        model = Comment
        fields = [
            'name',  # Field for the commenter's name
            'body',  # Field for the comment body
        ]

        widgets = {
            # Hides the author field from the form interface.
            'author': forms.HiddenInput(),
        }


class PostForm(forms.ModelForm):
    """
    Form for creating and updating posts.
    """

    class Meta:
        """
        Metadata for the PostForm.
        Specifies the model and fields to include in the form.
        """

        model = Post
        fields = [
            'title',
            'description',
            'slug',
            'reading_time',
        ]


class SearchForm(forms.Form):
    """
    Form for searching posts based on a query.
    """

    # Field for entering search query.
    query = forms.CharField()
