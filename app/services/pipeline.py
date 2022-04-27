import copy

from app.services.transformers import Transformer


class Compose(object):
    def __init__(self, transforms: list[Transformer]):
        self.transforms = transforms

    def __call__(self, data: dict):
        input_data = copy.deepcopy(data)
        for t in self.transforms:
            if isinstance(t, Transformer):
                input_data, result = t.transform(input_data)

            elif isinstance(t, list):
                for i in t:
                    input_data, result = i.transform(input_data)
                    print('HERE', result, input_data)
                    if result is True:
                        break
            if result is False:
                return input_data, False
        return input_data, True
