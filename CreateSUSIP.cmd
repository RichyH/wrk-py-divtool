#!/bin/bash
LAST_BACKUP_DIRECTORY=$(ls /var/opt/eri_sn/ -t1|head -n1)
sudo cp /var/opt/eri_sn/$LAST_BACKUP_DIRECTORY/DED.D ./DED.D.bak
sudo echo "#!/bin/bash" > susip.cmd
sudo sed -e '1,138d;s/[ \t] //g;s/^["[]*/mdsh -c susip:dir=/;s/".*/\\;/' DED.D.bak >> susip.cmd
sudo rm -f DED.D.bak
sudo chmod +x susip.cmd
echo SUSIP.log wird erstellt. Dies kann einige Minuten dauern, bitte um etwas Geduld
#export PATH=$PATH:/opt/eri_sn/bin;./susip.cmd > SUSIP.log
./susip.cmd > SUSIP.log

