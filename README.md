
To test locally

tbears deploy -t tbears polling -f hxe9d75191906ccc604fc1e45a9f3c59fb856c215f -k keystore1.json -c tbears_cli_config.json

password for keystore1 is p@ssword1

Replace keystore2.json and keystore3.json with your keystore files from testnet wallets
and change the password under wallets in line 23 of webapp/main.py accordingly

tbears sendtx -k keystore1.json testcmdline/send.json

tbears call testcmdline/call.json
