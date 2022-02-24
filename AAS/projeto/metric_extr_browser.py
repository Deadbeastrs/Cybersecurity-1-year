import sys
import argparse
import datetime
from netaddr import IPNetwork, IPAddress, IPSet
import pyshark
import json
import re
import datetime
import ijson

def get_entry_items(filepath):

    logs = []
    count = 0
    entry = ["","","",""] #[startDateTime, cookies, url,status]
    for prefix, the_type, value in ijson.parse(open(filepath)):
    
            
        if prefix == "log.entries.item.request.cookies.item.name":
            if value == "LOGIN_INFO" or value == "authenticated" or value == "__asc":
                if entry[1] == "":

                    entry[1] = str(value) 
                else:
                    entry[1] = entry[1]+ "," + str(value)

        if prefix == "log.entries.item.request.url" :
            entry[2] = value
            
        if prefix == "log.entries.item.response.status":
            entry[3] = value
            

        if prefix == "log.entries.item.startedDateTime" :
            
            entry[0] = value
            logs.append(entry)
            entry = ["","","",""]
    return logs

def apacheHandler(filePath,sampDelta=1):
    global nLogs
    global outc
    global T0
    global listOfVisited
    global listOfMetrics
    global startTimeStamp

    logs = get_entry_items(filePath)
    
    for entry in logs :
        
        date_time_obj = datetime.datetime.fromisoformat(str(entry[0]).replace("Z",""))
        timestamp = datetime.datetime.timestamp(date_time_obj)
        if timestamp >= startTimeStamp:
            if nLogs==0:
                T0=float(timestamp)
                last_ks=0
                
            ks=int((float(timestamp)-T0)/sampDelta)
            
            if ks>last_ks:
                listOfMetrics.append(outc)
                outc=[0,0,0,0]
                listOfVisited = []
                
            if ks>last_ks+1:
                for j in range(last_ks+1,ks):  
                    listOfMetrics.append(outc)
                    outc=[0,0,0,0]

            if entry[3]== 404: #errors
                outc[1]=outc[1]+1

            if outc[2] != 1:
                cookies = entry[1].split(",")
                for cookie in cookies : #2021-12-28T18:34:15.341+00:00"
                    if (cookie=="LOGIN_INFO" or cookie=="authenticated" or cookie=="__asc") :
                        outc[2] = 1
            
            tempUrl = re.sub(r'\?.*$',"",entry[2])
            if tempUrl not in listOfVisited:
                listOfVisited.append(tempUrl)
                outc[3]=outc[3]+1

            last_ks=ks
            nLogs=nLogs+1
            outc[0]=outc[0]+1

def pktHandler(pkt,sampDelta=1):

    global listofsources
    global scnets
    global ssnets
    global npkts
    global T0
    global outc1
    global outc2
    global last_ks
    global startTimeStamp
    global listOfMetricsPck
    global listOfMetricsDNS
    
    timestamp,srcIP,dstIP,lengthIP,protocol=pkt.sniff_timestamp,pkt.ip.src,pkt.ip.dst,pkt.ip.len,pkt.ip.proto

    if float(timestamp) > float(startTimeStamp):
        if (IPAddress(srcIP) in scnets and IPAddress(dstIP) in ssnets) or (IPAddress(srcIP) in ssnets and IPAddress(dstIP) in scnets):
            if npkts==0:
                T0=float(timestamp)
                last_ks=0
                
            ks=int((float(timestamp)-T0)/sampDelta)
            
            if ks>last_ks:
                listOfMetricsPck.append(outc1)
                listOfMetricsDNS.append(outc2)
                outc1=[0,0,0,0,0]
                outc2=[0,0]
                
            if ks>last_ks+1:
                for j in range(last_ks+1,ks):
                    listOfMetricsPck.append(outc1)
                    listOfMetricsDNS.append(outc2)
                    outc1=[0,0,0,0,0]
                    outc2=[0,0]
                    
            if IPAddress(srcIP) in scnets and IPAddress(dstIP) in scnets:
                outc1[0]=outc1[0]+1
                outc1[1]=outc1[1]+int(lengthIP)
                
                if int(protocol) == 6:
                    outc1[2]=outc1[2]+1
                elif int(protocol) == 17:
                    outc1[3]=outc1[3]+1
                elif int(protocol) == 1:
                    outc1[4]=outc1[4]+1
                    
            last_ks=ks
            npkts=npkts+1
        
        try:
            
            if ((int(str(pkt.dns.flags), 16)>>15) & 0x1) == 0:
                outc2[0] = outc2[0] + 1
            
            if (int(str(pkt.dns.flags), 16) & 0x000F) != 0:
                outc2[1] = outc2[1] + 1
        except:
            ola = 1

        


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',required=True, help='input file pcap')
    parser.add_argument('-f', '--format', nargs='?',required=True, help='format',default=1)
    parser.add_argument('-c', '--cnet', nargs='+',required=True, help='client network(s)')
    parser.add_argument('-s', '--snet', nargs='+',required=True, help='service network(s)')
    parser.add_argument('-b', '--browser', nargs='+',required=True, help='browser logs (har)')
    parser.add_argument('-o', '--output', nargs='?',required=True, help='output file name')
    
    args=parser.parse_args()
    
    cnets=[]

    global nLogs
    global T0
    global outc
    global outc1
    global outc2
    global last_ks
    global listOfVisited
    global listOfMetrics
    global listOfMetricsPck
    global listOfMetricsDNS

    outc=[0,0,0,0]
    outc1=[0,0,0,0,0]
    outc2 = [0,0]
    listOfVisited = []
    listOfMetrics = []
    listOfMetricsPck = []
    listOfMetricsDNS = []
    nLogs = 0
    output = open(args.output,"w")
    output.write("Num.pkt, sum pkt size, sum TCP,sum UDP, sum ICMP, Num.Apache.Req.Res, Num.error,Logged?,Num.Diff.Pages,Num.Dns.query,Num.Dns.Error\n")
    for n in args.cnet:
        try:
            nn=IPNetwork(n)
            cnets.append(nn)
        except:
            print('{} is not a network prefix'.format(n))
    #print(cnets)
    if len(cnets)==0:
        print("No valid client network prefixes.")
        sys.exit()
    global scnets
    scnets=IPSet(cnets)

    snets=[]
    for n in args.snet:
        try:
            nn=IPNetwork(n)
            snets.append(nn)
        except:
            print('{} is not a network prefix'.format(n))
    #print(snets)
    if len(snets)==0:
        print("No valid service network prefixes.")
        sys.exit()
        
    global ssnets
    ssnets=IPSet(snets)
        
    fileInput=args.input
    fileFormat=int(args.format)
        
    global npkts
    global listofsources
    global startTimeStamp
    

    npkts=0
    outc=[0,0,0,0]
    sampDelta=1

    if fileFormat in [1,2]:
        file = open(fileInput,'r') 
        for line in file: 
            pktData=line.split()
            if fileFormat==1 and len(pktData)==9: #script format
                timestamp,srcIP,dstIP,lengthIP=pktData[0],pktData[4],pktData[6],pktData[8]
                pktHandler(timestamp,srcIP,dstIP,lengthIP,sampDelta)
            elif fileFormat==2 and len(pktData)==4: #tshark format "-T fileds -e frame.time_relative -e ip.src -e ip.dst -e ip.len"
                timestamp,srcIP,dstIP,lengthIP=pktData[0],pktData[1],pktData[2],pktData[3]
                pktHandler(timestamp,srcIP,dstIP,lengthIP,sampDelta)
        file.close()
    elif fileFormat==3: #pcap format
        for prefix, the_type, value in ijson.parse(open(str(args.browser[0]))):
            if prefix == "log.entries.item.startedDateTime" :
                teste1 = value
                date_time_obj = datetime.datetime.fromisoformat(str(value).replace("Z",""))
                timestamp = datetime.datetime.timestamp(date_time_obj)
                break
        
        capture = pyshark.FileCapture(fileInput)
        if float(capture[0].sniff_timestamp) > float(timestamp) :
            startTimeStamp = float(capture[0].sniff_timestamp)
        else:
            startTimeStamp = float(timestamp)
        for pkt in capture:
            pktHandler(pkt,sampDelta)

        apacheHandler(str(args.browser[0]),1)
 
        finalList = []

        for i in range(0,len(listOfMetricsPck)):
            finalList.append(listOfMetricsPck[i])
            if i < len(listOfMetrics):
                finalList[i] = finalList[i] + listOfMetrics[i]
            else:
                finalList[i] = finalList[i] + [0,0,0,0]
            if i < len(listOfMetricsDNS):
                finalList[i] = finalList[i] + listOfMetricsDNS[i]
            else:
                finalList[i] = finalList[i] + [0,0]
            
        
        [output.write(str(i).replace("[","").replace(",","  ").replace("]","") + "\n") for i in finalList]

        



       
    


if __name__ == '__main__':
    main()
