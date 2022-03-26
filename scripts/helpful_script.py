from brownie import network,accounts

#                It's simple but it's made with 💙 by Mowgli


# to get account an account from mainnet-fork-dev or you can change it to development 
# else network is a testnet script will you you account (metamask) using privateKey.
def getAccount():
    if network.show_active() == "mainnet-fork-dev":
        return accounts[0]
    else:
        return accounts.load("metamask1")