#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import unittest

from chibi.file.temp import Chibi_temp_path
from chibi.madness.string import generate_string

from chibi_git import Git
from chibi_git.exception import Git_not_initiate
from chibi_git.obj import Branch, Commit


class Test_chibi_git_not_init( unittest.TestCase ):
    def setUp(self):
        self.path = Chibi_temp_path()
        self.repo = Git( self.path )

    def test_should_work(self):
        self.assertTrue( self.path.exists )
        self.assertTrue( self.repo )

    def test_status_when_not_have_git_should_raise_exception( self ):
        with self.assertRaises( Git_not_initiate ):
            self.repo.status


class Test_chibi_git( unittest.TestCase ):
    def setUp(self):
        self.path = Chibi_temp_path()
        self.repo = Git( self.path )
        self.repo.init()

    def test_should_work(self):
        self.assertTrue( self.path.exists )
        self.assertTrue( self.repo )
        self.assertTrue( self.repo.status )

    def test_status_should_return_untrack_files(self):
        self.path.temp_file()
        self.path.temp_file()
        self.path.temp_file()

        self.assertEqual( len( self.repo.status.untrack ), 3 )
        self.assertEqual( len( self.repo.status.modified ), 0 )

    def test_status_should_have_modifed_file( self ):
        file = self.path.temp_file()
        self.repo.add( file )
        self.repo.commit(
            "test_status_should_have_modifed_file" )
        file.open().append( generate_string() )
        status = self.repo.status
        self.assertTrue( status.modified )

    def test_status_modified_should_only_have_the_file( self ):
        file = self.path.temp_file()
        self.repo.add( file )
        self.repo.commit(
            "test_status_should_have_modifed_file" )
        file.open().append( generate_string() )
        status = self.repo.status
        self.assertFalse( status.modified[0].startswith( 'M ' ) )

    def test_is_dirty_should_return_true_when_modified_files( self ):
        file = self.path.temp_file()
        self.repo.add( file )
        self.repo.commit(
            "test_is_dirty_should_return_true_when_modified_files" )
        file.open().append( generate_string() )
        self.assertTrue( self.repo.is_dirty )


class Test_chibi_git_after_commit( unittest.TestCase ):
    def setUp(self):
        self.path = Chibi_temp_path()
        self.repo = Git( self.path )
        self.repo.init()
        self.file = self.path.temp_file()
        self.repo.add( self.file )
        self.repo.commit( "init" )

    def test_test_rename_file_should_be_returned_on_status( self ):
        new_file = self.file.base_name
        new_file = new_file[1:]
        new_file = self.file.dir_name + new_file
        self.file.move( new_file )
        self.repo.add( self.file )
        self.repo.add( new_file )
        self.assertTrue( self.repo.status.renamed )


class Test_chibi_git_head( Test_chibi_git_after_commit ):
    def test_repo_should_have_head( self ):
        self.assertTrue( self.repo.head )

    def test_repo_head_the_branch_is_aiming_head( self ):
        self.assertIsInstance( self.repo.head, Branch )

    def test_repo_head_should_have_name( self ):
        self.assertEqual( self.repo.head.name, 'master' )


class Test_chibi_git_commit( Test_chibi_git_after_commit ):
    def test_head_should_have_commits( self ):
        self.assertTrue( self.repo.head.commit )

    def test_commit_should_be_a_commit( self ):
        self.assertIsInstance( self.repo.head.commit, Commit )

    def test_commit_should_have_author( self ):
        self.assertTrue( self.repo.head.commit.author )

    def test_commit_should_have_date( self ):
        self.assertTrue( self.repo.head.commit.date )
        self.assertIsInstance( self.repo.head.commit.date, datetime.datetime )

    def test_commit_should_have_message( self ):
        self.assertTrue( self.repo.head.commit.message )
