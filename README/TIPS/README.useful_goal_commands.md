# Utility goal commands

## enter algod

./sandbox enter algod

## create new account

./sandbox goal account new

## fund new account

- ./sandbox goal account list
- SENDER_ACCOUNT=FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4
- RECEIVER_ACCOUNT=CJIU6KXJWOYACFLDMEQOJETA4PO3MXYLTH7TRHRZIODVWU47QYZBBVY6L4
- ./sandbox goal clerk send -a 10000000000 -f CJC25URJGTAXE7VQ5GEDMPV2SLGSAR2SOFXQFAQ3I73P2CXU3XUEKIPL2U -t RYMIOXYHNX5WEJRAEODXBSWX4LFVRR7LBRWEJ74NVKPMBLRVRRA7I2UNMU // Accounts must have a minimum of 100,000 mAlgos to reside onchain
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
wine sample method there olive type minute wire expect employ blast asthma year system plug club job arrive cram find atom spring claim ability mail
```
