from typing import List, Dict, Optional, Tuple, Union
import re


class Documentation:
    """
    A class to manage and parse documentation data.

    Attributes
    ----------
    data : dict
        The raw data for the documentation.
    text : str
        The raw text of the documentation.
    _tags : dict of {str: list of str}
        A dictionary holding parsed data of each documentation tag type.
    _assembled : bool
        Flag to indicate if the tags have been parsed or not.

    Methods
    -------
    _initialize_tag(tag_name)
        Initialize a new tag name in the _tags dictionary.
    _append_to_current_tag(current_tag, text)
        Append text to the last entry for the current tag.
    _add_new_tag(new_tag)
        Add a new tag and initialize it with an empty string.
    _assemble_tags()
        Parse the tags and their text from the raw documentation text.

    Properties
    ----------
    dev : list of str
        Returns all 'dev' tags as a list of strings.
    notice : list of str
        Returns all 'notice' tags as a list of strings.
    params : list of tuple
        Returns 'param' tags as a list of tuples, each containing parameter name and description.
    returns : Union[str, list of tuple]
        Returns 'return' tags either as a single string or as a list of tuples.
    """

    def __init__(self, data: Optional[Union[Dict, str]]):
        """
        Initializes Documentation object with given data dictionary.

        Parameters
        ----------
        data : dict
            The raw data dictionary containing documentation.
        """
        self.data = data

        if self.data is None:
            self.text = ''
        elif isinstance(self.data, str):
            self.text = data
        else:
            self.text: str = data.get('text', '')

        self._tags: Dict[str, List[str]] = {
            'dev': [],
            'notice': [],
            'param': [],
            'return': []
        }
        self._assembled = False

    def _assemble_tags(self):
        """
        Parse the tags and their text from the raw documentation text.
        """
        if self._assembled:
            return

        current_tag = None
        lines = self.text.strip().split('\n')

        for line in lines:
            # The regex r'@(\w+)' is used to find tags in the line.
            # '@' matches the literal '@' character.
            # '(\w+)' captures one or more word characters (letters, numbers, or underscores).
            # The captured word characters will represent the tag name (e.g., "param", "return").
            match = re.search(r'@(\w+)', line)

            if match:
                current_tag = match.group(1)
                # Initialize a new tag name in the _tags dictionary if it does not exist.
                if current_tag not in self._tags:
                    self._tags[current_tag] = [""]
                else:
                    self._tags[current_tag].append("")

            if current_tag:
                # Remove the tag from the line and strip the line of leading and trailing whitespaces.
                stripped_line = re.sub(r'@' + re.escape(current_tag), '', line).strip()
                # Append text to the last entry for the current tag.
                self._tags[current_tag][-1] += " " + stripped_line

        # Trim leading and trailing whitespaces for each tag's text.
        for tag, lines in self._tags.items():
            self._tags[tag] = [line.strip() for line in lines]

        self._assembled = True

    @property
    def dev(self) -> str:
        """
        Property to get all 'dev' tags as a list of strings.

        Returns
        -------
        list of str
            A list containing all 'dev' tags.
        """
        self._assemble_tags()
        return ' '.join(self._tags.get('dev', []))

    @property
    def notice(self) -> str:
        """
        Property to get all 'notice' tags as a list of strings.

        Returns
        -------
        list of str
            A list containing all 'notice' tags.
        """
        self._assemble_tags()
        return ' '.join(self._tags.get('notice', []))

    @property
    def params(self) -> Dict[str, Union[str, List[Tuple[str, str]]]]:
        """
        Property to get 'param' tags as a dictionary.

        Returns
        -------
        Dict[str, Union[str, List[Tuple[str, str]]]]
            A dictionary containing:
                - 'parsed': A list of tuples parsed from the @param string
                - 'text': The original @param string
        """
        self._assemble_tags()
        params = ' '.join(self._tags.get('param', []))

        # Using regex to find all occurrences of the pattern in the @param string
        # The regex pattern does the following:
        # 1. (\w+): Captures one or more word characters (e.g., "str", "int").
        # 2. (.+?): Captures one or more of any character (except line terminators), but as few as possible.
        # 3. (?:\.|$): Matches either a literal period '.' or the end of the string, but doesn't capture it.
        parsed_params = re.findall(r'(\w+) (.+?)(?:\.|$)', params)

        return {'parsed': parsed_params, 'text': params}

    @property
    def returns(self) -> Dict[str, Union[str, List[Tuple[str, str]]]]:
        """
        Property to get 'return' tags as a dictionary.

        Returns
        -------
        Dict[str, Union[str, List[Tuple[str, str]]]]
            A dictionary containing:
                - 'parsed': A list of tuples parsed from the @return string
                - 'text': The original @return string
        """
        self._assemble_tags()
        returns = ' '.join(self._tags.get('return', []))

        # Using regex to find all occurrences of the pattern in the @return string
        # The regex pattern does the following:
        # 1. (\w+): Captures one or more word characters (e.g., "str", "int").
        # 2. (.+?): Captures one or more of any character (except line terminators), but as few as possible.
        # 3. (?:\.|$): Matches either a literal period '.' or the end of the string, but doesn't capture it.
        parsed_returns = re.findall(r'(\w+) (.+?)(?:\.|$)', returns)

        return {'parsed': parsed_returns, 'text': returns}
