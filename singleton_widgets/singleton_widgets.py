# -*- coding: utf-8 -*-
r"""
IPywidgets with simple additional features to serve as singleton units to larger widgets.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from traitlets import HasTraits, Int, Unicode
from ipywidgets import Button, Combobox, Dropdown, HTML, HTMLMath, Text, Textarea, ToggleButton, register
JS_VERSION = '0.7.8'


class Singleton(HasTraits):
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
class ButtonSingleton(Button, Singleton):
    """Button with tooltip and focus."""
    _model_name = Unicode('ButtonSingletonModel').tag(sync=True)
    _model_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _model_module_version = Unicode(JS_VERSION).tag(sync=True)
    _view_name = Unicode('ButtonSingletonView').tag(sync=True)
    _view_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _view_module_version = Unicode(JS_VERSION).tag(sync=True)


@register
class ComboboxSingleton(Combobox, Singleton):
    """Combobox with tooltip and focus."""
    _model_name = Unicode('ComboboxSingletonModel').tag(sync=True)
    _model_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _model_module_version = Unicode(JS_VERSION).tag(sync=True)
    _view_name = Unicode('ComboboxSingletonView').tag(sync=True)
    _view_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _view_module_version = Unicode(JS_VERSION).tag(sync=True)


@register
class DropdownSingleton(Dropdown, Singleton):
    """Dropdown with tooltip and focus."""
    _model_name = Unicode('DropdownSingletonModel').tag(sync=True)
    _model_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _model_module_version = Unicode(JS_VERSION).tag(sync=True)
    _view_name = Unicode('DropdownSingletonView').tag(sync=True)
    _view_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _view_module_version = Unicode(JS_VERSION).tag(sync=True)


@register
class HTMLSingleton(HTML, Singleton):
    """HTML Math widget with tooltip and focus."""
    _model_name = Unicode('HTMLSingletonModel').tag(sync=True)
    _model_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _model_module_version = Unicode(JS_VERSION).tag(sync=True)
    _view_name = Unicode('HTMLSingletonView').tag(sync=True)
    _view_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _view_module_version = Unicode(JS_VERSION).tag(sync=True)


@register
class HTMLMathSingleton(HTMLMath, Singleton):
    """HTML Math widget with tooltip and focus."""
    _model_name = Unicode('HTMLMathSingletonModel').tag(sync=True)
    _model_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _model_module_version = Unicode(JS_VERSION).tag(sync=True)
    _view_name = Unicode('HTMLMathSingletonView').tag(sync=True)
    _view_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _view_module_version = Unicode(JS_VERSION).tag(sync=True)


@register
class TextSingleton(Text, Singleton):
    """Input text with tooltip and focus."""
    _model_name = Unicode('TextSingletonModel').tag(sync=True)
    _model_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _model_module_version = Unicode(JS_VERSION).tag(sync=True)
    _view_name = Unicode('TextSingletonView').tag(sync=True)
    _view_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _view_module_version = Unicode(JS_VERSION).tag(sync=True)


@register
class TextareaSingleton(Textarea, Singleton):
    """Text area with tooltip and focus."""
    _model_name = Unicode('TextareaSingletonModel').tag(sync=True)
    _model_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _model_module_version = Unicode(JS_VERSION).tag(sync=True)
    _view_name = Unicode('TextareaSingletonView').tag(sync=True)
    _view_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _view_module_version = Unicode(JS_VERSION).tag(sync=True)


@register
class ToggleButtonSingleton(ToggleButton, Singleton):
    """Toggle button with tooltip and focus."""
    _model_name = Unicode('ToggleButtonSingletonModel').tag(sync=True)
    _model_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _model_module_version = Unicode(JS_VERSION).tag(sync=True)
    _view_name = Unicode('ToggleButtonSingletonView').tag(sync=True)
    _view_module = Unicode('sage-combinat-widgets').tag(sync=True)
    _view_module_version = Unicode(JS_VERSION).tag(sync=True)
