import json
from pathlib import Path

from slither import Slither


TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
CUSTOM_COMMENTS_TEST_DATA_DIR = Path(TEST_DATA_DIR, "custom_comments")


def test_upgradeable_comments(solc_binary_path) -> None:
    solc_path = solc_binary_path("0.8.10")
    slither = Slither(Path(CUSTOM_COMMENTS_TEST_DATA_DIR, "upgrade.sol").as_posix(), solc=solc_path)
    compilation_unit = slither.compilation_units[0]
    proxy = compilation_unit.get_contract_from_name("Proxy")[0]

    assert proxy.is_upgradeable_proxy

    v0 = compilation_unit.get_contract_from_name("V0")[0]

    assert v0.is_upgradeable
    print(v0.upgradeable_version)
    assert v0.upgradeable_version == "version-0"

    v1 = compilation_unit.get_contract_from_name("V1")[0]
    assert v0.is_upgradeable
    assert v1.upgradeable_version == "version_1"


def test_contract_comments(solc_binary_path) -> None:
    comments = " @title Test Contract\n @dev Test comment"

    solc_path = solc_binary_path("0.8.10")
    slither = Slither(
        Path(CUSTOM_COMMENTS_TEST_DATA_DIR, "contract_comment.sol").as_posix(), solc=solc_path
    )
    compilation_unit = slither.compilation_units[0]
    contract = compilation_unit.get_contract_from_name("A")[0]

    assert contract.comments == comments

    # Old solc versions have a different parsing of comments
    # the initial space (after *) is also not kept on every line
    comments = "@title Test Contract\n@dev Test comment"
    solc_path = solc_binary_path("0.5.16")
    slither = Slither(
        Path(CUSTOM_COMMENTS_TEST_DATA_DIR, "contract_comment.sol").as_posix(), solc=solc_path
    )
    compilation_unit = slither.compilation_units[0]
    contract = compilation_unit.get_contract_from_name("A")[0]

    assert contract.comments == comments

    # Test with legacy AST
    comments = "@title Test Contract\n@dev Test comment"
    slither = Slither(
        Path(CUSTOM_COMMENTS_TEST_DATA_DIR, "contract_comment.sol").as_posix(),
        solc_force_legacy_json=True,
        solc=solc_path,
    )
    compilation_unit = slither.compilation_units[0]
    contract = compilation_unit.get_contract_from_name("A")[0]

    assert contract.comments == comments


def test_function_comments(solc_binary_path) -> None:
    solc_path = solc_binary_path("0.8.10")
    slither = Slither(
        Path(CUSTOM_COMMENTS_TEST_DATA_DIR, "contract_documentation.sol").as_posix(), solc=solc_path
    )

    expected_output = Path(CUSTOM_COMMENTS_TEST_DATA_DIR, "contract_documentation.json").as_posix()

    with open(expected_output, 'r') as f:
        expected_json_data = json.load(f)

    compilation_unit = slither.compilation_units[0]
    contract = compilation_unit.get_contract_from_name("A")[0]

    for function in contract.functions:
        assert function.has_documentation

        function_name = function.name
        expected_function_data = expected_json_data.get(function_name, {})

        assert function.documentation.notice == expected_function_data.get("notice", "")
        assert function.documentation.dev == expected_function_data.get("dev", "")

        param_parsed = function.documentation.params.get('parsed', {})
        actual_params = [{"name": param[0], "description": param[1]} for param in param_parsed]
        expected_params = expected_function_data.get("params", [])
        assert actual_params == expected_params

        actual_returns = function.documentation.returns
        expected_returns = expected_function_data.get('returns', '')

        if function_name == "_protected":
            return_parsed = function.documentation.returns.get('parsed', {})
            actual_returns = [{"name": param[0], "description": param[1]} for param in return_parsed]
            assert actual_returns == expected_returns
        else:
            actual_returns_text = actual_returns.get("text", "")
            assert actual_returns_text == expected_returns


def test_event_comments(solc_binary_path) -> None:
    solc_path = solc_binary_path("0.8.10")
    slither = Slither(
        Path(CUSTOM_COMMENTS_TEST_DATA_DIR, "contract_documentation.sol").as_posix(), solc=solc_path
    )

    expected_output = Path(CUSTOM_COMMENTS_TEST_DATA_DIR, "contract_documentation.json").as_posix()

    with open(expected_output, 'r') as f:
        expected_json_data = json.load(f)

    compilation_unit = slither.compilation_units[0]
    contract = compilation_unit.get_contract_from_name("A")[0]

    for event in contract.events:
        event_name = event.name
        expected_event_data = expected_json_data.get(event_name, {})

        assert event.documentation.notice == expected_event_data.get("notice", "")
        assert event.documentation.dev == expected_event_data.get("dev", "")

        params = event.documentation.params
        expected_params = expected_event_data.get("params", [])
        if event_name == "NotProtectedAsmCalled":
            actual_params_text = params.get("text", "")
            assert actual_params_text == expected_params
        else:
            params_parsed = params.get('parsed', {})
            actual_params = [{"name": param[0], "description": param[1]} for param in params_parsed]
            assert actual_params == expected_params

        actual_returns = event.documentation.returns.get("text", "")
        expected_returns = expected_event_data.get("returns", "")
        assert actual_returns == expected_returns
