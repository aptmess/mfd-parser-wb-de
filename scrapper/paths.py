DIV = "div[@class='mfd-post-top']"
DIV_0 = DIV + "/div[@class='mfd-post-top-0']"
DIV_1 = DIV + "/div[@class='mfd-post-top-1']"
DIV_2 = DIV + "/div[@class='mfd-post-top-2']"
DIV_0_LINK = DIV_0 + "/a[@class='mfd-poster-link']"
DIV_0_ANONYMOUS = DIV_0 + "/a[@class='mfd-anonymous-link']"


class POSTLinks:
    post_id = 'table/' + "/button[@class='mfd-button-attention']" + '/@data-id'
    is_post_deleted = 'table/' + "/div[@class='mfd-post-remark']" + '/text()'
    created_at = DIV_1 + "/a[@class='mfd-post-link']" + '/text()'
    post_rating = DIV_2 + '/span' + '/text()'
    answered_posts_ids_path = (
        'table/'
        + "/div[@class='mfd-post-text']"
        + '/blockquote'
        + "/div[@class='mfd-quote-info']"
        + '/a[2]'
        + '/@href'
    )
    post_text = (
        'table/'
        + "/div[@class='mfd-post-text']"
        + "/div[@class='mfd-quote-text']"
    )


class AUTHORLinks:
    author_id = DIV_0_LINK + '/@title'
    author_name = DIV_0_LINK


class AnonymousAuthorLinks:
    author_id = DIV_0_ANONYMOUS + '/@title'
    author_name = DIV_0_ANONYMOUS + '/text()'
