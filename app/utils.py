from sqids import Sqids

sqids = Sqids()


def get_short_path(url_id: int) -> str:
    return sqids.encode([url_id])


def get_id(short_path: str) -> int | None:
    num_repr = sqids.decode(short_path)

    if num_repr and len(num_repr) == 1:
        url_id = num_repr[0]

        if 0 < url_id < 2147483647:  # 2^31 - 1 (max len serial4)
            return url_id
