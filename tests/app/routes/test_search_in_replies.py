from datetime import datetime

import pytest

from tests.assets import POSTS_DICT


class TestSearchPostInReplies:
    @pytest.mark.parametrize(
        ('body', 'result'),
        (
            (
                {'post_id': 2},
                {'amount': 0, 'result': []},
            ),
            (
                {'post_id': 4},
                {'amount': 1, 'result': [POSTS_DICT[5]]},
            ),
        ),
    )
    def test_clear_search(self, client_with_data, body, result):
        resp = client_with_data.post(url='/replies', json=body)
        assert resp.status_code == 200

        data = resp.json()

        for i in data['result']:
            i['post_created_at'] = datetime.strptime(
                i['post_created_at'], '%Y-%m-%dT%H:%M:%S'
            )
        assert data == result
