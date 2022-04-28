from datetime import datetime

import pytest

from tests.assets import POSTS_DICT


class TestSearchPostByTopicID:
    @pytest.mark.parametrize(
        ('body', 'result'),
        (
            (
                {'thread_id': 3},
                {'amount': 0, 'result': []},
            ),
            (
                {'thread_id': 1},
                {'amount': 2, 'result': [POSTS_DICT[2], POSTS_DICT[1]]},
            ),
            (
                {'thread_id': 2},
                {
                    'amount': 3,
                    'result': [POSTS_DICT[5], POSTS_DICT[4], POSTS_DICT[3]],
                },
            ),
        ),
    )
    def test_clear_search(self, client_with_data, body, result):
        resp = client_with_data.post(url='/by_thread', json=body)
        assert resp.status_code == 200

        data = resp.json()

        for i in data['result']:
            i['post_created_at'] = datetime.strptime(
                i['post_created_at'], '%Y-%m-%dT%H:%M:%S'
            )
        assert data == result
