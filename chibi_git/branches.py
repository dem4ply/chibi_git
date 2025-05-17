from chibi_git.obj import Branch
from chibi_git.command import Git


class Branches:
    def __init__( self, repo ):
        self.repo = repo

    def __repr__( self ):
        return (
            f"Branches( repo={repo} )"
        )

    @property
    def local( self ):
        branches = Git.branch( src=self.repo.path ).run()
        result = map( lambda x: Branch( self.repo, x ), branches.result )
        return list( result )

    @property
    def remote( self ):
        branches = Git.branch( remote=True, src=self.repo.path ).run()
        result = map( lambda x: Branch( self.repo, x ), branches.result )
        return Branches_remote( result )

    def __iter__( self ):
        return iter( self.local )


class Branches_remote( list ):
    @property
    def origin( self ):
        return Branches_remote( self._get_without_prefix( 'origin' ) )

    def _get_without_prefix( self, prefix ):
        for branch in self:
            if branch.name.startswith( 'origin' ):
                name = branch.name.replace( 'origin/', '', 1 )
                yield Branch( repo=branch.repo, name=name )
