
import argparse
import click
import logging
import re
import platform
import os
import json
import configparser
from datetime import date

PATH_CONFIG = os.getenv('USERPROFILE') + os.sep +  "settings.ini"

class SmartRM(object):
    def __init__(self):
        self.platfors = platform.system()
        self.crateSmart()

    def crateSmart(self):
        logging.basicConfig(filename="Log.log", level=logging.DEBUG)
        homedirect = os.getenv('USERPROFILE')
        self.smart = homedirect + os.sep + "smart"
        if self.platfors == "windows":
            if not os.path.exists(homedirect + os.sep + "smart"):
                try:
                    os.mkdir(homedirect + os.sep + "smart")
                except Exception as e:
                    raise e
        elif self.platfors == "posix":
            if not os.path.exists(homedirect + os.sep + "smart"):
                try:
                    os.mkdir(homedirect + os.sep + "smart")
                except Exception as e:
                    raise e

    def delete(self,  path):
        logging.basicConfig(filename="Log.log", level=logging.DEBUG)
        path = os.path.abspath(path)
        name = os.path.basename(path)
        size = os.path.getsize(path)
        date_delete = str(date.today())

        self.move(path, self.smart + os.sep + name)
        add_deleted_file(path, self.smart + os.sep + name, name, size, date_delete)
        os.remove(path)

    def delete_directory(self,  path_directory, derict_smart_path = ""):
        logging.basicConfig(filename="Log.log", level=logging.DEBUG)
        all_files = os.listdir(path_directory)
        if not derict_smart_path :
            derict_smart_path = self.smart
        os.mkdir(derict_smart_path + os.sep + os.path.basename(path_directory))
        for el in all_files:
            if os.path.isdir(el):
                self.delete_directory(el, derict_smart_path + os.sep + os.path.basename(path_directory))
            else:
                path = os.path.abspath(el)
                name = os.path.basename(el)
                size = os.path.getsize(el)
                date_delete = str(date.today())
                self.move(path, derict_smart_path + os.sep + name)
                add_deleted_file(path, derict_smart_path + os.sep + name, name, size, date_delete)
                os.remove(path)
        os.rmdir(path_directory)

    def delete_directory_smart(self, path):
        logging.basicConfig(filename="Log.log", level=logging.DEBUG)
        all_files = os.listdir(path)
        for el in all_files:
            if os.path.isdir:
                delete_directory_smart(el)
            else:
                os.remove(el)
                self.remove_smart_info(os.path.abspath(el))

    def delete_smart(self):
        logging.basicConfig(filename="Log.log", level=logging.DEBUG)
        all_files = os.listdir(self.smart)
        for el in all_files:
            if os.path.isdir:
                delete_directory_smart(el)
            else:
                os.remove(el)
                self.remove_smart_info(os.path.abspath(el))

    def remove_smart_info(self, path):
        delete_info(path)

    @staticmethod
    def move(path_from, path_to):
        logging.basicConfig(filename="Log.log", level=logging.DEBUG)
        try:
            with open(path_from, "rb") as f_from:
                with open(path_to, "wb") as f_to:
                    window = f_from.read(1024)
                    f_to.write(window)

        except Exception as e:
            raise e


def create_config(path):
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    config = configparser.ConfigParser()
    with open(path, "w") as config_file:
        config.write(config_file)

def add_deleted_file( path, newpath, name, size, date):
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    config = get_config(PATH_CONFIG)
    config.add_section(newpath)
    config.set(newpath, "new", str(path))
    config.set(newpath, "name", str(name))
    config.set(newpath, "size", str(size))
    config.set(newpath, "date", str(date))
    with open(PATH_CONFIG, "w") as config_file:
        config.write(config_file)

def show_list():
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    config = get_config(PATH_CONFIG)
    list_smart = config.sections()
    for index, el in enumerate(list_smart):

        print( str(index + 1) + "." + str(config.get(el, "new")) + " " + str(config.get(el, "name")) + " " + str(config.get(el, "size")) + " " + str(config.get(el, "date")))

def delete_info(path):
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    config = get_config(PATH_CONFIG)
    config.remove_section(path)
    with open(PATH_CONFIG, "w") as config_file:
        config.write(config_file)

def get_config(path):
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    if not os.path.exists(path):
        create_config(path)
    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_setting(section, setting):
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    config = get_config(PATH_CONFIG)
    value = config.get(section, setting)
    return value

def update_setting(section, setting, value):
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    config = get_config(PATH_CONFIG)
    config.set(section, setting, value)
    with open(PATH_CONFIG, "w") as config_file:
        config.write(config_file)


def delete_setting( section, setting):
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    config = get_config(PATH_CONFIG)
    config.remove_option(section, setting)
    with open(PATH_CONFIG, "w") as config_file:
        config.write(config_file)




@click.command()
@click.option('--command', default="List_smart", help='Delete_File - Delete file.\n Delete_Folder - Delete Folder.\n List_smart - show smart rm list.\n Delete_File_smart - delete file from smart rm.\n Clear_smart - clear smart rm.\n Restore_file_smart - restore file from smart.\n ')
@click.option('--path', help='The file or folder path.')
@click.option('--number', help='The person to greet.')

def main(command, path, number = 0):
    logging.basicConfig(filename="Log.log", level=logging.DEBUG)
    if not os.path.exists(PATH_CONFIG):
        create_config(PATH_CONFIG)
    
    smart =  SmartRM()
    smart.crateSmart()
    if command == "Delete_File":
        logging.info("Delete_File")
        smart.delete(path)
    elif command == "Delete_Folder":
        logging.info("Delete_Folder")
        smart.delete_directory(path)
    elif command == "List_smart":
        logging.info("List")
        show_list()
    elif command == "Delete_File_smart":
        logging.info(number)
        smart.show_list(number)
    elif command == "Clear_smart":
        logging.info("Clear_smart")
        smart.delete_smart()
    elif command == "Restore_file_smart":
        logging.info(number)
        smart.delete_smart(number)
    else:
        logging.error("Incorrect command")
def NewSmart():
    smart =  SmartRM()
    return smart

if __name__ == "__main__":
    if not os.path.exists(PATH_CONFIG):
        create_config(PATH_CONFIG)
    main()

