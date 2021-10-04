import sys
sys.path.append("../../")

from connector.mysql.source.GetData import GetData


getdata=GetData();
getdata.getMaysqlVersion()
