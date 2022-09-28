'''
Author : rizad
Last Updated : 09/28/2022
Repo : @riz4d/TempMail-CLI
'''
import io
import wget
from banner import banner
import requests as req
from bs4 import BeautifulSoup

mailid=''
domain=''
id=''
no_of_msgs=''
filename=''
filenam=''



def mail_gen():
    global no_of_random_mails
    no_of_random_mails=input("How many mail's you need : ")    
    for i in range(0,int(no_of_random_mails)):   
       api='https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1'
       api_req=req.get(api)
       result=api_req.json()[0]
       print(result+'\n')


def mailbox_msgs():
    
    checking_mailboxapi='https://www.1secmail.com/api/v1/?action=getMessages&login='+mailid+'&domain='+domain
    mailbox_req=req.get(checking_mailboxapi)
    mailbox_json=mailbox_req.json()
    global no_of_msgs
    no_of_msgs=len(mailbox_json)
    print('\n'+str(no_of_msgs)+ ' Mails Recieved\n-------------\n\n')
    
    if str(mailbox_json)=='[]':
        print('No Messages Where Recieved')
    else:
        for i in range(no_of_msgs):
                  
                  id=mailbox_json[i]['id']
                  sender=mailbox_json[i]['from']
                  subject=mailbox_json[i]['subject']
                  maildate=mailbox_json[i]['date']
                  print('Mail Number : '+str(id))
                  print('Mail From : '+sender)
                  print('Recieved Time : '+maildate)
                  print('Subject : '+subject)
                  print('\n========================\n')
                  
def read_mailboxmgs():
    global filename
    read_mailboxapiurl= 'https://www.1secmail.com/api/v1/?action=readMessage&login='+mailid+'&domain='+domain+'&id='+id
    read_mailboxapiurl_req= req.get(read_mailboxapiurl)
    read_mailboxapiurl_json=read_mailboxapiurl_req.json()

   
    read_msg_fr=read_mailboxapiurl_json['from']
    read_msg_dt=read_mailboxapiurl_json['date']
    read_msg_sub=read_mailboxapiurl_json['subject']
    read_msg_att=read_mailboxapiurl_json['attachments']
    if str(read_msg_att)=='[]':
        read_msg_att='No Attachments'
        filename=='non'
    else:
        read_msg_att=read_mailboxapiurl_json['attachments'][0]
        
        read_msg_att=read_msg_att['filename']
        
        filename= read_msg_att
        
        
    read_msg_bod=read_mailboxapiurl_json['textBody']
    
    mail='\n'+mailid+'@'+domain+"'s Inbox"+'\n'+'-----------------------'+'\n\n'+'Mail no : '+id+'\n'+'From : '+str(read_msg_fr)+'\n'+'Date : '+str(read_msg_dt)+'\n'+'Subject : '+str(read_msg_sub)+'\n'+'Attachments : '+str(read_msg_att)+'\n'+'Message : '+str(read_msg_bod)+'\n======================'+' \n\n'
    file = open('mail.txt','w')
    file.write(str(mail)) 
    file.close()

    bk=open('mail.txt',mode='r',encoding='utf-8')
    html = bk.read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()   
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)
    bk.close()

def dl_attachments():

      att_mailboxapiurl= 'https://www.1secmail.com/api/v1/?action=download&login='+mailid+'&domain='+domain+'&id='+id+'&file='+str(filename)
      att_mailboxapiurl_req= req.get(att_mailboxapiurl)
      if att_mailboxapiurl=='https://www.1secmail.com/api/v1/?action=download&login='+mailid+'&domain='+domain+'&id='+id+'&file=':
          print('no attachments')
      else:
        attdl=wget.download(att_mailboxapiurl)
        print(att_mailboxapiurl_req)
        print('\nAttachment Has Been Successfully Saved as '+filename+'\n')


def main():
    
  global id
  global domain
  global mailid
  global checkmethod
  checkmethod=str(input(': '))


  if checkmethod=='1':
    mail_gen()
  elif checkmethod=='2':
      print('''
      Select a Domain
      
       1  - @1secmail.com
       2  - @1secmail.org
       3  - @1secmail.net
       4  - @bheps.com
       5  - @dcctb.com
       6  - @kzccv.com
       7  - @qiott.com
       8  - @wuuvo.com
       9  - @wwjmp.com
       10 - @esiix.com
       11 - @oosln.com
       12 - @vddaz.com
     
       ''')
      select_domain=str(input('Choose a option : '))
      if select_domain=='1':
            domain='1secmail.com'
      elif select_domain=='2':
          domain='1secmail.org'
      elif select_domain=='3':
          domain='1secmail.net'
      elif select_domain=='4':
          domain='bheps.com'
      elif select_domain=='5':
          domain='dcctb.com'
      elif select_domain=='6':
          domain='kzccv.com'
      elif select_domain=='7':
          domain='qiott.com'
      elif select_domain=='8':
        domain='wuuvo.com'
      elif select_domain=='9':
          domain='wwjmp.com'
      elif select_domain=='10':
          domain='esiix.com'
      elif select_domain=='11':
          domain='oosln.com'
      elif select_domain=='12':
          domain='vddaz.com'
      else:
          print('Invalid entry')
          banner()
          main()
      enter_user=input('Enter a username : ')
      mailid=enter_user
      print('your mail is '+mailid+'@'+domain)
      for i in range(100):
          input('refresh inbox press enter,for stop ctrl+c')
          mailbox_msgs()
          if no_of_msgs>0:
            check_show=input('Enter The Mail Number To Access The Message : ')
            id=check_show
            read_mailboxmgs()
            dl_attachments()
          else:
           print('')
  else:
    print('WARNING : Please Choose Correct Option [1/2] ')
    main()

banner()
main()
