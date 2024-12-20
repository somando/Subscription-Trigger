import today, advance

def lambda_handler(event, context):
    
    task = event.get('task', '')
    
    if task == 'today':
        
        today.main()
    
    elif task == 'advance':
        
        advance.main()

