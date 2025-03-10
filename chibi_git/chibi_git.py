# -*- coding: utf-8 -*-
from chibi.file import Chibi_path
from chibi_command import Result_error

from chibi_git.command import Git as Git_command
from chibi_git.exception import Git_not_initiate
from chibi_git.obj import Head, Commit
from chibi_atlas import Chibi_atlas
from .obj import Remote_wrapper, Chibi_status_file


class Git:
    def __init__( self, path ):
        if isinstance( path, str ):
            path = Chibi_path( path )
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
        prev = status.result
        result = Chibi_atlas()
        for k, v in prev.items():
            result[ k ] = list( Chibi_status_file( f, repo=self ) for f in v )
        return result

    def add( self, file ):
        if isinstance( file, Chibi_status_file ):
            relative_path = file.relative_to( self._path )
            if relative_path.startswith( '..' ):
                raise NotImplementedError(
                    f"no esta implementado {type(file)} con valor {file}, "
                    "no es tatalmente relativo al repo" )
            if relative_path.startswith( '/' ):
                raise NotImplementedError(
                    f"no esta implementado {type(file)} con valor {file}, "
                    "empieza con root" )
            Git_command.add( relative_path, src=self._path ).run()
        elif isinstance( file, Chibi_path ):
            relative_path = file.relative_to( self._path )
            if relative_path.startswith( '..' ):
                raise NotImplementedError(
                    f"no esta implementado {type(file)} con valor {file}, "
                    "no es tatalmente relativo al repo" )
            if relative_path.startswith( '/' ):
                raise NotImplementedError(
                    f"no esta implementado {type(file)} con valor {file}, "
                    "empieza con root" )
            Git_command.add( relative_path, src=self._path ).run()
        elif isinstance( file, str ):
            raise NotImplementedError(
                f"no esta implementado {type(file)} con valor {file}" )
        else:
            raise NotImplementedError(
                f"no esta implementado {type(file)} con valor {file}" )

    def commit( self, message ):
        Git_command.commit( message, src=self._path ).run()

    def reset( self, hard=False ):
        if hard:
            Git_command.reset( '--hard', src=self._path ).run()
        else:
            Git_command.reset( src=self._path ).run()

    def checkout( self ):
        Git_command.checkout( '.', src=self._path ).run()

    @property
    def is_dirty( self ):
        status = self.status
        result = bool(
            status.modified
            or status.renamed
            or status.modified
            or status.added
            or status.deleted
            or status.copied
            or status.type_change
        )
        return result

    @property
    def head( self ):
        current_branch = Git_command.rev_parse(
            '--abbrev-ref', 'HEAD', src=self._path ).run()
        branch = Head( self, current_branch.result )
        # commit = Commit( self, current_branch.result )
        return branch

    @property
    def path( self ):
        return Chibi_path( self._path )

    def log( self ):
        commit_hashs = Git_command.rev_list(
            'HEAD', src=self._path ).run().result
        yield from map( lambda x: Commit( self, x ), commit_hashs )

    def push( self, origin, branch, set_upstream=False ):
        push = Git_command.push(
            origin, branch, set_upstream=set_upstream, src=self._path )
        result = push.run()
        return bool( result )

    @property
    def remote( self ):
        result = Remote_wrapper( repo=self )
        return result

    def _remote( self ):
        remote_list = Git_command.remote( src=self._path ).run().result
        return remote_list

    def _remote__get_url( self, name ):
        return Git_command.remote__get_url( name, src=self._path ).run().result

    def _remote__add( self, name, url ):
        Git_command.remote__add( name, url, src=self._path ).run()
