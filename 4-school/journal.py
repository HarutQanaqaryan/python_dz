from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


# ---------- Домен ----------
@dataclass(frozen=True)
class Grade:
    student_id: int
    subject_id: int
    value: float


# ---------- Порты (абстракции) ----------
class JournalRepository(ABC):
    @abstractmethod
    def add(self, g: Grade) -> None: ...
    @abstractmethod
    def all(self) -> List[Grade]: ...


class StatisticsStrategy(ABC):
    @abstractmethod
    def by_student(self, grades: Iterable[Grade]) -> Dict[int, float]: ...
    @abstractmethod
    def by_subject(self, grades: Iterable[Grade]) -> Dict[int, float]: ...


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, student_id: int, message: str) -> None: ...


class NotificationRule(ABC):
    @abstractmethod
    def check(self, student_id: int, avg: float) -> Optional[str]: ...


# ---------- Адаптеры ----------
class InMemoryJournal(JournalRepository):
    def __init__(self) -> None:
        self._grades: List[Grade] = []

    def add(self, g: Grade) -> None:
        self._grades.append(g)

    def all(self) -> List[Grade]:
        return list(self._grades)


class MeanStatistics(StatisticsStrategy):
    def by_student(self, grades):
        acc: Dict[int, List[float]] = {}
        for g in grades:
            acc.setdefault(g.student_id, []).append(g.value)
        return {k: sum(v) / len(v) for k, v in acc.items()}

    def by_subject(self, grades):
        acc: Dict[int, List[float]] = {}
        for g in grades:
            acc.setdefault(g.subject_id, []).append(g.value)
        return {k: sum(v) / len(v) for k, v in acc.items()}


class ConsoleChannel(NotificationChannel):
    def send(self, student_id: int, message: str) -> None:
        print(f"[NOTIFY student={student_id}] {message}")


class LowAverageRule(NotificationRule):
    def __init__(self, threshold: float = 3.5) -> None:
        self.threshold = threshold

    def check(self, student_id: int, avg: float) -> Optional[str]:
        if avg < self.threshold:
            return f"Средний балл {avg:.2f} < {self.threshold}"
        return None


# ---------- Сервисы ----------
class Journal:
    def __init__(self, repo: JournalRepository) -> None:
        self._repo = repo

    def add_grade(self, student_id: int, subject_id: int, value: float) -> None:
        self._repo.add(Grade(student_id, subject_id, value))

    def grades(self) -> List[Grade]:
        return self._repo.all()


class Statistics:
    def __init__(self, repo: JournalRepository, strategy: StatisticsStrategy) -> None:
        self._repo = repo
        self._strategy = strategy

    def by_student(self) -> Dict[int, float]:
        return self._strategy.by_student(self._repo.all())

    def by_subject(self) -> Dict[int, float]:
        return self._strategy.by_subject(self._repo.all())


class Notifier:
    def __init__(self, channel: NotificationChannel, rules: List[NotificationRule]) -> None:
        self._channel = channel
        self._rules = rules

    def process(self, student_id: int, avg: float) -> None:
        for rule in self._rules:
            msg = rule.check(student_id, avg)
            if msg:
                self._channel.send(student_id, msg)


class Monitor:
    def __init__(self, stats: Statistics, notifier: Notifier) -> None:
        self._stats = stats
        self._notifier = notifier

    def run(self) -> None:
        for sid, avg in self._stats.by_student().items():
            self._notifier.process(sid, avg)


# ---------- Сборка ----------
if __name__ == "__main__":
    repo = InMemoryJournal()
    journal = Journal(repo)
    stats = Statistics(repo, MeanStatistics())
    monitor = Monitor(stats, Notifier(ConsoleChannel(), [LowAverageRule()]))

    journal.add_grade(1, 1, 5)
    journal.add_grade(1, 1, 4)
    journal.add_grade(2, 1, 2)
    journal.add_grade(2, 1, 3)

    print("По ученикам:", stats.by_student())
    print("По предметам:", stats.by_subject())
    monitor.run()