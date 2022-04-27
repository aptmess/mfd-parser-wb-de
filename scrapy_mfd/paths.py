div_post_top = "div[@class='mfd-post-top']"
div_post_top_plus_0 = div_post_top + "/div[@class='mfd-post-top-0']"
div_post_top_plus_1 = div_post_top + "/div[@class='mfd-post-top-1']"
div_post_top_plus_2 = div_post_top + "/div[@class='mfd-post-top-2']"
div_post_top_plus_0_plus_poster_link = (
    div_post_top_plus_0 + "/a[@class='mfd-poster-link']"
)
div_post_top_plus_0_anonymous = (
    div_post_top_plus_0 + "/a[@class='mfd-anonymous-link']"
)


class POSTLinks:
    post_id = "table//button[@class='mfd-button-attention']/@data-id"
    is_post_deleted = "table//div[@class='mfd-post-remark']/text()"
    created_at = div_post_top_plus_1 + "/a[@class='mfd-post-link']/text()"
    post_rating = div_post_top_plus_2 + '/span/text()'
    answered_posts_ids_path = "table//div[@class='mfd-post-text']/blockquote/div[@class='mfd-quote-info']/a[2]/@href"
    post_text = (
        "table//div[@class='mfd-post-text']/div[@class='mfd-quote-text']"
    )


class AUTHORLinks:
    author_id = div_post_top_plus_0_plus_poster_link + '/@title'
    author_name = div_post_top_plus_0_plus_poster_link


class AnonymousAuthorLinks:
    author_id = div_post_top_plus_0_anonymous + '/@title'
    author_name = div_post_top_plus_0_anonymous + '/text()'
