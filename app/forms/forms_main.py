from wtforms import Form, TextField

class SearchForm(Form):
    autocomp = TextField('Insert City', id='location-search-autocomplete')

class SearchForm2(Form):
    autocomp2 = TextField('Insert City2', id='location-search-autocomplete2')