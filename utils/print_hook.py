import sys


# this class gets all output directed to stdout(e.g by print statements)
# and stderr and redirects it to a user defined function
class PrintHook:
    # out = 1 means stdout will be hooked
    # out = 0 means stderr will be hooked
    def __init__(self, out=1):
        self.func = None  ##self.func is userdefined function
        self.origOut = None
        self.out = out

    # user defined hook must return three variables
    # proceed,lineNoMode,newText
    def TestHook(self, text):
        f = open('hook_log.txt', 'a')
        f.write(text)
        f.close()
        return 0, 0, text

    def Start(self, func=None):
        if self.out:
            sys.stdout = self
            self.origOut = sys.__stdout__
        else:
            sys.stderr = self
            self.origOut = sys.__stderr__

        if func:
            self.func = func
        else:
            self.func = self.TestHook

    def flush(self):
        self.origOut.flush()
        pass

    # Stop will stop routing of print statements thru this class
    def Stop(self):
        if self.out:
            sys.stdout = sys.__stdout__
        else:
            sys.stderr = sys.__stderr__
        self.func = None

    # override write of stdout
    def write(self, text):
        global postNewText, newText
        proceed = 1
        lineNo = 0
        addText = ''
        if self.func != None:
            proceed, lineNo, newText, postNewText = self.func(text)


        if proceed:
            if text.split() == []:
                self.origOut.write(text)
            else:
                # if goint to stdout then only add line no file etc
                # for stderr it is already there
                if self.out:
                    if lineNo:
                        try:
                            raise Exception("Err print hook")
                        except:
                            if newText is not None:
                                self.origOut.write(newText)
                            if postNewText is not None:
                                self.origOut.write(postNewText)

    # # pass all other methods to __stdout__ so that we don't have to override them
    # def __getattr__(self, name):
    #     return self.origOut.__getattr__(name)
