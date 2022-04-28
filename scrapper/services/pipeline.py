import copy
from typing import Any, Dict, Tuple, Union

from scrapper.services.transformers import Transformer


class Compose:
    def __init__(
        self, transforms: list[Union[Transformer, list[Transformer]]]
    ) -> None:
        self.transforms = transforms

    def __call__(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        input_data = copy.deepcopy(data)
        result = True
        for t in self.transforms:
            if isinstance(t, Transformer):
                input_data, result = t.transform(input_data)

            elif isinstance(t, list):
                for i in t:
                    input_data, result = i.transform(input_data)
                    if result is True:
                        break
            if result is False:
                return input_data, False
        return input_data, True
