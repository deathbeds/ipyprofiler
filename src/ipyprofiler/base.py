"""Widget bases for ``ipyprofiler``."""

import ipywidgets as W
import traitlets as T

from ipyprofiler import __ext__, __ns__, __version__

module_name = f"{__ns__}/{__ext__[0]}"
module_version = f"^{__version__}"


class IPyProfilerBase(W.Widget):
    """Base model definitions for speedscope widgets."""

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)
