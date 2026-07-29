import pytest
from data_structures.sequence import Sequence

# a helper for this only, because in the real program sequences will be created uniquely.
def make_sequence(commands):
    seq = Sequence()
    seq.commands = list(commands)
    return seq


class TestGetNext:
    def test_returns_commands_in_order(self):
        seq = make_sequence(["A", "B", "C"])
        assert seq.get_next() == "A"
        assert seq.get_next() == "B"
        assert seq.get_next() == "C"

    def test_advances_completed_counter(self):
        seq = make_sequence(["A", "B"])
        assert seq.completed == 0
        seq.get_next()
        assert seq.completed == 1
        seq.get_next()
        assert seq.completed == 2

    def test_returns_none_when_exhausted(self):
        seq = make_sequence(["A"])
        seq.get_next()
        assert seq.get_next() is None

    def test_calling_past_end_repeatedly_stays_none(self):
        seq = make_sequence(["A"])
        seq.get_next()
        assert seq.get_next() is None
        assert seq.get_next() is None
        # completed shouldn't run away past len(commands)
        assert seq.completed == 1

    def test_empty_sequence_returns_none_immediately(self):
        seq = make_sequence([])
        assert seq.get_next() is None


class TestIsComplete:
    def test_false_at_start_with_commands(self):
        seq = make_sequence(["A", "B"])
        assert seq.is_complete() is False

    def test_true_once_all_consumed(self):
        seq = make_sequence(["A", "B"])
        seq.get_next()
        seq.get_next()
        assert seq.is_complete() is True

    def test_true_for_empty_sequence(self):
        seq = make_sequence([])
        assert seq.is_complete() is True

    def test_false_partway_through(self):
        seq = make_sequence(["A", "B", "C"])
        seq.get_next()
        assert seq.is_complete() is False


class TestRetry:
    def test_retry_with_no_args_reissues_last_command(self):
        seq = make_sequence(["A", "B", "C"])
        seq.get_next()  # A, completed -> 1
        seq.get_next()  # B, completed -> 2
        result = seq.retry()
        assert result == "B"

    def test_retry_resets_completed_to_reissued_index(self):
        seq = make_sequence(["A", "B", "C"])
        seq.get_next()
        seq.get_next()
        seq.retry()
        # after retrying B, completed should reflect that B was just re-handed-out
        assert seq.completed == 2
        assert seq.get_next() == "C"

    def test_retry_with_explicit_index(self):
        seq = make_sequence(["A", "B", "C"])
        seq.get_next()
        seq.get_next()
        seq.get_next()
        result = seq.retry(index=0)
        assert result == "A"
        assert seq.completed == 1

    def test_retry_does_not_increment_retry_count(self):
        # retry() is for re-issuing a single command; retry_count is tracked by restart()
        seq = make_sequence(["A", "B"])
        seq.get_next()
        seq.retry()
        assert seq.retry_count == 0

    def test_retry_immediately_after_start_uses_index_minus_one(self):
        # completed=0, so index defaults to -1, which re-fetches the last item (wrap-around).
        # This documents current behavior; flag if this isn't the intended semantics.
        seq = make_sequence(["A", "B", "C"])
        result = seq.retry()
        assert result == seq.commands[-1]


class TestRestart:
    def test_restart_defaults_to_index_zero(self):
        seq = make_sequence(["A", "B", "C"])
        seq.get_next()
        seq.get_next()
        seq.restart()
        assert seq.completed == 0
        assert seq.get_next() == "A"

    def test_restart_from_specific_index(self):
        seq = make_sequence(["A", "B", "C", "D"])
        seq.get_next()
        seq.get_next()
        seq.get_next()
        seq.restart(index=2)
        assert seq.completed == 2
        assert seq.get_next() == "C"

    def test_restart_increments_retry_count(self):
        seq = make_sequence(["A", "B"])
        assert seq.retry_count == 0
        seq.restart()
        assert seq.retry_count == 1
        seq.restart()
        assert seq.retry_count == 2

    def test_restart_warns_after_two_or_more_retries(self, capsys):
        seq = make_sequence(["A"])
        seq.restart()  # retry_count = 1, no warning
        captured = capsys.readouterr()
        assert "[WARNING]" not in captured.out

        seq.restart()  # retry_count = 2, should warn
        captured = capsys.readouterr()
        assert "[WARNING]" in captured.out
        assert "retried 2 times" in captured.out

    def test_restart_returns_new_retry_count(self):
        seq = make_sequence(["A"])
        assert seq.restart() == 1
        assert seq.restart() == 2


class TestFromMove:
    def test_from_move_is_not_yet_implemented(self):
        # Placeholder: from_move() is a TODO pending the mechanical team's work.
        # This test just documents current (no-op) behavior so it fails loudly
        # once the method is implemented and this test should be replaced.
        seq = Sequence()
        result = seq.from_move(move=None)
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])