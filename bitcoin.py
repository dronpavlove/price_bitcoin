import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

price_xpr_dict = {}


def get_price_xrp(url: str) -> float:
    """
    Получает стоимость биткоина
    на сайте www.binance.com и отдаёт её в виде числа
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36",
    }
    try:
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.text, "lxml")
        price_xrp = soup.find("div", class_="css-12ujz79").text
        price_xrp = float(price_xrp.split(' ')[1])
    except:
        price_xrp = 0
    return price_xrp


def changes_per_hour():
    """
    Каждые 30 секунд в течение часа получает стоимость биткоина
    на сайте www.binance.com и выдаёт сообщение о падении
    более чем на 1 % от максимума за час
    """
    global price_xpr_dict
    bitcoin_api_url = 'https://www.binance.com/ru/price/xrp'
    max_xpr_price = get_price_xrp(bitcoin_api_url)
    sleep(30)
    for _ in range(119):
        price_xrp = get_price_xrp(bitcoin_api_url)
        if price_xrp > max_xpr_price:
            max_xpr_price = price_xrp
        elif price_xrp < max_xpr_price and price_xrp != 0:
            difference = max_xpr_price - price_xrp
            percent = max_xpr_price / 100
            if difference > percent:
                difference_percent = difference / percent
                print("Цена снизилась на ", difference_percent, "%")
        else:
            print(datetime.now(), "Не удалось получить ответ от сайта")
        sleep(30)
    price_xpr_dict[str(datetime.now())] = max_xpr_price


if __name__ == "__main__":
    while True:
        changes_per_hour()
