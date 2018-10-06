from iconservice import *

TAG = 'PollingScore'


class PollingScore(IconScoreBase):
    _VOTE_YES = "VOTE_YES"
    _VOTE_NO = "VOTE_NO"
    _VOTE_TRACK = "VOTE_TRACK"

    @eventlog(indexed=1)
    def Vote(self, _by: Address, _vote: int):
        pass

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._vote_talley_yes = VarDB(self._VOTE_YES, db, value_type=int)
        self._vote_talley_no = VarDB(self._VOTE_NO, db, value_type=int)
        self._voteMapping = DictDB(self._VOTE_TRACK, db, value_type=int)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    @external
    def vote(self, _vote: int):

        # make sure vote is allowed just once
        if self._voteMapping[self.msg.sender] == 0:
            self._voteMapping[self.msg.sender] = _vote
            self.Vote(self.msg.sender, _vote)
            Logger.debug(f'vote of {_vote} registered for {self.msg.sender}', TAG)
            # 1 is yes and 2 is no
            if _vote == 1:
                self._vote_talley_yes.set(self._vote_talley_yes.get() + 1)
            elif _vote == 2:
                self._vote_talley_no.set(self._vote_talley_no.get() + 1)
            else:
                Logger.debug(f'vote sent {_vote} is not valid', TAG)
                self.revert('invalid vote!')
        else:
            Logger.debug(f'already voted', TAG)
            self.revert('already voted!')

    @external(readonly=True)
    def get_vote(self) -> dict:
        result = self._voteMapping[self.msg.sender]
        Logger.debug(f'get_vote for {self.msg.sender} is {result}', TAG)
        return {'vote': result}

    @external(readonly=True)
    def get_vote_talley(self) -> dict:
        result = {"yes": self._vote_talley_yes.get(), "no": self._vote_talley_no.get()}
        Logger.debug(f'get_vote_talley {result}', TAG)
        return result
