import argparse
import shutil
import os


def arguments():
    parser = argparse.ArgumentParser(description="Elimina uno a una plots viejos y pone los nuevos")
    parser.version = "1.0"
    parser.add_argument("-d", "--directory", type=str, action="store", nargs="+",
                        help="Directorios donde borrar y añadir nuevos plots")
    parser.add_argument("-n", "--number", type=int, help="Número de plots a crear/eliminar, 1 si no se especifica")
    parser.add_argument("-v", "--version", action="version", help="Muestra la versión")
    args = parser.parse_args()
    return args


def check_directories_space(directories):
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
    last_plot = folder + max(os.listdir(folder))
    if not os.path.isdir(last_plot):
        print("Remove old plot {}".format(last_plot))
        os.remove(last_plot)


def create_new_plots():
    print("Create new plots")
    os.system("")


def check_if_old_plots_exist(folder):
    plots = os.listdir(folder)
    if "new_plots" in plots and len(plots) == 1:
        return False
    elif plots != "":
        return True
    else:
        check_new_plots_folder(folder)
        return True


def check_new_plots_folder(folder):
    content = os.listdir(folder)
    if "new_plots" not in content:
        print("Create {}/new_plots folder".format(folder))
        os.makedirs(folder+"/new_plots")


def main():
    args = arguments()
    spaces = check_directories_space(args.directory)

    for i in range(len(spaces)):
        old_plots_exist = True
        while old_plots_exist:
            check_new_plots_folder(spaces[i]["folder"])
            old_plots_exist = check_if_old_plots_exist(spaces[i]["folder"])
            if spaces[i]["free_space"] > 1000:
                create_new_plots()
            else:
                remove_old_plots(spaces[i]["folder"])


if __name__ == '__main__':
    main()
