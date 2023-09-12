import os
from datetime import datetime
import shutil

import minio

from rich.traceback import install
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

install(show_locals=True)
console = Console()

console.print(f"[bold]Bienvenue dans Optifleme[/bold]")
console.print(f"[bold]Initialisation du client minio[/bold]")
remote_client = minio.Minio(
    "127.0.0.1:9000",
    access_key="2PiRGZT0CMytjPrLMp7V",
    secret_key="FNrhKRFW1hn9nYcWQZQozccMP2tn8wKKEf2yLLN3",
    secure=False,
)
if not remote_client.bucket_exists("python"):
    print("Not s3 bucket found")
    exit(1)
console.print(f"[bold]Initialisation du client minio terminé[/bold]")


def convert_date_to_str(date):
    return datetime.fromtimestamp(date, tz=None).strftime("%d/%m/%Y %H:%M:%S")


def convert_size_to_str(size):
    if size > 1024:
        return f"{size / 1024}K"
    elif size > 1024 * 1024:
        return f"{size / 1024 / 1024}M"
    elif size > 1024 * 1024 * 1024:
        return f"{size / 1024 / 1024 / 1024}G"
    else:
        return f"{size}B"


def help_print():
    console.print(f"[bold]Commandes disponibles:[/bold]")
    console.print(f"[bold]cd[/bold] [cyan]chemin[/cyan] : changer de répertoire")
    console.print(f"[bold]ls[/bold] [cyan]chemin[/cyan] : lister les fichiers et répertoires")
    console.print(f"[bold]mkdir[/bold] [cyan]chemin[/cyan] : créer un répertoire")
    console.print(f"[bold]touch[/bold] [cyan]chemin[/cyan] : créer un fichier")
    console.print(f"[bold]mv[/bold] [cyan]chemin[/cyan] [cyan]chemin[/cyan] : déplacer un répertoire ou un fichier")
    console.print(f"[bold]cp[/bold] [cyan]chemin[/cyan] [cyan]chemin[/cyan] : copier un répertoire ou un fichier")
    console.print(f"[bold]rm[/bold] [cyan]chemin[/cyan] : supprimer un répertoire ou un fichier")
    console.print(
        f"[bold]backup[/bold] [cyan]chemin[/cyan] : sauvegarder les anciennes versions des fichiers dans un serveur offsite")
    console.print(
        f"[bold]lsb[/bold] [cyan]chemin[/cyan] : list les anciennes versions des fichiers depuis un serveur offsite")
    console.print(
        f"[bold]restore[/bold] [cyan]chemin[/cyan] : restaurer les anciennes versions des fichiers depuis un serveur offsite")
    console.print(f"[bold]exit[/bold] : quitter le programme")


def main():
    try:
        while True:
            action = Prompt.ask(f"{os.getcwd()} > ")
            if not action:
                console.print(f"[red]Commande invalide[/red]")
                continue

            split_action = action.split(" ")
            size = len(split_action)

            match split_action[0]:
                case "exit":
                    break
                case "clear":
                    console.clear()
                case "help":
                    help_print()
                case "cd":
                    if size == 1:
                        console.print(f"[red]cd: missing folder name[/red]")
                    else:
                        # check if folder exist
                        if not os.path.isdir(split_action[1]):
                            console.print(f"[red]cd: {split_action[1]}: No such file or directory[/red]")
                            continue
                        os.chdir(split_action[1])
                case "ls":

                    str_folders = os.getcwd()
                    if size == 2:
                        str_folders += split_action[1]
                        if not os.path.isdir(split_action[1]):
                            console.print(f"[red]cd: {split_action[1]}: No such file or directory[/red]")
                            continue

                    table = Table(title="Liste des fichiers et répertoires")
                    table.add_column("Nom", justify="right", style="cyan", no_wrap=True)
                    table.add_column("Taille", justify="right", style="magenta")
                    table.add_column("Date de modification", justify="right", style="green")
                    for file in os.listdir(str_folders):
                        file_stats = os.stat(f"{str_folders}/{file}")
                        table.add_row(file, convert_size_to_str(file_stats.st_size),
                                      convert_date_to_str(file_stats.st_mtime))
                    console.print(table)
                case "mkdir":
                    if size == 1:
                        console.print(f"[red]mkdir: missing folder name[/red]")
                    else:
                        os.mkdir(split_action[1])
                        console.print(f"[green]mkdir: {split_action[1]}[/green]")
                case "touch":
                    if size == 1:
                        console.print(f"[red]touch: missing file name[/red]")
                    else:
                        open(split_action[1], "w").close()
                        console.print(f"[green]touch: {split_action[1]}[/green]")
                case "mv":
                    if size <= 2:
                        console.print(f"[red]mv: missing 2 file name[/red]")
                    f1 = split_action[1]
                    f2 = split_action[2]
                    if not os.path.exists(f1):
                        console.print(f"[red]mv: {f1}: No such file or directory[/red]")
                        continue

                    if os.path.isdir(f2):  # move file to folder
                        shutil.move(f1, f"{f2}/{os.path.basename(f1)}")
                        console.print(f"[green]mv: {f1} -> {f2}/{os.path.basename(f1)}[/green]")

                    if not os.path.isdir(f1) and not os.path.isdir(f2):  # rename file
                        shutil.move(f1, f2)
                        console.print(f"[green]mv: {f1} -> {f2}[/green]")

                case "cp":
                    if size <= 2:
                        console.print(f"[red]cp: missing 2 file name[/red]")
                    f1 = split_action[1]
                    f2 = split_action[2]
                    if not os.path.exists(f1):
                        console.print(f"[red]cp: {f1}: No such file or directory[/red]")
                        continue

                    if os.path.isdir(f2):  # copy file to folder
                        shutil.copy(f1, f"{f2}/{os.path.basename(f1)}")
                        console.print(f"[green]cp: {f1} -> {f2}/{os.path.basename(f1)}[/green]")

                    if not os.path.isdir(f1) and not os.path.isdir(f2):  # copy file
                        shutil.copy(f1, f2)
                        console.print(f"[green]cp: {f1} -> {f2}[/green]")
                case "rm":
                    if size == 1:
                        console.print(f"[red]rm: missing file name[/red]")
                    else:
                        os.remove(split_action[1])
                        console.print(f"[green]rm: {split_action[1]}[/green]")

                case "backup":
                    if size == 1:
                        console.print(f"[red]backup: missing file name[/red]")
                        continue
                    if not os.path.exists(split_action[1]):
                        console.print(f"[red]backup: {split_action[1]}: No such file found[/red]")
                        continue
                    if os.path.isdir(split_action[1]):
                        console.print(f"[red]backup: {split_action[1]}: is a folder[/red]")
                        continue

                    # push file to server
                    console.print(f"[green]backup: {split_action[1]}[/green]")
                    console.print(f"[green]backup: pushing file to server[/green]")
                    try:
                        remote_client.fput_object("python", f"{os.getcwd()}/{split_action[1]}", split_action[1])
                    except minio.S3Error as e:
                        console.print(f"[red]backup: {e}[/red]")
                        continue
                    console.print(f"[green]backup: file pushed to server[/green]")

                case "lsb":

                    str_folders = ""
                    if size == 2:
                        str_folders += split_action[1]

                    if len(str_folders) > 0 and not str_folders.endswith("/"):
                        str_folders += "/"

                    table = Table(title="Liste des fichiers et répertoires")
                    table.add_column("Nom", justify="right", style="cyan", no_wrap=True)
                    table.add_column("Version", justify="right", style="magenta")
                    table.add_column("Taille", justify="right", style="magenta")
                    table.add_column("Date de modification", justify="right", style="green")

                    for item in remote_client.list_objects("python", str_folders, recursive=False):
                        if item.is_dir:
                            table.add_row(item.object_name, "", "")
                            continue
                        table.add_row(item.object_name, str(item.version_id), convert_size_to_str(item.size), str(item.last_modified))
                    console.print(table)

                case "restore":
                    if size == 1:
                        console.print(f"[red]restore: missing file name to restore[/red]")
                        continue

                    console.print(f"[green]restore: {split_action[1]}[/green]")
                    try:
                        remote_client.fget_object("python", split_action[1], f"{split_action[1]}.restored")
                        console.print(f"[green]restore: file restored[/green]")
                    except minio.S3Error as e:
                        console.print(f"[red]restore: {e}[/red]")
                        continue

    except KeyboardInterrupt:
        console.print(f"[red]Programme interrompu par l'utilisateur[/red]")
        exit(0)
    except Exception as e:
        console.print(f"[red]Erreur: {e}[/red]")
        console.print(f"[red]Restarting console[/red]")
        main()


if __name__ == "__main__":
    console.print("Bienvenue dans le terminal")
    main()
    console.print("Bye :wave:")
