import datetime

def get_datetime():
    now = datetime.datetime.now()
    
    time = now.strftime("%Y-%m-%d %H:%M")
    return time

print(get_datetime())