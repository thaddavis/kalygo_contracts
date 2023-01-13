#!/bin/bash

echo "WALLETS"
goal wallet list
while read i; do
    asArray=($i)
    default_account=${asArray[2]}
    break
done <<< "`goal account list`"
# exit 0
echo ""
echo "Default Account: ${default_account}"
echo ""
account_a_creation_output=`goal account new -w wallet_QWEASD`
account_b_creation_output=`goal account new -w wallet_QWEASD`
account_c_creation_output=`goal account new -w wallet_QWEASD`
echo $account_a_creation_output
echo $account_b_creation_output
echo $account_c_creation_output
account_a=$(echo $account_a_creation_output | cut -c 34-91)
account_b=$(echo $account_b_creation_output | cut -c 34-91)
account_c=$(echo $account_c_creation_output | cut -c 34-91)
echo ""
echo "account_a"
echo $account_a
account_a_export_output=`goal account export -a $account_a -w wallet_QWEASD`
account_a_mneumonic=$(echo $account_a_export_output | awk -F'"' '{print $2}')
echo $account_a_mneumonic
echo ""
echo "account_b"
echo $account_b
account_b_export_output=`goal account export -a $account_b -w wallet_QWEASD`
account_b_mneumonic=$(echo $account_b_export_output | awk -F'"' '{print $2}')
echo $account_b_mneumonic
echo ""
echo "account_c"
echo $account_c
account_c_export_output=`goal account export -a $account_c -w wallet_QWEASD`
account_c_mneumonic=$(echo $account_c_export_output | awk -F'"' '{print $2}')
echo $account_c_mneumonic
echo ""
sed \
"
s/ACCOUNT_A_ADDRESS/$account_a/g;
s/ACCOUNT_A_MNEMONIC/$account_a_mneumonic/g;
s/ACCOUNT_B_ADDRESS/$account_b/g;
s/ACCOUNT_B_MNEMONIC/$account_b_mneumonic/g;
s/ACCOUNT_C_ADDRESS/$account_c/g;
s/ACCOUNT_C_MNEMONIC/$account_c_mneumonic/g;
" config/config_escrow_template.py > config/config_escrow.py

mAlgoAmount=10000000000
echo ""
goal clerk send -a $mAlgoAmount -f $default_account -t $account_a
echo ""
goal clerk send -a $mAlgoAmount -f $default_account -t $account_b
echo ""
goal clerk send -a $mAlgoAmount -f $default_account -t $account_c
echo ""
# Print Balance
account_a_balance=`goal account balance -a $account_a`
echo "account a balance: $account_a_balance"
echo ""
account_b_balance=`goal account balance -a $account_b`
echo "account b balance: $account_b_balance"
echo ""
account_c_balance=`goal account balance -a $account_c`
echo "account c balance: $account_c_balance"
echo ""
