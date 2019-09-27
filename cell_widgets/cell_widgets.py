# -*- coding: utf-8 -*-
r"""
IPywidgets with simple additional features to serve as elements for larger widgets.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from traitlets import Unicode
from ipywidgets import Combobox, Text, Textarea, register

@register
class TextWithTooltip(Text):
    """Input text with a help title (tooltip)."""
    _view_name = Unicode('TextWithTooltipView').tag(sync=True)
    _view_module = Unicode('cell-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)
    description_tooltip = Unicode().tag(sync=True)

    def set_tooltip(self, s=''):
        self.description_tooltip = s


@register
class ComboboxWithTooltip(Combobox):
    """Combobox with a help title (tooltip)."""
    _view_name = Unicode('ComboboxWithTooltipView').tag(sync=True)
    _view_module = Unicode('cell-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)
    description_tooltip = Unicode().tag(sync=True)

    def set_tooltip(self, s=''):
        self.description_tooltip = s


@register
class TextareaWithTooltip(Textarea):
    """Text area with a help title (tooltip)."""
    _view_name = Unicode('TextareaWithTooltipView').tag(sync=True)
    _view_module = Unicode('cell-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.7.6').tag(sync=True)
    description_tooltip = Unicode().tag(sync=True)

    def set_tooltip(self, s=''):
        self.description_tooltip = s
