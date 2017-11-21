from wtforms import Form, TextField

class SearchForm(Form):
    autocomp = TextField('Insert City', id='location-search-autocomplete')