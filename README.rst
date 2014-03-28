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

Example Usage
-------------

```python

from caslogin import login_to_cas_service

opener = login_to_cas_service('<url>/cas/login', username, password)

```
Note that the login function accepts callable/functions as username and password
in case you want to save encoded informations. See API below.



Contributors
------------

* Morgan Fouesneau
* Alex Yermolaev
* Leigh McCuen


References
----------

.. [1] http://www.jasig.org/cas


API
---

```python

def login_to_cas_service(url, username, password, opener=None)
    Attempt to authenticate to a CAS /login form using the provided username
    and password. Optionally update an existing OpenerDirector.

    Parameters
    ----------

    url: str
        the location of the login form

    username: str or callable
        login username
        if a callable is provided, it must take no arguments and return a
        string

    password: str or callable
        login password associated to username
        if a callable is provided, it must take no arguments and return a
        string

    opener: OpenerDirector, Optional
        custom opener (use this to do https certificate validation).

    Returns
    -------
    opener: OpenerDirector, Optional
        custom opener which will contain the authentication certificates. A
        :class:`HTTPCookieProcessor`, will be added if it does not already
        contain one.

    Raises
    ------
    :exc:`CASLoginError`
        if there was a problem parsing the login form or if username or
        password retrievel caused an exception

    :exc:`CASLoginError`
        if the form location or login result page could not be retrieved
        successfully

```
