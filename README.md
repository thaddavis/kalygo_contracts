# TLDR

This is a production-ready POC for leveraging smart contracts to securely purchase large items such as real estate.

## Additional info

Refer to the various markdowns in the READMEs folder.

## Useful commands

- poetry run deploy
- poetry run pytest <!-- test WITHOUT console output -->
- poetry run pytest -s <!-- test with console output -->
- poetry run pytest tests/counter_contract/test_counter_contract.py
- poetry run pytest tests/escrow_contract/test_escrow_contract.py
- poetry run pytest tests/test_counter_contract.py::Test_Counter_Contract
- poetry run pytest tests/test_counter_contract.py::Test_Counter_Contract::test_initial_state
