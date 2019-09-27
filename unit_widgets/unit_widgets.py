# -*- coding: utf-8 -*-
r"""
IPywidgets with simple additional features to serve as units to larger widgets.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from traitlets import Unicode
from ipywidgets import Combobox, Text, Textarea, register

@register
class TextUnit(Text):
    """Input text with a help title (tooltip)."""
    _model_name = Unicode('TextUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('TextUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)
    description_tooltip = Unicode().tag(sync=True)
    focuspos = Unicode().tag(sync=True)

    def set_tooltip(self, s=''):
        self.description_tooltip = s

    def focus(self):
        self.focuspos = 'on'

    def blur(self):
        self.focuspos = 'off'


@register
class ComboboxUnit(Combobox):
    """Combobox with a help title (tooltip)."""
    _view_name = Unicode('ComboboxUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)
    description_tooltip = Unicode().tag(sync=True)

    def set_tooltip(self, s=''):
        self.description_tooltip = s


@register
class TextareaUnit(Textarea):
    """Text area with a help title (tooltip)."""
    _view_name = Unicode('TextareaUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)
    description_tooltip = Unicode().tag(sync=True)

    def set_tooltip(self, s=''):
        self.description_tooltip = s
