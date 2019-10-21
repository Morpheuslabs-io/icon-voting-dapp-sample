import json
from pprint import pprint

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.exception import JSONRPCException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.convert_type import convert_hex_str_to_int
from iconsdk.wallet.wallet import KeyWallet

from repeater import retry

icon_service = IconService(HTTPProvider("https://icon-27107-test.morpheuslabs.io"))

wallet = KeyWallet.create()
print("address: ", wallet.get_address()) # Returns an address
print("private key: ", wallet.get_private_key()) # Returns a private key

# file_path = "./test_keystore.json"
# wallet.store(file_path, "a12345678");
