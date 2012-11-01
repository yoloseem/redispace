""":mod:`redispace.version` --- Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

#: (:class:`tuple`) The version numbers.
VERSION_NUMERIC = (0, 1, 1)


#: (:class:`str`) The version string.
VERSION = '{0}.{1}.{2}'.format(*VERSION_NUMERIC)


if __name__ == '__main__':
    print VERSION
