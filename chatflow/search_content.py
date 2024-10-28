
from promptflow import tool
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(is_env_ready: str, question: str) -> list:
    if is_env_ready == "Ready":
        service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        index_name = "azureblob-index"
        search_client = SearchClient(endpoint=service_endpoint,index_name= index_name,credential= AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY")))
        context = search_client.search(search_text=question, select=["Attribute_Groups","Attributes","Count2","Count1","Growth","Country"], top=5)
        grounded_context = []
        for result in context:
            result.pop("@search.score")
            result.pop("@search.reranker_score")
            result.pop("@search.highlights")
            result.pop("@search.captions")
            grounded_context.append(result)
        return grounded_context
    else:
        raise Exception("Environment is not ready")