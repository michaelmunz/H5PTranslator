
#import requests
#from requests_html import HTMLSession
import sys
from googletrans import Translator
import base64


class GoogleTrans:
    translator = Translator()
    def translate(self, source_language, target_language, text):
        res = self.translator.translate(text, src=source_language, dest=target_language)
        return res.text


# class GoogleTranslate:
#     url = "https://translate.google.com/?sl={sl}&tl={tl}&text={text}&op=translate"
#
#     def translate(self, source_language, target_language, text):
#         text_encoded = requests.utils.quote(text)
#         text_encoded = text_encoded
#
#         query = self.url.format(sl=source_language, tl=target_language, text=text_encoded)
#
#         #session = HTMLSession()
#
#         res = requests.get(query)
#
#         #res = session.get(query)
#         #res.html.render()
#
#         button = res.html.xpath('//button[@aria-label="Reject all"]')
#         if button is not None:
#             script = '() => {document.getElementsByTagName("button")[0].click()}'
#             res.html.render(sleep=1, timeout=10000, script=script, reload=False)
#
#         classname_to_search = "ryNqvb"
#         #search_res = res.html.search(classname_to_search)[0]
#         res.html.render(sleep=5)
#
#
#         pathres = res.html.xpath('//span[@class="ryNqvb"]')
#         pathres


# class DeeplTranslate():
#     url = "https://www.deepl.com/translator#{sl}/{tl}/{text}"
#
#     def translate(self, source_language, target_language, text):
#         text_encoded = requests.utils.quote(text)
#         text_encoded = text_encoded
#
#         query = self.url.format(sl=source_language, tl=target_language, text=text_encoded)
#
#         session = HTMLSession()
#         res = session.get(query)
#         res.html.render(sleep=1)
#
#         classname_to_search = "ryNqvb"
#         #search_res = res.html.search(classname_to_search)[0]
#
#         pathres = res.html.html.xpath('//span[@class="ryNqvb"]')
#         pathres



if __name__ == "__main__":
    #text = b"<h2><span style=\"color:#0455a2;\">Let's start getting into the MDR</span></h2>\n\n<p>&nbsp;</p>\n\n<p>&nbsp;</p>\n\n<p>We already know that the<strong> <a href=\"https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0745\" target=\"_blank\">MDR</a></strong> is more extensive and conrete compared to the MDD. Instead of 23 articles, there are now <strong>123 articles</strong>, 7 <strong>annexes </strong>became<strong> 17.</strong></p>\n\n<p>However, the MDR is legally binding (mandatory justification), all contents are directly defined and specified by the MDR. For example, the documentation for compliance with safety standards is described in detail, also how much data and which are collected is defined in the MDR at the European level.</p>\n\n<p><strong>All devices already placed on the market must be re-certified according to the new requirements by 2024/2025.</strong></p>\n\n<p><br>\n&nbsp;</p>\n"
    #translate = GoogleTranslate()
    # translate = DeeplTranslate()
    #translate = GoogleTrans()
    #res = translate.translate("en", "de", text)
    #print(res)

    translate = GoogleTrans()


    if len(sys.argv)==4:
        src_lang = sys.argv[1]
        target_lang = sys.argv[2]
        text_b64 = sys.argv[3]+"="
    else:
        src_lang = "en"
        target_lang = "de"
        text = r"<h2><span style=\"color:#0455a2;\">Let's start getting into the MDR</span></h2>\n\n<p>&nbsp;</p>\n\n<p>&nbsp;</p>\n\n<p>We already know that the<strong> <a href=\"https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0745\" target=\"_blank\">MDR</a></strong> is more extensive and conrete compared to the MDD. Instead of 23 articles, there are now <strong>123 articles</strong>, 7 <strong>annexes </strong>became<strong> 17.</strong></p>\n\n<p>However, the MDR is legally binding (mandatory justification), all contents are directly defined and specified by the MDR. For example, the documentation for compliance with safety standards is described in detail, also how much data and which are collected is defined in the MDR at the European level.</p>\n\n<p><strong>All devices already placed on the market must be re-certified according to the new requirements by 2024/2025.</strong></p>\n\n<p><br>\n&nbsp;</p>\n"
        text_b64 = base64.b64encode(text.encode('utf-8')).decode('utf-8')

    text = base64.b64decode(text_b64.encode('utf-8')).decode('utf-8')
    res = translate.translate(src_lang, target_lang, text)

    res_encoded = base64.b64encode(res.encode('utf-8')).decode('utf-8')
    print(res_encoded)

