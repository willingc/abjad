# -*- encoding: utf-8 -*-
from experimental import *


def test_Session___repr___01():

    session = scoremanager.core.Session(pending_user_input='foo')
    assert repr(session) == "Session(initial_pending_user_input='foo', pending_user_input='foo')"