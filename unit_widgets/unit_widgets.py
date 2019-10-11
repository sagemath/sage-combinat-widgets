# -*- coding: utf-8 -*-
r"""
IPywidgets with simple additional features to serve as units to larger widgets.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from traitlets import HasTraits, Int, Unicode
from ipywidgets import Button, Combobox, Dropdown, HTMLMath, Text, Textarea, ToggleButton, register


class Unit(HasTraits):
    """Additional features to an ipywidgets widget."""
    _focus = Unicode().tag(sync=True)
    _tooltip = Unicode('').tag(sync=True) # set '' as default value
    tabindex = Int().tag(sync=True)

    def set_tooltip(self, s=''):
        self._tooltip = s

    def focus(self):
        self._focus = ''
        self._focus = 'on'

    def blur(self):
        self._focus = ''
        self._focus = 'off'

    def set_tabindex(self, i=0):
        self.tabindex = i

    def allow_focus(self):
        self.set_tabindex(0)

    def disallow_focus(self):
        self.set_tabindex(-1)


@register
class ButtonUnit(Button, Unit):
    """Button with tooltip and focus."""
    _model_name = Unicode('ButtonUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('ButtonUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)


@register
class ComboboxUnit(Combobox, Unit):
    """Combobox with tooltip and focus."""
    _model_name = Unicode('ComboboxUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('ComboboxUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)


@register
class DropdownUnit(Dropdown, Unit):
    """Dropdown with tooltip and focus."""
    _model_name = Unicode('DropdownUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('DropdownUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)


@register
class HTMLMathUnit(HTMLMath, Unit):
    """HTML Math widget with tooltip and focus."""
    _model_name = Unicode('HTMLMathUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('HTMLMathUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)


@register
class TextUnit(Text, Unit):
    """Input text with tooltip and focus."""
    _model_name = Unicode('TextUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('TextUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)


@register
class TextareaUnit(Textarea, Unit):
    """Text area with tooltip and focus."""
    _model_name = Unicode('TextareaUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('TextareaUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)


@register
class ToggleButtonUnit(ToggleButton, Unit):
    """Toggle button with tooltip and focus."""
    _model_name = Unicode('ToggleButtonUnitModel').tag(sync=True)
    _model_module = Unicode('unit-widgets').tag(sync=True)
    _model_module_version = Unicode('^0.7.6').tag(sync=True)
    _view_name = Unicode('ToggleButtonUnitView').tag(sync=True)
    _view_module = Unicode('unit-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)
