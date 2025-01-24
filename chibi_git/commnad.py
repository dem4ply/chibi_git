from chibi_command import Command, Command_result
from chibi_atlas import Chibi_atlas
from chibi.file import Chibi_path


class Status_result( Command_result ):
    def parse_result( self ):
        lines = self.result.split( '\n' )
        lines = list( map( str.strip, lines ) )
        #files = lines[1:]
        result = Chibi_atlas()
        untrack = list( filter( lambda x: x.startswith( "??" ), lines ) )
        modified = list( filter( lambda x: x.startswith( "M" ), lines ) )
        result.untrack = untrack
        result.modified = modified
        self.result = result


class Git( Command ):
    command = 'git'
    captive = True

    @classmethod
    def rev_parse( cls, src=None ):
        command = cls._build_command( 'rev-parse', src=src )
        return command

    @classmethod
    def init( cls, src=None ):
        command = cls._build_command( 'init', src=src )
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
