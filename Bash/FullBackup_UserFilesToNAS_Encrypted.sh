#!/bin/bash

#This script adds user's file directories to a 7zip archive on a network folder, encrypts the archive with a GPG key
#and deletes encrypted archives over 30 days old. Archive filename based on computer's hostname

#Variables
cdate=$(date +"%Y_%m_%d")
bdir="/path/to/network/folder/$HOSTNAME" #Set HOSTNAME as target folder
master_dirs=(~/.ssh ~/Desktop ~/Documents ~/Keys ~/Music ~/Pictures ~/Videos)
fp='EnterEncryptionKeyFingerprintHere'  #Use GPG key's fingerprint to use the correct encryption key
log_dir='/path/to/log/folder'
log_file=$log_dir"/"$cdate"_EncryptedUserFileBackup.log"

#Functions
convert_time() {
    H=`echo $1 / 3600 | bc`
    M=`echo $1 % 3600 / 60 | bc`
    S=`echo $1 % 60 | bc`
    echo "Total Runtime: $H hrs, $M mins, $S secs" >> $log_file
}

#Write start time to log
start=$(date +%s)
echo "$(date +"%m.%d.%y %H:%M:%S") Starting User File Backup Process" >> $log_file

#If network connection is off, turn on network connection
if [[ $(sudo nmcli networking) = *disabled* ]]; then
    echo "$(date +"%m.%d.%y %H:%M:%S") Network connection was off. Turning on network connection" >> $log_file
    sudo nmcli networking on  #Must allow sudo without password for nmcli command using visudo 
    sleep 10  #Wait for network connection to come up before testing NAS path
fi

#Test NAS path
if [ ! -d "$bdir" ]; then
  echo "$(date +"%m.%d.%y %H:%M:%S") Please check NAS Backup folder and ensure UserFiles folder is accessible" >> $log_file
  exit
fi

#Add folders to 7zip archive - Only adds folder(s) that exist in user's home folder
echo "$(date +"%m.%d.%y %H:%M:%S") Zipping user files" >> $log_file
dirs=()

for dir in ${master_dirs[@]}
do
    if [ -d $dir ]; then
      dirs+=($dir)
    fi
done

echo "$(date +"%m.%d.%y %H:%M:%S") Backing up the following directories: ${dirs[@]}" >> $log_file
7z a $bdir/$cdate"_"$HOSTNAME"_UserFiles.7z" ${dirs[@]} >> $log_file

#Encrypt .7z file with GPG key
echo "$(date +"%m.%d.%y %H:%M:%S") Encrypting 7z file" >> $log_file
gpg -sea -r $fp $bdir"/"$cdate"_"$HOSTNAME"_UserFiles.7z" >> $log_file

#Securely delete unencrypted 7z file
echo "$(date +"%m.%d.%y %H:%M:%S") Shredding 7z file" >> $log_file
shred -u $bdir/$cdate"_"$HOSTNAME"_UserFiles.7z" >> $log_file

#Delete .asc files older than 30 days
dfile=$(find $bdir -name "*.asc" -type f -mtime +30)
echo "$(date +"%m.%d.%y %H:%M:%S") Deleting .asc files older than 30 days: $dfile" >> $log_file
rm -f $dfile >> $log_file

#Write completed time to log
echo "$(date +"%m.%d.%y %H:%M:%S") User File Backup Process has completed" >> $log_file

#Calculate and write total runtime to log
end=$(date +%s)
runtime=$((end-start))
convert_time $runtime  #Total runtime written to log in function
