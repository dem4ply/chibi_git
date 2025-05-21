#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest.mock import patch
from chibi_git.obj import Commit, Branch
from tests.test_chibi_git import (
    Test_chibi_git_after_commit,
    Test_chibi_git_with_history,
)


class Test_chibi_commit( Test_chibi_git_after_commit ):
    def test_str_commit_should_return_something( self ):
        commit = list( self.repo.log() )[0]
        self.assertIsInstance( commit, Commit )
        self.assertTrue( str( commit ) )


class Test_chibi_remote_wrapper( Test_chibi_git_after_commit ):
    def test_without_remotes_should_be_false( self ):
        remote = self.repo.remote
        self.assertFalse( remote )


class Test_branch_obj( Test_chibi_git_with_history ):
    @patch( 'chibi_git.command.Git.checkout' )
    def test_checkout_local_should_not_try_track( self, checkout ):
        branch = Branch(
            repo=self.repo, name='master', is_remote=False )
        branch.checkout()
        checkout.assert_called_once_with( 'master', src=self.repo.path )

    @patch( 'chibi_git.command.Git.checkout' )
    def test_checkout_remote_should_not_try_track( self, checkout ):
        branch = Branch(
            repo=self.repo, name='origin/master', is_remote=True )
        branch.checkout()
        checkout.assert_called_once_with(
            '--track', 'origin/master', src=self.repo.path )
