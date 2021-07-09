# README.md

Programa para replotear Chia sin tener que borrar los plots uno a uno

Este programa comprueba las rutas donde se guardan los plots de chia, comprueba 
si existe suficiente espacio en el disco y de ser así, crea un nuevo plot adaptado a las pools.

Si no existe suficiente espacio, elimina un plot y luego crea el nuevo para las pools

## Opciones:
**-d :** directorio donde repoblar los plots, eliminado viejos si no hay espacio y creando nuevos. Los nuevos se crean 
en una carpeta llamada /new_plots dentro del directorio especificado. (Recordad añadir el directorio /new_plots al farmeo)

**-mmr:** ruta donde se encuentra el plotter madmax

**-fk:** Tu clave de farmer

**-nft:** Tu contrato inteligente que apunta al pool o a local.

**-nptd:** Directorio temporal donde se crearan los plots. (Dispositivo SSD)

**-v :** muestra la versión del programa

## Uso:
Este programa se usa a través de la consola linux.

```bash
crashbit@crashbit-GT62VR-6RE:~/plots_temp$ python3 chia_replot_pools.py -d /media/sas15/ -mmr /home/crashbit/chia-plotter/ -fk change_with_your_farmer_key -nft change_with_your_pool_contract -nptd /media/zfs_ssd/
```
Este comando comprueba si existe espacio en el directorio /media/sas15 para crear plots para las pools.
De no ser así, elimina un plot viejo, vuelve a comprobar el espacio libre y si puede, crea un plot nuevo dentro
de la carpeta /media/sas15/new_plots/

## Recuperar datos necesarios desde consola:
Para conseguir los datos necesarios poner los siguientes comandos:
```bash
(venv) crashbit@sun:~/chia-blockchain$ chia keys show | grep Farmer
Farmer public key (m/12381/8444/0/0): XXXXXXXXXX9956edc48397da28dc0e465cce8b71e9ab46654b5ae2c3fae5e5c93b78d66c6a3ec631d55c2cab12196dd5
(venv) crashbit@sun:~/chia-blockchain$ chia plotnft show | grep contract
P2 singleton address (pool contract address for plotting): XXXXXXXXXXXXXXrs5md8akd7cvcmjn5wmrm4rzsa6nq4kv2xlgx0nyqlar9tn 
```
El primer comando devuelve la clave de farmer y el segundo tu dirección de smart contract para las pools

**RECORDAD** que antes de usar el programa hay que crear el smart contract (NFT).

Para crearlo puedes hacer lo siguiente:
```bash
[crashbit@virtual-arch ~]$ chia plotnft create -s pool -u https://api.biopool.tk
```
Esto si quieres plotear y usar la pool de [Chia.tk](https://chiatk.com/), o bién:
```bash
[crashbit@virtual-arch ~]$ chia plotnft create -s local
```
Si quieres que tu contrato inteligente apunte a ti mismo, es decir, para plotear SOLO.
Recuerda que si usas esta última opción, luego podrás sin problema apuntar tu NFT a un pool y los plots apuntarán
al pool sin problema. Es decir, todos los nuevos plots creados con el NFT, aunque apunten a tu propia máquina, podrán 
más tarde apuntar a un pool sin ningún problema.

## Estado del programa y notas importantes

Los plots nuevos se guardarán en la carpeta new_plots.
Hasta el momento no detecta si el plot es nuevo o viejo, simplemente borra los que hay en la carpeta raíz del directorio indicado con la opción **-d**

## License:
Este programa está registrado bajo la licencia GPLv3.
Copyright 2021

## Contribución:
Si quieres agradecer el esfuerzo puedes hacer una donación ahí

**XCH**: xch1l0nm3fukzvgqakauks7tl4rwr9kdwqyl4aaw4cnhapj9ex5jngls49dsj6