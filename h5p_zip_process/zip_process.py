import sys
import h5p_python.zipfile2 as zip

if __name__ == "__main__":
    #TODO: check arguments lenghts!

    action = sys.argv[1]
    zip_path = sys.argv[2]
    member_name = sys.argv[3]

    if action == "extract":
        tempdirname = sys.argv[4]
        with zip.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extract(member_name, tempdirname)

    elif action == "replace":
        file = sys.argv[4]
        with zip.ZipFile(zip_path, 'a') as zipObj:
            if(member_name in zipObj.filelist):
                zipObj.remove(member_name)
                zipObj.write(file, member_name)



