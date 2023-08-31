from captcha.fields import ReCaptchaField
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Row, Layout, Column
from django import forms
from blog_app.blog.models import Articles, Comment


class CreateArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Articles
        fields = ('title', 'image', 'category', 'content', 'intro', 'home_slider')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a new title', 'class': 'form-control form-control-lg form-control-rounded'}),
            'content': forms.Textarea(attrs={'placeholder': 'Draft your article', 'class': 'form-control input-field'}),
            'intro': forms.Textarea(attrs={'placeholder': 'Enter an article snippet', 'class': 'form-control form-control form-control-rounded'}),
            'home_slider': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        '''Overwrite the save method with the idea
        the article not to be submitted automatically in terms of security and SEO reasons.
        The admin should approve the article for publishing.
        '''

        instance = super().save(commit=False)
        instance.admin_approved = False
        if commit:
            instance.save()
        return instance


class UpdateArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Articles
        fields = ('title', 'category', 'content', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('category', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('content', css_class='form-group col-md-12 mb-3'),
            ),

            Row(
                Column('tags', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column(Submit('submit', "Update Article", css_class="form-control"), css_class='form-group mt-4'),
            ),
        )

        # Bllow allows auto initial value for the tags field
        self.initial['tags'] = ', '.join([tag.title for tag in self.instance.tag.all()])
    def save(self, commit=True):
        '''Overwrite the save method with the idea
        the article not to be submitted automatically in terms of security and SEO reasons.
        The admin should approve the article for publishing.
        '''

        instance = super().save(commit=False)
        instance.admin_approved = False
        if commit:
            instance.save()
        return instance


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ('name', 'email', 'content')

    captcha = ReCaptchaField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field("name",css_class="form-control"),
            Field("email",css_class="form-control"),
            Field("content",css_class="form-control mb-10"),
            Field("captcha",),
        )

        self.helper.add_input(Submit('submit', 'Submit Comment', css_class="primary-btn submit_btn"))

