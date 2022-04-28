import contextlib


def parametrized_repr(parametrized_value):
    return repr(parametrized_value)


@contextlib.contextmanager
def raise_nothing():
    yield
