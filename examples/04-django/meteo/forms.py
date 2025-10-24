from django import forms


class CityQueryForm(forms.Form):
    cities = forms.CharField(
        label="Miejscowości",
        help_text="Podaj jedną lub kilka miejscowości (oddziel przecinkami). Np. Gdynia, Warszawa",
        widget=forms.TextInput(attrs={"placeholder": "Gdynia, Warszawa"}),
    )
    include_forecast_hours = forms.IntegerField(
        label="Prognoza (godziny)", min_value=0, max_value=72, initial=12, required=False,
        help_text="Ile godzin prognozy pokazać (0 aby tylko bieżąca pogoda)."
    )
