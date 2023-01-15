# Escrow v7 development

TLDR - using stablecoins makes more sense then ALGO

## Build and deploy

- ./build.sh contracts.escrow.escrow_v7.escrow_v7
- python deploy_escrow_v7.py

## Test plan is

INSPECTION START - INSPECTION END - CLOSING DATE - MOVING DATE - FREE FUNDS DATE

- Create Contract
- Send ASA Escrow #1 to contract

- Buyer can `PULL_OUT` before `INSPECTION_END` (100%)
- If Buyer DOES NOT send full payment (Escrow #1 + Escrow #2) before the `CLOSING_DATE`, then the Seller CAN withdraw funds after the `CLOSING_DATE` (100%)
- If Buyer DOES send full payment (Escrow #1 + Escrow #2) before `CLOSING_DATE`, then the Seller CAN withdraw funds after the `FREE_FUNDS_DATE` (w/ no `ARBITRATION_FLAG`) (100%)

### ### ###

- Either party can raise an `ARBITRATION_FLAG` before the `CLOSING_DATE`
- The other party who has not raised an `ARBITRATION_FLAG` can do so between the `CLOSING_DATE` and the `FREE_FUNDS` date to decide whether or not to go to court!

### ### ###

- If both Buyer/Seller raise `ARBITRATION FLAGS` after the `FREE_FUNDS_DATE`, then only the ASA Manager can withdraw funds from the contract

TIMELINE...

INSPECTION START -> INSPECTION END -> MOVING DATE -> CLOSING DATE -> FREE_FUNDS DATE

-- MOVING DATE IS FOR GUIDANCE BUT DOES NOT AFFECT FUNDS --
