==============
Python-USDOL
==============

Python wrapper for the US Dept. of Labor's `developer API <http://developer.dol.gov/>`_. 

-----
Usage
-----

Usage is straightforward.

  import python_usdol

  conn = python_usdol.Connection()
  
  data = conn.fetch_data('FAQ', 'Topic')


Where 'FAQ' and 'Topic' are the names of the targeted dataset and table within the dataset, respectively. For a full list of datasets and tables, please consult the Dept. of Labor's developer website, linked above.

In the above example, `data` will be a list of `Datum` instances. Each `Datum` instance provides access to all of the data from the dictionary object it represents, as well as some metadata about itself, using attribute syntax.

e.g. from the example: data[0].TopicID == 1, data[0].TopicValue == u'Wages & Work Hours'


-----------
Parameters
-----------

Python-USDOL has some "alpha quality" support for many of the request parameters outlined in the DOL's `API Access Guide <http://developer.dol.gov/html-req.htm>`_. These include:

  $metadata
  $top
  $skip
  $orderby

If you are looking for a way to contribute, adding the rest of the more complex filtering parameters would be an excellent starting point.

------
Future
------

Please help make this API better for everyone by reporting bugs, forking and submitting patches.
