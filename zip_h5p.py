import h5p_python.zipfile2 as zip
import os

# important:
# for h5p, the zip file must not use file attributes:
# zip -rDX myNewFile.h5p *
# cf. https://h5p.org/comment/43244#comment-43244


def zip_as_h5p(zipname, dirname):
    with zip.ZipFile(zipname, 'w') as zipFile:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(dirname):
           for filename in filenames:
               #create complete filepath of file in directory
               filePath = os.path.join(folderName, filename)
               # Add file to zip
               subdirname = filePath.replace(dirname, '')
               zipFile.write(filePath, subdirname)



def extract(zipfile, member_name, tempdirname):
    with zip.ZipFile(zipfile, 'r') as zip_ref:
        zip_ref.extract(member_name, tempdirname)


def replace(zipfile, member_name, file):
    with zip.ZipFile(zipfile, 'a') as zipFile:
        if member_name in zipFile.namelist():
            zipFile.remove(member_name)
            zipFile.write(file, member_name)