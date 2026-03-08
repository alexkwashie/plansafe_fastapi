from typing import Any, List


def paginated_response(data: List[Any], total: int, page: int, per_page: int) -> dict:
    return {
        "data": data,
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total,
        },
    }
