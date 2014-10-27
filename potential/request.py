'''
Created on Sep 23, 2014

@author: James
'''
import telnetlib

class Request(object):
    TERMNATOR = ["\end", "ok", "\nfail"]
    tn = None
    @classmethod
    def connect(cls, host, port):
        Request.tn = telnetlib.Telnet(host, port)
        print cls.tn.read_until("bzrobots 1")
        cls.tn.write('agent 1\n')
        
    def __init__(self):
        if self.tn == None:
            raise Exception("Not connected")
        self.ack = ""
        self.list = []

        
    def ex(self, *args):
        print " ".join(list(args))
        self.tn.write(" ".join(list(args)) + "\n")
        response = self.tn.expect(self.TERMNATOR)
        line_split = response[2].split("\n")
        self.ack = line_split[1].split()
        if response[0] == 0:
            for idx in range(line_split.index("begin")+1, len(line_split)-1):
                self.list.append(line_split[idx].split())
        elif response[0] == 2:
            print "Error"

    def __getitem__(self, key):
        return self.list.__getitem__(key)
    
    def __repr__(self):
        return str(self.list)


class Shoot(Request):
    def __init__(self, index):
        super(Shoot, self).__init__()
        return self.ex("shoot", str(index))
    
class Speed(Request):
    def __init__(self, index, speed):
        super(Speed, self).__init__()
        return self.ex("speed", str(index), str(speed))
    
class Angvel(Request):
    def __init__(self, index, angvel):
        super(Angvel, self).__init__()
        return self.ex("angvel", str(index), str(angvel))

class Teams(Request):
    def __init__(self):
        super(Teams, self).__init__()
        return self.ex("teams")
    
class Obstacles(Request):
    def __init__(self):
        super(Obstacles, self).__init__()
        return self.ex("obstacles")
    
    def get_Obstacles(self):
        float_list = [map(float, x[1:]) for x in self.list]
        return [zip(x[0::2], x[1::2]) for x in float_list]
    
class Bases(Request):
    def __init__(self):
        super(Bases, self).__init__()
        return self.ex("bases")
    
    def center(self, num_color):
        try:
            base = self.list[num_color]
        except TypeError:
            base = [b for b in self.list if b[1] == num_color][0]
        return (sum(map(float, base[2::2]))/4, sum(map(float, base[3::2]))/4)
                
class Flags(Request):
    def __init__(self):
        super(Flags, self).__init__()
        return self.ex("flags")
    
    def index(self, num):
        return map(float, self.list[num][3:5])

class Shots(Request):
    def __init__(self):
        super(Shots, self).__init__()
        return self.ex("shots")

class Mytanks(Request):
    def __init__(self):
        super(Mytanks, self).__init__()
        return self.ex("mytanks")
    
    def position(self, num):
        return map(float, self.list[num][7:9])
    
    def angle(self, num):
        return float(self[num][9])
    
    def angvel(self, num):
        return float(self.list[num][12])
    
    def flag(self, num):
        if self.list[num][6] != "-":
            return True
        return False

class Othertanks(Request):
    def __init__(self):
        super(Othertanks, self).__init__()
        return self.ex("othertanks")
    
class Constants(Request):
    def __init__(self):
        super(Constants, self).__init__()
        return self.ex("constants")
    
    def dictionary(self):
        return {item[1]: item[2] for item in self.list}
    
    
class Query(Request):
    TERMNATOR = "\nend"

class RSingle(Request):
    TERMNATOR = "\nok"
    def __init__(self):
        pass