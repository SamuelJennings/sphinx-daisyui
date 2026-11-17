Body
====

Salt & <pepper>
---------------

.. list-table:: Fish & <chips> *one*
   :header-rows: 1

   * - Fish
     - Chips
   * - cod
     - thick

.. list-table::

   * - plain
     - table

.. list-table:: Outer
   :header-rows: 1

   * - Cell
     - Holds a table
   * - one
     - .. list-table:: Inner

          * - inner
            - cell

.. list-table:: *Only markup*
   :header-rows: 0

   * - markup
     - only

Equations
---------

.. math::
   :label: eq-one

   a^2 + b^2 = c^2

.. math::

   e^{i\pi} + 1 = 0

Inline :math:`x` stays inline.

Quotations
----------

   A first quotation.

   -- Ada

..

   A second quotation.

   --  Grace

..

   A third quotation.

   — Alan

Admonitions
-----------

.. note:: A note.
.. warning:: A warning.
.. tip:: A tip.
.. hint:: A hint.
.. important:: Important.
.. caution:: Caution.
.. attention:: Attention.
.. danger:: Danger.
.. error:: An error.
.. seealso:: Somewhere else.
.. todo:: Something to do.

.. admonition:: A custom title

   Generic body.

.. admonition:: Another one
   :class: something-unknown

   Unknown class.

.. versionadded:: 1.0
   Added.

.. versionchanged:: 1.1
   Changed.

.. deprecated:: 1.2
   Deprecated.

.. versionremoved:: 2.0
   Removed.

Figures
-------

.. figure:: pixel.svg

   A figure & its caption

API
---

.. autofunction:: sample.greet

.. autoclass:: sample.Thing
   :members:
