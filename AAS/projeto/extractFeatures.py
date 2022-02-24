import argparse
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from baseObsWindows import slidingObsWindow
import requests
import geopy
import geopy.distance 
from numpy import savetxt

global s_coords
s_coords = (40.636277,-8.656569)

def extractStats(data):
    global s_coords
    global args
    
    nSamp,nCols=data.shape
    timeBetweenRequests = []
    counter = 0
    
    for i in range(0,len(data)-1):
        
        if int(data[i][5]) >= 1 and int(data[i+1][5]) >= 1:
            timeBetweenRequests.append(0)
        elif (int(data[i][5]) == 0 and int(data[i+1][5]) == 0) or (int(data[i][5]) >= 1 and int(data[i+1][5]) == 0):
            counter = counter + 1
        elif int(data[i][5]) == 0 and int(data[i+1][5]) >= 1:
            timeBetweenRequests.append(counter)
            counter=0
    
    if len(timeBetweenRequests) == 0:
        timeBetweenRequests.append(counter)
    
    Var_Req=np.var(timeBetweenRequests)
    
    Var_Req_Apache=np.var([a[8] for a in data])

    response = requests.get("https://geolocation-db.com/json/"+args.ip+"&position=true").json()
    
    coords_2 = (response['latitude'],response['longitude'])

    Var_Distance_IP = int(geopy.distance.distance(s_coords, coords_2).km)
    


    #Num_packets = np.sum([a[0] for a in data])
    Num_packets_Mean = np.mean([a[0] for a in data])
    Num_packets_Max = np.max([a[0] for a in data])
    Num_packets_Min = np.min([a[0] for a in data])

    #Pkt_sum = np.sum([a[1] for a in data])
    Pkt_size_Mean = np.mean([a[1] for a in data])
    Pkt_size_Max = np.max([a[1] for a in data])
    Pkt_size_Min = np.min([a[1] for a in data])

    #TCP_sum = np.sum([a[2] for a in data])
    TCP_Mean = np.mean([a[2] for a in data])
    TCP_Max = np.max([a[2] for a in data])
    TCP_Min = np.min([a[2] for a in data])

    #UDP_sum = np.sum([a[3] for a in data])
    UDP_Mean = np.mean([a[3] for a in data])
    UDP_Max = np.max([a[3] for a in data])
    UDP_Min = np.min([a[3] for a in data])
    
    #ICMP_sum = np.sum([a[4] for a in data])
    ICMP_Mean = np.mean([a[4] for a in data])
    ICMP_Max = np.max([a[4] for a in data])
    ICMP_Min = np.min([a[4] for a in data])

    #APACHE_sum = np.sum([a[5] for a in data])
    APACHE_Mean = np.mean([a[5] for a in data])
    APACHE_Max = np.max([a[5] for a in data])
    APACHE_Min = np.min([a[5] for a in data])
    
    #ERROR_APACHE_sum = np.sum([a[6] for a in data])
    ERROR_APACHE_Mean = np.mean([a[6] for a in data])
    ERROR_APACHE_Max = np.max([a[6] for a in data])
    ERROR_APACHE_Min = np.min([a[6] for a in data])


    APACHE_LOGIN = 0 if np.sum([a[7] for a in data])==0 else 1

    #ERROR_DNS_sum = np.sum([a[10] for a in data])
    ERROR_DNS_Mean = np.mean([a[10] for a in data])
    ERROR_DNS_Max = np.max([a[10] for a in data])
    ERROR_DNS_Min = np.min([a[10] for a in data])


    #QUERY_DNS_sum = np.sum([a[9] for a in data])
    QUERY_DNS_Mean = np.mean([a[9] for a in data])
    QUERY_DNS_Max = np.max([a[9] for a in data])
    QUERY_DNS_Min = np.min([a[9] for a in data])

    #features=np.hstack((Num_packets,Pkt_sum,TCP_sum,UDP_sum,ICMP_sum,APACHE_sum,APACHE_LOGIN,Var_Req,Var_Req_Apache,Var_Distance_IP))
    features = np.hstack((Num_packets_Mean,Num_packets_Max,Num_packets_Min,
                          
                          Pkt_size_Mean,Pkt_size_Max,Pkt_size_Min,  
                          
                          TCP_Mean,TCP_Max,TCP_Min,
                          
                          UDP_Mean,UDP_Max,UDP_Min,
                          
                          ICMP_Mean,ICMP_Max,ICMP_Min,
                          
                          APACHE_Mean,APACHE_Min,APACHE_Max,
                          
                          ERROR_APACHE_Mean,ERROR_APACHE_Max,ERROR_APACHE_Min,
                          
                          APACHE_LOGIN,Var_Req_Apache,Var_Req,Var_Distance_IP,
                          
                          ERROR_DNS_Mean,ERROR_DNS_Max,ERROR_DNS_Min,
                          
                          QUERY_DNS_Mean,QUERY_DNS_Min,QUERY_DNS_Max))
    return(features)

def extratctSilenceActivity(data,threshold=0):
    if(data[0]<=threshold):
        s=[1]
        a=[]
    else:
        s=[]
        a=[1]
    for i in range(1,len(data)):
        if(data[i-1]>threshold and data[i]<=threshold):
            s.append(1)
        elif(data[i-1]<=threshold and data[i]>threshold):
            a.append(1)
        elif (data[i-1]<=threshold and data[i]<=threshold):
            s[-1]+=1
        else:
            a[-1]+=1
    return(s,a)
    
def extractStatsSilenceActivity(data):
    features=[]
    nSamples,nMetrics=data.shape
    silence_features=np.array([])
    activity_features=np.array([])
    for c in range(nMetrics):
        silence,activity=extratctSilenceActivity(data[:,c],threshold=0)
        
        if len(silence)>0:
            silence_faux=np.array([len(silence),np.mean(silence),np.std(silence)])
        else:
            silence_faux=np.zeros(3)
        silence_features=np.hstack((silence_features,silence_faux))
        
        if len(activity)>0:
            activity_faux=np.array([len(activity),np.mean(activity),np.std(activity)])
        else:
            activity_faux=np.zeros(3)
        activity_features=np.hstack((activity_features,activity_faux))       
            
    features=np.hstack((silence_features,activity_features))
        
    return(features)

def extractFeatures(obsData):
    if type(obsData) is list:
        nLengthsObsWindow=len(obsData)
        nObs,nSamples,nMetrics=obsData[0].shape
    else:
        nLengthsObsWindow=1
        print(obsData.shape)
        nObs,nSamples,nMetrics=obsData.shape

    obsFeatures=np.zeros((0,140))
    #print("windows->" + str(obsData))
    for o in range(0,nObs):
        features=np.array([])
        for n in range(0,nLengthsObsWindow):
            
            if type(obsData) is not list:
                subdata=obsData[o]
            else:
                subdata=obsData[n][o]
 
            faux=extractStats(subdata)
            
            faux2 = None
            features=np.hstack((features,faux))
        if o==0:
            obsFeatures=features
        else:
            obsFeatures=np.vstack((obsFeatures,features))

    return obsFeatures

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',required=True, help='input file')
    parser.add_argument('-ip', '--ip', nargs='?',required=True, help='ip')
    parser.add_argument('-o', '--output', nargs='?',required=True, help='output file')
    global args
    args=parser.parse_args()
    
    fileInput=args.input
        
    data=np.loadtxt(fileInput,dtype=int)
            
    lengthObsWindow=10
    slidingValue=3
    obsData=slidingObsWindow(data,lengthObsWindow,slidingValue)
    features=extractFeatures(obsData)
    
    savetxt(args.output, features, delimiter=',')
        

if __name__ == '__main__':
    main()
