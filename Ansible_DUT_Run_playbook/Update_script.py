import zipfile
import cloudshell.api.cloudshell_api as api


NameOfDriver = 'DUTExecutePlaybook'
ZipAddress = NameOfDriver + '.zip'
z = zipfile.ZipFile(ZipAddress, "w")
# z.write("drivermetadata.xml")
# z.write("requirements.txt")
z.write("DUTexecuteplaybook.py")
z.write("__main__.py")
z.close()

ss = api.CloudShellAPISession('localhost', 'admin', 'admin', 'Global')
ss.UpdateScript(NameOfDriver, ZipAddress)