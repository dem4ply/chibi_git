import datetime
import functools
import re

from chibi.file import Chibi_path
from chibi_atlas import Chibi_atlas

from chibi_git.command import Git


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

    def __repr__( self ):
        return (
            f"{type(self)}( name={self.name}, repo={self.repo} )"
        )

    def __eq__( self, other ):
        if isinstance( other, str ):
            return self.name == other
        else:
            raise NotImplementedError(
                f"no implementado eq {self} con {other}" )


class Head( Branch ):
    @property
    def branch( self ):
        return Branch( self.repo, self.name )

    @property
    def commit( self ):
        result = Git.rev_parse(
            'HEAD', src=self.repo.path ).run()
        return Commit( self.repo, result.result )


class Remote_wrapper:
    def __init__( self, repo ):
        self.repo = repo
        self.reload()

    def reload( self ):
        names = self.repo._remote()
        self._names = Chibi_atlas()
        for n in names:
            self._names[ n ] = self.repo._remote__get_url( n )

    def append( self, name, url ):
        self.repo._remote__add( name, url )
        self.reload()

    def __bool__( self ):
        return bool( self._names )

    def __getattr__( self, name ):
        try:
            return super().__getattribute__( name )
        except AttributeError as e:
            try:
                return self._names[ name ]
            except KeyError:
                raise e


class Chibi_status_file( Chibi_path ):
    def __new__( cls, path, *args, repo=None, **kw ):
        if repo:
            path = repo._path + path
            path = path.inflate
        result = super().__new__( cls, path, *args, **kw )
        result._repo = repo
        return result

    def add( self ):
        return self._repo.add( self )
