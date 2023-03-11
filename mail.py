import os
import traceback
from imbox import Imbox

def export_mail(username, password):
    host = "imap.gmail.com"
    download_folder = os.getcwd()
    
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder, exist_ok=True)
        
    mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
    messages = mail.messages()
    
    for (uid, message) in messages:
        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"mail/{att_fn}"
                print(f"[GM] Downloaded file: {message.date}")
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
                # mail.delete(uid)
            except:
                print(traceback.print_exc())
            break

    mail.logout()