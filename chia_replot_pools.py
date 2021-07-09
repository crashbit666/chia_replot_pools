import argparse
import shutil
import os
import subprocess
# from shlex import quote as shlex_quote


class Colors:
    reset = "\033[0m"

    # Red
    fgRed = "\033[31m"
    fgBrightRed = "\033[31;1m"
    bgRed = "\033[41m"
    bgBrightRed = "\033[41;1m"

    # Green
    fgGreen = "\033[32m"
    fgBrightGreen = "\033[32;1m"
    bgGreen = "\033[42m"
    bgBrightGreen = "\033[42;1m"

    # Yellow
    fgYellow = "\033[33m"
    fgBrightYellow = "\033[33;1m"
    bgYellow = "\033[43m"
    bgBrightYellow = "\033[43;1m"

    # Blue
    fgBlue = "\033[34m"
    fgBrightBlue = "\033[34;1m"
    bgBlue = "\033[44m"
    bgBrightBlue = "\033[44;1m"


def arguments():
    # Esta función busca los argumentos pasados al programa y los devuelve

    parser = argparse.ArgumentParser(description="Elimina uno a una plots viejos y pone los nuevos")
    parser.version = "1.0"
    parser.add_argument("-d", "--directory", type=str, action="store", nargs="+",
                        help="Directorios donde borrar y añadir nuevos plots")
    parser.add_argument("-nptd", "--new_plots_temp_dir", type=str, action="store",
                        help="Directorio donde se crean los plots temporales")
    parser.add_argument("-fk", "--farmer_public_key", type=str, action="store", help="Farmer public key")
    parser.add_argument("-nft", "--new_plots_nft", type=str, action="store",
                        help="Dirección del contrato inteligente para la pool")
    parser.add_argument("-mmr", "--madmax_route", type=str, action="store", help="Ruta del ploteador madmax")
    parser.add_argument("-r", "--threads", type=int, action="store", help="Número de threads (por defecto = 4)")
    parser.add_argument("-n", "--number", type=int, action="store", help="Numero de plots simultáneos")
    parser.add_argument("-v", "--version", action="version", help="Muestra la versión")
    args = parser.parse_args()
    return args


'''
Este apartado hay que configurarlo para que funcione y arregle las rutas en caso de poner el "/" al final

def folders_format_fix(directory, nptd, npfd, mmr):
    fix_directory = []
    for dirs in directory:
        fix_directory[dirs] = os.path.join(directory[dirs], "")
    fix_nptd = os.path.join(nptd, "")
    fix_npfd = os.path.join(npfd, "")
    fix_mmr = os.path.join(mmr, "")
    return fix_directory, fix_nptd, fix_npfd, fix_mmr
'''


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
        folders["total_space"] = folders_base["total_space"] = shutil.disk_usage(ruta).total // 2 ** 30
        folders["used_space"] = folders_base["used_space"] = shutil.disk_usage(ruta).used // 2 ** 30
        folders["free_space"] = folders_base["free_space"] = shutil.disk_usage(ruta).free // 2 ** 30
        all_folders.append(folders)
    return all_folders


def remove_old_plots(folder):
    # Elimina los plots viejos, check los ficheros que no sean un directorio
    # Pendiente testear que pasa si la carpeta es la primera opción devuelta en last_plot, ya que podría no eliminarlos
    # La parte de que pasa si detecta una carpeta está solventada con os.walk, pero esta parte debe testearse mas
    # ya que capturo una excepción Out of Index para que no salte el programa y luego hago un pass (no es muy limpio)

    folder_walk = os.walk(folder)
    try:
        last_plot = folder + next(folder_walk)[2][0]
        print(Colors.fgRed, "Remove old plot {}".format(last_plot))
        os.remove(last_plot)
    except IndexError:
        pass


def create_new_plots(args, folder):
    # Pendiente . . . Aquí se crearán los nuevos plots

    print(Colors.fgGreen, "Create new plot")
    farmer_public_key = args.farmer_public_key
    new_plots_temp_directory = args.new_plots_temp_dir
    new_plots_final_directory = folder + "new_plots/"
    new_plots_pool_contract = args.new_plots_nft
    madmax_route = args.madmax_route + "build/chia_plot"
    threads = args.threads
    number_of_plots = args.number
    if number_of_plots is None:
        number_of_plots = 1
    if threads is None:
        threads = 4
    command_to_execute = madmax_route + (" -f " + farmer_public_key + " -t " + new_plots_temp_directory +
                                         " -c " + new_plots_pool_contract + " -d " + new_plots_final_directory +
                                         " -r " + threads + " -n " + number_of_plots)
    # Atención con el shell=True e intentar usar shlex_quote
    subprocess.run(command_to_execute, shell=True)


def check_if_old_plots_exist(folder):
    # Mira si en las carpetas pasadas existen plots. En caso contrario, hace salir del bucle while en main

    plots = os.listdir(folder)

    # Ahí miramos que hay en el directorio, si hay solo la carpeta new_plots, significa que no queda nada que borrar
    # Si hay la carpeta new_plots y solo este fichero o el fichero lost+found, significa lo mismo
    if "new_plots" in plots and (len(plots) == 1 or "lost+found" in plots):
        print(Colors.fgYellow, "No existen mas plots viejos para eliminar")
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
        print(Colors.fgGreen, "Create new_plots folder at: {}".format(folder))
        os.makedirs(folder + "new_plots")


def main():
    args = arguments()
    # args = folders_format_fix(args.directory, args.new_plots_temp_dir, args.new_plots_final_dir, args.madmax_route)
    spaces = check_directories_space(args.directory)

    for i in range(len(spaces)):
        check_new_plots_folder(spaces[i]["folder"])
        old_plots_exist = True
        first_loop = 2
        if args.number == 1:
            necessary_space = 103
        else:
            necessary_space = 103 * args.number

        while old_plots_exist or first_loop > 0:
            old_plots_exist = check_if_old_plots_exist(spaces[i]["folder"])
            if spaces[i]["free_space"] > necessary_space:
                create_new_plots(args, spaces[i]["folder"])
                spaces = check_directories_space(args.directory)
            else:
                remove_old_plots(spaces[i]["folder"])
                spaces = check_directories_space(args.directory)
            first_loop += -1


if __name__ == '__main__':
    main()
