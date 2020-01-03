# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import math

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def wind_speed():
    options = Options()
    # スクレピングする際に、ブラウザの表示をなくす
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)

    # 東京の風速を調査
    driver.get("http://www.jma.go.jp/jp/amedas_h/today-44132.html?areaCode=000&groupCode=30")

    # 気象データを抜き出し
    weather_products = driver.find_elements_by_class_name("middle")

    winds = []

    # 今日のすべての風速を抜き出す
    for i in range(24):
        wind_take = 8 * i + 3
        if not weather_products[wind_take].text == " ":
            winds.append(weather_products[wind_take].text)

    # 最新の風速を抜き出す
    wind = winds[-1]

    driver.close()

    return wind


def moving_point(rad_x, shift, w, h):
    diameter = 200
    x = diameter * (math.sin(rad_x - math.radians(shift))) + w/2
    y = diameter * (math.cos(rad_x - math.radians(shift))) + h/2

    return (x, y)


def main(w_speed):
    (w, h) = (600, 600)   # 画面サイズ
    pygame.init()       # 初期化
    screen = pygame.display.set_mode((w, h))  # 画面の大きさを設定

    counter = 0  # 風速の初期値

    sysfont = pygame.font.SysFont(None, 80)  # フォントの作成

    # テキストオブジェクトの作成
    wind_text = sysfont.render("WindSpeed " + str(w_speed) + "m/s", False, (255, 255, 255))

    while(True):
        pygame.display.update()             # 画面更新
        pygame.time.wait(20)                # 更新時間間隔
        screen.fill((0, 20, 0, 0))  # 画面の色
        pygame.display.set_caption("WindCulclator")  # タイトルの指定

        counter += w_speed  # 風車の速度を決定
        rad_x = math.radians(counter)

        # 回転のさせるための点を管理
        x1, y1 = moving_point(rad_x, 0, w, h)
        x2, y2 = moving_point(rad_x, 180, w, h)
        x3, y3 = moving_point(rad_x, 90, w, h)
        x4, y4 = moving_point(rad_x, 270, w, h)

        # 風車の作成
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 5)
        pygame.draw.line(screen, (255, 255, 255), (x3, y3), (x4, y4), 5)

        pygame.draw.rect(screen, (255, 255, 255), Rect(270, 330, 60, 200))  # 風車の土台

        screen.blit(wind_text, (50, 50))  # 先程作成したテキストを描画

        for event in pygame.event.get():  # イベント(キー入力等)を取得
            # 終了用のイベント処理
            if event.type == QUIT:          # 閉じるボタンが押されたとき
                pygame.quit()  # Pygameを終了
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    '''
    注意事項：風速が早すぎると、風車がゆっくり回ってみえる
    '''
    w_speed = float(wind_speed())
    # w_speed = 1.0
    main(w_speed)