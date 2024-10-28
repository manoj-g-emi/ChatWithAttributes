import os
from typing import Union

from promptflow.core import tool
from promptflow.connections import CognitiveSearchConnection


@tool
def setup_ai_search(connection: CognitiveSearchConnection, config: dict):
    if not connection or not config:
        return

    if isinstance(connection, CognitiveSearchConnection):
        os.environ["AZURE_SEARCH_ENDPOINT"] = connection.api_base
        os.environ["AZURE_SEARCH_API_KEY"] = connection.api_key
        print(connection.api_key)   

    for key in config:
        os.environ[key] = str(config[key])

    return "Ready"
