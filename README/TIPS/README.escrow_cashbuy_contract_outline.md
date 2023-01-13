# Escrow v7 development

TLDR - using stablecoins makes more sense then ALGO

## Build and deploy

- ./build.sh contracts.escrow.escrow_v7.escrow_v7
- python deploy_escrow_v7.py

## Test plan is

INSPECTION START - INSPECTION END - CLOSING DATE - MOVING DATE - FREE FUNDS DATE

- Create Contract
- Send ASA Escrow #1 to contract

- Buyer can `PULL_OUT` before `INSPECTION_END` and trigger the funds to be sent back after `INSPECTION_END`

- Buyer can raise an `ARBITRATION_FLAG` any time after the `INSPECTION_END` and before the `MOVING_DATE` date
- If only the Buyer raises `ARBITRATION_FLAG` after `FREE_FUNDS_DATE`, then Buyer can withdraw funds after `FREE_FUNDS_DATE`
   but Seller is allowed to raise `ARBITRATION_FLAG` after the `MOVING_DATE` but before `FREE_FUNDS_DATE` to involve legal process

- If Buyer DOES NOT send Escrow #2 before `CLOSING_DATE`, then Seller can cancel the contract (Buyer can no longer withdraw funds or set flags but Seller can)
- If Buyer DOES send Escrow #2 before `CLOSING_DATE`, then Seller CANNOT cancel the contract

- Seller can raise an `ARBITRATION_FLAG` any time after the `INSPECTION_END` and before the `MOVING_DATE`
- If only the Seller raises `ARBITRATION_FLAG` after `FREE_FUNDS_DATE`, then Seller can withdraw funds after the `FREE_FUNDS_DATE`
    but Buyer is allowed to raise `ARBITRATION_FLAG` after the `MOVING_DATE` but before `FREE_FUNDS_DATE` to involve legal process

- If both Buyer/Seller raise `ARBITRATION FLAGS` after the `FREE_FUNDS_DATE`, then only the ASA Manager can withdraw funds from the contract
