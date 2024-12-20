from datetime import datetime, timedelta
import data, send

def main():
    
    today = datetime.now() + timedelta(hours=9)
    today_string = today.strftime('%Y-%m-%d')
    
    items = data.getItems(today_string)
    
    datas = data.pickUserData(items)
    
    send.send(datas, "本日")
    
    data.setNewDate(items)
