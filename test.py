import sys
import h5p_python.zipfile2 as zip

if __name__ == "__main__":
    #TODO: check arguments lenghts!

    action = "replace"
    zip_path = r"U:\source\MedTec\H5PTranslator\data\course-presentation-36.h5p"
    member_name = 'content/content.json'

    if action == "extract":
        #tempdirname = sys.argv[4]
        with zip.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extract(member_name, tempdirname)

    elif action == "replace":
        file = r'U:\source\MedTec\H5PTranslator\data\content.json'
        with zip.ZipFile(zip_path, 'a') as zipObj:
            zipObj.remove(member_name)
            zipObj.write(file, member_name)



