from django import forms


class InvalidTextInputWidget(forms.TextInput):
    def __init__(self):
        super().__init__(attrs={"class": "is-invalid"})
