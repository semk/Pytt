# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by Petru Paler

import logging
import sys


decode_func = {}
encode_func = {}
valid_chars = '0123456789.-+eE'


class BTFailure(Exception):
    pass


class Bencached(object):

    __slots__ = ['bencoded']

    def __init__(self, s):
        self.bencoded = s


def bdecode(x):
    logging.debug('bdecode({})'.format(x))
    try:
        r, l = decode_func[x[0]](x, 0)
    except (IndexError, KeyError, ValueError):
        raise BTFailure("not a valid bencoded string")
    if l != len(x):
        raise BTFailure("invalid bencoded value (data after valid prefix)")
    return r


def bencode(x):
    def _to_bytes(x):
        if isinstance(x, bytes):
            return x
        else:
            return str(x).encode('utf-8')
    logging.debug('bencode({})'.format(x))
    r = []
    encode_func[type(x)](x, r)
    return b''.join(map(_to_bytes, r))


def decode_int(x, f):
    f += 1
    newf = x.index('e', f)
    n = int(x[f:newf])
    if x[f] == '-':
        if x[f + 1] == '0':
            raise ValueError
    elif x[f] == '0' and newf != f+1:
        raise ValueError
    return (n, newf + 1)


def assert_finite(n):
    """Raises ValueError if n is NaN or infinite."""

    if translate(repr(n)) != '':
        raise ValueError('encountered NaN or infinite')


def decode_float(x, f):
    f += 1
    newf = x.index('e', f)
    try:
        n = float(x[f:newf].replace('E', 'e'))
        assert_finite(n)
    except (OverflowError, ValueError):
        raise ValueError('encountered NaN or infinite')

    return (n, newf + 1)


def decode_string(x, f):
    colon = x.index(':', f)
    n = int(x[f:colon])
    if x[f] == '0' and colon != f+1:
        raise ValueError
    colon += 1
    return (x[colon:colon+n], colon+n)


def decode_list(x, f):
    r, f = [], f + 1
    while x[f] != 'e':
        v, f = decode_func[x[f]](x, f)
        r.append(v)
    return (r, f + 1)


def decode_dict(x, f):
    r, f = {}, f + 1
    while x[f] != 'e':
        k, f = decode_string(x, f)
        r[k], f = decode_func[x[f]](x, f)
    return (r, f + 1)


def encode_bencached(x, r):
    r.append(x.bencoded)


def encode_int(x, r):
    r.extend(('i', x, 'e'))


def encode_float(x, r):
    r.extend(('f', repr(x).replace('e', 'E'), 'e'))


def encode_bool(x, r):
    encode_int(int(bool(x)), r)


def encode_string(x, r):
    r.extend((len(x), ':', x))


def encode_list(x, r):
    r.append(b'l')
    for i in x:
        encode_func[type(i)](i, r)
    r.append(b'e')


def encode_dict(x, r):
    r.append(b'd')
    for k, v in sorted(x.items()):
        r.extend((str(len(k)), b':', k))
        encode_func[type(v)](v, r)
    r.append(b'e')


encode_func = {
    Bencached: encode_bencached,
    int: encode_int,
    float: encode_float,
    str: encode_string,
    list: encode_list,
    tuple: encode_list,
    dict: encode_dict,
    bool: encode_bool,
}


decode_func = {
    'l': decode_list,
    'd': decode_dict,
    'i': decode_int,
    'f': decode_float,
    '0': decode_string,
    '1': decode_string,
    '2': decode_string,
    '3': decode_string,
    '4': decode_string,
    '5': decode_string,
    '6': decode_string,
    '7': decode_string,
    '8': decode_string,
    '9': decode_string,
}


if sys.version_info >= (3, 0):
    encode_func[bytes] = encode_string

    def translate(value):
        return value.translate(str.maketrans('', '', valid_chars))
else:
    encode_func[unicode] = encode_string
    import string

    def translate(value):
        return value.translate(string.maketrans('', ''), valid_chars)
