import pandas as pd, sys, os, datetime,time as rtrtrt

# make function that takes given station, returns amount of time and all connecting stations
# make station class
bingbingbing=rtrtrt.perf_counter()
system=sys.argv[1]
class Station:
    def __init__(self,statid,name):
        self.statid=statid
        self.name=name
        self.neighbors=set()
        self.neighbors_id=set()
        self.neighbortotrips=dict()
        self.tripstotime=dict()
        self.endofroute=set()
        self.transfers=set()
        self.transfers_id=set()
        self.transfertotime=dict()
    def addneighbor(self,stationid,station):
        if stationid not in self.neighbors_id:
            self.neighbors_id.add(stationid)
            self.neighbors.add(station)
            self.neighbortotrips[stationid]=set()
class SimpliStation:
    def __init__(self,basestation):
        self.statid=basestation.statid
        self.name=basestation.name
        self.neighbors=set()
        self.neighbors_id=set()
        self.neighbortotrips=dict()
        self.tripstotime=dict()
        self.transfers=basestation.transfers
        self.transfers_id=basestation.transfers_id
        self.transfertotime=basestation.transfertotime
oneday=datetime.timedelta(days=1)
checkpriordaythreshold=datetime.time(6,0,0)
checknextdaythreshold=datetime.time(18,0,0)
midnight=datetime.time(0,0,0)
def getchildren(station, time, day):
    # CHECK IF ENDOFROUTE FOR STATION INTERSECTS WITH DATETRIPS

    # day will be a Date object
    # time will be a Time object
    children=set()
    aftertime=datetime.datetime.combine(day,time)
    for n in station.neighbors_id:
        midnightday=datetime.datetime.combine(day,midnight)
        least=aftertime+oneday
        ltuple=tuple()
        # print(station.neighbortotrips.keys())
        available=station.neighbortotrips[n]&datetrips[day]
        for i in available:
            # maybe make base datetime thing, use timedelta to add seconds to the thing?
            s=station.tripstotime[(n,i)]
            td=midnightday+s[0]
            if least>td>=aftertime:
                least=td
                ltuple=(n[0],n[1],td,midnightday+s[1],i)
        # pr={(datetime.datetime.combine(day,midnight)+station.tripstotime[(n,i)],i) for i in available if datetime.datetime.combine(day,midnight)+station.tripstotime[(n,i)]}

        if time<=checkpriordaythreshold: # if time is so early that potentially the previous day also has a route
            yesterdayavail=station.neighbortotrips[n]&datetrips[day-oneday]
            for i in yesterdayavail:
                s=station.tripstotime[(n,i)]
                td=midnightday-oneday+s[0]
                if least>td>=aftertime:
                    least=td
                    ltuple=(n[0],n[1],td,midnightday-oneday+s[1],i)
            

        if checknextdaythreshold<=time: # if time is so late that potentially the next day also has a route
            tomorrowavail=station.neighbortotrips[n]&datetrips[day+oneday]
            for i in tomorrowavail:
                s=station.tripstotime[(n,i)]
                td=midnightday+oneday+s[0]
                if least>td>=aftertime:
                    least=td
                    ltuple=(n[0],n[1],td,midnightday+oneday+s[1],i)

        # qual={i for i in pr if aftertime<=i[0]} # maybe change so qual is not needed 
        # if qual!=pr:
            
        #     input()
        # try:
        # sel=min(pr)
        # except:
        #     print(n,previousline,day,time,station.name,len(pr),len(available),len(aservice),len(station.neighbortotrips[n]))
        #     print(path)
        #     tttt=set()
        #     for k in station.neighbortotrips.values():
        #         tttt.update(k)

        #     open('temp.txt','w').write(str((station.neighbors_id,tttt,aservice,tttt.intersection(aservice),aservice.intersection(tttt))))
        #     input()
        # children.add((n,sel[1],sel[2]))
        if ltuple!=tuple():
            children.add(ltuple)
        # input(sel)
    for n in station.transfertotime:
        children.add((n,-1,aftertime,aftertime+station.transfertotime[n],None))
    # input(children)

    #station is a Station object
    # iterate through sttion neighbors and find what times or smth
    # uhhhh find some way to deal with trips that start after midnight or smth like that????

    # before like 6 am, check previous day routes, see if there are any too
    return children


# FOR NYC: SOUTH FERRY AND WHITEHALL SHOULD BE CONNECTED BUT THEY ARE NOT BECAUSE THE ID GIVEN SHOULD BE 142, NOT 140 - MANUALLY CHANGE?


# go through stop times, trips
# drop unnecessary routes
# merge stations using df['stop_id'].replace()
# use df.where(df.isna(), df.astype(str)) to convert necessary colunms into str
# if parent station empty or smth then merge by station name or smth

transferreplace={'nyc':[('140','142')],'sf':[]}
curdir=os.listdir(system+' subway gtfs')
anytransfers=False
if 'transfers.txt' in curdir:
    anytransfers=True
    transfers=pd.read_csv(system+' subway gtfs/transfers.txt')
    for i in transferreplace[system]:
        transfers['from_stop_id']=transfers['from_stop_id'].replace(i[0],i[1]).where(transfers['from_stop_id'].isna(), transfers['from_stop_id'].astype(str))
        transfers['to_stop_id']=transfers['to_stop_id'].replace(i[0],i[1]).where(transfers['to_stop_id'].isna(), transfers['to_stop_id'].astype(str))
st=pd.read_csv(system+' subway gtfs/stop_times.txt')
stop=pd.read_csv(system+' subway gtfs/stops.txt')
routeinfo=pd.read_csv(system+' subway gtfs/routes.txt')
trips=pd.read_csv(system+' subway gtfs/trips.txt')
st['trip_id'],st['stop_id']=st['trip_id'].where(st['trip_id'].isna(), st['trip_id'].astype(str)),st['stop_id'].where(st['stop_id'].isna(), st['stop_id'].astype(str))

stop['stop_id'],stop['stop_name']=stop['stop_id'].where(stop['stop_id'].isna(), stop['stop_id'].astype(str)),stop['stop_name'].where(stop['stop_name'].isna(), stop['stop_name'].astype(str))
yesparent=False
if 'parent_station' in stop.columns:
    yesparent=True
    stop['parent_station']=stop['parent_station'].where(stop['parent_station'].isna(), stop['parent_station'].astype(str))

routeinfo['route_id']=routeinfo['route_id'].where(routeinfo['route_id'].isna(), routeinfo['route_id'].astype(str))
trips['route_id'],trips['service_id'],trips['trip_id']=trips['route_id'].where(trips['route_id'].isna(), trips['route_id'].astype(str)),trips['service_id'].where(trips['service_id'].isna(), trips['service_id'].astype(str)),trips['trip_id'].where(trips['trip_id'].isna(), trips['trip_id'].astype(str))
pstat=dict()
stopcoord=dict()
stoptoname=dict()
tobemerged=dict()
stoptrips=dict()
servicetrips=dict()
statidtostationindex=dict()
statidtochr=dict()
datetrips=dict()
deleo=set(trips[trips['route_id'].isin(set(routeinfo[routeinfo['route_type']!=1]['route_id']))]['trip_id'])
st=st[~st['trip_id'].isin(deleo)]
for i in set(trips['service_id']):
    servicetrips[i]=set(trips[trips['service_id']==i]['trip_id'])
with open(system+' servicetrips.txt','w')as f:
    f.write(str(servicetrips))
for i in stop.index:
    if yesparent:
        pstat[stop.loc[i,'stop_id']]=stop.loc[i,'parent_station']
    stopcoord[stop.loc[i,'stop_id']]=(stop.loc[i,'stop_lat'],stop.loc[i,'stop_lon'])
    statname=stop.loc[i,'stop_name'].strip()
    while statname.find('  ')>=0:
        statname=statname.replace('  ',' ')
    stoptoname[stop.loc[i,'stop_id']]=statname
old=[i for i in pstat if not pd.isna(pstat[i])]
new=[pstat[i] for i in old]
st['stop_id']=st['stop_id'].replace(old,new)
stations=[]
statids=[]
costat=dict()

if 'location_type' in stop.columns:
    loctypeopt=True
else:
    loctypeopt=False
loctypeset=set()
temp=set(st['stop_id'])

for i in temp:
    if stopcoord[i] in costat:
        costat[stopcoord[i]].add(i)
    else:
        costat[stopcoord[i]]={i}
    if loctypeopt:
        loctype=list(stop[stop['stop_id']==i]['location_type'])[0]
        if not pd.isna(loctype):
            loctypeset.add(loctype)
if loctypeset==set() and loctypeopt:
    # group by name
    namegroups=dict()
    for i in temp:
        if stoptoname[i] in namegroups:
            namegroups[stoptoname[i]].add(i)
        else:
            namegroups[stoptoname[i]]={i}
    for i in namegroups:
        namegroups[i]=sorted(tuple(namegroups[i]))
        for j in namegroups[i][1:]:
            tobemerged[j]=namegroups[i][0]
    print(namegroups)

for i in costat:
    if len(costat[i])>1:
        print(i,costat[i])
        m=tuple(sorted(costat[i]))
        print(m)
        if len(set(stoptoname[j] for j in costat[i]))==1:
            if m[0] not in tobemerged:
                stations.append(Station(m[0],stoptoname[m[0]]))
                statids.append(m[0])
            for j in m[1:]:
                tobemerged[j]=m[0]
        else:
            for j in m:
                if j not in tobemerged:
                    stations.append(Station(j,stoptoname[j]))
                    statids.append(j)
    else:
        s=list(costat[i])[0]
        if s not in tobemerged:
            stations.append(Station(s,stoptoname[s]))
            statids.append(s)
for i in range(len(statids)):
    statidtostationindex[statids[i]]=i
    statidtochr[statids[i]]=chr(i)
print(tobemerged)

old=list(tobemerged.keys())
new=[tobemerged[i] for i in old]
st['stop_id']=st['stop_id'].replace(old,new)
with open(system+' stations set.txt','w',encoding='utf-8')as f:
    f.write(str((set(st['stop_id']),stoptoname)))
# go down each route, add neighboras being only station in front
atr=set()
routetotrips=dict()
print(len(set(st['stop_id'])))
print(len(set(st['trip_id'])))
ct=0
for trip in set(st['trip_id']):
    ct+=1
    if ct%250==0:
        print(ct)
    routetable=st[st['trip_id']==trip].sort_values('stop_sequence',ascending=1)
    r=tuple(routetable['stop_id'])
    stoptrips[trip]=tuple(routetable['arrival_time']) 
    atr.add(r)
    if r in routetotrips:
        routetotrips[r].add(trip)
    else:
        routetotrips[r]={trip}

with open(system+' rtt.txt','w')as f:
    f.write(str(routetotrips))

with open(system+' atr.txt','w') as f:
    f.write(str(atr))
print(len(atr))

for trip in atr:
    # change this to be dependent on date?
    ar=routetotrips[trip]
    stations[statidtostationindex[trip[0]]].endofroute.update(ar)
    stations[statidtostationindex[trip[-1]]].endofroute.update(ar)
    for j in range(len(trip)-1):
        statindex=statidtostationindex[trip[j]]
        # if trip[j]!=trip[j+1]: maybe?
        stations[statindex].addneighbor(trip[j+1],stations[statidtostationindex[trip[j+1]]])
        stations[statindex].neighbortotrips[trip[j+1]].update(ar)
        for k in ar:
            s,ss=stoptrips[k][j],stoptrips[k][j+1]# ARRIVAL TIME OF FIRST, ARRIVAL OF SECOND
            t,tt=s.split(':'),ss.split(':')
            stations[statindex].tripstotime[(trip[j+1],k)]=(datetime.timedelta(hours=int(t[0]),minutes=int(t[1]),seconds=int(t[2])),datetime.timedelta(hours=int(tt[0]),minutes=int(tt[1]),seconds=int(tt[2])))

if anytransfers:
    for i in statids:
        transfersubset=transfers[(transfers['from_stop_id']==i) & (transfers['to_stop_id']!=i) & (transfers['to_stop_id'].isin(statids))]
        statindex=statidtostationindex[i]
        for j in transfersubset.index:
            tostatid=transfersubset.loc[j,'to_stop_id']
            stations[statindex].transfers.add(stations[statidtostationindex[tostatid]])
            stations[statindex].transfers_id.add(tostatid)
            stations[statindex].transfertotime[tostatid]=datetime.timedelta(seconds=int(transfersubset.loc[j,'min_transfer_time']))

ckckck=sorted([(statids[i],stations[i].name,stations[i].neighbors_id,stations[i].transfertotime,len(stations[i].endofroute)) for i in range(len(statids))])
with open(system+' neighbors.txt','w',encoding='utf-8') as f:
    f.write('\n'.join([' '.join([str(j) for j in i]) for i in ckckck]))
# start alg with finding what day of the week it is, then finding what trips are available


# get children returns list of neighboring stations and stop times there, maybe also add number of unique stations visited to it?
# make separate cases depending on if calendar.txt exists or not
datetoservices=dict()
dotwlist=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

if 'calendar.txt' in curdir: # nyc, also dont bother using calendar dates maybe
    calendar=pd.read_csv(system+' subway gtfs/calendar.txt')
    calendar['service_id'],calendar['start_date'],calendar['end_date']=calendar['service_id'].where(calendar['service_id'].isna(), calendar['service_id'].astype(str)),calendar['start_date'].where(calendar['start_date'].isna(), calendar['start_date'].astype(str)),calendar['end_date'].where(calendar['end_date'].isna(), calendar['end_date'].astype(str))
    for i in set(calendar['service_id']):
        if i not in servicetrips:
            servicetrips[i]=set()
    for i in calendar.index:
        startd=calendar.loc[i,'start_date']
        endd=calendar.loc[i,'end_date']
        startdate=datetime.date.fromisoformat(startd[:4]+'-'+startd[4:6]+'-'+startd[6:])
        enddate=datetime.date.fromisoformat(endd[:4]+'-'+endd[4:6]+'-'+endd[6:])
        while (startdate <= enddate):
            if startdate not in datetoservices:
                datetoservices[startdate]=set()
            dotw=startdate.weekday()
            if calendar.loc[i,dotwlist[dotw]]==1:
                datetoservices[startdate].add(calendar.loc[i,'service_id'])
            startdate += oneday
if 'calendar_dates.txt' in curdir:
    cd=pd.read_csv(system+' subway gtfs/calendar_dates.txt')
    cd['service_id'],cd['date']=cd['service_id'].where(cd['service_id'].isna(), cd['service_id'].astype(str)),cd['date'].where(cd['date'].isna(), cd['date'].astype(str))
    for i in cd.index:
        serv=cd.loc[i,'service_id']
        dat=cd.loc[i,'date']
        date=datetime.date.fromisoformat(dat[:4]+'-'+dat[4:6]+'-'+dat[6:])
        if date not in datetoservices:
            datetoservices[date]=set()
        if cd.loc[i,'exception_type']==1:
            datetoservices[date].add(serv)
        else:
            if serv in datetoservices:
                datetoservices[date].remove(serv)
    for i in set(cd['service_id']):
        if i not in servicetrips:
            servicetrips[i]=set()
for i in datetoservices:
    datetoservices[i]=tuple(sorted(datetoservices[i]))
    datetrips[i]=set()
    for j in datetoservices[i]:
        datetrips[i].update(servicetrips[j])

with open(system+' datetoservice.txt','w') as f:
    f.write('\n'.join(sorted([' '.join((str(i),str(datetoservices[i]))) for i in datetoservices])))
# with open(system+' datetrips.txt','w') as f:
#     f.write('\n'.join(sorted([' '.join((str(i),str(datetrips[i]))) for i in datetrips])))
cingcingcing=rtrtrt.perf_counter()
print('%s seconds'%(cingcingcing-bingbingbing))

# time, number of unique stations visited in fringe
# us stored time and date to find what services and routes are available

NUMBEROFSTATIONS=len(stations)
# ITERATE THROUGH ALL DATES
datetoallworthy=dict()
# d
# MAKE BIG ALLWORTHY SET FOR ALL STATIONS, GIVE THOSE ROUTES TO THEM, ON EACH DAY WILL SELECTOVELY CHOOSE ROUTES THAT ARE AVAILABLE
endstoletter=dict()
endsset=dict()
lettertoskipped=dict()
setlettertoskipped=dict()
simpletripstotime=dict()
lettertosymbol=dict()
counter=1
servicetoallworthy=dict()
servicetonodes=dict()
datetonodes=dict()
for date in datetrips:
    if datetoservices[date] not in servicetoallworthy:  
        allworthy=set() # set of station ids which correspond to stations that are worthy of stopping at
        print(date)
        if len(datetrips[date])>0:
            for i in range(NUMBEROFSTATIONS):
                stationinquestion=stations[i]
                # print(stationinquestion.endofroute,datetrips[date])
                if len(stationinquestion.endofroute&datetrips[date])>0:
                    allworthy.add(statids[i])
                elif len({j for j in stationinquestion.neighbors if len(stationinquestion.neighbortotrips[j.statid]&datetrips[date])>0})>2:
                    allworthy.add(statids[i])
                elif len(stationinquestion.transfers)>0:
                    allworthy.add(statids[i])
            servicetoallworthy[datetoservices[date]]=allworthy
            datetoallworthy[date]=allworthy
            datetonodes[date]=set()
            servicetonodes[datetoservices[date]]=set()
        # (newstation.endofroute and len(newstation.neighbors)>1) or ((not newstation.endofroute) and len(newstation.neighbors)>2) or (len(newstation.transfers)>0)
        # allworthychr={statidtochr[i] for i in allworthy}

        # MAKE SOMETHING TO SIMPLIFY NODES AND EDGES

        # MAKE GLOBAL ROUTE TO CHR THING OR SMTH - CHECKS IF ROUTE IS ALREADY IN THERE AND IF NOT ADDS IT IN
        
            for stationid in allworthy:
                cstation=stations[statidtostationindex[stationid]]
                # for otherstation in cstation.transfers:
                #     endstoletter[(stationid,otherstation.statid,counter)]=''
                #     counter+=1
                for otherstation in cstation.neighbors:
                    if len(cstation.neighbortotrips[otherstation.statid]&datetrips[date])>0:
                        prev=cstation
                        pointer=otherstation
                        visitid=[otherstation.statid]
                        visitedrun={cstation,otherstation}
                        while pointer.statid not in allworthy:
                            pointerset=pointer.neighbors-visitedrun
                            pointerset={i for i in pointerset if len(pointer.neighbortotrips[i.statid]&prev.neighbortotrips[pointer.statid])>0}


                            pointerset={i for i in pointerset if len(pointer.neighbortotrips[i.statid]&prev.neighbortotrips[pointer.statid])>0 and len(pointer.neighbortotrips[i.statid]&datetrips[date])>0}
                            prev=pointer

                            # pointerset={i for i in pointerset if (len(i.neighbors-visitedrun)>0 or i.statid in allworthy)}
                            pointer=list(pointerset)[0]

                            visitid.append(pointer.statid)
                            visitedrun.add(pointer)
                        visitid.remove(pointer.statid)
                        symbols=''.join([statidtochr[i] for i in visitid])

                        g=False
                        if (stationid,pointer.statid) in endsset:
                            for b in endsset[(stationid,pointer.statid)]:
                                if lettertoskipped[lettertosymbol[endstoletter[b]]]==visitid:
                                    servicetonodes[datetoservices[date]].add(b)
                                    datetonodes[date].add(b)
                                    g=True
                            if not g:
                                endsset[(stationid,pointer.statid)].add((stationid,pointer.statid,counter))
                                servicetonodes[datetoservices[date]].add((stationid,pointer.statid,counter))
                                datetonodes[date].add((stationid,pointer.statid,counter))

                                endstoletter[(stationid,pointer.statid,counter)]=chr(counter)#change to like a letter or smth?
                                lettertosymbol[chr(counter)]=symbols
                                temptttd=cstation.tripstotime
                                tempttta=prev.tripstotime
                                deptimes={((pointer.statid,counter),i[1]):temptttd[i] for i in temptttd if i[0]==otherstation.statid}
                                arrtimes={((i[0],counter),i[1]):tempttta[i] for i in tempttta if i[0]==pointer.statid}
                                newttt=dict()
                                for i in deptimes:
                                    if i in arrtimes:
                                        newttt[i]=(deptimes[i][0],arrtimes[i][1])
                                simpletripstotime[(stationid,pointer.statid,counter)]=newttt
                                lettertoskipped[symbols]=visitid
                                setlettertoskipped[symbols]=set(visitid)
                                
                                counter+=1
                        else:
                            endsset[(stationid,pointer.statid)]={(stationid,pointer.statid,counter)}
                            servicetonodes[datetoservices[date]].add((stationid,pointer.statid,counter))
                            datetonodes[date].add((stationid,pointer.statid,counter))

                            endstoletter[(stationid,pointer.statid,counter)]=chr(counter)#change to like a letter or smth?
                            lettertosymbol[chr(counter)]=symbols
                            temptttd=cstation.tripstotime
                            tempttta=prev.tripstotime
                            deptimes={((pointer.statid,counter),i[1]):temptttd[i] for i in temptttd if i[0]==otherstation.statid}
                            arrtimes={((i[0],counter),i[1]):tempttta[i] for i in tempttta if i[0]==pointer.statid}
                            newttt=dict()
                            for i in deptimes:
                                if i in arrtimes:
                                    newttt[i]=(deptimes[i][0],arrtimes[i][1])
                            simpletripstotime[(stationid,pointer.statid,counter)]=newttt
                            lettertoskipped[symbols]=visitid
                            setlettertoskipped[symbols]=set(visitid)

                            counter+=1
    else:
        datetoallworthy[date]=servicetoallworthy[datetoservices[date]]
        datetonodes[date]=servicetonodes[datetoservices[date]]

with open (system+' datetoallworthy.txt','w',encoding='utf-8')as f:
    f.write('\n'.join(sorted([' '.join((str(i),str(sorted([stoptoname[j] for j in datetoallworthy[i]])))) for i in datetoallworthy])))
with open (system+' datetonodes.txt','w',encoding='utf-8')as f:
    f.write('\n'.join(sorted([' '.join((str(i),str(sorted(datetonodes[i])))) for i in datetonodes])))
with open (system+' new simplified nodes.txt','w',encoding='utf-8')as f:
    f.write('\n'.join([str((stoptoname[i[0]],stoptoname[i[1]],i[2]))+'\t'+lettertosymbol[endstoletter[i]]+'\t'+str({stoptoname[j] for j in lettertoskipped[lettertosymbol[endstoletter[i]]]}) for i in endstoletter]))
with open (system+' new simplified tripstotime.txt','w',encoding='utf-8')as f:
    f.write(str(simpletripstotime))
endsworthykeys={j:{i for i in endstoletter if i[0]==j} for j in allworthy}
# print(len(allworthy))
print(len(set(i[0] for i in endstoletter)))
print(len(set(i[1] for i in endstoletter)))
print(counter-1)
print(rtrtrt.perf_counter()-cingcingcing)
#now, let's build the thing:
# for i in allworthy:
#     stat=stations[statidtostationindex[i]]
#     for j in stat.neighbors:
#         print(stat.name,j.name)
#         for k in j.neighbors:
#             print(k.name)
#             print(len(stat.neighbortotrips[j.statid]),len(j.neighbortotrips[k.statid]),len(stat.neighbortotrips[j.statid]&j.neighbortotrips[k.statid]))
simplistations=[]
statidtosimplistationindex={}
for n,i in enumerate(allworthy):
    ostation=stations[statidtostationindex[i]]
    statidtosimplistationindex[i]=n
    currentstation=SimpliStation(ostation)
    for j in endsworthykeys[i]:
        neighborname=j[1:]
        currentstation.neighbors_id.add(neighborname)
        direction=setlettertoskipped[lettertosymbol[endstoletter[j]]]&ostation.neighbors_id
        if len(direction)>1:
            print(currentstation.name,stoptoname[j[1]],{stoptoname[k] for k in direction})
        if len(direction)==0:
            currentstation.neighbortotrips[neighborname]=ostation.neighbortotrips[j[1]]
        else:
            currentstation.neighbortotrips[neighborname]=ostation.neighbortotrips[list(direction)[0]]
    simplistations.append(currentstation)
for i in simpletripstotime:
    simplistations[statidtosimplistationindex[i[0]]].tripstotime.update(simpletripstotime[i])
for i in simplistations:
    i.neighbors={(simplistations[statidtosimplistationindex[j[0]]],j[1]) for j in i.neighbors_id}
    i.transfers={simplistations[statidtosimplistationindex[j]] for j in i.transfers_id}
ckckck=sorted([(simplistations[i].statid,simplistations[i].name,simplistations[i].neighbors_id,simplistations[i].transfertotime) for i in range(len(simplistations))])
with open(system+' simplified neighbors.txt','w',encoding='utf-8') as f:
    f.write('\n'.join([' '.join([str(j) for j in i]) for i in ckckck]))

import pickle
with open(system+' pickled.txt','wb') as f:
    pickle.dump((datetrips,statidtochr,NUMBEROFSTATIONS,endstoletter,lettertosymbol,simplistations,statids,stoptoname,statidtosimplistationindex),f)


def astar_heur(timesincestart, prevline, numuni, numstat, stringofthings,routestring):
    # g=(timesincestart.seconds//60)
    # g+=(numstat-numuni)*(NUMBEROFSTATIONS/(2*NUMBEROFSTATIONS-numstat))
    # g+=numstat*1.5
    # h=NUMBEROFSTATIONS-numuni
    # # prevline gets high until end of route, worthyofstopping gets low, prevworthy gets high
    # if prevline:
    #     h-=0
    # if len(routestring)>1:
    #     curroute,path=routestring[0],routestring[1:]
    #     j=path.count(curroute)
    #     if j>0:
    #         h+=60000
    return timesincestart.seconds/numuni
    return g+h

# make set of all stations that are worthy of stopping at


# could make an algorithm that uses only the average (if applicable) of the times between stations in order to find path - basic version
# advanced version - define start date and time, 
from heapq import heappush, heappop
NUMSOLS=1
def a_star(start,starttime,startday): #for hueristic add thing for if previous station was a transfer station or smth
    startingdatetime=datetime.datetime.combine(startday,starttime)
    heur=astar_heur(datetime.timedelta(seconds=0),False,1,1,statidtochr[start.statid],'') 
    fringe=[(heur,-1,startingdatetime,0,1,statidtochr[start.statid],statidtochr[start.statid],'',start,tuple(),None,(None,))]#'"'+start.statid+'",',start,None)]
    sols=[]
    while len(fringe)>0:
        heuristic,numuni,timeofday,numunistatdiff,numstat,stringofthings,simplisot,routesot,curstation,timetuple,line,linetuple=heappop(fringe)
        # print(heuristic,numuni,timeofday,numunistatdiff,numstat,curstation.name)
        if -numuni==NUMBEROFSTATIONS:
            sols.append((timeofday,numuni,numstat,stringofthings,simplisot,curstation,timetuple,linetuple,routesot))
            if len(sols)==NUMSOLS:
                print(' '.join([str(i[2]) for i in sorted(sols)]))
                return sorted(sols)[0]
        childset=getchildren(curstation,timeofday.time(),timeofday.date())
        # with open('childset.txt','w',encoding='utf-8')as f:
        #     f.write(str((curstation.name,timeofday,childset,[statids[ord(i)] for i in stringofthings],[str(i) for i in timetuple])))
        # input()
        for nstat,countnumber,oldtime,newtime,nextline in childset:
            # print(nstat,countnumber,oldtime,newtime,nextline)
            if len(timetuple)==0:
                timetuple=(oldtime,)
            nsot=stringofthings
            if countnumber>0:
                nsot=nsot+lettertosymbol[endstoletter[(curstation.statid,nstat,countnumber)]]
                routesot=routesot+endstoletter[(curstation.statid,nstat,countnumber)]
            nsot=nsot+statidtochr[nstat]
            newstation=simplistations[statidtosimplistationindex[nstat]]
            nnuni=len(set(nsot))
            nasta=len(nsot)
            nheur=astar_heur(newtime-startingdatetime,nextline==line,nnuni,nasta,nsot,routesot)
            # print(nheur,nstat,oldtime,newtime)
            heappush(fringe,(nheur,-nnuni,newtime,-nnuni+nasta,nasta,nsot,simplisot+statidtochr[nstat],routesot,newstation,timetuple+(newtime,),nextline,linetuple+(nextline,)))
        # input()
dingdingding=rtrtrt.perf_counter()
tim='08:00:00'
dat='2022-12-18'
# tim='00:00:00'
# dat='2018-01-01'
# dat='2022-11-01'
# import cProfile, pstats, io
# profiler = cProfile.Profile()
# profiler.enable()
startstats={'kochi':'ALVA', 'dc':'STN_N12', 'la': '80201S','nyc':'H11','sf':'place_ANTC','atlanta':'730'}
# try:
if True:
    solution=a_star(simplistations[statidtosimplistationindex[startstats[system]]],datetime.time.fromisoformat(tim),datetime.date.fromisoformat(dat))
    # print(tuple(str(i) for i in solution[6]))
    print('solution found in %s seconds :)'%(rtrtrt.perf_counter()-dingdingding))
    with open(system+' solution simplified.txt','w',encoding='utf-8') as f:
        f.write('\n'.join([stoptoname[statids[ord(solution[4][i])]]+' ('+statids[ord(solution[4][i])]+') - '+str(solution[6][i])+' '+str(solution[7][i]) for i in range(len(solution[4]))]))
# except:
#     print('error after %s seconds :('%(rtrtrt.perf_counter()-dingdingding))
# s = io.StringIO()
# ps = pstats.Stats(profiler, stream=s).sort_stats('tottime')
# ps.print_stats()

# with open(system+' test.txt', 'w+') as f:
    # f.write(s.getvalue())
