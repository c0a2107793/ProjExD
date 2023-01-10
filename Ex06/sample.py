import pygame as pg
import os
import random
import sys
import time


main_dir = os.path.split(os.path.abspath(__file__))[0]


class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title) 
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect() 

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 


class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img_path, ratio, xy):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]  
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)                    


class Bomb:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)
#キノコを生成する関数
class BigMushroom:
    def __init__(self, img_path, vxy, xy, ratio):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.vx, self.vy = vxy
        
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)

#スコアを計測する関数
class Score:
    def __init__(self):
        self.t = 0#時間の変数
        self.sco = 0#スコアの変数
    
    def update(self):
        self.t += 1
        if self.t % 200 == 0:#一定時間ごとにスコアを１追加する
            self.sco += 1
            if self.t >= 5000:#時間が長くなるにつれ、スコアの上がり幅が上がる
                if self.t % 100 == 0:
                    self.sco += 2
        return self.sco

def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def load_sound(file):
    """because pygame can be be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None


def main():
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    boom_sound = load_sound("boom.wav")
    shoot_sound = load_sound("car_door.wav")
    if pg.mixer:
        music = os.path.join(main_dir, "data", "house_lo.wav")
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1)

    clock =pg.time.Clock()

    # 練習１
    scr = Screen("逃げろ！こうかとん", (1600,900), "fig/pg_bg.jpg")

    # 練習３
    kkt = Bird("fig/6.png", 2.0, (900,400))
    kkt.update(scr)

    # 練習５
    bkd_lst = []
    color_lst = ["red", "green", "blue", "yellow", "magenta"]
    for i in range(5):
        bkd = Bomb(color_lst[i%5], 10, (random.choice(range(-2, 3)), random.choice(range(-2, 3))), scr)
        bkd_lst.append(bkd)
    # bkd.update(scr)
    #キノコの生成
    knk = BigMushroom("fig/bigkinoko.png", (random.choice(range(-2, 3)),
                      random.choice(range(-2, 3))), (100,100), 0.1) 
    life = 0
    font1 = pg.font.SysFont(None, 50)
    score = Score()

    # 練習２
    while True:        
        scr.blit()

        #ゲーム中のスコアの表示
        ans = score.update()
        text = font1.render(f"{ans}", True, (255,0,0))
        scr.sfc.blit(text, (100, 100))




        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kkt.update(scr)
        for i in range(len(bkd_lst)):
            bkd_lst[i].update(scr)
            if kkt.rct.colliderect(bkd_lst[i].rct):
                if life == 1: #ライフがある場合
                    life -= 1
                    bkd_lst[i].rct.centerx = -9999 #爆弾を画面外に
                    bkd_lst[i].rct.centery = -9999
                    kkt = Bird("fig/6.png", 2, kkt.rct.center) #元の大きさに変更
                else:
                    #ゲーム終了時のスコアの表示
                    text_2 = font1.render(f"your score is {ans}", True, (255,0,0))
                    text_2_place = text_2.get_rect(midbottom=(800, 450))
                    scr.sfc.blit(text_2, text_2_place)
                    pg.display.update()
                    time.sleep(5)
                    return
                    
        if kkt.rct.colliderect(knk.rct):
            life += 1 #内部的なライフを増やす
            knk.rct.centerx = -9999 #衝突時きのこを画面外に
            knk.rct.centery = -9999
            kkt = Bird("fig/6.png", 4, kkt.rct.center) #大きさを変更
        
        else: 
            knk.update(scr)
        pg.display.update()
        clock.tick(1000)
    

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()