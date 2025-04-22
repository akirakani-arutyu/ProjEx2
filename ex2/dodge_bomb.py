import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_RIGHT:(5,0),
    pg.K_LEFT:(-5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとんRectか爆弾Rect
    戻り値:判定結果タプル
    画面内ならTrue
    """
    x, y = False, False
    if 0 < rct.left < WIDTH:
        x = True
    if 0 < rct.top < HEIGHT:
        y = True
    return x, y


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))#空の正方形作る
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)#正方形に円を描く
    bb_rct = bb_img.get_rect()#画面に貼付
    bb_rct.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)#貼付場所指定
    
    bb_img.set_colorkey((0,0,0))
    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx,vy)#爆弾移動
        x, y =  check_bound(bb_rct)
        if not x:
            vx *= -1
        if not y:
            vy *= -1
        screen.blit(bb_img, bb_rct)#爆弾描画

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()