#!/usr/bin/env python
# -*- coding: utf-8 -*-
class User:
    def __init__(self, email, pw_hash):
        self.email = email
        if type(pw_hash) == str:
            self.pw_hash = pw_hash.encode('utf-8')
        else:
            self.pw_hash = pw_hash
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False

    def get_id(self):
        return self.email
        pass

    def __bool__(self):
        return True
