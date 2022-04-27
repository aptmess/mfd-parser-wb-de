from fastapi.exceptions import HTTPException


def get_size() -> int:
    from app.config import config

    return config.PAGE_SIZE


def get_and_check_total_pages(
    page: int, total_items: int, page_size: int
) -> bool:
    total_pages = (total_items - 1) // page_size + 1 if total_items != 0 else 1
    if page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f'Page number = {page} must be less than '
            f'total number of pages = {total_pages}',
        )
    return page < total_pages


def get_total_pages(total_items: int, page_size: int) -> int:
    total_pages = (total_items - 1) // page_size + 1 if total_items != 0 else 1

    return total_pages
