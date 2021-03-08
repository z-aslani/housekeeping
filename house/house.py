import os
import concurrent.futures


class House:
    def __init__(self, name, rooms):
        self.rooms = rooms
        self.name = name

    def keep(self, dry_run=False, rooms=None):
        excess_files = []

        if rooms:
            rooms = list(
                filter(None, [self.get_room_by_name(room) for room in rooms]))
        else:
            rooms = self.rooms

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda room: excess_files.append(
                (room.name, self.__keep_room(room, dry_run))), rooms)

        return excess_files

    def __keep_room(self, room, dry_run):
        excess_files = room.get_all_excess_files()
        if not dry_run:
            room.clean(excess_files)
        return excess_files

    def add_room(self, room):
        self.rooms.append(room)

    def get_room_by_name(self, name):
        for r in self.rooms:
            if r.name == name:
                return r
        return None

        # excess_files=[]
        # if rooms:
        #     rooms=list(filter(None,[self.get_room_by_name(room) for room in rooms]))
        #     [excess_files.append((room.name,self.__keep_room(room,dry_run))) for room in rooms]
        # else:
        #     [excess_files.append((room.name,self.__keep_room(room,dry_run))) for room in self.rooms]
        # return excess_files
