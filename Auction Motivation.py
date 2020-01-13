import pandas as pd
import json 

data = pd.read_csv('Auction Motivation/Engagement - Auction Motivation.csv')
data.set_index(['Cycle','Current_Bid'],inplace=True)

def getCycle(cycle):
    cycles = data.index.levels[0]
    n = len(cycles)
    i = 0
    while True:
        if(i < n and cycles[i]>cycle):
            return cycles[i-1]
        elif(i>=n):
            return None
        i+=1 

def get_threshold_discount(cycle,current_discount):
    threshold_discounts = data.loc[cycle].index
    n = len(threshold_discounts)
    i = 0 
    while True:
        if(i>=n):
            return None
        if(i < n and current_discount < threshold_discounts[i]):
            return threshold_discounts[i]
        i+=1 

def get_auction_motivation_message(cycle, current_bid_amount, group_amount):
    try:
        data.loc[(cycle,)]
    except KeyError:
        cycle = getCycle(cycle)
    current_discount = (group_amount - current_bid_amount)/100 
    if(current_discount==30):
        return 'Congrats! Group bid has reached max limit. Place your bid to participate in lucky draw.'
    threshold_discount = get_threshold_discount(cycle,current_discount)
    if(not threshold_discount):            #Projected discount achieved
        message = 'No message'                   
    else:
        message = data.loc[(cycle, threshold_discount)]['Messages'].replace('<current bid value>;',"Rs "+str(current_bid_amount))
    return message 

message = get_auction_motivation_message(cycle=3, current_bid_amount=8200, group_amount=10000)

with open("bid_remainder.json", "r") as bid_remainder_json:
    json_dict = json.load(bid_remainder_json)
    
json_dict['message_data']['text']  = message

with open("bid_remainder.json", "w") as bid_remainder_json:
    json.dump(json_dict, bid_remainder_json)
