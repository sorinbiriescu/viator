from wtforms import Form, TextField

class SearchForm(Form):
    autocomp = TextField('Insert City', id='location-search-autocomplete')

class SearchForm2(Form):
    autocomp2 = TextField('Insert City2', id='location-search-autocomplete2')

class SearchForm3(Form):
    autocomp3 = TextField('Insert City3', id='location-search-autocomplete3')