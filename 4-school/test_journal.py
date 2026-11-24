from journal import (
    ConsoleChannel, InMemoryJournal, Journal, LowAverageRule,
    MeanStatistics, Monitor, Notifier, Statistics,
)


class SpyChannel(ConsoleChannel):
    def __init__(self):
        self.sent = []

    def send(self, student_id, message):
        self.sent.append((student_id, message))


def test_journal_and_statistics():
    repo = InMemoryJournal()
    journal = Journal(repo)
    journal.add_grade(1, 1, 5)
    journal.add_grade(1, 1, 4)
    journal.add_grade(2, 1, 2)
    journal.add_grade(2, 1, 3)

    stats = Statistics(repo, MeanStatistics())
    assert stats.by_student() == {1: 4.5, 2: 2.5}
    assert stats.by_subject() == {1: 3.5}


def test_monitor_notifies_low_average():
    repo = InMemoryJournal()
    Journal(repo).add_grade(1, 1, 2)
    Journal(repo).add_grade(1, 1, 3)

    spy = SpyChannel()
    monitor = Monitor(
        Statistics(repo, MeanStatistics()),
        Notifier(spy, [LowAverageRule()]),
    )
    monitor.run()

    assert len(spy.sent) == 1
    assert spy.sent[0][0] == 1