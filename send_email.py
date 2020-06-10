from tkinter import *
from tkinter import messagebox
import os
from selenium.webdriver.common.action_chains import ActionChains
from random import *
from selenium import webdriver
from time import sleep, time, localtime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import datetime
from selenium.webdriver.common.keys import Keys
import pyperclip
from threading import Thread

stopped = False

def remove_sender(senders) :
    cs = sender_list.curselection()
    sender_list.delete(cs[0], cs[0])
    senders.pop(cs[0])

def updateInfo(send_num, num) :
    temp = send_num['text'].split('\n')
    send_num['text'] = "발송 횟수 : " + str(int(temp[0].split(':')[1].strip()) + 1) + "\n발송 이메일 수 : " + str(int(temp[1].split(':')[1].strip()) + num)
    

def getCurrentTime() :
    now = localtime()
    return "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

def add_sender(se, sp, st, senders) :
    senders.append([se.get(), sp.get()])
    st.insert(END, se.get() + '--' + sp.get() + '')
    st.see(END)
  

def filelist(directory) :
    return os.listdir(directory)

def plus_text() :
    files = filelist('./plus_text')
    if(len(files) == 0) :
        return ''
    i = randint(0, len(files) - 1)

    text = ''
    with open('./plus_text/' + files[i], 'r', encoding='UTF8') as f :
        lines = f.readlines()
        for line in lines:
            text += line
    return text

def rand_text() :
    files = filelist('./description')
    
    if(len(files) == 0) :
        return ''
    i = randint(0, len(files) - 1)

    text = ''
    with open('./description/' + files[i], 'r', encoding='UTF8') as f :
        lines = f.readlines()
        for line in lines:
            text += line
    return text

def copy_input(driver, val, text):
    pyperclip.copy(text)
    driver.find_element_by_id(val).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    sleep(1)

def copy_input2(driver, val, text):
    pyperclip.copy(text)
    driver.find_element(By.XPATH, val).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    sleep(1)

def do_naver(sender, receivers, title, description, rnum, fname, log_text, send_num) :

    driver = webdriver.Chrome('chromedriver.exe')
     
    driver.implicitly_wait(3)  # 대기

    driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com') # 로그인창 이동
    driver.implicitly_wait(3)

    copy_input(driver, 'id', sender[0])
    copy_input(driver, 'pw', sender[1])
    driver.find_element_by_id('log.login').click()
    sleep(2)
    log_text.insert(END, sender[0] + ' - 로그인 성공!\n')
    log_text.see(END)

    driver.get('https://mail.naver.com/') # 메일창 이동
    driver.implicitly_wait(3)

    driver.find_element(By.XPATH, '//strong[@class="skin_corp_bg skin_corp_txt"]').click() # 메일쓰기 클릭
    sleep(3)

    driver.find_element_by_id('checkSeveral').click()

    copy_input(driver, 'toInput', ','.join(receivers))
    copy_input(driver, 'subject', title)
    copy_input(driver, 'se2_iframe', description)

    # 이메일 유효성 확인
    ul = driver.find_element_by_id('toDiv')
    li = ul.find_elements(By.XPATH, '//li[@class="_addressObj _draggable caution"]')
    for l in li :
        l.find_elements_by_tag_name('a')[1].click()
    sleep(0.5)
    if(len(fname) != 0) :
        for f in fname :
            driver.find_element(By.XPATH, '//input[@id="fileContent"]').send_keys(os.getcwd() + '/' + f.strip())
        sleep(3)

    driver.find_element_by_id('sendBtn').click()
    
    updateInfo(send_num, len(receivers))
    
    log_text.insert(END, '\n'.join(receivers))
    log_text.insert(END, '\n' + str(len(receivers)) + '명 전송 완료\n')
    log_text.insert(END, '발송완료시간 [' + getCurrentTime() + '\n\n')
    log_text.see(END)

    sleep(len(receivers) * 0.5 + 2)
    driver.quit()


def do_google(sender, receivers, title, description, rnum, fname, log_text, send_num) :
    driver = webdriver.Chrome('chromedriver.exe')
    driver.implicitly_wait(3)  # 대기

    driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27') # 로그인창 이동
    driver.implicitly_wait(5)

    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    driver.find_element_by_xpath('//input[@type="email"]').send_keys(sender[0])
    driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
    sleep(5)

    driver.find_element_by_xpath('//input[@type="password"]').send_keys(sender[1])
    driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
    sleep(5)

    log_text.insert(END, sender[0] + ' - 로그인 성공!\n')
    log_text.see(END)
    driver.get('https://mail.google.com/') # 메일창 이동
    driver.implicitly_wait(5)
    sleep(5)
    
    driver.find_element_by_xpath('//div[@class="T-I J-J5-Ji T-I-KE L3"]').click()
    sleep(3)

    copy_input2(driver, '//textarea', ','.join(receivers))
    driver.find_element_by_xpath('//input[@name="subjectbox"]').send_keys(title)
    sleep(0.5)
    driver.find_element_by_xpath('//div[@class="Am Al editable LW-avf tS-tW"]').send_keys(description)
    #copy_input2(driver, '//input[@name="subjectbox"]', title)
    #copy_input2(driver, '//div[@class="Am Al editable LW-avf tS-tW"]', description)
    sleep(1.5)

    if(len(fname) != 0) :
        for f in fname :
            print(f)
            driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(os.getcwd() + '/' + f.strip())
            sleep(0.5)
        sleep(3)

    driver.find_element_by_xpath('//div[@class="T-I J-J5-Ji aoO v7 T-I-atl L3"]').click()
    
    updateInfo(send_num, len(receivers))
    log_text.insert(END, '\n'.join(receivers))
    log_text.insert(END, '\n' + str(len(receivers)) + '명 전송 완료\n')
    log_text.insert(END, '발송완료시간 [' + getCurrentTime() + ']\n\n')
    log_text.see(END)
    sleep(len(receivers) * 0.5 + 2)
    
    driver.quit()

def isPossible(num) :

    f = open('num.txt', 'r', encoding='UTF8')
    lines = f.readlines()
    f.close()
    t = lines[0].strip()
    if(t != getCurrentTime()[:10]) :
        with open('num.txt', 'w') as f :
            f.write(getCurrentTime()[:10] + '\n')
            f.write('0')
        return True
    if (int(lines[1].strip()) > num) :
        return False
    return True

def updateSendNum(num) :
    
    with open('num.txt', 'r', encoding='UTF8') as f :
        lines = f.readlines()
        n = int(lines[1].strip())
    n += num
    with open('num.txt', 'w') as f :
        f.write(getCurrentTime()[:10] + '\n')
        f.write(str(n))
        


def send_email(rt, senders, radVar, cVar, rcv_num, send_time, file_name, log_text, send_num, stop_btn, limit_num) :
    global stopped
    stopped = False
    rad = radVar.get()

    if(rcv_num.get().strip() == '') :
        messagebox.showinfo("알림", "수신자 수를 입력하세요.")
        return
    elif(send_time.get().strip() == '') :
        messagebox.showinfo("알림", "발송 주기를 입력하세요.")
        return
    elif(rad == 0) :
        messagebox.showinfo("알림", "메일 종류를 선택해주세요.")
        return
    elif (rad == 2) :
        messagebox.showinfo("알림", "네이트는 아직 지원하지 않습니다.")
        return
    elif (rad == 3) :
        messagebox.showinfo("알림", "다음은 아직 지원하지 않습니다.")
        return
    elif (len(senders) == 0) :
        messagebox.showinfo("알림", "송신자를 추가해주세요.")
        return
    fname = file_name.get()
    fname = fname.strip(',').strip().split(',')

    receivers = rt.get("1.0", END).strip().strip('\n').split('\n') # 수신자
    rcvnum = rcv_num.get().strip().split('~')
    rcvnum = [int(rcvnum[0]), int(rcvnum[1])] # 1~10

    sendtime = send_time.get().strip().split('~')
    sendtime = [int(sendtime[0]), int(sendtime[1])] # 300~3600

    sender_idx = 0
    receiver_idx = 0

    while True :

        if (isPossible(int(limit_num.get())) == False):
            messagebox.showinfo("알림", "발송자 수를 초과하였습니다.")
            return

        if rad==1 and senders[sender_idx][0].split('@')[1] != 'naver.com':
            sender_idx = (sender_idx + 1) % len(senders)
            continue
        elif rad==4 and senders[sender_idx][0].split('@')[1] != 'gmail.com' :
            sender_idx = (sender_idx + 1) % len(senders)
            continue

        plus = '' # 명언
        if(cVar.get()==1) :
            plus = plus_text()

        text = rand_text()
        i = text.find('\n')
        title = text[:i]
        description = text[i+1:]

        if (randint(1, 2) == 1) : # 앞 또는 뒤 내용 추가
            description = '<오늘의명언>' + plus + '\n' + description
        else :
            description = description + '\n' + '<오늘의명언>' + plus

        rnum = randint(rcvnum[0], rcvnum[1])
        stime = randint(sendtime[0], sendtime[1])
        
        if (receiver_idx + rnum > len(receivers)) :
            rnum = len(receivers) - receiver_idx
        
        if (rad == 1) :
            do_naver(senders[sender_idx], receivers[receiver_idx:receiver_idx+rnum], title, description, rnum, fname, log_text, send_num)
        elif (rad == 4) :
            do_google(senders[sender_idx], receivers[receiver_idx:receiver_idx+rnum], title, description, rnum, fname, log_text, send_num)

        rt.delete("1.0", str(rnum + 1) + ".0")
        sender_idx = (sender_idx + 1) % len(senders)
        receiver_idx += rnum
        updateSendNum(rnum)
        if(receiver_idx == len(receivers)) : break

        # 정지눌렀을때 처리
        if stopped :
            log_text.insert(END, '정지되었습니다.\n\n')
            log_text.see(END)
            return

        log_text.insert(END, str(stime) + '초만큼 대기합니다.\n')
        log_text.see(END)
        sleep(stime)

    log_text.insert(END, '전송이 끝났습니다.\n\n')
    log_text.see(END)
    messagebox.showinfo("알림", "전송이 끝났습니다.")
    
def createDirectory(directory) :
    try :
        if not os.path.exists(directory) :
            os.makedirs(directory)
    except OSError:
        pass

def start(rt, senders, radVar, cVar, rcv_num, send_time, file_name, log_text, send_num, stop_btn, limit_num) :
    task = Thread(target=send_email, args=(rt, senders, radVar, cVar, rcv_num, send_time, file_name, log_text, send_num, stop_btn, limit_num))
    task.start()

def sender_init(senders, sender_list) : # 초기화
    senders.clear()
    sender_list.delete(0, sender_list.size())

def loadSave(senders, radVar, file_name, receiver_text, rcv_num, send_time, sender_list, cVar, limit_num) :
    
    if os.path.exists('./save.txt') == False:
        return
        
    with open('./save.txt', 'r', encoding='cp949') as f :
        lines = f.readlines()
        i=0
        for line in lines:
            
            if(line.strip()!='') :
                if i==0 :
                    ss = line.strip().split(',')
                    for s in ss :
                        se = s.strip().split('-')
                        senders.append([se[0], se[1]])
                        sender_list.insert(END, se[0] + '--' + se[1])
                        
                elif i == 1:  
                    radVar.set(line.strip())
                elif i == 2 :
                    file_name.insert(0, line.strip())
                elif i == 3 :
                    rcv_num.insert(0, line.strip())
                elif i==4:
                    send_time.insert(0, line.strip())
                elif i == 5 :
                    cVar.set(line.strip())
                elif i == 6 :
                    limit_num.insert(0, line.strip())
                else :
                    receiver_text.insert(END, line.strip() + '\n')
                    receiver_text.see(END)
            i+=1
            


def save(senders, radVar, file_name, receiver_text, rcv_num, send_time, cVar, limit_num) :
    with open('./save.txt', 'w') as f :
        ss = []
        for s in senders :
            ss.append('-'.join(s))
        f.write(','.join(ss))
        f.write('\n')
        f.write(str(radVar.get()) + '\n')
        f.write(file_name.get() + '\n')
        f.write(rcv_num.get() + '\n')
        f.write(send_time.get() + '\n')
        f.write(str(cVar.get()) + '\n')
        f.write(limit_num.get() + '\n')
        f.write(receiver_text.get("1.0", END))
    
def search(search_receiver, receiver_text) :
    pos = receiver_text.search(search_receiver.get(), "1.0", stopindex=END)
    receiver_text.see(pos)
    receiver_text.tag_delete("강조")
    receiver_text.tag_add("강조", pos, str(int(pos.split('.')[0])+1) + ".0")
    receiver_text.tag_config("강조", background="yellow")
    
def stop(log_text) :
    global stopped
    stopped = True

    log_text.insert(END, '현재 실행이 끝나면 종료됩니다.\n\n')
    log_text.see(END)

#def on_closing(senders, radVar, file_name, receiver_text, rcv_num, send_time, cVar, limit_num) :
#    save(senders, radVar, file_name, receiver_text, rcv_num, send_time, cVar, limit_num)
#    window.destroy()

def updateReceiverNum(rt, rnum_btn) :
    while True :
        rcv = rt.get("1.0", END).strip().strip('\n').split('\n') # 수신자
        if len(rcv) == 1 and rcv[0] == '' : rcv = [] 
        rnum_btn['text'] = '수신자수:'+str(len(rcv))
        sleep(3)


def init(window) :
    try :
        if not os.path.exists('num.txt') :
            with open('num.txt', 'w') as f :
                f.write(getCurrentTime()[:10] + '\n')
                f.write('0')
    except OSError:
        pass

    createDirectory('./plus_text')
    createDirectory('./description')
    senders = []
    root_frame = Frame(window)

    radVar = IntVar()
    r1 = Radiobutton(root_frame, text="네이버", variable=radVar, value=1)
    r1.grid(column = 0, row=0)
    r2 = Radiobutton(root_frame, text="네이트", variable=radVar, value=2)
    r2.grid(column = 1, row=0)
    r3 = Radiobutton(root_frame, text="다음", variable=radVar, value=3)
    r3.grid(column = 2, row=0)
    r4 = Radiobutton(root_frame, text="구글", variable=radVar, value=4)
    r4.grid(column = 3, row=0)
    cVar = IntVar()
    chk = Checkbutton(root_frame, text="명언", variable=cVar)
    chk.grid(column=4, row=0)
    
    Label(root_frame, text="사용자이메일").grid(column=0, row=1)
    sender_email = Entry(root_frame, width=20)
    sender_email.grid(column=1, row=1)
    Label(root_frame, text="패스워드").grid(column=0, row=2)
    sender_password = Entry(root_frame, width=20)
    sender_password.grid(column=1, row=2)

 
    sender_list = Listbox(root_frame, width=40, height=15)
    sender_list.bind('<Double-Button-1>', lambda event, senders=senders: remove_sender(senders))

    Button(root_frame, text="송신자추가", command=lambda se=sender_email, sp=sender_password, st=sender_list, senders=senders: add_sender(se, sp, st, senders)).grid(column=2, row=2)

    sender_list.grid(column=1, row=3)

    Label(root_frame, text="같은 폴더내 파일명 입력----->").grid(column=3, row=1)
    file_name = Entry(root_frame, width=20)
    file_name.grid(column=4, row=1)

    Label(root_frame, text="수신자 검색어 입력----->").grid(column=3, row=2)
    search_receiver = Entry(root_frame, width=15)
    search_receiver.grid(column=4, row=2)

    frame2 = Frame(root_frame)

    receiver_text = Text(frame2, width=40, height=15)
    scrollbar2 = Scrollbar(frame2)
    receiver_text.pack(side=LEFT, fill=Y)
    scrollbar2.pack(side=RIGHT, fill=Y)
    scrollbar2.config(command=receiver_text.yview)
    receiver_text.config(yscrollcommand=scrollbar2.set)

    Button(root_frame, text="검색", command=lambda search_receiver=search_receiver, receiver_text=receiver_text: search(search_receiver, receiver_text)).grid(column=5, row=2)

    frame2.grid(column=4,row=3)

    Label(root_frame, text="수신자 수 ?~?").grid(column=0, row=6)
    rcv_num = Entry(root_frame, width=20)
    rcv_num.grid(column=1, row=6)

    Label(root_frame, text="발송 주기 ?~?").grid(column=2, row=6)
    send_time = Entry(root_frame, width=20)
    send_time.grid(column=3, row=6)

    Label(root_frame, text='발송자 수 제한 ----->').grid(column=2, row=5)
    limit_num = Entry(root_frame, width=20)
    limit_num.grid(column=3, row=5)

    frame3 = Frame(root_frame)

    log_text = Text(frame3, width=40, height=20)
    scrollbar3 = Scrollbar(frame3)
    log_text.pack(side=LEFT, fill=Y)
    scrollbar3.pack(side=RIGHT, fill=Y)
    scrollbar3.config(command=log_text.yview)
    log_text.config(yscrollcommand=scrollbar3.set)

    log_text.insert(END, '로그를 보여줍니다.\n확인만 하세요.\n\n')
    log_text.see(END)

    send_num = Label(root_frame, text="발송 횟수 : 0\n발송 이메일 수 : 0")
    send_num.grid(column=3, row=3)

    stop_btn = Button(root_frame, text="정지", command=lambda log_text=log_text : stop(log_text))
    stop_btn.grid(column=4, row=6)

    Button(root_frame, text="발송시작", command=lambda rt=receiver_text, senders=senders, radVar=radVar, cVar=cVar, rcv_num=rcv_num, send_time=send_time, file_name=file_name, log_text=log_text, send_num=send_num, stop_btn=stop_btn, limit_num=limit_num : start(rt, senders, radVar, cVar, rcv_num, send_time, file_name, log_text, send_num, stop_btn, limit_num)).grid(column=5, row=6)
    
    frame3.grid(column=2, row=3)
    Button(root_frame, text="송신자초기화", command=lambda senders=senders, sender_list=sender_list: sender_init(senders, sender_list)).grid(column=2, row=1)
    
    
    
    Button(root_frame, text="저장", command=lambda senders=senders, radVar=radVar, file_name=file_name, receiver_text=receiver_text, rcv_num=rcv_num, send_time=send_time, cVar=cVar, limit_num=limit_num : save(senders, radVar, file_name, receiver_text, rcv_num, send_time, cVar, limit_num)).grid(column=5, row=3)
    
    loadSave(senders, radVar, file_name, receiver_text, rcv_num, send_time, sender_list, cVar, limit_num)
    
    rnum_label = Label(root_frame, text="수신자수:0")
    #rnum_btn['command'] = lambda receiver_text=receiver_text, rnum_btn=rnum_btn: updateReceiverNum(receiver_text,rnum_btn)
    rnum_label.grid(column=4, row=5)

    task = Thread(target=updateReceiverNum, args=(receiver_text, rnum_label))
    task.start()

    root_frame.grid(row=1, column=0, columnspan=2)

    return receiver_text, lambda rt=receiver_text, senders=senders, radVar=radVar, cVar=cVar, rcv_num=rcv_num, send_time=send_time, file_name=file_name, log_text=log_text, send_num=send_num, stop_btn=stop_btn, limit_num=limit_num : start(rt, senders, radVar, cVar, rcv_num, send_time, file_name, log_text, send_num, stop_btn, limit_num)
    #window.protocol("WM_DELETE_WINDOW", lambda : on_closing(senders, radVar, file_name, receiver_text, rcv_num, send_time, cVar, limit_num))

def func() :
    lambda rt=receiver_text, senders=senders, radVar=radVar, cVar=cVar, rcv_num=rcv_num, send_time=send_time, file_name=file_name, log_text=log_text, send_num=send_num, stop_btn=stop_btn, limit_num=limit_num : start(rt, senders, radVar, cVar, rcv_num, send_time, file_name, log_text, send_num, stop_btn, limit_num)

if __name__ == '__main__' :
    window = Tk()
    window.title('이메일 발송')
    init(window)
    window.mainloop()