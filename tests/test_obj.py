#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chibi_git.obj import Commit
from tests.test_chibi_git import Test_chibi_git_after_commit


class Test_chibi_commit( Test_chibi_git_after_commit ):
    def test_str_commit_should_return_something( self ):
        commit = list( self.repo.log() )[0]
        self.assertIsInstance( commit, Commit )
        self.assertTrue( str( commit ) )
