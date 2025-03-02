from chibi.file import Chibi_path
from chibi_atlas import Chibi_atlas
from chibi_command import Command, Command_result


def remove_type_from_status_string( file ):
    return file.split( ' ', 1 )[1]


class Status_result( Command_result ):
    def parse_result( self ):
        lines = self.result.split( '\n' )
        lines = list( map( str.strip, lines ) )
        # files = lines[1:]
        result = Chibi_atlas()
        untrack = filter( lambda x: x.startswith( "??" ), lines )
        untrack = list( map( remove_type_from_status_string, untrack ) )
        modified = filter( lambda x: x.startswith( "M" ), lines )
        modified = list( map( remove_type_from_status_string, modified ) )
        renamed = filter( lambda x: x.startswith( "R" ), lines )
        renamed = list( map( remove_type_from_status_string, renamed ) )
        added = filter( lambda x: x.startswith( "A" ), lines )
        added = list( map( remove_type_from_status_string, added ) )
        deleted = filter( lambda x: x.startswith( "D" ), lines )
        deleted = list( map( remove_type_from_status_string, deleted ) )
        copied = filter( lambda x: x.startswith( "C" ), lines )
        copied = list( map( remove_type_from_status_string, copied ) )
        type_change = filter( lambda x: x.startswith( "T" ), lines )
        type_change = list(
            map( remove_type_from_status_string, type_change ) )
        update_no_merge = filter( lambda x: x.startswith( "U" ), lines )
        update_no_merge = list(
            map( remove_type_from_status_string, update_no_merge ) )

        result.untrack = untrack
        result.modified = modified
        result.renamed = renamed
        result.added = added
        result.deleted = deleted
        result.copied = copied
        result.update_no_merge = update_no_merge
        result.type_change = type_change
        self.result = result


class Clean_result( Command_result ):
    def parse_result( self ):
        self.result = self.result.strip()


class Rev_parse_result( Clean_result ):
    pass


class Rev_list_parse_result( Command_result ):
    def parse_result( self ):
        self.result = list(
            map( lambda x: x.strip(), self.result.strip( '\n' ) ) )


class Remote_result( Command_result ):
    def parse_result( self ):
        self.result = list( filter( bool, self.result.split( '\n' ) ) )


class Git( Command ):
    command = 'git'
    captive = True

    @classmethod
    def rev_parse( cls, *args, src=None, **kw ):
        command = cls._build_command(
            'rev-parse', *args, src=src, result_class=Rev_parse_result, **kw )
        return command

    @classmethod
    def rev_list( cls, *args, src=None, **kw ):
        command = cls._build_command(
            'rev-list', *args, src=src,
            result_class=Rev_list_parse_result, **kw )
        return command

    @classmethod
    def checkout( cls, *args, src=None, **kw ):
        command = cls._build_command(
            'checkout', *args, src=src, **kw )
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
    def push( cls, origin, branch, set_upstream=False, src=None ):
        args = []
        if set_upstream:
            args.append( '--set-upstream' )
        command = cls._build_command(
            'push', origin, branch, *args, src=src, )
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

    @classmethod
    def remote( cls, src=None ):
        command = cls._build_command(
            'remote', src=src,
            result_class=Remote_result )
        return command

    @classmethod
    def remote__get_url( cls, name, src=None ):
        command = cls._build_command(
            'remote', 'get-url', name, src=src,
            result_class=Clean_result
        )
        return command

    @classmethod
    def remote__add( cls, name, url, src=None ):
        command = cls._build_command(
            'remote', 'add', name, url, src=src,
        )
        return command
