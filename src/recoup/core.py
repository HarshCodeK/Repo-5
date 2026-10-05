from dataclasses import dataclass


@dataclass(frozen=True)
class Txn:
    source: str
    reference: str
    amount_paise: int
    timestamp: int


@dataclass(frozen=True)
class Match:
    left: str
    right: str
    score: float


def normalize(row: dict) -> Txn:
    amount = int(row["amount_paise"])
    if amount < 0:
        raise ValueError("negative amount")
    return Txn(
        str(row["source"]),
        str(row["reference"]).strip(),
        amount,
        int(row["timestamp"]),
    )


def match(left: list[Txn], right: list[Txn], window: int = 300) -> list[Match]:
    candidates: list[tuple[int, int, float, int]] = []
    for left_index, a in enumerate(left):
        for right_index, b in enumerate(right):
            delta = abs(a.timestamp - b.timestamp)
            if delta > window or a.amount_paise != b.amount_paise:
                continue
            score = 1.0 if a.reference and a.reference == b.reference else 0.5
            candidates.append((left_index, right_index, score, delta))

    candidates.sort(key=lambda item: (-item[2], item[3], item[0], item[1]))
    used_right: set[int] = set()
    used_left: set[int] = set()
    out: list[Match] = []

    for left_index, right_index, score, _ in candidates:
        if left_index in used_left or right_index in used_right:
            continue
        used_left.add(left_index)
        used_right.add(right_index)
        out.append(Match(left[left_index].reference, right[right_index].reference, score))

    return out


def recovery_allowed(reason: str, amount_paise: int) -> bool:
    return reason == "amount_mismatch" and 10_000 <= amount_paise <= 1_000_000
