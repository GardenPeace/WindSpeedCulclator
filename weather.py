from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options


def wind_speed():
    options = Options()
    # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
    options.add_argument('--headless')
    # ChromeのWebDriverオブジェクトを作成する。
    driver = webdriver.Chrome(chrome_options=options)

    # 指定したURLのスクレピング
    driver.get("http://www.jma.go.jp/jp/amedas_h/today-67437.html?areaCode=000&groupCode=50")

    # 気象データを抜き出し
    weather_products = driver.find_elements_by_class_name("middle")

    winds = []

    for i in range(24):
        wind_take = 8 * i + 3
        if not weather_products[wind_take].text == " ":
            winds.append(weather_products[wind_take].text)

    wind = winds[-1]

    # 閉じる
    driver.close()

    return wind

