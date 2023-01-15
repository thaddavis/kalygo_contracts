# TLDR

This is a production-ready POC for leveraging smart contracts to securely purchase large items such as real estate.

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
