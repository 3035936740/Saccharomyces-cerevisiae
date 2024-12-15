import base64
import xml.etree.ElementTree as ET
from xml.dom import minidom

def decode_b64(msg: str, dst: str):
    _f = open(dst, 'wb')
    _f.write(base64.b64decode(msg))
    _f.close()


def jis_2_utf(jis: str, utf: str, is_mod_data: bool = False):
    jis_data: list[str] = []
    
    if is_mod_data:
        with open(jis, 'r', encoding='cp932') as jis_xml:
            xml_string = jis_xml.read()
        # 解析 XML 字符串
        root = ET.fromstring(xml_string)

        # 使用 minidom 格式化 XML
        xml_str = ET.tostring(root).decode('cp932')
        xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
        jis_data = xml_str.splitlines()
    else:
        with open(jis, 'r', encoding='cp932') as jis_xml:
            jis_data = jis_xml.readlines()

    utf_xml = open(utf, 'w', encoding='utf-8')
    utf_xml.write('<?xml version="1.0" encoding="utf-8"?>\n')
    jis_data.pop(0)
    for line in jis_data:
        utf_xml.write(line)
    utf_xml.close()


def amend_jis(jis_str: str) -> str:
    if not jis_str:
        return ''
    new = jis_str
    # latin field
    new = new\
        .replace("驫", "ā").replace("騫", "á").replace("曦", "à").replace('頽', 'ä').replace("罇", "ê").replace("曩", "è")\
        .replace("齷", "é").replace("彜", "ū").replace("鬥", "Ã").replace("雋", "Ǜ").replace("隍", "Ü").replace("趁", "Ǣ")\
        .replace("鬆", "Ý").replace("驩", "Ø")
    # symbol field
    new = new\
        .replace("龕", "€").replace("蹇", "₂").replace("鬻", "♃").replace('黻', '*').replace('鑷', 'ゔ')
    # graph field
    new = new\
        .replace("齶", "♡").replace("齲", "❤").replace("躔", "★").replace('釁', '🍄').replace('齪', '♣').replace('鑈', '♦')\
        .replace('霻', '♠').replace('盥', '⚙')
    return new
