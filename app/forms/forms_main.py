from wtforms import Form, TextField,BooleanField

class SearchForm(Form):
    autocomp = TextField('Insert City', id='location-search-autocomplete')

class PoiTypeForm(Form):
    restaurant = BooleanField(label='Restaurants', id='restaurant-poi-type-checkbox')
    bar = BooleanField(label='Bar', id='bar-poi-type-checkbox')
    nightclub = BooleanField(label='Nightclub', id='nightclub-poi-type-checkbox')
    toilets = BooleanField(label='Toilet', id='toilets-poi-type-checkbox')

class SearchForm2(Form):
    autocomp2 = TextField('Insert City2', id='location-search-autocomplete2')

class SearchForm3(Form):
    autocomp3 = TextField('Insert City3', id='location-search-autocomplete3')