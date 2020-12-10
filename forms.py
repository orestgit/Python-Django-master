from django.forms import ModelForm, Form, TypedChoiceField, CharField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field
from .models import Item, Identifier, IdentifierType


class SearchForm(Form):
    identifier_types = [(i.id, i.name)
                        for i in IdentifierType.objects.all()]
    identifier_types.insert(0, (0, 'Name'))
    search_property = TypedChoiceField(
        choices=identifier_types,
        coerce=int,
        empty_value=0
    )
    search_keyword = CharField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('search_property', css_class='form-helper'),
                    css_class='col-sm-6'
                ),
                Div(
                    Field('search_keyword', css_class='form-helper'),
                    css_class='col-sm-6'
                ),
                css_class='row'
            )
        )

        super(SearchForm, self).__init__(*args, **kwargs)


class ItemForm(ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'desc', 'bucket']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div('name', css_class='col-md-6'),
                Div('bucket', css_class='col-md-6'),
                css_class='row'
            ),
            Field('desc', rows=2, cols=50)
        )

        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['bucket'].required = True


class BucketItemForm(ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'desc', 'bucket']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name'),
            Field('desc', rows=2, cols=50),
            Field('bucket', type='hidden')
        )

        super(BucketItemForm, self).__init__(*args, **kwargs)


class IdentifierForm(ModelForm):

    class Meta:
        model = Identifier
        fields = ['type', 'value']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div('type', css_class='col-md-6'),
                Div('value', css_class='col-md-6'),
                css_class='row'
            )
        )

        super(IdentifierForm, self).__init__(*args, **kwargs)
