from scripts.deploy.escrow.deploy_new import main as deploy
import config.config_escrow as config
import pytest
from helpers.time import get_current_timestamp, get_future_timestamp_in_secs


@pytest.fixture(scope="session")
def escrow_contract():
    print("deploy escrow_contract")

    app_id = deploy(
        config.account_a_address,
        config.account_a_mnemonic,
        config.account_b_address,
        config.account_c_address,
        config.escrow_payment_1,
        config.escrow_payment_2,
        config.total_price,
        int(get_current_timestamp()),
        int(get_future_timestamp_in_secs(60)),
        int(get_future_timestamp_in_secs(240)),
        int(get_future_timestamp_in_secs(360)),
        False,  # True, -> ENABLE_TIME_CHECKS
    )
    yield app_id
