import datetime
import functools
import re

from chibi_atlas import Chibi_atlas

from chibi_git.commnad import Git


class Commit:
    def __init__( self, repo, hash ):
        self.repo = repo
        self._hash = hash

    @property
    def author( self ):
        return self.info.author

    @property
    def message( self ):
        return self.info.message

    @property
    def date( self ):
        return self.info.date

    def __hash__( self ):
        return hash( self._hash )

    def get_info( self ):
        result = Git.log(
            '-n', 1, '--date=iso8601-strict', self._hash, src=self.repo.path )
        result = result.run()
        return self.parse( result.result )

    @functools.cached_property
    def info( self ):
        return self.get_info()

    def parse( self, info ):
        lines = info.split( '\n' )
        author = lines[1]
        date = lines[2]
        message = lines[4:]
        email = re.search( r'<(.*)>', author )
        author = author[ :email.span()[0] ]
        email = email.groups()[0]
        author = author.split( ':', 1 )[1].strip()
        author = Chibi_atlas( author=author, email=email )
        date = datetime.datetime.fromisoformat(
            date.split( ':', 1 )[1].strip() )
        message = map( lambda x: x.lstrip(), message )
        message = "\n".join( message )
        result = Chibi_atlas( author=author, date=date, message=message )
        return result

    def __str__( self ):
        return f"{self._hash}"


class Branch:
    def __init__( self, repo, name ):
        self.repo = repo
        self.name = name


class Head( Branch ):
    @property
    def branch( self ):
        return Branch( self.repo, self.name )

    @property
    def commit( self ):
        result = Git.rev_parse(
            'HEAD', src=self.repo.path ).run()
        return Commit( self.repo, result.result )
