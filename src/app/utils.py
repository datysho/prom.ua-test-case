# -*- coding: utf-8 -*-
import hashlib


def password_hash(password):
    hash = hashlib.new('ripemd160')
    try:
        hash.update(password)
        return hash.hexdigest()
    except UnicodeEncodeError:
        return False


def sifter(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]