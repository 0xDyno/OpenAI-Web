from django import forms


class SettingsFrom(forms.Form):
    openai_key = forms.CharField(max_length=100, label="OpenAI Key", required=False)
