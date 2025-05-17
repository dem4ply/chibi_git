#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import datetime
import unittest

from unittest.mock import patch, Mock
from chibi.file import Chibi_path
from chibi.file.temp import Chibi_temp_path
from chibi.madness.string import generate_string

from chibi_git import Git
from chibi_git.exception import Git_not_initiate
from chibi_git.obj import Branch, Commit, Remote_wrapper


class Test_chibi_git_with_history( unittest.TestCase ):
    def setUp(self):
        self.path = Chibi_temp_path()
        self.repo = Git( self.path )
        self.repo.init()
        self.amount_commits = random.randint( 1, 20 )
        for i in range( self.amount_commits ):
            file = self.path.temp_file()
            self.repo.add( file )
            self.repo.commit( f"commit {i}" )

    def test_repo_should_have_correct_amount_of_commits( self ):
        commits = list( self.repo.log() )
        self.assertEqual( len( commits ), self.amount_commits )


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

    def test_should_work_with_repo_is_string(self):
        repo = Git( str( self.path ) )
        self.assertTrue( repo )
        self.assertTrue( repo.status )

    def test_should_work_with_dot_string(self):
        repo = Git( '.' )
        self.assertTrue( repo )
        self.assertTrue( repo.status )

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

    def test_is_dirty_should_return_false_when_only_have_untrack( self ):
        self.assertFalse( self.repo.is_dirty )
        self.path.temp_file()
        self.assertFalse( self.repo.is_dirty )

    def test_status_added_should_no_have_spaces( self ):
        self.path.temp_file()
        self.repo.status.untrack[0].add()
        self.assertEqual( len( self.repo.status.added ), 1 )
        self.assertNotIn( ' ', self.repo.status.added[0] )


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


class Test_chibi_git_push( Test_chibi_git_after_commit ):
    @patch( 'chibi_command.Popen' )
    def test_push_should_work( self, popen ):
        proccess = Mock()
        popen.return_value = proccess
        proccess.returncode = 0
        proccess.communicate.return_value = ( b"", b"" )
        self.repo.push( 'origin', 'master' )
        popen.assert_called_once()
        called_args = popen.call_args[0][0][3:]
        self.assertEqual( called_args, ( 'push', 'origin', 'master' ) )

    @patch( 'chibi_command.Popen' )
    def test_push_set_upstream_should_be_sended_in_command( self, popen ):
        proccess = Mock()
        proccess.returncode = 0
        proccess.communicate.return_value = ( b"", b"" )
        popen.return_value = proccess

        self.repo.push( 'origin', 'master', set_upstream=True )
        called_args = popen.call_args[0][0][3:]
        self.assertEqual(
            called_args, ( 'push', 'origin', 'master', '--set-upstream' ) )


class Test_chibi_git_checkout( Test_chibi_git_after_commit ):
    def test_should_work( self ):
        self.repo.checkout()

    @patch( 'chibi_git.command.Git.checkout' )
    def test_should_call_checkout_command_with_src_path( self, checkout ):
        self.repo.checkout()
        self.assertIn( 'src', checkout.call_args[1] )
        self.assertIsNotNone( checkout.call_args[1][ 'src' ] )

    def test_checkout_should_no_remove_untrack_files( self ):
        file = self.path.temp_file()
        self.repo.checkout()
        for f in self.repo.status.untrack:
            if file.base_name in str( f ):
                break
        else:
            self.fail(
                f"no se encontro {file} en {self.repo.status.untrack}" )

    def test_checkout_should_reset_changes( self ):
        file = self.path.temp_file()
        file.open().append( generate_string() )
        self.repo.add( file )
        self.repo.commit(
            "test_checkout_should_reset_changes" )
        self.assertFalse( self.repo.is_dirty )
        file.open().append( generate_string() )
        self.assertTrue( self.repo.is_dirty )
        self.repo.checkout()
        self.assertFalse( self.repo.is_dirty, "checkout no limpio el repo" )


class Test_chibi_git_remote( Test_chibi_git_after_commit ):
    def test_remote_should_be_a_remote_wrapper( self ):
        self.assertIsInstance( self.repo.remote, Remote_wrapper )

    def test_remote_should_accept_append_with_parameters( self ):
        self.assertFalse( self.repo.remote )
        self.repo.remote.append( "origin", "some_url" )
        self.assertTrue( self.repo.remote )
        self.assertEqual( self.repo.remote.origin, "some_url" )


class Test_chibi_git_status_file_obj( Test_chibi_git_after_commit ):
    def test_status_obj_should_be_a_object_like_chibi_path( self ):
        self.path.temp_file()
        self.assertEqual( len( self.repo.status.untrack ), 1 )
        self.assertIsInstance( self.repo.status.untrack[0], Chibi_path )

    def test_status_obj_can_add_himself( self ):
        file = self.path.temp_file()
        self.repo.status.untrack[0].add()
        self.assertEqual( len( self.repo.status.added ), 1 )
        self.assertEqual( self.repo.status.added[0], file )


class Test_chibi_git_branchs( Test_chibi_git_after_commit ):
    def test_repo_should_have_branchs( self ):
        self.assertTrue( self.repo.branches )

    def test_branches_should_have_local( self ):
        self.assertTrue( self.repo.branches.local )

    def test_branches_local_should_be_a_list( self ):
        self.assertIsInstance( self.repo.branches.local, dict )

    def test_master_should_be_in_branches( self ):
        self.assertIn( 'master', self.repo.branches )

    def test_master_should_be_in_branches_local( self ):
        self.assertIn( 'master', self.repo.branches.local )

    def test_can_create_a_new_brach( self ):
        self.assertNotIn( 'new_branch', self.repo.branches.local )
        self.repo.branches.create( 'new_branch' )
        self.assertIn( 'new_branch', self.repo.branches.local )

    def test_new_branch_should_have_his_commit( self ):
        self.assertNotIn( 'new_branch', self.repo.branches.local )
        branch = self.repo.branches.create( 'new_branch' )
        self.assertIsInstance( branch.commit, Commit )


class Test_create_branch( Test_chibi_git_with_history ):
    def test_can_create_branch_in_any_commit( self ):
        self.assertNotIn( 'new_branch', self.repo.branches.local )
        commits = list( self.repo.log() )
        commit = random.choice( commits )
        branch = self.repo.branches.create( 'new_branch', str( commit ) )
        self.assertEqual( branch.commit, commit )
        self.assertIsInstance( branch.commit, Commit )

    def test_can_create_branch_in_any_commit_obj( self ):
        self.assertNotIn( 'new_branch', self.repo.branches.local )
        commits = list( self.repo.log() )
        commit = random.choice( commits )
        branch = self.repo.branches.create( 'new_branch', commit )
        self.assertEqual( branch.commit, commit )
        self.assertIsInstance( branch.commit, Commit )


class Test_create_tag( Test_chibi_git_with_history ):
    def test_can_create_tag_in_any_commit( self ):
        self.assertNotIn( 'new_tag', self.repo.tags )
        commits = list( self.repo.log() )
        commit = random.choice( commits )
        tag = self.repo.tags.create( 'new_tag', str( commit ) )
        self.assertEqual( tag.commit, commit )
        self.assertIsInstance( tag.commit, Commit )

    def test_can_create_tag_in_any_commit_obj( self ):
        self.assertNotIn( 'new_tag', self.repo.tags )
        commits = list( self.repo.log() )
        commit = random.choice( commits )
        tag = self.repo.tags.create( 'new_tag', commit )
        self.assertEqual( tag.commit, commit )
        self.assertIsInstance( tag.commit, Commit )


class Test_chibi_git_branches_remote( unittest.TestCase ):
    def setUp( self ):
        self.repo = Git( '.' )

    def test_branches_should_have_remote( self ):
        self.assertTrue( self.repo.branches.remote )

    def test_branches_remote_should_have_origin( self ):
        self.assertTrue( self.repo.branches.remote.origin )

    def test_branches_remote_should_be_a_list( self ):
        self.assertIsInstance( self.repo.branches.remote, list )

    def test_branches_remote_origin_should_be_a_list( self ):
        self.assertIsInstance( self.repo.branches.remote.origin, list )

    def test_master_should_be_in_branches_remote( self ):
        self.assertIn( 'origin/master', self.repo.branches.remote )

    def test_master_should_be_in_branches_remote_origin( self ):
        self.assertIn( 'master', self.repo.branches.remote.origin )


class Test_chibi_git_tag( unittest.TestCase ):
    def setUp( self ):
        self.repo = Git( '.' )

    def test_tags_should_return_a_list( self ):
        self.assertTrue( list( self.repo.tags ) )

    def test_tags_should_have_some_version( self ):
        self.assertIn( 'v0.0.2', self.repo.tags )

    def test_tags_should_have_commits( self ):
        self.assertTrue( self.repo.tags )
        for tag in self.repo.tags:
            self.assertTrue( tag.commit )
            self.assertIsInstance( tag.commit, Commit )
