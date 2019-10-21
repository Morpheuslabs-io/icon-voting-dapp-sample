import json
from pprint import pprint

from flask import Flask, render_template, url_for, request, redirect
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.exception import JSONRPCException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.convert_type import convert_hex_str_to_int
from iconsdk.wallet.wallet import KeyWallet

from repeater import retry

app = Flask(__name__)
default_account = 'hx86f8117539f039f7c6b5a8ca8d233e2e752bd8fa'
default_score = "cx26da99fcddd7f06a0e565e0e3edde3d1218ff5da" # voting smart contract address
icon_node_rpc = "http://bops-t.morpheuslabs.io:27107/api/v3"; # internal RPC node URL
icon_service = IconService(HTTPProvider(icon_node_rpc))

wallets = {
    'wallet1': KeyWallet.load(bytes.fromhex("fb9164edaf46e254917694e3ea7daa65796c6899d2382c977fd9e8ffd995f348")),
    'wallet2': KeyWallet.load(bytes.fromhex("19d8fa5a7dcb3ab6aa1a6348a88007bf100827f43c26457d01ca0260711ac2df")),
    'wallet3': KeyWallet.load(bytes.fromhex("6c1a06076e7b115be29f0446f332b4f3968c9eb218106d2c6da46a29687f7161"))
}

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    print(app.url_map)
    return render_template('site-map.html', context=links)


@app.route('/account/<address>')
def account(address):
    params = {"account": address}
    return render_template('index2.html', context=params)


@app.route('/score/<score>/api')
def apis(score):
    score_apis = icon_service.get_score_api(score)
    result = json.dumps(score_apis, sort_keys=True, indent=4)
    return render_template('result.html', context=result)


@app.route('/myVote/<walletName>', methods=['GET', 'POST'])
def myVote(walletName):
    params = {}
    call = CallBuilder().from_(wallets.get(walletName).get_address()) \
        .to(default_score) \
        .method("get_vote") \
        .params(params) \
        .build()
    result = icon_service.call(call)
    result_value = convert_hex_str_to_int(result['vote'])
    voted = ''

    if result_value == 1:
        voted = 'YES'
    elif result_value ==2:
        voted = 'NO'
    elif result_value ==0:
        voted='-'

    return voted


@app.route('/vote/<walletName>', methods=['GET', 'POST'])
def vote(walletName):
    result = {}

    if request.method == 'POST':
        params = {
            "_vote": request.form['element']
        }
        transaction = CallTransactionBuilder() \
            .from_(wallets.get(walletName).get_address()) \
            .to(default_score) \
            .step_limit(9999999) \
            .nid(3) \
            .nonce(100) \
            .method("vote") \
            .params(params) \
            .build()
        signed_transaction = SignedTransaction(transaction, wallets.get(walletName))

        tx_hash = icon_service.send_transaction(signed_transaction)
        result['post'] = signed_transaction.signed_transaction_dict
        result['transactionHash'] = tx_hash
        transaction_status = get_tx_result(tx_hash)
        result['status'] = transaction_status['status']
        result['message'] = ''
        if transaction_status['status'] == 0:
            result['message'] = transaction_status["failure"]["message"]
        return json.dumps(result, sort_keys=True, indent=4)


@retry(JSONRPCException, tries=10, delay=1, back_off=2)
def get_tx_result(tx_hash):
    tx_result = icon_service.get_transaction_result(tx_hash)
    return tx_result


@app.route('/result/<walletName>', methods=['GET', 'POST'])
def votingResults(walletName) -> dict:
    params = {}
    call = CallBuilder().from_(wallets.get(walletName).get_address()) \
        .to(default_score) \
        .method("get_vote_talley") \
        .params(params) \
        .build()
    result = icon_service.call(call)

    votesResult = {}
    votesResult['yes'] = convert_hex_str_to_int(result['yes'])
    votesResult['no'] = convert_hex_str_to_int(result['no'])
    return json.dumps(votesResult)


@app.route('/<walletName>')
@app.route('/')
def index_wallet(walletName=None):
    if not walletName:
        return redirect('/wallet1')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)

