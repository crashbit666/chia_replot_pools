#README.md

Programa para replotear Chia sin tener que borrar ficheros uno a uno

Este programa lo que hace es comprueba las rutas donde se guardan los plots de chia, comprueba 
si existe suficiente espacio en el disco y de ser así, crea un nuevo plot adaptado a las pools.

Si no existe suficiente espacio, elimina un plot y luego crea el nuevo para las pools

## Opciones:
**-d :** directorio donde repoblar los plots, eliminado viejos si no hay espacio y creando nuevos,

**-n :** número de plots a crear. Si no especifica un número, no se parará hasta ocupar todo el espacio
con los nuevos plots.

**-v :** muestra la versión del programa

## Uso:
Este programa se usa a través de la consola linux.

```bash
crashbit@crashbit-GT62VR-6RE:~/plots_temp$ python3 ./chia_replot_pools.py -d /media/disco1/ /media/disco2
```
Este comando comprueba si existe espacio en el directorio /media/disco1 para crear plots para las pools.
De no ser así, elimina un plot viejo, vuelve a comprobar el espacio libre y si puede, crea un plot nuevo

## Estado del programa y notas importantes
Actualmente la opción **-n** todavía no está activa
Tampoco está activa la creación de plots nuevos
Los plots nuevos se guardarán en la carpeta new_plots.
Hasta el momento no detecta si el plot es nuevo o viejo, simplemente borra los que hay en la carpeta raíz
El tamaño está puesto a 1TB, para las pruebas. Bajar a 102GB para producción.