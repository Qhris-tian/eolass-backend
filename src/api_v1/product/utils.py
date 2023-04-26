from typing import List

import snakecase  # type: ignore


def sanitize_response(response: List):
    data: List = [{}] * len(response)

    for index, item in enumerate(response):
        for key, value in item.items():
            new_key = snakecase.convert(key)
            data[index][new_key] = (
                sanitize_response(item[key])
                if isinstance(item[key], list) and isinstance(item[key][0], dict)
                else item[key]
            )

    return data
