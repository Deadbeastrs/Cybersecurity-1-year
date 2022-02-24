<#
get-vm "Ubuntu 20.04" | Select-Object ID,Name,State,Path,Uptime; get-vmharddiskdrive -VMName "Ubuntu 20.04"|Select-Object Path     -> get vm hyper-v info
Checkpoint-VM -Name 'Windows Server 2016' -SnapshotName Update1
Test-VHD -Path C:\Testing.vhd             -> see if file exists
Get-FileHash "C:\Program Files\FabFilter\Readme.txt"  -Algorithm MD5 | Select-object Hash | Format-List        --> Hash to md5 (in this case)
$ErrorActionPreference = "SilentlyContinue"

#>

$ErrorActionPreference = "SilentlyContinue"
$md5

function menufunc{
    Write-Host "

    Choose an option:

vmlist          - list all virtual machines
vmdisk          - search of disks on the host OS
vmactions       - actions on all virtual machines 
vhd_vhdx        - convert vhd to vhdx or vice versa
gen_report      - generate a report with the VM's information
help            - display the menu
exit            - closes the script"
}


function vhd_vhdx{
    Write-Host " 
     VHD <-> VHDX Converter
     (to leave type exit at any point) 
    "
    $src = Read-Host -Prompt "Insert path to source file: "
    if($src -eq "exit"){
        Write-Host "Exiting..."
        pause
        clear
        return

    }
    if(test-vhd $src){}
    else
    {
        Write-host "Source path not valid. Try again..."
        pause
        clear
        return
    }

    $dst = Read-Host -Prompt "Insert the destination path: "
    if($dst -eq "exit"){
        Write-Host "Exiting..."
        pause
        clear
        return

    }


    $ext =Read-Host -Prompt "Choose the destination extension(vhd or vhdx) "
    if($ext -eq "exit"){
        Write-Host "Exiting..."
        pause
        clear
        return
    }
    elseif($ext -eq "vhdx"){
        Convert-VHD -Path $src -DestinationPath $dst".vhdx"
    }
    elseif($ext -eq "vhd"){
        Convert-VHD -Path $src -DestinationPath $dst".vhd"
    }
    else{
    Write-Host " Incorrect file type. Aborting..."
    pause
    return
    }
    Write-Host "Operation Sucessfull."
    pause
    clear
    return


}

function gen_report{

$vms = GET-VM

$name = @()
$state = @()
$uptime = @()
$path = @()
$hash = @()
$vms | ForEach-Object{$name += $_.Name}
$vms | ForEach-Object{$state += $_.State}
$vms | ForEach-Object{$uptime += $_.uptime}

Foreach ($vm in $vms)
{
  $HardDrives = $vm.HardDrives
  Foreach ($HardDrive in $HardDrives)
  {
    $path += $HardDrive.path
    if($md5){
        $hash += Get-FileHash $HardDrive.path -Algorithm MD5 | Select-Object Hash | ft -HideTableHeaders
    }
    $hash += "Hash Deactivated"
    
  }
}
Write-Host "==============================================================" 
for($i = 0; $i -lt $name.count ;$i++){

$vm_button +='
    <button class="collapsible">Virtual Machine '+ $i+'</button>             
    <div class="content" style="background-color: #d7dfe2;">
    <p></p>
    <div style="border-style: solid;background-color: white">
        <table style="text-align: center;">
            <tr>
            <th>Id:</th>
            <td>'+$i+'</td>
            </tr>
            <tr>
            <th>Name:</th>
            <td>'+$($name[$i])+'</td>
            </tr>
            <tr>
            <th>State:</th>
            <td>'+$($state[$i])+'</td>
            </tr>
            <tr>
            <th>Os:</th>
            <td>Undefined</td>
            </tr>
            <tr>
            <th>Uptime:</th>
            <td>'+$($uptime[$i])+'</td>
            </tr>
            <tr>
            <th>Virt.:</th>
            <td>Hyper-V</td>
            </tr>
            <tr>
            <th>Disks:</th>
            <td>
                <p>'+$($path[$i])+'
                <p>'+$($hash[$i])+'
            </td>
            </tr>
        </table>
    </div>
    </div>
    <p></p>
    '
}



$general_html_code_1='<!DOCTYPE html>             
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
    <p></p>'



$part2='<p></p>
    <h2>Other Discovered Virtual Machines Disks:</h2>
    <p></p>'

$paths = Get-ChildItem C:\ -Include *.vhd,*.vhdx,*.avhdx -File -Recurse -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName | ft -HideTableHeaders | Out-String

$diskinfo
Foreach($pt in $paths){
$diskinfo += "<p>$pt</p></b>
"
}

$part3='<p></p>
      <script>             var coll = document.getElementsByClassName("collapsible");             var i;             for (i = 0; i < coll.length; i++) {                 coll[i].addEventListener("click", function() {                     this.classList.toggle("active");                     var content = this.nextElementSibling;                     if (content.style.display === "block") {                         content.style.display = "none";                     } else {                         content.style.display = "block";                     }                 });             }             </script>                          
   </body>
</html>
'


$general_html_code_1| Out-File -FilePath C:\report.html
$vm_button | Add-Content C:\report.html
$part2 |Add-Content C:\report.html
$diskinfo|Add-Content C:\report.html  
$part3 |Add-Content C:\report.html 

Write-Host 'Operation Successful. Report saved: "C:\report.html" '
}

function vmdisk{
Write-Host "Searching for non disclosured disks on vmlist command (This process could take a while):"
Get-Childitem –Path C:\ -Include *.vhd,*.vhdx,*.avhdx -File -Recurse -force -ErrorAction SilentlyContinue

}

function vmlist{
$vms = GET-VM

$name = @()
$state = @()
$uptime = @()
$path = @()
$hash = @()
$vms | ForEach-Object{$name += $_.Name}
$vms | ForEach-Object{$state += $_.State}
$vms | ForEach-Object{$uptime += $_.uptime}

Foreach ($vm in $vms)
{
  $HardDrives = $vm.HardDrives
  Foreach ($HardDrive in $HardDrives)
  {
    $path += $HardDrive.path
    if($md5){
        $hash += Get-FileHash $HardDrive.path -Algorithm MD5 | Select-Object Hash | ft -HideTableHeaders
    }
    $hash += "Not Activated"
    
  }
}
Write-Host " "
Write-Host "==============================================================" 
for($i = 0; $i -lt $name.count ;$i++){
    Write-Host "
    VM ID   : $i
    Name    : $($name[$i])
    State   : $($state[$i])
    Uptime  : $($uptime[$i])
    Virt.   : Hyper-V
    Disk    : $($path[$i])
    Hash    : $($hash[$i])"
    Write-Host " "
    Write-Host "=============================================================="
}
}

function vmactions{
$vms = GET-VM
$name = @()
$vms | ForEach-Object{$name += $_.Name}
for($i = 0; $i -lt $name.count ;$i++){
    Write-Host "
    ID	: $i
    Name    : $($name[$i])"
    Write-Host " "
    Write-Host "=============================================================="
}

while(!$name.Contains($($name[$vmname]))){
    $vmname = Read-Host -Prompt " Which VM ID do you want to execute actions on "
}


$function = Read-Host -Prompt "Type start/stop/snapshot to execute an action on the specified vm  "
switch($function){
    start{Start-VM -Name $($name[$vmname])}
    stop{Stop-VM -Name $($name[$vmname])}
    snapshot{
        $hour=Get-Date -Format HH:mm
        Checkpoint-VM -Name $($name[$vmname]) -SnapshotName $($name[$vmname])+$hour
    }
} 
Write-Host "Operation Concluded"
pause
return  

}

function mainfunc{
    $c = Read-Host -Prompt "Do you want to use md5 (Note: md5 increases the processing time of the script) y/n"
    switch($c){
    y{$md5=1}
    n{$md5=0}
    }
    menufunc
    while(1){
        $cmd =Read-Host -Prompt "Choose an option (or type help for the menu) "
        switch($cmd){
            vmlist {vmlist}
            vmdisk{vmdisk}
            vmactions{vmactions}
            vhd_vhdx{vhd_vhdx}
            gen_report{gen_report}
            help{menufunc}
            exit{
            clear
            exit
            }
        }
    }

}


mainfunc

