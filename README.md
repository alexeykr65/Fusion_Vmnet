## Configure VMNET on Vmware Fusion
Добавление или удаление  интерфейсов VMNETXX на Mac OS X.<br>
#### Добавление интерфейсов, описание которых находится в файле fusion_network.cfg<br>
***./vmnet_cfg.py -a 'fusion_network.cfg'***  <br>
#### Удаление интефейсов vmnet21, vmnet22, vmnet23, vmnet24 <br>
***./vmnet_cfg.py -r "21,22,23,24"*** <br>
#### Удалить все интерфейсы, начиная с 10 и заканчивая 100, если есть<br>
***./vmnet_cfg.py -rr "100"***

