from datetime import datetime, timedelta
import data, send

def main():
    
    day = datetime.now() + timedelta(days=3, hours=9)
    day_string = day.strftime('%Y-%m-%d')
    
    items = data.getItems(day_string)
    
    datas = data.pickUserData(items)
    
    send.send(datas, "3日後")