#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chibi_git.obj import Commit, Remote_wrapper
from tests.test_chibi_git import Test_chibi_git_after_commit


class Test_chibi_commit( Test_chibi_git_after_commit ):
    def test_str_commit_should_return_something( self ):
        commit = list( self.repo.log() )[0]
        self.assertIsInstance( commit, Commit )
        self.assertTrue( str( commit ) )


class Test_chibi_remote_wrapper( Test_chibi_git_after_commit ):
    def test_without_remotes_should_be_false( self ):
        remote = self.repo.remote
        self.assertFalse( remote )
