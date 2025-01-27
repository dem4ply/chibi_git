from chibi.file import Chibi_path
from chibi_atlas import Chibi_atlas
from chibi_command import Command, Command_result


class Status_result( Command_result ):
    def parse_result( self ):
        lines = self.result.split( '\n' )
        lines = list( map( str.strip, lines ) )
        # files = lines[1:]
        result = Chibi_atlas()
        untrack = list( filter( lambda x: x.startswith( "??" ), lines ) )
        modified = list( filter( lambda x: x.startswith( "M" ), lines ) )
        renamed = list( filter( lambda x: x.startswith( "R" ), lines ) )
        added = list( filter( lambda x: x.startswith( "A" ), lines ) )
        deleted = list( filter( lambda x: x.startswith( "D" ), lines ) )
        copied = list( filter( lambda x: x.startswith( "C" ), lines ) )
        type_change = list( filter( lambda x: x.startswith( "T" ), lines ) )
        update_no_merge = list(
            filter( lambda x: x.startswith( "U" ), lines ) )
        result.untrack = untrack
        result.modified = modified
        result.renamed = renamed
        result.added = added
        result.deleted = deleted
        result.copied = copied
        result.update_no_merge = update_no_merge
        result.type_change = type_change
        self.result = result


class Rev_parse_result( Command_result ):
    def parse_result( self ):
        self.result = self.result.strip()


class Git( Command ):
    command = 'git'
    captive = True

    @classmethod
    def rev_parse( cls, *args, src=None, **kw ):
        command = cls._build_command(
            'rev-parse', *args, src=src, result_class=Rev_parse_result, **kw )
        return command

    @classmethod
    def init( cls, src=None ):
        command = cls._build_command( 'init', src=src )
        return command

    @classmethod
    def log( cls, *args, src=None, **kw ):
        command = cls._build_command( 'log', *args, src=src, **kw )
        return command

    @classmethod
    def status( cls, src=None ):
        command = cls._build_command(
            'status', '-sb', src=src, result_class=Status_result )
        return command

    @classmethod
    def add( cls, file, src=None ):
        command = cls._build_command( 'add', file, src=src, )
        return command

    @classmethod
    def commit( cls, message, src=None ):
        command = cls._build_command( 'commit', '-m', message, src=src, )
        return command

    @classmethod
    def _build_command( cls, *args, src=None, **kw ):
        if src:
            src = Chibi_path( src )
        else:
            src = Chibi_path( '.' )
        command = cls(
            f'--git-dir={src}/.git', f'--work-tree={src}',
            *args, **kw )
        return command
