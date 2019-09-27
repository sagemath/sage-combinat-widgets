# -*- coding: utf-8 -*-
r"""
IPywidgets with simple additional features to serve as units to larger widgets.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from traitlets import Unicode, HasTraits
from ipywidgets import Combobox, Text, Textarea, register


class Unit(HasTraits):
    """Additional features to an ipywidgets widget."""
    _focus = Unicode().tag(sync=True)

    def set_tooltip(self, s=''):
        self.description_tooltip = s

    def focus(self):
        self._focus = 'on'

    def blur(self):
        self._focus = 'off'


@register
class TextUnit(Text, Unit):
    """Input text with a help title (tooltip)."""
    _model_name = Unicode('TextUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('TextUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)


@register
class ComboboxUnit(Combobox, Unit):
    """Combobox with a help title (tooltip)."""
    _model_name = Unicode('ComboboxUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('ComboboxUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)


@register
class TextareaUnit(Textarea, Unit):
    """Text area with a help title (tooltip)."""
    _model_name = Unicode('TextareaUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('TextareaUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)
