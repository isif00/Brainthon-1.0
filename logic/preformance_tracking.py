import pandas as pd
import json
import datetime

'''
worker_json should be is this format:
 "worker":
{
 "name":"ahmed" 
 "selected_orders":[order1,order2]
 "deliveries_history":[order1,order2] 
 "ratings":[4.5,3,5,5]
 "is_avalaible":True
 "coordinate":[123244,4994492]
}

order_json should be is this format:
"order":
{
 "cleint_name": "salmi sifo"
 "address": "blida - yyyyy"
 "order_name": "mega pizza"
 "requesting_date": "2022-09-12 Monday 8:45 PM"
 "delivery_date": "2022-09-12 Monday 8:45 PM"
 "cleint_rating": 4.8
}
'''
def sconds_to_hours_min(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d" % (hour, minutes)
def worker_preformance(worker_json):
    worker_json = json.loads(worker_json)
    #. list<int> delivered order per day
    df = list(map(lambda x:pd.DataFrame.from_dict(x) ,worker_json['worker']['deliveries_history'][:]))
    df = pd.concat(df,ignore_index=False).transpose()
    delivered_count_per_day = []
    average_daily_rating = []
    for i in range(30):
        delivered_count_per_day.append(len(df[df['delivery_date'] == datetime.date.today() - datetime.timedelta(days=i)]))
        average_daily_rating.append(df[df['delivery_date'] == datetime.date.today() - datetime.timedelta(days=i)]['client_rating'].sum())
    #shows number of delivered orders for the every week in the last few weeks
    delivered_count_per_week = []
    average_weekly_rating = []
    for i in range(4):
        delivered_count_per_week.append(sum(delivered_count_per_day[i*7:i*7 + 7]))
        average_weekly_rating.append(sum(average_daily_rating[i*7:i*7 + 7]))
    average_daily_working_hours  = 0
    for i in range(30):
        c = df[df['delivery_date'] == datetime.date.today() - datetime.timedelta(days=i)].sort_values(by='requesting_date')['requesting_date']
        average_daily_working_hours +=  (c[len(c)-1] -c[0]).total_sconds()/ 30 
    average_daily_working_hours = sconds_to_hours_min(average_daily_working_hours)
    average_delivery_time = 0
    for i in range(20):
        average_delivery_time = '30 min'
    
    average_rating = sum(average_daily_rating)/30
    return json.dumps({
        'delivered_orders_per_day':delivered_count_per_day,
        'delivered_orders_per_week':delivered_count_per_week,
        'average_rating':average_rating,
        'average_delivery_time':average_delivery_time,
        'average_daily_rating':average_daily_rating,
        'average_weekly_rating':average_weekly_rating,
        'average_daily_working_hours':average_daily_working_hours
        
    })

def workers_preformance(workers_json):
    workers_json = json.loads(workers_json)
    most_loved_worker = ('name',0)
    fastest_worker = ('name',100000000000)
    best_worker_of_the_week = ('name',0) # worker who delivered highest number of orders last week
    average_delivery_times = []
    average_ratings = []
    average_daily_working_hours = []
    delivered_orders_per_day = []
    delivered_orders_per_week = []
    for worker in workers_json:
        prefromance = worker_preformance(worker)
        average_delivery_times.append(prefromance.average_delivery_time)
        average_ratings.append(prefromance.average_rating)
        average_daily_working_hours.append(prefromance.average_daily_working_hours)
        delivered_orders_per_day.append(prefromance.average_daily_working_hours)
        delivered_orders_per_week.append(prefromance.delivered_orders_per_week)
        if prefromance.average_rating > most_loved_worker[1]:
            most_loved_worker = (worker['name'],prefromance.average_rating)
        if prefromance.average_delivery_time < fastest_worker[1]:
            fastest_worker = (worker.name,prefromance.average_delivery_time)
        if prefromance.delivered_orders_per_week[0] > best_worker_of_the_week[1]:
            best_worker_of_the_week = (worker.name,prefromance.delivered_orders_per_week[0])
    return json.dumps({
        'most_loved_worker': most_loved_worker,
        'fastest_worker': fastest_worker,
        'best_worker_of_the_week':best_worker_of_the_week,
        'average_delivery_times':average_delivery_times,
        'average_ratings':average_ratings,
        'average_daily_working_hours':average_daily_working_hours,
        'delivered_orders_per_day':delivered_orders_per_day,
        'delivered_orders_per_week':delivered_orders_per_week   
    })
'''
workers_json is json string that contains list of all workers 
'''

worker_preformance('{"worker": {"coordinate": [987654, 1234567], "deliveries_history": [{"order": {"address": "456 Elm St, CityB", "client_name": "Bob Smith", "client_rating": 4.9, "delivery_date": "2023-09-20 Monday 6:30 PM", "order_name": "Sushi Delight", "requesting_date": "2023-09-20 Monday 6:00 PM"},"order": {"address": "456 Elm St, CityB", "client_name": "Bob Smith", "client_rating": 4.9, "delivery_date": "2023-09-20 Monday 6:30 PM", "order_name": "Sushi Delight", "requesting_date": "2023-09-20 Monday 6:00 PM"}}], "is_available": true, "name": "John", "ratings": [3.8, 4.1, 4.3], "selected_orders": [{"order": {"address": "123 Main St, CityA", "client_name": "Alice Johnson", "client_rating": 4.6, "delivery_date": "2023-09-22 Wednesday 1:00 PM", "order_name": "Burger Combo", "requesting_date": "2023-09-22 Wednesday 12:30 PM"}}]}}')
