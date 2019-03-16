Welcome to brunns-row's documentation!
======================================

Convenience wrapper for DB API and csv.DictReader rows, and similar,
inspired by Greg Stein’s lovely `dtuple module`_.

.. _dtuple module: https://code.activestate.com/recipes/81252-using-dtuple-for-flexible-query-result-access/

.. toctree::
   :maxdepth: 2
   :caption: Contents:

      API <api.rst>

Installation
------------

Install from `Pypi <https://pypi.org/project/brunns-row/>`_ as usual, using pip , `tox`_, or ``setup.py``.

.. _tox: https://tox.readthedocs.io

Usage
-----

The basic approach is to create a wrapper object from some kind of
description - typically a `DBAPI cursor`_\ ’s `description`_, or a
`csv.DictReader`_\ ’s `fieldnames`_ attribute - then to use the
wrapper’s ``wrap(row)`` method to wrap each row. ``wrap(row)`` returns
an object from which you can access the row’s fields as attributes. A
couple of simple examples:

DB API
~~~~~~

.. code:: python

   cursor = conn.cursor()
   cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")
   wrapper = RowWrapper(cursor.description)
   rows = [wrapper.wrap(row) for row in cursor.fetchall()]
   for row in rows:
       print(row.kind, row.rating)

csv.DictReader
~~~~~~~~~~~~~~

.. code:: python

   reader = csv.DictReader(csv_file)
   wrapper = RowWrapper(reader.fieldnames)
   rows = [wrapper.wrap(row) for row in reader]
   for row in rows:
       print(row.kind, row.rating)

Attributes names are simply the column names where possible, converted
to valid identifiers where necessary by replacing invalid characters
with “\_”s, prefixing any leading numerics with “a\_”, and
de-duplicating where necessary by adding numeric suffixes.

.. _DBAPI cursor: https://www.python.org/dev/peps/pep-0249/#cursor-objects
.. _description: https://www.python.org/dev/peps/pep-0249/#description
.. _csv.DictReader: https://docs.python.org/3/library/csv.html#csv.DictReader
.. _fieldnames: https://docs.python.org/3/library/csv.html#csv.csvreader.fieldnames

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
