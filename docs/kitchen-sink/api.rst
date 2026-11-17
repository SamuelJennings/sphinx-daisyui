API reference
=============

How autodoc output is drawn: signatures on a raised strip, then their description, parameters
and return values.

.. automodule:: palette
   :members:
   :undoc-members:
   :show-inheritance:

Hand-written entries
--------------------

.. py:function:: build(source: str, *, theme: str = "light") -> None
   :no-index:

   Build the documentation at *source* with *theme*.

   :param source: The directory that holds ``conf.py``.
   :param theme: The daisyUI theme to start with.
   :raises FileNotFoundError: If *source* has no ``conf.py``.

.. option:: --theme <name>

   The daisyUI theme to build with.

.. envvar:: DAISY_PRESET

   Builds this site with a Furo or pydata-sphinx-theme configuration.

.. confval:: theme_picker
   :type: ``bool`` or ``list[str]``
   :default: ``False``

   The themes offered to the reader.
