# Scripts

> [!CAUTION]
> **Nota:** Primero de debe eliminar todas las carpetas con nombre 'results' en la carpeta 'khipu' y 'EMU_release_pymarl' antes de ejecutar los scripts. De otra manera puede haber problemas con los nombres de los archivos.

1. Modificar el archivo `run_smac.sh` :

```bash
# En la rama FabryzzioMezaBranch
cd ~/MLRC-EMU/scripts/khipu
```
Modificar la linea 47(mail) 


2. Ejecutar el script `run_smac.sh` con los índices de los mapas que se desean entrenar:
```bash

bash run_smac.sh {indexes of maps}
# Ej: bash run_smac.sh 4 5 6
```
