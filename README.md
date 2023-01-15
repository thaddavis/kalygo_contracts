# TLDR

This is a production-ready POC for leveraging smart contracts to securely purchase large items such as real estate.

## Non-exhaustive overiew of project

- .vscode (for integrating this project with VSCode)
- config (contains config used by the scripts in the `scripts` folder)
- contracts (all PyTeal code resides here)
- modules (all code used by automated tests in the `tests` folder resides here)
- READMEs (documentation to assist in understanding this project)
- scripts (utility scripts for assisting with various aspects of this application - uses the `config` folder for script configuration)

  - delete_test_accounts.sh (will delete all accounts in the sandbox via `goal`)
  - generate_test_accounts.sh (will generate test accounts and prefund them with ALGO and "USDCa")
  - many other helpful scripts as well...

- tests (e2e tests for solid automated testing against the smart contract can be found here)
- build.sh (compiles the smart contract 1/2)
- compile.py (compiles the smart contract 2/2)
- pyproject.toml (python-poetry.org)
- README.md (meta, right?)

## Additional info

Refer to the various markdowns in the READMEs folder.

## Concerning the `scripts` folder

The scripts in this folder are designed to be ran via the `poetry run` command and can be configured via the `./config/config_escrow.py`

## Concerning the `tests` directory

All tests are using the code in found in the `modules` folder as helper functions. The code in the modules folder aims to use as much dependency injection as possible and all the tests are designed to be ran with the `pytest` command.

## Useful commands

- poetry run deploy
- poetry run pytest <!-- test WITHOUT console output -->
- poetry run pytest -s <!-- test with console output -->
- poetry run pytest tests/escrow_contract/test_escrow_contract.py
- poetry run pytest tests/test_counter_contract.py::Test_Counter_Contract::test_initial_state
