import argparse
import shutil
import os


def arguments():
    # Esta función busca los argumentos pasados al programa y los devuelve

    parser = argparse.ArgumentParser(description="Elimina uno a una plots viejos y pone los nuevos")
    parser.version = "1.0"
    parser.add_argument("-d", "--directory", type=str, action="store", nargs="+",
                        help="Directorios donde borrar y añadir nuevos plots")
    parser.add_argument("-n", "--number", type=int, help="Número de plots a crear/eliminar, 1 si no se especifica")
    parser.add_argument("-s", "--ptd", type=str, action="store", help="Directorio donde se crear los plots temporales")
    parser.add_argument("-f", "--final_dir", type=str, action="store", help="Directorio final de los plots")
    parser.add_argument("-p", "--pool_key", type=str, action="store", help="Contrato para la pool")
    parser.add_argument("-v", "--version", action="version", help="Muestra la versión")
    args = parser.parse_args()
    return args


def check_directories_space(directories):
    # Calcula el tamaño del disco, la parte usada y la parte libre, para saber si puede crear un plot o debe eliminarlo

    folders_base = {
        "folder": "",
        "total_space": 0,
        "used_space": 0,
        "free_space": 0,
    }

    all_folders = []
    for ruta in directories:
        folders = folders_base.copy()
        folders["folder"] = folders_base["folder"] = ruta
        folders["total_space"] = folders_base["total_space"] = shutil.disk_usage(ruta).total // 2**30
        folders["used_space"] = folders_base["used_space"] = shutil.disk_usage(ruta).used // 2**30
        folders["free_space"] = folders_base["free_space"] = shutil.disk_usage(ruta).free // 2**30
        all_folders.append(folders)
    return all_folders


def remove_old_plots(folder):
    # Elimina los plots viejos, check los ficheros que no sean un directorio
    # Pendiente testear que pasa si la carpeta es la primera opción devuelta en last_plot, ya que podría no eliminarlos
    # La parte de que pasa si detecta una carpeta está solventada con os.walk, pero esta parte debe testearse mas
    # ya que el capturo una excepción Out of Index para que no salte el programa y luego hago un pass (no es muy limpio)

    folder_walk = os.walk(folder)
    try:
        last_plot = folder + next(folder_walk)[2][0]
        print("Remove old plot {}".format(last_plot))
        os.remove(last_plot)
    except IndexError:
        pass


def create_new_plots():
    # Pendiente . . . Aquí se crearán los nuevos plots

    print("Create new plots")
    os.system("")


def check_if_old_plots_exist(folder):
    # Mira si en las carpetas pasadas existen plots. En caso contrario, hace salir del bucle while en main

    plots = os.listdir(folder)
    if "new_plots" in plots and len(plots) == 1:
        return False
    elif plots != "":
        return True
    else:
        check_new_plots_folder(folder)
        return True


def check_new_plots_folder(folder):
    # Los plots nuevos, en principio los pondrá en la carpeta new_plots. Si no existe, la crea
    # Mas adelante está previsto que detecte los nuevos/viejos y esto quedara obsoleto

    content = os.listdir(folder)
    if "new_plots" not in content:
        print("Create {}/new_plots folder".format(folder))
        os.makedirs(folder+"/new_plots")


def main():
    args = arguments()
    spaces = check_directories_space(args.directory)
    if args.number is not None:
        number_of_new_plots = args.number
    else:
        number_of_new_plots = 1
    iterations = 0

    for i in range(len(spaces)):
        old_plots_exist = True
        while old_plots_exist or iterations <= number_of_new_plots:
            check_new_plots_folder(spaces[i]["folder"])
            old_plots_exist = check_if_old_plots_exist(spaces[i]["folder"])
            if spaces[i]["free_space"] > 1000:
                create_new_plots()
            else:
                remove_old_plots(spaces[i]["folder"])
            iterations += 1


if __name__ == '__main__':
    main()
