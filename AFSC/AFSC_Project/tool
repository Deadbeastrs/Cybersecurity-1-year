#!/bin/bash
out="none"
md5gen="no"
declare -A info_vm

general_html_code='<!DOCTYPE html>             
<html>
   <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>    td {
        text-align: center;
      }         #myDIV {                 width: 100%;                 padding: 50px 0;                 text-align: center;                 background-color: lightblue;                 margin-top: 20px;             }             table {                 border-collapse: collapse;                 border-spacing: 0;                 width: 100%;                 border: 1px solid #ddd;             }                          th, td {                 text-align: center;                 padding: 16px;             }                          th:first-child, td:first-child {                 text-align: left;             }                          tr:nth-child(even) {                 background-color: #f2f2f2             }                          .fa-check {                 color: green;             }                          .fa-remove {                 color: red;             }             .collapsible {                 background-color: #777;                 color: white;                 cursor: pointer;                 padding: 18px;                 width: 100%;                 border: none;                 text-align: left;                 outline: none;                 font-size: 15px;             }             .active, .collapsible:hover {                 background-color: #555;             }                          .content {                 padding: 0 18px;                 display: none;                 overflow: hidden;                 background-color: #f1f1f1;             }             </style>
   </head>
   <body bgcolor="#d7dfe2">
    <h1 align="center">Forensic Tool Report</h1>
    <p></p>
    <h2>Virtual Machines Overview</h2>
    <p></p>
    {VmInfo}

    <p></p>
    <h2>Discoved Virtual Machines Disks:</h2>
    <p></p>
    {DiskInfo}
    <p></p>
      <script>             var coll = document.getElementsByClassName("collapsible");             var i;             for (i = 0; i < coll.length; i++) {                 coll[i].addEventListener("click", function() {                     this.classList.toggle("active");                     var content = this.nextElementSibling;                     if (content.style.display === "block") {                         content.style.display = "none";                     } else {                         content.style.display = "block";                     }                 });             }             </script>                          
   </body>
</html>
'
general_html_code_base="$general_html_code"
vm_html='
    <button class=\"collapsible\">Virtual Machine {Id}</button>             
    <div class=\"content\" style=\"background-color: #d7dfe2;\">
    <p></p>
    <div style=\"border-style: solid;background-color: white\">
        <table style=\"text-align: center;\">
            <tr>
            <th>Id:</th>
            <td>{Id}</td>
            </tr>
            <tr>
            <th>Name:</th>
            <td>{Name}</td>
            </tr>
            <tr>
            <th>State:</th>
            <td>{State}</td>
            </tr>
            <tr>
            <th>Os:</th>
            <td>{OS}</td>
            </tr>
            <tr>
            <th>Uptime:</th>
            <td>{Uptime}</td>
            </tr>
            <tr>
            <th>Virt.:</th>
            <td>{Virt}</td>
            </tr>
            <tr>
            <th>Disks:</th>
            <td>
                <p>{Disk}
                <p>{Hash}
            </td>
            </tr>
        </table>
    </div>
    </div>
    <p></p>
    '

vm_html_base="$vm_html"

Menu(){
    echo "Available Tools:"
    echo ""
    echo "vmlist        - list all virtual machines"
    echo "vmdisks       - list all virtual machines disks in system"
    echo "vmactions     - actions on all virtual machines running"
    echo "vdi_vmdk      - convert vmi to vmdk or vice versa"
    echo "gen_report    - generate a report with the VM's information"
    echo "help          - display the menu"
    echo "exit          - closes the script"
}

fileVmListReplace() {
    temp=$vm_html
    vm_html=`echo $temp | awk "{gsub(/$1/,\"$2\") ; print}" 2> /dev/null`
}

fileVmListAdd() {
    temp=$vm_html
    vm_html=`echo $temp | awk "{gsub(/$1/,\"$2</p>$1\") ; print}" 2> /dev/null`
}

htmlGenListAdd() {
    general_html_code=`echo $general_html_code | awk "{gsub(/$1/,\"$2$1\") ; print}" 2> /dev/null`
}

htmlGenListAdd_2() {
    general_html_code=`echo $general_html_code | awk "{gsub(/$1/,\"$2<br><br>$1\") ; print}" 2> /dev/null`
}

print() {
    if [[ $out == "rep_vmlist" ]];then
        if [[ $1 =~ ":" ]];then
            IFS=':'
            vmList=($1)
            unset IFS
            vmList_0=`echo "{${vmList[0]}}" | sed -e 's/ //g'`
            vmList_1=`echo "${vmList[1]}"`
            if [[ "$vmList_0" == "{Disk}" || "$vmList_0" == "{Hash}" ]];then
                fileVmListAdd "$vmList_0" "$vmList_1"
            else
                fileVmListReplace "$vmList_0" "$vmList_1"
            fi
        fi
    elif [[ $out == "rep_vmdisks" ]]; then
        if [[ $1 =~ "/" ]];then
            htmlGenListAdd_2 "{DiskInfo}" "$1"
        fi
    elif [[ $out == "none" ]]; then
        echo "" > /dev/null
    else
        echo "$1"
    fi
}

diskList() {
    print "" 
    print "List of all disk files in the system:" 
    print "" 
    dirp=`find / -type f \( -iname \*.vmdk -o -iname \*.qcow2 -o -iname \*.vdi \) 2> /dev/null | tr '\n' '|'` 
    IFS='|'
    dirlist=($dirp)
    unset IFS
    for dir in "${dirlist[@]}"
    do  
        print "$dir"
        print "" 
    done
}

vbList() {
    listVB_str=`VBoxManage list vms 2> /dev/null | sed -e 's/{.*}//g' -e 's/"//g' -e 's/[ ]/;/g'`
    listVB=(${listVB_str//;/ })
    vmId1=$1
    for vmName in "${listVB[@]}"
    do  
        vmUptime=""
        vmInfo=`VBoxManage showvminfo $vmName 2> /dev/null`
        vmOS=`echo $vmInfo | sed -e 's/^.*Guest OS://g' -e 's/ UUID:.*$//g' -e 's/ //g'`
        vmState=`echo $vmInfo | sed -e 's/^.*State://g' -e 's/^ //g' -e 's/ Graphics Controller:.*$//g' -e 's/(.*$//g'`
        vmDisks=`echo $vmInfo | sed -e 's/^.*on IDE//g' -e 's/NIC 1: .*$//g' -e 's/([0-9], [0-9]):/|/g'`
        vmApplication="VirtualBox"
        vmUuid=`echo $vmInfo | sed -e 's/^.*Hardware UUID://g' -e 's/Memory.*$//g' -e 's/ //g'`
        vmProcess=`ps -eo etime,command | grep $vmUuid | grep -v grep`
        temp=(${vmProcess// / })
        if [[ ${temp[0]} == "" ]];then
            vmUptime=""
        else
            vmUptime=`echo "${temp[0]}sec" | sed -e 's/:/min /g'`
        fi
        print "" 
        print "Id: $vmId1" 
        print "" 
        print "  Name    : $vmName" 
        print "  State   : $vmState" 
        print "  OS      : $vmOS" 
        print "  Uptime  : $vmUptime" 
        print "  Virt   : $vmApplication" 
        print "  Disks: " 
        info_vm[$vmId1]="$vmName|$vmApplication";
        vmId1=$(( $vmId1 + 1 ))
        IFS='|'
        vmDisksList=($vmDisks)
        unset IFS
        for vmDisk in "${vmDisksList[@]}"
        do  
            pathT=`echo $vmDisk | sed -e 's/ (.*$//g' -e 's/ /\\ /g'`
            if [[ $vmDisk != " " ]]; then
                if [ -f "$pathT" ]; then
                    pathT1=`echo $pathT | sed -e 's/ /\\\ /g'` 
                    print "      Disk : $pathT1" 
                    if [[ "$2" == "yes" ]]; then
                        hash=`eval md5sum $pathT1`
                        print "      Hash : ${hash:0:16} (MD5)"
                    fi
                fi
            fi
        done
        htmlGenListAdd "{VmInfo}" "$vm_html"
        vm_html="$vm_html_base"
        print "" 
        print "***********" 
    done
    return $vmId1
}

qemuList(){
    listVB_str=`virsh list --name --all 2> /dev/null`
    listVB=(${listVB_str//\\n/ })
    vmId1=$1
    for vmName in "${listVB[@]}"
    do  
        vmInfo=`virsh dominfo $vmName 2> /dev/null`
        vmState=`echo $vmInfo | sed -e 's/^.*State://g' -e 's/ CPU(s).*$//g' -e 's/ //g'`
        vmUuid=`echo $vmInfo | sed -e 's/^.*UUID://g' -e 's/OS Type:.*$//g' -e 's/ //g'`
        vmProcess=`ps -eo etime,label | grep $vmUuid | grep -v grep`
        temp=(${vmProcess// / })
        if [[ ${temp[0]} == "" ]];then
            vmUptime=""
        else
            vmUptime=`echo "${temp[0]}sec" | sed -e 's/:/min /g'`
        fi
        vmApplication="QEMU_KVM"
        print "" 
        print "Id: $vmId1" 
        print "" 
        print "  Name    : $vmName" 
        print "  State   : $vmState" 
        print "  OS      : $vmOS" 
        print "  Uptime  : $vmUptime" 
        print "  Virt    : $vmApplication" 
        print "  Disks: " 
        info_vm[$vmId1]="$vmName|$vmApplication";
        vmId1=$(( $vmId1 + 1 ))
        vmDisks=`virsh domblklist $vmName 2> /dev/null | tr '\n' '|' | sed -e 's/.*---//g' | sed -e 's/.*Source//g'`
        IFS='|'
        vmDisksList=($vmDisks)
        unset IFS
        for vmDisk in "${vmDisksList[@]}"
        do  
            if [[ $vmDisk != "" ]]; then
                vmDiskPath=`echo $vmDisk | sed -e 's/^.* \///g' | sed -e 's/^.* \-//g'`
                if [[ $vmDiskPath != "" ]]; then
                    vmDiskPath="/$vmDiskPath"
                    print "      Disk : $vmDiskPath" 
                    hash=`eval md5sum $vmDiskPath 2>/dev/null `
                    if [[ "$2" == "yes" ]]; then
                        if [ -n "$hash" ]; then
                            print "      Hash : ${hash:0:16} (MD5)" 
                        else
                            print "      Hash : MD5 Permission Denied" 
                        fi
                    fi
                fi
            fi
        done
        htmlGenListAdd "{VmInfo}" "$vm_html"
        vm_html="$vm_html_base"
        print "" 
        print "***********" 
    done
    return $vmId1
}

echo "Forensic tool - 2021/2022 - AFSC" 
echo "" 
vmId=0
qemuList $vmId "no"
vmId=$?
vbList $vmId "no"
out="cons"

if [[ $1 == "md5" ]];then
    md5gen="yes"
fi

Menu

while :
do
    echo "" 
    echo "Choose an option:"
    read option

    case $option in

    vmlist)
        vmId=0
        qemuList $vmId $md5gen
        vmId=$?
        vbList $vmId $md5gen
        ;;

    vmdisks)
        diskList
        ;;

    vmactions)
        # Prossible actions: start, stop, snapshot <path>
        echo "Possible actions: start <id>, stop <id>, snapshot <id>" 
        read actionOp
        vmId=`echo $actionOp | sed -e 's/start //g' -e 's/stop //g' -e 's/snapshot //g' `
        vmAction=`echo $actionOp | sed -e 's/ .*$//g' -e 's/ //g'`
        case $vmAction in
            start)
                if [[ ${info_vm[$vmId]} =~ "VirtualBox" ]]; then
                    vmName=`echo ${info_vm[$vmId]} | sed -e 's/|VirtualBox//g'`  
                    echo "" 
                    VBoxManage startvm $vmName 2> /dev/null
                elif [[ ${info_vm[$vmId]} =~ "QEMU/KVM" ]]; then
                    vmName=`echo ${info_vm[$vmId]} | sed -e 's/|QEMU\/KVM//g'`
                    echo "" 
                    virsh start $vmName 2> /dev/null
                fi
            ;;

            stop)
                if [[ ${info_vm[$vmId]} =~ "VirtualBox" ]]; then
                    vmName=`echo ${info_vm[$vmId]} | sed -e 's/|VirtualBox//g'`
                    echo ""   
                    VBoxManage controlvm $vmName poweroff 2> /dev/null
                elif [[ ${info_vm[$vmId]} =~ "QEMU/KVM" ]]; then
                    vmName=`echo ${info_vm[$vmId]} | sed -e 's/|QEMU\/KVM//g'`
                    echo "" 
                    virsh destroy $vmName 2> /dev/null
                fi
            ;;

            snapshot)
                if [[ ${info_vm[$vmId]} =~ "VirtualBox" ]]; then
                    vmName=`echo ${info_vm[$vmId]} | sed -e 's/|VirtualBox//g'`
                    echo ""  
                    VBoxManage snapshot $vmName take "$vmName-$vmId" 2> /dev/null
                elif [[ ${info_vm[$vmId]} =~ "QEMU/KVM" ]]; then
                    vmName=`echo ${info_vm[$vmId]} | sed -e 's/|QEMU\/KVM//g'`
                    echo "" 
                    virsh snapshot-create-as --domain $vmName --name "$vmName-$vmId" 2> /dev/null
                fi
            ;;
        esac
        ;;

    vdi_vmdk)
        echo ""
        echo "Before converting the files, make sure to detatch the vdi/vmdk from VirtualBox/VmWare"
        echo ""
        echo "Choose one of the folowing commands:" 
        echo "vdi_vmdk <source> <destination> or vmdk_vdi <source> <destination>" 
        read com
        if [[ $com =~ "vdi_vmdk" ]]; then
            procCom=`echo $com | sed -e 's/vdi_vmdk//g' `
            listArgs=(${procCom// / })
            VBoxManage clonehd "${listArgs[0]}" "${listArgs[1]}" -format VMDK -variant standard
        elif [[ $com =~ "vmdk_vdi" ]]; then
            procCom=`echo $com | sed -e 's/vmdk_vdi//g' `
            listArgs=(${procCom// / })
            VBoxManage clonehd "${listArgs[0]}" "${listArgs[1]}" -format VDI -variant standard
        fi
        ;;
    
    gen_report)
        echo "" 
        echo "Input the report filename:"
        read com_name
        out="rep_vmlist"
        general_html_code=$general_html_code_base
        vmId=0
        qemuList $vmId $md5gen
        vmId=$?
        vbList $vmId $md5gen
        out="rep_vmdisks"
        diskList
        general_html_code=`echo $general_html_code | sed -e 's/{VmInfo}//g' -e 's/{Disk}//g' -e 's/{Hash}//g' -e 's/{DiskInfo}//g'`
        echo $general_html_code > "$PWD/$com_name.html"
        general_html_code=$general_html_code_base
        out="cons"
        ;;
    
    help)
        Menu
        echo "" 
        ;;
    
    exit)
        exit 0
        ;;

    *)
        echo "Invalid Command" 
        echo "" 
        ;;
    esac
done
