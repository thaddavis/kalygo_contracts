# Utility goal commands

## enter algod

./sandbox enter algod

## create new account

./sandbox goal account new

## fund new account

- ./sandbox goal account list
- SENDER_ACCOUNT=FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4
- RECEIVER_ACCOUNT=CJIU6KXJWOYACFLDMEQOJETA4PO3MXYLTH7TRHRZIODVWU47QYZBBVY6L4
- ./sandbox goal clerk send -a 100000000 -f TW6XVPVWA2WH6G4UDWACQM7W4WW2SX756764UFAPS77OKY4PM3PO3QEVPQ -t GVPNGHFMZAFO3ZWXJKQ532T562RJOY7HMCY3PX7BVIVED5SMZXP5ECCWX4 // Accounts must have a minimum of 100,000 mAlgos to reside onchain
- ./sandbox goal account list // verification

## rename account

- ./sandbox goal account rename help
- ./sandbox goal account rename Unnamed-0 Test-Account-1
- ./sandbox goal account list // verification

## inspect contract state

goal app read --global --app-id 1 --guess-format

## List goal wallets

goal wallet list

## List account in wallet

goal account list -w wallet_QWEASD

## List balance of account

goal account balance -a I6GQAHTW7YHHHX6G5J6VJH7TA3EZUK4NCAFNATATFFQYDFZIVNUQJE5TV4

## Export seed phrase for account

goal account export -a 4KN7RXBW3IBGA4P6PSJQPBEKXJAKXVQ45JH5IVKX6ZJZT2JPIMB46HBVUY -w wallet_QWEASD

## Get app info

goal app info --app-id 57

## Look up current parameters for an ASA

goal asset info --assetid 65

## Create a new account in wallet

goal account new -w wallet_QWEASD

## Create a new wallet

goal wallet new wallet_QWEASD

```will provide a wallet seed phrase
motor series ripple elbow wrist cabbage elite gun debris meat force parade crazy age ocean exile bottom resemble flower whale strike assume balcony abandon subject
```
