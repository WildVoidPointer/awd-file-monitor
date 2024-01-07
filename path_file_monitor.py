""" 
path_file_monitor is a project for document monitoring and unified management in the AWD schedule of CTF competitions
"""

from __future__ import annotations
# from typing import TYPE_CHECKING
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime
import time

# if TYPE_CHECKING:
#     from time import struct_time


class PathFileMonitor:
    def __init__(self, path: Path) -> None:
        self.path: Path = path
        self.original_file_list: list[str] = self.path_file_name_scanner()
        self.previous_scanning_res: list[str] = self.original_file_list
        self.current_scanning_res: list[str] = []

    @staticmethod
    def set_directory_path() -> PathFileMonitor:
        file_parser: ArgumentParser = ArgumentParser(description='Welcome to the File Dynamic Monitor')
        file_parser.add_argument('-path', help="Specify a directory path")
        file_path: str = file_parser.parse_args().path
        current_time: str= datetime.now().time().strftime("%H:%M:%S")
        try:
            path: Path = Path(file_path)
        except TypeError:
            print(f"[{current_time}]  [runtime status]  Please enter an existing directory path")
            exit()
        else:
            if path.exists():  
                print(f"""[{current_time}]  [runtime status]  The directory exists and scanning is about to begin: [{file_path}] """)
                return PathFileMonitor(path=path)
            else:
                print(f"[{current_time}]  [runtime status]  Please enter an existing directory path")
                exit()
    
    def path_file_name_scanner(self) -> list[str]:
        temp_file_list: list[str] = []
        for file_path in self.path.rglob("*"):
            if file_path.is_file():
                temp_file_list.append(file_path)
        return temp_file_list
    
    def path_file_time_scanner(self) -> dict[str, str]:
        file_change_time: dict[str, str] = {}
        scan_file_queue: list[str] = self.path_file_name_scanner()
        for scan_file in scan_file_queue:
            current_time = datetime.now().time().strftime("%H:%M:%S")
            try:
                file_path: Path = Path(scan_file)
                modification_time: datetime = datetime.fromtimestamp(file_path.stat().st_mtime)
                formatted_time: str = modification_time.strftime("%Y-%m-%d %H:%M:%S")
            except FileNotFoundError:
                print(f"[{current_time}]  [runtime status]  File not found: [{scan_file}]")
            else:
                file_change_time[f"{scan_file}"] = formatted_time
    
    def path_file_add_monitor(self) -> None:
        current_time = datetime.now().time().strftime("%H:%M:%S")
        self.current_scanning_res: list[str] = self.path_file_name_scanner()
        file_differences: list[str] = list(set(self.current_scanning_res) - set(self.previous_scanning_res))
        self.previous_scanning_res = self.current_scanning_res
        for file_name in file_differences:
            print(f"[{current_time}]  [file increase]  Add the file path to: [{file_name}]")
        file_differences = []

    def path_file_change_monitor(self) -> None:
        pass

    def delete_all_not_original_file(self) -> None:
        original_file_differences: list[str] = list(set(self.current_scanning_res) - set(self.original_file_list))
        
        for delete_file_path in original_file_differences:
            current_time = datetime.now().time().strftime("%H:%M:%S")
            delete_file: Path = Path(delete_file_path)        
            if delete_file.exists():
                delete_file.unlink()
                print(f"[{current_time}]  [runtime status]  This file has been deleted : [{delete_file_path}]")



if __name__ == "__main__":
    path_object: PathFileMonitor = PathFileMonitor.set_directory_path()
    path_object.path_file_name_scanner()

    while True:
        path_object.path_file_add_monitor()
        time.sleep(1)
