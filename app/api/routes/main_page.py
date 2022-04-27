from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Query, Session

from app.core.engine import get_session
from app.core.models import Post, Topic
from app.core.utils import get_and_check_total_pages, get_size
from app.schemas.input_schemas import (
    Pagination,
    SearchByReplies,
    SearchByTextInputModel,
    SearchByThread,
)
from app.schemas.output_schemas import PostOutput

router = APIRouter()


@cbv(router)
class MainRoutes:
    session: Session = Depends(get_session)
    page_size: int = Depends(get_size)

    def get_all_posts_pagination(
        self, body: Pagination, posts: Query
    ) -> list[PostOutput]:
        page_size = body.count or self.page_size
        page = body.page
        if page:
            total_posts = posts.count()
            posts = posts.offset((page - 1) * page_size).limit(page_size)
            get_and_check_total_pages(page, total_posts, page_size)
        else:
            posts = posts.limit(page_size)
        all_posts = [u.__dict__ for u in posts.all()]
        return all_posts

    @router.post('/search', response_model=list[PostOutput])
    def search_post_by_page(self, body: SearchByTextInputModel):
        """
        Эндпойнт /search для поиска постов по тексту:
            на вход в API приходит запрос с текстом и лимитом числа постов в формате {"text": "золото", "count": 1000},
            на выходе отдаются все посты (по каждому посту отдаются все доступные в БД данные) с учетом лимита (параметр count), содержащие данный текст (параметр text).

        Сортировка результатов: от самомого нового к самому старому

        Pagination: available
        """
        posts = (
            self.session.query(Post)
            .filter(Post.post_text.like(f'%{body.text}%'))
            .order_by(Post.post_created_at.desc())
        )

        return self.get_all_posts_pagination(body, posts)

    @router.post('/by_thread', response_model=list[PostOutput])
    def search_post_by_thread(self, body: SearchByThread):
        """
        Эндпойнт /by_thread для вывода постов темы:
            на вход подается id темы и лимит числа сообщений в формате {"thread_id": 114198, "count": 1000},
            на выходе отдаются посты данной темы (по каждому посту отдаются все доступные в БД данные) с учетом лимита.

        Сортировка результатов: от самомого нового к самому старому

        Pagination: available
        """
        posts = (
            self.session.query(Post)
            .join(Topic)
            .filter_by(topic_id=body.thread_id)
            .order_by(Post.post_created_at.desc())
        )
        return self.get_all_posts_pagination(body, posts)

    @router.post('/replies', response_model=list[PostOutput])
    def search_post_by_replies(self, body: SearchByReplies):
        """
        Эндпойнт /replies для поиска реплаев:
            на входе подается id поста (пример: {"post_id": 20202744})
            на выходе отдается список id постов, которые отвечали на это сообщение.

        Сортировка результатов: по возрастанию id

        Pagination: available
        """
        posts = (
            self.session.query(Post)
            .filter(Post.related_to.like(f'%{body.post_id}%'))
            .order_by(Post.post_id.asc())
        )
        return self.get_all_posts_pagination(body, posts)
