from inhouse import Inhouse

class InhouseManager:
    def __init__(self) -> None:
        self.timemap = {}
        self.idmap = {}
    
    async def schedule(self, inhouse: Inhouse) -> None:
        if inhouse.id in self.idmap:
            raise Exception("Inhouse with this id already present. Please try a new id.")
            return
        
        self.idmap[inhouse.id] = inhouse

        if inhouse.time in self.timemap:
            # iterate through and find the last spot
            x = self.timemap[inhouse.time]
            while (x.next != None):
                x = x.next
            inhouse.prev = x
            x.next = inhouse
        else:
            self.timemap[inhouse.time] = inhouse
        
        print(self.timemap)
        print(self.idmap)
        

    async def cancel(self, id: str) -> bool:
        if id not in self.idmap:
            return False # id to cancel not present
        
        time = self.idmap[id].time
        
        x = self.timemap[time]
        while (x != None and x.id != id):
            x = x.next
        
        if x == None:
            return False
        elif (x.prev == None):
            if (x.next == None):
                self.timemap.pop(time)
            else:
                self.timemap[time] = x.next
                x.next.prev = None
        else:
            temp = x.prev
            if x.next != None:
                x.next.prev = x.prev
                temp.next = x.next
            else:
                temp.next = None
        
        return True
        
        
