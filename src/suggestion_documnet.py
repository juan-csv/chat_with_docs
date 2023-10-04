if True:
    import sys
    sys.path.append("../")
import json
from src.base_llm import BaseLLM
from langchain.output_parsers import PydanticOutputParser
from pydantic import Field

from test_full_document import prompt_doc, prompt_map, prompt_reduce


class MapOutput(PydanticOutputParser):
    """Map output"""
    original_parragraph: list = Field(
        description="List of three original parragraphs")
    modified_parragraph: list = Field(
        description="List of three modified parragraphs")
    explanation: list = Field(
        description="List of three explanations of why the parragraph should be modified")


class DocumentSuggestion:
    """Document suggestion"""

    def __init__(self, splitter, base_llm, debug: bool = False) -> None:
        """Document suggestion constructor"""
        self.splitter = splitter
        self.llm = base_llm()
        self.debug = self.debug

    def build_map_reduce_chain(self):

        # Map chain
        map_chain = LLMChain(
            llm=self.llm,
            prompt=self.splitter.map_prompt,
            output_parser=MapOutput,
            output_key="suggestions",
            verbose=self.debug,
        )

    @staticmethod
    def parse_output_suggestions(response_str: str) -> list:
        """Parse output suggestions
        Args:
            response: response from the chain
        Returns:
            List of tuples with the original parragraph and the modified parragraph
            example:
            [
                ("original parragraph 1", "modified parragraph 1"),
                ("original parragraph 2", "modified parragraph 2"),
                ("original parragraph 3", "modified parragraph 3"),
            ]

        """
        response_dict = json.loads(response_str)

        original_parragraph_ls = []
        for r in response_dict['original_parragraph']:
            if type(r) == str:
                original_parragraph_ls.append(r)
            if type(r) == dict:
                if 'Original parragraph' in list(r.keys()):
                    original_parragraph_ls.append(r['Original parragraph'])
                if 'Original Parragraph' in list(r.keys()):
                    original_parragraph_ls.append(r['Original Parragraph'])

        modified_parragraph_ls = []
        for r in response_dict['modified_parragraph']:
            if type(r) == str:
                modified_parragraph_ls.append(r)
            if type(r) == dict:
                if 'Modified parragraph' in list(r.keys()):
                    modified_parragraph_ls.append(r['Modified parragraph'])
                if 'Modified Parragraph' in list(r.keys()):
                    modified_parragraph_ls.append(r['Modified Parragraph'])

        explanation_ls = []
        for r in response_dict['explanation']:
            if type(r) == str:
                explanation_ls.append(r)
            if type(r) == dict:
                if 'Explanation' in list(r.keys()):
                    explanation_ls.append(r['Explanation'])
                if 'explanation' in list(r.keys()):
                    explanation_ls.append(r['explanation'])

        # join the original parragraphs and modified parragraphs as tuple
        res_parsed = {}
        res_parsed['suggestions'] = []
        for i in range(len(original_parragraph_ls)):
            res_parsed['suggestions'].append({
                'orgiginal_parragraph': original_parragraph_ls[i],
                'modified_parragraph': modified_parragraph_ls[i],
                'explanation': explanation_ls[i],
            })

        # res_parsed = list(zip(original_parragraph_ls,
            #   modified_parragraph_ls, explanation_ls))
        return res_parsed


if __name__ == '__main__':
    # Args
    path_file = "../docs_example/contract.pdf"
    debug = True
    # Parameters
    chunk_size = 1000
    chunk_overlap = 0.1
    document_variable_name = "context"
