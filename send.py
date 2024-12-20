import format, api

def send(datas, day):
    
    for user, items in datas.items():
        
        for item in items:
            
            print(item)
        
        send_data = [
            format.messageText(day + "更新のアイテムがあります。"), 
            format.userData(datas[user], day + "更新のアイテムがあります。", day)
        ]
        
        if day == "本日":
            
            day_en = "today"
        
        else:
            
            day_en = "advance"
        
        if len(items) > 12:
            
            send_data.append(
                format.quickReply("現在表示されていないアイテムがあります。\n続きを表示する場合は下記クイックリプライをご利用ください。", [{"label": "続きを表示", "text": "> get " + str(12) + " " + day_en}])
            )
        
        api.sendMessage(user, send_data)