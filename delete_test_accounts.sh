wallet_id=wallet_QWEASD

while read i; do
    echo "$i"
    asArray=($i)
    echo ${asArray[2]}
    address=${asArray[2]}
    goal account delete -a ${address} -w ${wallet_id}
done <<< "`goal account list -w ${wallet_id}`"