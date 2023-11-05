import json
import hadithFields

import helpers

class Hadith:
    def __init__(self, chapter_info, reference, text, link):
        self.chapter_info = chapter_info
        self.reference = reference
        self.text = text
        self.link = link
    
    def get_json(self):
        payload = {}
        payload['chapter_info'] = self.chapter_info.get_json()
        payload['reference'] = self.reference.get_json()
        payload['text'] = self.text.get_json()
        payload['link'] = self.link.get_json()
        return payload
    
    def pprint_str(self, indent=0):
        result = "{\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.chapter_info + hadithFields.colon + self.chapter_info.pprint_str(indent + 1) + "\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.reference + hadithFields.colon + self.reference.pprint_str(indent + 1) + "\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.text + hadithFields.colon + self.text.pprint_str(indent + 1) + "\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.link + hadithFields.colon + self.link.pprint_str(indent + 1) + "\n"
        result = result + helpers.add_indent(indent + 1) + "}"
        return result

class ChapterInfo:
    def __init__(self, chapter_no, chapter_name):
        self.chapter_no = chapter_no
        self.chapter_name = chapter_name
    
    def get_json(self):
        payload = {}
        payload['chapter_no'] = self.chapter_no
        payload['chapter_name'] = self.chapter_name
        return payload
    
    def pprint_str(self, indent=0):
        result = "{\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.chapter_no + hadithFields.colon + self.chapter_no + "\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.chapter_name + hadithFields.colon + self.chapter_name + "\n"
        result = result + helpers.add_indent(indent + 1) + "}"
        return result

class Text:
    def __init__(self, english_text, arabic_text):
        self.english_text = english_text
        self.arabic_text = arabic_text
    
    def get_json(self):
        payload = {}
        payload['english_text'] = self.english_text.get_json()
        payload['arabic_text'] = self.arabic_text.get_json()
        return payload
    
    def pprint_str(self, indent=0):
        result = "{\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.english_text + hadithFields.colon + self.english_text.pprint_str(indent + 1) + "\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.arabic_text + hadithFields.colon + self.arabic_text.pprint_str(indent + 1) + "\n"
        result = result + helpers.add_indent(indent + 1) + "}"
        return result

class EnglishText:
    def __init__(self, narrated_text, details_text):
        self.narrated_text = narrated_text
        self.details_text = details_text
    
    def get_json(self):
        payload = {}
        payload['narrated_text'] = self.narrated_text
        payload['details_text'] = self.details_text
        return payload
    
    def pprint_str(self, indent=0):
        result = "{\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.narrated_text + hadithFields.colon + self.narrated_text + "\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.details_text + hadithFields.colon + self.details_text + "\n"
        result = result + helpers.add_indent(indent + 1) + "}"
        return result

class ArabicText:
    def __init__(self, full_arabic_text):
        self.full_arabic_text = full_arabic_text
    
    def get_json(self):
        payload = {}
        payload['full_arabic_text'] = self.full_arabic_text
        return payload

    def pprint_str(self, indent=0):
        result = "{\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.full_arabic_text + hadithFields.colon + self.full_arabic_text + "\n"
        result = result + helpers.add_indent(indent + 1) + "}"
        return result

class Reference:
    def __init__(self, reference, in_book_reference, uscmsa_web_reference):
        self.reference = reference
        self.in_book_reference = in_book_reference
        self.uscmsa_web_reference = uscmsa_web_reference

    def get_json(self):
        payload = {}
        payload['reference'] = self.reference
        payload['in_book_reference'] = self.in_book_reference
        payload['uscmsa_web_reference'] = self.uscmsa_web_reference
        return payload
    
    def pprint_str(self, indent=0):
        result = "{\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.reference + hadithFields.colon + self.reference + "\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.in_book_reference + hadithFields.colon + self.in_book_reference + "\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.uscmsa_web_reference + hadithFields.colon + self.uscmsa_web_reference + "\n"
        result = result + helpers.add_indent(indent + 1) + "}"
        return result

class Link:
    def __init__(self, url):
        self.url = url

    def get_json(self):
        payload = {}
        payload['url'] = self.url
        return payload
    
    def pprint_str(self, indent=0):
        result = "{\n"
        result = result + helpers.add_indent(indent + 1) + hadithFields.url + hadithFields.colon + self.url + "\n"
        result = result + helpers.add_indent(indent + 1) + "}"
        return result


class HadithProcessor():
    def __init__(self):
        pass

    def hadith_to_json(self, hadith):
        hadith_json = hadith.get_json()
        hadith_json_str = json.dumps(hadith_json)
        return hadith_json_str

    def json_to_hadith(self, hadith_json):
        hadith_json_object = json.loads(hadith_json)
        
        chapter_info = ChapterInfo(chapter_no=hadith_json_object[hadithFields.chapter_info][hadithFields.chapter_no], chapter_name=hadith_json_object[hadithFields.chapter_info][hadithFields.chapter_name])
        english_text = EnglishText(narrated_text=hadith_json_object[hadithFields.text][hadithFields.english_text][hadithFields.narrated_text], details_text=hadith_json_object[hadithFields.text][hadithFields.english_text][hadithFields.details_text])
        arabic_text = ArabicText(full_arabic_text=hadith_json_object[hadithFields.text][hadithFields.arabic_text][hadithFields.full_arabic_text])
        text = Text(english_text=english_text, arabic_text=arabic_text)
        link = Link(url=hadith_json_object[hadithFields.link][hadithFields.url])
        reference = Reference(reference=hadith_json_object[hadithFields.reference][hadithFields.reference], in_book_reference=hadith_json_object[hadithFields.reference][hadithFields.in_book_reference], uscmsa_web_reference=hadith_json_object[hadithFields.reference][hadithFields.uscmsa_web_reference])
        
        hadith = Hadith(chapter_info=chapter_info, reference=reference, text=text, link=link)
        return hadith
