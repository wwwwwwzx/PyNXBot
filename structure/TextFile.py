from structure.ByteStruct import ByteStruct
# https://github.com/kwsch/pkNX/blob/master/pkNX.Structures/Text/TextFile.cs
class TextFile(ByteStruct):
    KEY_BASE = 0x7C89
    KEY_ADVANCE = 0x2983
    KEY_VARIABLE = 0x0010
    KEY_TERMINATOR = 0x0000
    KEY_TEXTRETURN = 0xBE00
    KEY_TEXTCLEAR = 0xBE01
    KEY_TEXTWAIT = 0xBE02
    KEY_TEXTNULL = 0xBDFF

    def textSection(self):
        return self.getushort(0x0)
    def lineCount(self):
        return self.getushort(0x2)
    def totalLength(self):
        return self.getuint(0x4)
    def initialKey(self):
        return self.getuint(0x8)
    def sectionDataOfs(self):
        return self.getuint(0xC)
    def sectionLength(self):
        return self.getuint(self.sectionDataOfs())

    def isValid(self):
        if self.initialKey() != 0 or self.textSection() != 1:
            return False
        if self.sectionDataOfs() + self.totalLength() != self.datalength():
            return False
        if self.sectionLength() != self.totalLength():
            return False
        return True

    def datalength(self):
        return len(self.data)

    def lineOffsets(self):
        result = []
        sdo = self.sectionDataOfs()
        for ii in range(self.lineCount()):
            Ofs = self.getuint(ii * 8 + sdo + 4) + sdo
            Len = self.getushort(ii * 8 + sdo + 8)
            result.append([Ofs,Len])
        return result

    def lineData(self):
        key = self.KEY_BASE
        result = []
        lines = self.lineOffsets()
        for ii in range(self.lineCount()):
            encryptedLineData = self.data[lines[ii][0]:lines[ii][0]+(2*lines[ii][1])]
            result.append(self.cryptLineData(encryptedLineData,key))
            key += self.KEY_ADVANCE
            key &= 0xFFFF
        return result

    def cryptLineData(self,data,key):
        result = data[:]
        for ii in range(0,len(data),2):
            result[ii] ^= key & 0xFF
            result[ii + 1] ^= (key >> 8) & 0xFF
            key = (key << 3 | key >> 13) & 0xFFFF
        return result

    def getString(self,data):
        result = ""
        ii = 0
        while ii < len(data):
            val = int.from_bytes(data[ii:ii + 2], byteorder='little'); ii += 2            
            if val == self.KEY_TERMINATOR: 
                return result
            elif val == self.KEY_VARIABLE:
                varstr , ii = self.getVarStr(data,ii)
                result += varstr
            else:
                result += str(val.to_bytes(2,byteorder='little'),encoding = 'utf-16')
        return result

    def getVarStr(self,data,ii):
        print('here')
        cnt = int.from_bytes(self.data[ii:ii + 2], byteorder='little'); ii += 2
        var = int.from_bytes(self.data[ii:ii + 2], byteorder='little'); ii += 2
        if var == self.KEY_TEXTRETURN:
            return '\r',ii
        elif var == self.KEY_TEXTCLEAR:
            return '[CLEAR]',ii
        elif var == self.KEY_TEXTWAIT:
            time = int.from_bytes(self.data[ii:ii + 2], byteorder='little'); ii += 2
            return f'[WAIT {time}]',ii
        elif var == self.KEY_TEXTNULL:
            line = int.from_bytes(self.data[ii:ii + 2], byteorder='little'); ii += 2
            return f'[~ {line}]',ii

        s = f'[VAR {var}'
        if cnt > 1:
            s += '('
            while cnt > 1:
                arg = int.from_bytes(self.data[ii:ii + 2], byteorder='little'); ii += 2
                s += f'{arg:X}'
                cnt -= 1
                if cnt == 1:
                    break
                s += ','
            s += ')'
        s += ']'
        return s,ii

    def lineString(self):
        result = []
        for data in self.lineData():
            result.append(self.getString(data))
        return result