#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from chibi.file.temp import Chibi_temp_path

from chibi_git import Git
from chibi_git.snippets import get_base_name_from_git_url


class Test_chibi_git_clone( unittest.TestCase ):
    def setUp(self):
        self.path = Chibi_temp_path()
        self.url_git = 'git@github.com:dem4ply/chibi_git.git'

    def test_clone_should_get_the_repo( self ):
        repo = Git.clone( self.url_git, self.path )
        self.assertIsInstance( repo, Git )
        self.assertTrue( repo.has_git )


class Test_snippet_clone( unittest.TestCase ):
    def setUp(self):
        self.url_git = 'git@github.com:dem4ply/chibi_git.git'

    def test_clone_should_get_the_repo( self ):
        result = get_base_name_from_git_url( self.url_git )
        self.assertEqual( 'chibi_git', result )
