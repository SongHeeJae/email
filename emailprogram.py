import navercafe
import send_email
from tkinter import *

if __name__ == '__main__' :
    window = Tk()
    window.title('이메일 프로그램')
    start_send, radVar, radVar2, items = navercafe.init(window)
    receiver_text, start = send_email.init(window)
    start_send['command'] = lambda radVar=radVar, radVar2=radVar2, items=items, receiver_text=receiver_text, start=start: navercafe.do_crawling(radVar, radVar2, items, True, receiver_text, start)

    
    window.mainloop()
