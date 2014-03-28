"""
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

.. [1]: http://www.jasig.org/cas
"""

from __future__ import print_function
import sys
if sys.version_info.major < 3:
    py3k = False
    from urlparse import urljoin
    from urllib import urlencode
    from HTMLParser import HTMLParser
    import urllib2 as request
else:
    py3k = True
    from html.parser import HTMLParser
    from urllib import request
    from urllib.parse import urljoin, urlencode


__all__ = ['CASLoginError', 'login_to_cas_service']


class CASLoginError(Exception):
    pass


class _CASLoginParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.data = {}

    def handle_starttag(self, tag, attrs):
        if tag in ['input', 'form']:
            d = {}
            for attr_name, attr_value in attrs:
                d[attr_name] = attr_value
                if 'name' in d and 'value' in d:
                    if d['name'] not in ['username', 'password']:
                        self.data[d['name']] = d['value']
                if attr_name in ['action']:
                    self.data['action'] = attr_value


def login_to_cas_service(url, username, password, opener=None):
    """Attempt to authenticate to a CAS /login form using the provided username
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
    """

    if not opener:
        opener = request.build_opener()

    if not any( isinstance(h, request.HTTPCookieProcessor) for h in opener.handlers ):
        opener.add_handler(request.HTTPCookieProcessor())

    login_fh = opener.open(url)
    login_str = login_fh.read()

    p = _CASLoginParser()

    if py3k:
        p.feed(login_str.decode('utf8'))
    else:
        p.feed(login_str)

    action = p.data.pop('action')
    params = list(p.data.items())

    if not action:
        raise CASLoginError('Could not find a CAS login form at %s' % login_fh.url)

    action = urljoin(login_fh.url, action)

    try:
        if callable(username):
            username = username()
        if callable(password):
            password = password()
    except Exception as e:
        raise CASLoginError('username or password could not be retrieved: %s', e)

    params.append(('username', username))
    params.append(('password', password))
    data = urlencode(params, True)

    # If successful, this should redirect to the service which will validate
    # the service ticket and create a session (or something)
    if py3k:
        logged_in_fh = opener.open(action, data.encode('utf8')).read()
        if b'successfully logged' not in logged_in_fh:
            print(logged_in_fh)
            raise CASLoginError('Login error')
    else:
        logged_in_fh = opener.open(action, data).read()
        if 'successfully logged' not in logged_in_fh:
            print(logged_in_fh)
            raise CASLoginError('Login error')

    print('You have successfully logged into the Central Authentication Service.')

    return opener
