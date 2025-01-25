# -*- coding: utf-8 -*-
from chibi.file import Chibi_path
from chibi_command import Result_error
from chibi_git.commnad import Git as Git_command
from chibi_git.exception import Git_not_initiate


class Git:
    def __init__( self, path ):
        self._path = path

    @property
    def has_git( self ):
        try:
            Git_command.rev_parse( src=self._path ).run()
        except Result_error as e:
            raise Git_not_initiate(
                f"repository in '{self._path}' is not initialize" ) from e
        return True

    def init( self ):
        try:
            self.has_git
            raise NotImplementedError
        except Git_not_initiate:
            Git_command.init( src=self._path ).run()

    @property
    def status( self ):
        if not self.has_git:
            raise NotImplementedError
        status = Git_command.status( src=self._path ).run()
        return status.result

    def add( self, file ):
        result = Git_command.add( file, src=self._path ).run()

    def commit( self, message ):
        result = Git_command.commit( message, src=self._path ).run()

    def reset( self ):
        raise NotImplementedError

    @property
    def is_dirty( self ):
        status = self.status
        result = bool(
            status.modified
            or status.renamed
            or status.untrack
            or status.modified
            or status.added
            or status.deleted
            or status.copied
            or status.type_change
        )
        return result

    @property
    def path( self ):
        return Chibi_path( self._path )
