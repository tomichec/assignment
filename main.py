import requests
from datetime import datetime

def averageTime(events, eventType = 'PullRequestEvent'):
    '''return the average time between specific events'''
    eventCreation = []
    for event in events:
        print(event['type'])
        if event['type'] == eventType:
             eventCreation.append(
                 datetime.strptime(event['created_at'],'%Y-%m-%dT%H:%M:%SZ').timestamp()
             )
    
    # compute the average time -- this assumes that the events are sorted by time in reverse order
    N = len(eventCreation) - 1
    if N < 1:
        print("Not enough {} events were present.".format(eventType))
        return -1
    
    averageTime = (eventCreation[0] - eventCreation[-1])/N

    return averageTime

def totalEvents(events, offset = 24*60):
    '''return a dictionary of total number of events grouped by event type for a given offset'''
    E = {}
    for event in events:
        eventTimestamp = datetime.strptime(event['created_at'],'%Y-%m-%dT%H:%M:%SZ').timestamp()
        if datetime.now().timestamp() -  eventTimestamp > offset*60:
            break
        try:
            E[event['type']] += 1
        except:
            E[event['type']] = 1

    return E

def fetchEvents(user, repo):
    url = "https://api.github.com/repos/{}/{}/events".format(user,repo)
    data = requests.get(url)
    
    if data.status_code != 200:
        raise Exception("Fetching the data failed.")

    events = data.json()

    return events

def main():
    user = 'pandas-dev'
    repo = 'pandas'

    events = fetchEvents(user, repo)

    print("average time between PullRequestEvents is: {} seconds".format(averageTime(events)))

    offset = 24*60
    countEventsByGroup = totalEvents(events, offset)
    print("in the last 24 hours there were the following events:")
    print("event type\tnumber of")
    for k in countEventsByGroup.keys():
        print("{}:  {}".format(k,countEventsByGroup[k]))
    
if __name__ =='__main__':
    main()
