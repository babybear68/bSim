import requests, json

def sell(usd):
    p = price()
    f = 0.0
    if usd < 1.99:
        return "Amount too low"
    elif usd < 11:
        f = 0.99
    elif usd < 26.5:
        f = 1.49
    elif usd < 52:
        f = 1.99
    elif usd < 204:
        f = 2.99
    else:
        return "Amount too high"

    b = usd / p["sell"]

    if b > loadBTCAccount():
        return "Insufficient fund"

    writeUSDAccount(loadUSDAccount() + usd - f)
    writeBTCAccount(loadBTCAccount() - b)

    return "Successfully sold " + str(b) + " BTC"

def buy(usd):
    p = price()
    f = 0.0
    if usd < 1.99:
        return "Amount too low"
    elif usd < 11:
        f = 0.99
    elif usd < 26.5:
        f = 1.49
    elif usd < 52:
        f = 1.99
    elif usd < 204:
        f = 2.99
    else:
        return "Amount too high"

    c = loadUSDAccount()

    if usd + f > c:
        return "Insufficient fund"

    btc = usd / p["buy"]
    writeUSDAccount(c - usd)
    writeBTCAccount(loadBTCAccount() + btc)

    return "Successfully bought " + str(btc) + " BTC"

def price():
    r = requests.get("https://blockchain.info/ticker")
    if not r.ok:
        raise Exception("Unable to fetch price data")
    return {"buy": r.json()["USD"]["buy"], "sell": r.json()["USD"]["sell"]}

def writeUSDAccount(usd):
    with open("account.json", 'r') as fr:
        d = json.load(fr)
        d["USD"] = usd
    with open("account.json", 'w') as fw:
        json.dump(d, fw)

def writeBTCAccount(btc):
    with open("account.json", 'r') as fr:
        d = json.load(fr)
        d["BTC"] = btc
    with open("account.json", 'w') as fw:
        json.dump(d, fw)

def loadUSDAccount():
    with open("account.json", 'r') as f:
        d = json.load(f)
        return d["USD"]

def loadBTCAccount():
    with open("account.json", 'r') as f:
        d = json.load(f)
        return d["BTC"]

def openAccount(usd):
    d = {"USD": usd + 0.0, "BTC": 0.0}
    with open("account.json", 'w') as f:
        json.dump(d, f)
    return "Successfully opened new account with " + str(usd + 0.0) + " USD"

def main():
    print("bSim v0.1")
    exit = False
    while not exit:
        i = input().split(' ')
        if i[0] == "exit":
            exit = True
            continue
        if i[0] == "open":
            print(openAccount(int(i[1])))
        if i[0] == "show":
            print("USD:\t" + str(loadUSDAccount()))
            print("BTC:\t" + str(loadBTCAccount()))
            p = price()
            print("Total:\t" + str(loadUSDAccount() + (p["buy"] + p["sell"]) / 2 * loadBTCAccount()))
        if i[0] == "price":
            p = price()
            print("BUY:\t" + str(p["buy"]))
            print("SELL:\t" + str(p["sell"]))
        if i[0] == "buy":
            print(buy(int(i[1])))
        if i[0] == "sell":
            print(sell(int(i[1])))

if __name__ == "__main__":
    main()
