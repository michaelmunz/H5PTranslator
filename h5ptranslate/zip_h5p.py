from zipfile import ZipFile
import os

# important:
# for h5p, the zip file must not use file attributes:
# zip -rDX myNewFile.h5p *
# cf. https://h5p.org/comment/43244#comment-43244


def zip_as_h5p(zipname, dirname):
    with ZipFile(zipname, 'w') as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(dirname):
           for filename in filenames:
               #create complete filepath of file in directory
               filePath = os.path.join(folderName, filename)
               # Add file to zip
               subdirname = filePath.replace(dirname, '')
               zipObj.write(filePath, subdirname)
