"""
smart rm -f -r
DxSetFox59HgK23
"""
import argparse
import click
import logging
import re
import platform
import os
import json
import shutil # no used
import configparser
from datetime import date

PATH_CONFIG = os.getenv('USERPROFILE') + os.sep +  "settings.ini"

class Smart(object):
    def __init__(self, path_smart):
        self.platfors = platform.system()
        self.crateSmart()

    def crateSmart(self):
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
                """
                    DIRECT FOR EVERYONE USER
                    I hate
                """

    def delete(self,  path):
        path = os.path.abspath(path)
        name = os.path.basename(path)
        size = os.path.getsize(path)
        date = str(date.today())

        move(path, self.path_smart + os.sep + name)
        add_deleted_file(path, self.path_smart + os.sep + name, name, size, date)
        os.remove(path)

    def delete_directory(self,  path_directory, derict_smart_path):
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
                date = str(date.today())
                move(path, derict_smart_path + os.sep + name)
                add_deleted_file(path, derict_smart_path + os.sep + name, name, size, date)
                os.remove(path)
        os.rmdir(path_directory)

    def delete_directory_smart(self, path):
        all_files = os.listdir(path)
        for el in all_files:
            if os.path.isdir:
                delete_directory_smart(el)
            else:
                os.remove(el)
                self.remove_smart_info(os.path.abspath(el))

    def delete_smart(self):
        all_files = os.listdir(self.path_smart)
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
        try:
            with open(path_from, "rb") as f_from:
                with open(path_to, "wb") as f_to:
                    window = f_from.read(1024)
                    f_to.write(window)

        except Exception as e:
            raise e


def create_config(path):
    config = configparser.ConfigParser()
    with open(path, "w") as config_file:
        config.write(config_file)

def add_deleted_file( path, newpath, name, size, date):
    config = get_config(PATH_CONFIG)
    config.add_section(newpath)
    config.set(newpath, "new", path)
    config.set(newpath, "name", name)
    config.set(newpath, "size", size)
    config.set(newpath, "date", date)
    with open(PATH_CONFIG, "w") as config_file:
        config.write(config_file)

def delete_info(path):
     config = get_config(PATH_CONFIG)
     config.remove_section(path)
     with open(PATH_CONFIG, "w") as config_file:
        config.write(config_file)

def get_config(path):
    if not os.path.exists(path):
        create_config(path)
    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_setting(section, setting):
    config = get_config(PATH_CONFIG)
    value = config.get(section, setting)
    return value

def update_setting(section, setting, value):
    config = get_config(PATH_CONFIG)
    config.set(section, setting, value)
    with open(PATH_CONFIG, "w") as config_file:
        config.write(config_file)


def delete_setting( section, setting):
    config = get_config(PATH_CONFIG)
    config.remove_option(section, setting)
    with open(PATH_CONFIG, "w") as config_file:
        config.write(config_file)




@click.command()
@click.option('--command', default="list", help='Command ')
@click.option('--path', prompt='Your name',
              help='The person to greet.')
def main(command, name):
    "The programm smart"
    print("Hello, World!")



if __name__ == "__main__":
    # need static path
    if not os.path.exists(PATH_CONFIG):
        create_config(PATH_CONFIG)
    main()


"""
Section ->
config.sections()
"""