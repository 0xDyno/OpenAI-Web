from django import forms


class SettingsFrom(forms.Form):
    openai_key = forms.CharField(max_length=100, label="OpenAI Key", required=False)


class TextGPTForm(forms.Form):
    MODELS = [
        ("text-davinci-003", "Davinci 3"),
        ("text-davinci-edit-001", "Edit"),
        ("code-davinci-002", "Davinci 2"),
        ("text-curie-001", "Curie"),
        ("text-babbage-001", "Babbage"),
        ("text-ada-001", "Ada"),
    ]
    
    model = forms.ChoiceField(choices=MODELS, label=False,
                              widget=forms.RadioSelect(attrs={"class": "default-indent"}))
    
    accuracy = forms.IntegerField(min_value=0, max_value=100, step_size=1,
                                  widget=forms.NumberInput(attrs={"type": "range"}))
    
    prompt_attrs = {"placeholder": "Enter your request here", "cols": "10", "rows": "10"}
    prompt = forms.CharField(max_length=8000, label=False,
                             widget=forms.Textarea(prompt_attrs))


class ChatGPTForm(forms.Form):
    MODELS = [
        ("gpt-4-32k", "gpt-4-32k"),
        ("gpt-4", "gpt-4"),
        ("gpt-3.5-turbo", "gpt-3.5-turbo"),
    ]
    
    model = forms.ChoiceField(choices=MODELS, label=False, widget=forms.RadioSelect(attrs={"class": "default-indent"}))
    
    prompt_attrs = {"placeholder": "Start chatting...", "cols": "10", "rows": "10",
                    "style": "text-align:left; padding:20px;"}
    prompt = forms.CharField(max_length=100000, label=False,
                             widget=forms.Textarea(prompt_attrs))


class DalleForm(forms.Form):
    SIZES = [
        ("1", "1024x1024"),
        ("2", "512x512"),
        ("3", "256x256"),
    ]
    
    size = forms.ChoiceField(choices=SIZES, label="Size:",
                             widget=forms.RadioSelect(attrs={"class": "default-indent"}))
    
    amount = forms.IntegerField(min_value=1, max_value=10, step_size=1, label="Amount:",
                                widget=forms.NumberInput(attrs={"type": "number", "class": "image_generator-amount"}))
    
    prompt_attrs = {"placeholder": "Enter your request here", "cols": "10", "rows": "10"}
    prompt = forms.CharField(widget=forms.Textarea(prompt_attrs), max_length=4000, label=False)
