import pygame
import pygame.font
import sys
import traceback
import copy
from math import sqrt
from pygame.locals import *
 
 
pygame.font.init()
pygame.init()
 
#用于控制顺序
order = True
#用于结束游戏后阻止落子
working = True
#用来存储棋子信息，主要用于悔棋
backups = []
 
#定义棋子半径
r = 40
#一格代表的像素
#直接安格子存放，打印时计算像素
i = 80
 
#绘制棋盘
def Draw_a_chessboard(screen):
    #填充背景色
    screen.fill((233,204,138))
    #画外框
    outer_frame_color = (60,20,0)
    pygame.draw.rect(screen,outer_frame_color,[50,20,740,660],5)
    #行
    inner_frame_color = (0,0,0)
    for i in range(0,9):
        pygame.draw.line(screen, inner_frame_color, (60, 30+80*i), (780, 30+80*i)) 
    #列
    for i in range(0,10):
        pygame.draw.line(screen,inner_frame_color, (60+80*i, 30), (60+80*i, 670))
    #‘将’
    jiang_rote_color = (0,0,0)
    pygame.draw.lines(screen, jiang_rote_color, True,[(60, 270),(220, 270),(220,430),(60,430)],3)
    pygame.draw.lines(screen, jiang_rote_color, True,[(620, 270),(780, 270),(780,430),(620,430)],3)
    #‘士’路线
    shi_rote_color = (0,0,0)
    pygame.draw.line(screen, shi_rote_color, (60, 270), (220, 430),3)
    pygame.draw.line(screen, shi_rote_color, (60, 430), (220, 270),3) 
    pygame.draw.line(screen, shi_rote_color, (620, 270), (780, 430),3)
    pygame.draw.line(screen, shi_rote_color, (620, 430), (780, 270),3)
    #‘象’路线
    xiang_rote_color = (0,0,0)
    pygame.draw.lines(screen, xiang_rote_color, True,[(220, 350),(60, 190),(220,30),(380,190)])
    pygame.draw.lines(screen, xiang_rote_color, True,[(220, 350),(60, 510),(220,670),(380,510)])
    pygame.draw.lines(screen, xiang_rote_color, True,[(620, 350),(780, 190),(620,30),(460,190)])
    pygame.draw.lines(screen, xiang_rote_color, True,[(620, 350),(780, 510),(620,670),(460,510)])
    # #‘兵’,用抗锯齿连续线段
    # bing_rote_color = (255,0,0)
    # for j in range(0,2):
    #     for k in range(0,4):
    #         pygame.draw.aalines(screen, bing_rote_color, False,[(330+270*j, 260+180*k),(350+270*j, 260+180*k),(350+270*j,240+180*k)],3)
    #         pygame.draw.aalines(screen, bing_rote_color, False,[(390+270*j, 260+180*k),(370+270*j, 260+180*k),(370+270*j,240+180*k)],3)
    #         pygame.draw.aalines(screen, bing_rote_color, False,[(330+270*j, 100+180*k),(350+270*j, 100+180*k),(350+270*j,120+180*k)],3)
    #         pygame.draw.aalines(screen, bing_rote_color, False,[(390+270*j, 100+180*k),(370+270*j, 100+180*k),(370+270*j,120+180*k)],3)
    # #‘炮’
    # pao_rote_color = (255,0,0)
    # for m in range(0,2):
    #     for n in range(0,2):
    #         pygame.draw.aalines(screen, pao_rote_color, False,[(240+450*m, 170+540*n),(260+450*m, 170+540*n),(260+450*m,150+540*n)],3)
    #         pygame.draw.aalines(screen, pao_rote_color, False,[(300+450*m, 170+540*n),(280+450*m, 170+540*n),(280+450*m,150+540*n)],3)
    #         pygame.draw.aalines(screen, pao_rote_color, False,[(240+450*m, 190+540*n),(260+450*m, 190+540*n),(260+450*m,210+540*n)],3)
    #         pygame.draw.aalines(screen, pao_rote_color, False,[(300+450*m, 190+540*n),(280+450*m, 190+540*n),(280+450*m,210+540*n)],3)
 
    #绘制‘楚河汉界’
    pygame.draw.rect(screen,[233,204,138],[381,31,79,639])
    chuhehanjie = pygame.image.load("楚河汉界.png").convert_alpha()
    screen.blit(chuhehanjie,(381,31))
    #画‘悔棋’，‘重新开始’和‘退出’按钮
    button_color = (163,80,21)
    pygame.draw.rect(screen,button_color,[980,150,200,100],5)
    pygame.draw.rect(screen,button_color,[980,350,200,100],5)
    pygame.draw.rect(screen,button_color,[980,550,200,100],5)
 
    s_font = pygame.font.Font('JDFLS.ttf',45)
 
    text1 = s_font.render("悔    棋",True,button_color)
    text2 = s_font.render("重新开始",True,button_color)
    text3 = s_font.render("退出游戏",True,button_color)
    screen.blit(text1,(1000,170))
    screen.blit(text2,(980,370))
    screen.blit(text3,(980,570))
 
#绘制棋子
def Draw_a_chessman(screen,color,qizi,x,y):
    red_color = (255,0,0)
    black_color = (0,0,0)
 
    pygame.draw.circle(screen,(0,0,0),(x,y),40)
    pygame.draw.circle(screen,(247,157,12),(x,y),39)
    pygame.draw.circle(screen,(0,0,0),(x,y),35,3)
    pygame.draw.circle(screen,(181,131,16),(x,y),31)
 
    q_font = pygame.font.Font('JDFLS.ttf',60)
 
    if color == 'red':
        q_color = red_color
    elif color == 'black':
        q_color = black_color
    screen.blit(q_font.render(qizi[0],True,q_color),(x-30,y-40))
 
#绘制带有棋盘的棋子
def Draw_a_chessboard_with_chessman(screen):  
    Draw_a_chessboard(screen)
    for each_qizi in hongqi.keys():
        Draw_a_chessman(screen,hongqi[each_qizi]['color'],each_qizi,hongqi[each_qizi]['now_weizhi'][0],hongqi[each_qizi]['now_weizhi'][1])
    for each_qizi in heiqi.keys():
        Draw_a_chessman(screen,heiqi[each_qizi]['color'],each_qizi,heiqi[each_qizi]['now_weizhi'][0],heiqi[each_qizi]['now_weizhi'][1])
 
#通过位置寻找棋子
def find(x,y):
    for key in hongqi.keys():
          if sqrt((hongqi[key]['now_weizhi'][0] - x)**2+(hongqi[key]['now_weizhi'][1]-y)**2) < r:
              return [key,hongqi[key],'red']
    for key in heiqi.keys():
          if sqrt((heiqi[key]['now_weizhi'][0] - x)**2+(heiqi[key]['now_weizhi'][1]-y)**2) < r:
              return [key,heiqi[key],'black']
#判断该位置有无棋子
def weizhi_panduan(x,y):
    for key in hongqi.keys():
        if [x,y] == hongqi[key]['now_weizhi']:
            return True
    for key in heiqi.keys():
        if [x,y]==heiqi[key]['now_weizhi']:
            return True
    return False
 
#棋子移动的规则
def move_rules(qizi,chess_color,x,y):
    can_move =[]
    
    if qizi == '将':
        can_move += [[x+i,y],[x-i,y],[x,y+i],[x,y-i]]
    elif qizi[0] == '士':
        can_move += [[x+i,y+i],[x-i,y-i],[x-i,y+i],[x+i,y-i]]
    elif qizi[0] == '相':
        can_move += [[x+2*i,y+2*i],[x-2*i,y-2*i],[x-2*i,y+2*i],[x+2*i,y-2*i]]
    elif qizi[0] == '马':
        can_move += [[x+i,y+2*i],[x+2*i,y+i],[x-i,y-2*i],[x-2*i,y-i],[x+i,y-2*i],[x+2*i,y-i],[x-i,y+2*i],[x-2*i,y+i]]
    elif qizi[0] == '车':
        for m in range(10):
            can_move.append([x,y+m*i])
            can_move.append([x,y-m*i])
            can_move.append([x+m*i,y])
            can_move.append([x-m*i,y])
    elif qizi[0] == '炮':
        for m in range(10):
            can_move.append([x,y+m*i])
            can_move.append([x,y-m*i])
            can_move.append([x+m*i,y])
            can_move.append([x-m*i,y])
    elif qizi[0] == '兵':
        if chess_color == 'red':
            if 60<=x<=60+4*i: 
                can_move += [[x+i,y]]
            else:
                can_move +=[[x+i,y],[x,y-i],[x,y+i]]
        elif chess_color == 'black':
            if 60+5*i<=x<=60+9*i:
                can_move += [[x-i,y]]
            else:
                can_move += [[x-i,y],[x,y-i],[x,y+i]]
 
    return can_move                
 
#判断棋子是否可以走该位置
#（棋子，棋子现在所处位置，判断棋子是否可走的位置）
def weizhi_able(qizi,chess_color,x,y,d_x,d_y):
    can_move = move_rules(qizi,chess_color,x,y)
    if [d_x,d_y] in can_move:
        #如果第二次点击的位置为自身位置，以不可走处理
        if [d_x,d_y] == [x,y]:
            return False
        elif qizi == '将' or qizi[0] == '士':
            if ((60<=d_x<=60+2*i and 30+3*i<=d_y<=30+5*i) or (60+7*i<=d_x<=60+9*i and 30+3*i<=d_y<=30+5*i)):
                return True
        elif qizi[0] == '相':
            #删除相憋腿的情况
            if (chess_color == 'red' and 60<=d_x<=60+4*i) or (chess_color == 'black' and 60+5*i<=d_x<=60+9*i):
                if weizhi_panduan(x-i,y-i) and [d_x,d_y] == [x-2*i,y-2*i]:
                    return False
                elif weizhi_panduan(x+i,y-i) and [d_x,d_y] == [x+2*i,y-2*i]:
                    return False
                elif weizhi_panduan(x+i,y+i) and [d_x,d_y] == [x+2*i,y+2*i]:
                    return False
                elif weizhi_panduan(x-i,y+i) and [d_x,d_y] == [x-2*i,y+2*i]:
                    return False
                else:
                    return True
        elif qizi[0] == '马':
            #删除马憋腿的情况
            if weizhi_panduan(x,y-i) and ([d_x,d_y] == [x-i,y-2*i] or [d_x,d_y] == [x+i,y-2*i]):
                return False
            elif weizhi_panduan(x+i,y) and ([d_x,d_y] == [x+2*i,y-i] or [d_x,d_y] == [x+2*i,y+i]):
                return False
            elif weizhi_panduan(x,y+i) and ([d_x,d_y] == [x-i,y+2*i] or [d_x,d_y] == [x+i,y+2*i]):
                return False
            elif weizhi_panduan(x-i,y) and ([d_x,d_y] == [x-2*i,y-i] or [d_x,d_y] == [x-2*i,y+i]):
                return False
            else:
                return True
        elif qizi[0] == '兵':
            return True
        elif qizi[0] == '车':
            count = 0
            if d_y == y:
                weizhicha = abs(d_x - x)
                for each_cha in range(80,weizhicha,80):
                    if weizhi_panduan(min(d_x,x)+each_cha,y):
                        count += 1
                if count == 0 and weizhi_panduan(d_x,d_y)and find(d_x,d_y)[2]!=chess_color:
                    return True
                elif count == 0 and not weizhi_panduan(d_x,d_y):
                    return True
                else:
                    return False
            elif d_x == x:
                weizhicha = abs(d_y - y)
                for each_cha in range(80,weizhicha,80):
                    if weizhi_panduan(x,min(d_y,y)+each_cha):
                        count += 1
                if count == 0 and weizhi_panduan(d_x,d_y)and find(d_x,d_y)[2]!=chess_color:
                    return True
                elif count == 0 and not weizhi_panduan(d_x,d_y):
                    return True
                else:
                    return False
        elif qizi[0] == '炮':
            #记录原来位置与所走位置之间的棋子数
            count = 0
            #同一行
            if d_y == y:
                weizhicha = abs(d_x - x)
                for each_cha in range(80,weizhicha,80):
                    if weizhi_panduan(min(d_x,x)+each_cha,y):
                        count += 1
                if count == 1 and weizhi_panduan(d_x,d_y)and find(d_x,d_y)[2]!=chess_color:
                        return True
                elif count == 0:
                    if weizhi_panduan(d_x,d_y):
                        return False
                    else:
                        return True
                else:
                    return False
            #同一列
            elif d_x == x:
                weizhicha = abs(d_y - y)
                for each_cha in range(80,weizhicha,80):
                    if weizhi_panduan(x,min(d_y,y)+each_cha):
                        count += 1
                if count == 1 and weizhi_panduan(d_x,d_y)and find(d_x,d_y)[2]!=chess_color:
                    return True
                elif count == 0:
                    if weizhi_panduan(d_x,d_y):
                        return False
                    else:
                        return True
                else:
                    return False
    else:
        return False
 
#绘制提示器（类容，屏幕，字大小）
def text(s,screen,x):
    pygame.draw.rect(screen,(233,204,138),[980,20,1200,100])
    s_font = pygame.font.Font('JDFLS.ttf',45)
    s_text=s_font.render(s,True,(255,0,0))
    screen.blit(s_text,(980,100))
    pygame.display.flip()
    
def main():
    global hongqi,heiqi,running,order,working,backups
 
    #棋子初始位置
    hongqi = {'将':{'color':'red','now_weizhi':[60,350]},'士1':{'color':'red','now_weizhi':[60,270]},'士2':{'color':'red','now_weizhi':[60,430]},'相1':{'color':'red','now_weizhi':[60,190]},
              '相2':{'color':'red','now_weizhi':[60,510]},'马1':{'color':'red','now_weizhi':[60,110]},'马2':{'color':'red','now_weizhi':[60,590]},'车1':{'color':'red','now_weizhi':[60,30]},
              '车2':{'color':'red','now_weizhi':[60,670]},'炮1':{'color':'red','now_weizhi':[220,110]},'炮2':{'color':'red','now_weizhi':[220,590]},'兵1':{'color':'red','now_weizhi':[300,30]},
              '兵2':{'color':'red','now_weizhi':[300,190]},'兵3':{'color':'red','now_weizhi':[300,350]},'兵4':{'color':'red','now_weizhi':[300,510]},'兵5':{'color':'red','now_weizhi':[300,670]}
             }
    heiqi = {'将':{'color':'black','now_weizhi':[780,350]},'士1':{'color':'black','now_weizhi':[780,270]},'士2':{'color':'black','now_weizhi':[780,430]},'相1':{'color':'black','now_weizhi':[780,190]},
             '相2':{'color':'black','now_weizhi':[780,510]},'马1':{'color':'black','now_weizhi':[780,110]},'马2':{'color':'black','now_weizhi':[780,590]},'车1':{'color':'black','now_weizhi':[780,30]},
             '车2':{'color':'black','now_weizhi':[780,670]},'炮1':{'color':'black','now_weizhi':[620,110]},'炮2':{'color':'black','now_weizhi':[620,590]},'兵1':{'color':'black','now_weizhi':[540,30]},
             '兵2':{'color':'black','now_weizhi':[540,190]},'兵3':{'color':'black','now_weizhi':[540,350]},'兵4':{'color':'black','now_weizhi':[540,510]},'兵5':{'color':'black','now_weizhi':[540,670]}
            }
    #创建一个窗口
    screen = pygame.display.set_mode([1200,900])
    # 设置窗口标题
    pygame.display.set_caption("中国象棋")
    #定义两个存储棋子现在的状态
    backups1 = []
    backups2 = []
    #用于暂存所有棋子状态
    backup=copy.deepcopy([hongqi,heiqi])
    backups = []
    backups.append(backup)
    #鼠标第一次按下选择棋子
    running = True
 
    
     #在窗口画出棋盘以及按钮
    Draw_a_chessboard(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()
 
    while True: 
        Draw_a_chessboard_with_chessman(screen)
        #只有working为真才能落子，主要用于游戏结束后防止再次落子
        if working:
            if order:
                color = 'red'
                text('红棋落子',screen,54)
            else:
                color = 'black'
                text('黑棋落子',screen,54)
        #监听所有事件
        for event in pygame.event.get():
            #点击x则关闭窗口
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            #点击窗口里面类容则完成相应指令 
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y=event.pos[0],event.pos[1]
                    if working:
                        #鼠标第一次按下选择棋子
                        if running:
                            x,y = event.pos[0],event.pos[1]
                            for key in hongqi.keys():
                                if sqrt((hongqi[key]['now_weizhi'][0] - x)**2+(hongqi[key]['now_weizhi'][1]-y)**2) < r:
                                    backups1 = [key,hongqi[key]]
                            for key in heiqi.keys():
                                if sqrt((heiqi[key]['now_weizhi'][0] - x)**2+(heiqi[key]['now_weizhi'][1]-y)**2) < r:
                                    backups2 = [key,heiqi[key]]
                            if backups1:
                                #用于暂存棋子状态
                                backups3 = copy.deepcopy(backups1)
                                hongqi.pop(backups1[0])
                                running = not running
                            elif backups2:
                                #用于暂存棋子状态
                                backups4 = copy.deepcopy(backups2)
                                heiqi.pop(backups2[0])
                                running = not running
                        #鼠标再次按下，落下棋子
                        else:
                            if r < event.pos[0] < 900+r and 10 <event.pos[1] < 810+r:
                                x = (event.pos[0]+r-60)//80*80+60
                                y = (event.pos[1]+r-30)//80*80+30
                                # print('x = %s,y = %s'%(x,y))
                                if backups1 :#红棋
                                    #判断是否符合走棋规则
                                    if weizhi_able(backups1[0],backups1[1]['color'],backups1[1]['now_weizhi'][0],backups1[1]['now_weizhi'][1],x,y) and order:
                                        #判断所走位置是否有棋子
                                        if weizhi_panduan(x,y):
                                            #判断是否为敌方棋子
                                            if backups1[1]['color'] != find(x,y)[2]:
                                                heiqi.pop(find(x,y)[0])
                                                hongqi[backups1[0]] = backups1[1]
                                                hongqi[backups1[0]]['now_weizhi'] = [x,y]
                                                backup=copy.deepcopy([hongqi,heiqi])
                                                backups.append(backup)
                                                order = not order
                                            else:
                                                hongqi[backups3[0]] = backups3[1]
                                        else:
                                            hongqi[backups1[0]] = backups1[1]
                                            hongqi[backups1[0]]['now_weizhi'] = [x,y]
                                            backup=copy.deepcopy([hongqi,heiqi])
                                            backups.append(backup)
                                            order = not order
                                            # print('now_weizhi is %s'%(backups))
                                    else:
                                        #若不符合走棋规则，返回原位置
                                        hongqi[backups3[0]] = backups3[1]
                                    backups1 = []
                                    running = not running
                                    if '将' not in heiqi.keys():
                                         Draw_a_chessboard_with_chessman(screen)
                                         text('红棋胜利！',screen,30)
                                         pygame.display.flip()
                                         working = False
                                
 
                                elif backups2:#黑棋
                                    if weizhi_able(backups2[0],backups2[1]['color'],backups2[1]['now_weizhi'][0],backups2[1]['now_weizhi'][1],x,y) and not order:
                                        #判断所走位置是否有棋子
                                        if weizhi_panduan(x,y):
                                            #判断是否为敌方棋子
                                            if backups2[1]['color'] != find(x,y)[2]:
                                                hongqi.pop(find(x,y)[0])
                                                heiqi[backups2[0]] = backups2[1]
                                                heiqi[backups2[0]]['now_weizhi'] = [x,y]
                                                backup=copy.deepcopy([hongqi,heiqi])
                                                backups.append(backup)
                                                order = not order
                                            else:
                                                heiqi[backups4[0]] = backups4[1]
                                        else:
                                            heiqi[backups2[0]] = backups2[1]
                                            heiqi[backups2[0]]['now_weizhi'] = [x,y]
                                            backup=copy.deepcopy([hongqi,heiqi])
                                            backups.append(backup)
                                            order = not order
                                    else:
                                        heiqi[backups4[0]] = backups4[1]
                                    backups2=[]
                                    running=not running
                                    if '将' not in hongqi.keys():
                                        Draw_a_chessboard_with_chessman(screen)
                                        text('黑棋胜利！',screen,30)
                                        pygame.display.flip()
                                        working = False
                            else:
                                if backups1 :
                                    hongqi[backups1[0]] = backups3[1]
                                    backups1 = []
                                    running = not running
                                elif backups2:
                                    heiqi[backups2[0]] = backups4[1]
                                    backups2=[]
                                    running=not running
                    #如果点击‘重新开始’
                    if 900<x<1180 and 350<y<450:
                        #取消阻止
                        working=True
       
                        #重新开始
                        main()
                    
                        #点击‘退出游戏’，退出游戏
                    elif 900<x<1180 and 550<y<650:
                        pygame.quit()
                        sys.exit()                 
                    elif 900<x<1180 and 150<y<250 and len(backups)>1:
                        #删除maps里最后一个元素
                        del backups[len(backups)-1]
                        hongqi=copy.deepcopy(backups[-1][0])
                        heiqi=copy.deepcopy(backups[-1][1])
                        #切换顺序
                        order = not order
                        #将map显示出来
                        Draw_a_chessboard_with_chessman(screen)
                        #悔棋完成，阻止再次悔棋
                        x,y=0,0
  
 
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
