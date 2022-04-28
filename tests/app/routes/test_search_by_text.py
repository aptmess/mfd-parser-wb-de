import datetime

import pytest

from tests.assets import POSTS_DICT


class TestSearchPostByPageRoute:
    @pytest.mark.parametrize(
        ('body', 'error_status_code', 'error_reason'),
        (
            (
                {'page': 'in', 'count': 10, 'text': 'добрый день'},
                422,
                'value is not a valid integer',
            ),
            (
                {'page': 1, 'count': 0, 'text': 'добрый день'},
                422,
                'ensure this value is greater than or equal to 1',
            ),
            (
                {'page': 2, 'count': 10, 'text': 'добрый день'},
                400,
                'Page number = 2 must be less than '
                'total number of pages = 1',
            ),
        ),
    )
    def test_validation_body_errors(
        self, client_with_data, body, error_status_code, error_reason
    ):
        resp = client_with_data.post(url='/search', json=body)
        assert resp.status_code == error_status_code

        data = resp.json()
        detail_message = data['detail']
        if isinstance(detail_message, list):
            assert error_reason == detail_message[0]['msg']
        else:
            assert detail_message == error_reason

    @pytest.mark.parametrize(
        ('body', 'result'),
        (
            (
                {'text': 'привет'},
                {'amount': 2, 'result': [POSTS_DICT[2], POSTS_DICT[1]]},
            ),
            (
                {'text': ''},
                {
                    'amount': 5,
                    'result': [POSTS_DICT[i] for i in [2, 5, 4, 3, 1]],
                },
            ),
            (
                {'text': '', 'count': 1},
                {'amount': 1, 'result': [POSTS_DICT[2]]},
            ),
            (
                {'text': '', 'count': 2, 'page': 2},
                {'amount': 2, 'result': [POSTS_DICT[4], POSTS_DICT[3]]},
            ),
            (
                {'text': '', 'page': 1},
                {
                    'amount': 5,
                    'result': [POSTS_DICT[i] for i in [2, 5, 4, 3, 1]],
                },
            ),
        ),
    )
    def test_clear_search(self, client_with_data, body, result):
        resp = client_with_data.post(url='/search', json=body)
        assert resp.status_code == 200

        data = resp.json()

        for i in data['result']:
            i['post_created_at'] = datetime.datetime.strptime(
                i['post_created_at'], '%Y-%m-%dT%H:%M:%S'
            )
        assert data == result
