import subprocess
import os
import base64
import sys
class GoogleTransProxy:

    def translate(self, source_language, target_language, text):
        exe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../h5p_translate_process/dist/translate_process/translate_process.exe"))
        #exe_path = os.path.abspath("run_translate_process.bat")
        text_encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')

        #proc = subprocess.run([exe_path, source_language, target_language, text_encoded], capture_output=True)
        # res_b64 = proc.stdout.decode()
        res_b64 = subprocess.check_output([exe_path, source_language, target_language, text_encoded])


        res = base64.b64decode(res_b64).decode('utf-8')

        return res

if __name__ == "__main__":
    text = r"<h2><span style=\"color:#0455a2;\">Let's start getting into the MDR</span></h2>\n\n<p>&nbsp;</p>\n\n<p>&nbsp;</p>\n\n<p>We already know that the<strong> <a href=\"https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0745\" target=\"_blank\">MDR</a></strong> is more extensive and conrete compared to the MDD. Instead of 23 articles, there are now <strong>123 articles</strong>, 7 <strong>annexes </strong>became<strong> 17.</strong></p>\n\n<p>However, the MDR is legally binding (mandatory justification), all contents are directly defined and specified by the MDR. For example, the documentation for compliance with safety standards is described in detail, also how much data and which are collected is defined in the MDR at the European level.</p>\n\n<p><strong>All devices already placed on the market must be re-certified according to the new requirements by 2024/2025.</strong></p>\n\n<p><br>\n&nbsp;</p>\n"
    translate = GoogleTransProxy()
    res = translate.translate("en", "de", text)
    print(res)
