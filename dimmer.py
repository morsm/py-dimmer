'''
Dimmer class
'''

class Dimmer:
    addresses = []
    mapping = []

    def map(self, dimVal):
        ''' dimVal is 0-255, find the index in the map and return it '''
        mapLen = len(self.mapping)
        index = int((mapLen - 1) * dimVal / 255)
        return self.mapping[index]
    
    def readMapping(self, file):
        f = open(file, 'r')
        for line in f:
            line = line.strip('\n')
            self.mapping.append(int(line))
        f.close()

    def readAddresses(self, file):
        f = open(file, 'r')
        for line in f:
            line = line.strip('\n')
            self.addresses.append(line)
        f.close()

