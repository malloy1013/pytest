import sys
import os

# print os.getcwd()
m = __file__
current_dir = os.path.dirname(m)
parent_dir = os.path.dirname(current_dir)
grand_parent_dir = os.path.dirname(parent_dir)

def GetCurPath(m):
    return os.path.dirname(m)
def Get_P_Path(m):
    return os.path.dirname(os.path.dirname(m))
def Get_GP_Path(m):
    return os.path.dirname(os.path.dirname(os.path.dirname(m)))


if __name__ == '__main__':

    print (GetCurPath(__file__),'\n',Get_P_Path(__file__),'\n',Get_GP_Path(__file__))
    # t = testddd()