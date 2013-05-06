import xadmin
from xadmin import views
from models import *
from xadmin.layout import *

from xadmin.plugins.inline import Inline

from .models import Country, Continent, KitchenSink, Category, City, \
    Microwave, Fridge, WysiwygEditor, ReversionedItem


class CountryInline(object):
    model = Country
    fields = ('name', 'code', 'population',)
    extra = 1
    verbose_name_plural = 'Countries (Sortable example)'


class ContinentAdmin(object):
    search_fields = ('name',)
    list_display = ('name',)
    inlines = (CountryInline,)


xadmin.site.register(Continent, ContinentAdmin)

class CityInline(object):
    model = City
    extra = 3
    verbose_name_plural = 'Cities'


class CountryAdmin(object):
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'continent', 'independence_day')
    list_filter = ('continent',)

    inlines = (CityInline,)

    form_layout = (
        TabHolder(
            Tab('General',
                Fieldset(None,
                    'name', 'continent', 'code', 'independence_day',
                    css_class='unsort no_title'
                ),
                Fieldset('Statistics',
                    'area', 'population',
                    description="EnclosedInput widget examples"
                ),
                Fieldset('Autosized textarea',
                    'description',
                    description='AutosizedTextarea widget example - adapts height '
                                'based on user input'
                ),
            ),
            Tab('Cities',
                Fieldset('Architecture',
                    'architecture',
                    description="Tabs can contain any fieldsets and inlines"
                ),
                Inline(City),
            ),
        ),
    )

xadmin.site.register(Country, CountryAdmin)


# Inlines for KitchenSink
class FridgeInline(object):
    model = Fridge
    extra = 1
    verbose_name_plural = 'Fridges (Tabular inline)'
    style = "table"


class MicrowaveInline(object):
    model = Microwave
    extra = 1
    verbose_name_plural = 'Microwaves (Stacked inline)'

# Kitchen sink model admin
class KitchenSinkAdmin(object):
    inlines = (FridgeInline, MicrowaveInline)
    search_fields = ['name']
    list_editable = ('boolean', )
    list_filter = ('choices', 'date', 'country')
    readonly_fields = ('readonly_field',)
    raw_id_fields = ('raw_id_field',)
    
    form_layout = (
        Main(
            Fieldset(None,
                'name', 'help_text', 'textfield',
                Row('multiple_in_row', 'multiple2'),
                'file', 'readonly_field',
                css_class='unsort no_title'
            ),
            Fieldset("Date and time",
                'date_widget', 'datetime_widget',
                description='Improved date/time widgets (SuitDateWidget, '
                   'SuitSplitDateTimeWidget) . Uses original JS.'
            ),
            Fieldset("Foreign key relations",
                'country', 'linked_foreign_key', 'raw_id_field',
                description="Original select and linked select feature"
            ),
            Fieldset("EnclosedInput widget",
                PrependedText('enclosed1', 'G'), 'enclosed2',
                description='Supports Twitter Bootstrap prepended, '
                    'appended inputs',
            ),
            Fieldset("Boolean and choices",
                'boolean', 'boolean_with_help', 'choices',
                'horizontal_choices', 'vertical_choices'
            ),
        ),
        Side(
            Fieldset('Collapsed settings',
                'hidden_checkbox', 'hidden_choice'
            ),
            Fieldset('And one more collapsable',
                'hidden_charfield', 'hidden_charfield2'
            ),
        )
    )
    
    list_display = (
        'name', 'help_text', 'choices', 'horizontal_choices', 'boolean')


xadmin.site.register(KitchenSink, KitchenSinkAdmin)

