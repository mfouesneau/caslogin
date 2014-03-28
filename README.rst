CASLogin - Simple CAS authentication for python
===============================================

Provides a simple login interface to CAS [1]_ servers and services for python 2 and
python 3

The interface is reduced to a single function: :func:`login_to_cas_service`.
Any raised exception will be of class :class:`CASLoginError` that is also
defined in this package.


How does it work?
-----------------

CAS authentication works with a cookie. This package provide a dead simple
function that allow you to generate an OpenerDirector that takes care of
retrieving the cookie and keep it for further queries.

Custom Openers are also allowed. In this case, the code will check to make sure
that the cookiejar is instanciated or will do so prior to give it the
appropriate cookie.


Contributors
------------

* Morgan Fouesneau
* Alex Yermolaev
* Leigh McCuen


References
----------

.. [1] http://www.jasig.org/cas
