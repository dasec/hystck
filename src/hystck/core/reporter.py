try:
    from logging import DEBUG
    from hystck.utility.logger_helper import create_logger
    import xml.etree.ElementTree as ET
    import platform
    import os
    import datetime
except Exception as e:
    raise RuntimeError("Error while loading modules: " + str(e))


class Reporter(object):
    """ This class is responsible for the creation of a report for a case

    """
    root = ""
    doc = ""
    mails = []
    downloads = []
    browsings = []
    container = []
    imagename = ""
    author = ""
    hash = ""
    date = ""
    baseimage = ""
    basehash = ""

    def __init__(self):
        self.logger = create_logger("reporter", DEBUG)
        self.logger.info("Reporter has been loaded and can be used")
        self.root = ET.Element("root")
        self.date = datetime.datetime.today().strftime('%m-%d-%Y %H:%M')

    def add(self, tag, text):
        if(tag == "mail"):
            self.mails.append(text)
        elif(tag == "download"):
            self.downloads.append(text)
        elif(tag == "browsings"):
            self.browsings.append(text)
        elif(tag == "veracrypt"):
            self.container.append(text)
        elif(tag == "imagename"):
            self.imagename = text
        elif (tag == "author"):
            self.author = text
        elif (tag == "hash"):
            self.hash = text
        elif (tag == "baseimage"):
            self.baseimage = text
        elif (tag == "basehash"):
            self.basehash = text
        else:
            print("unknown tag.")

    def generateTags(self):
        self.doc = ET.SubElement(self.root, "general")
        ET.SubElement(self.doc, "imagename").text = self.imagename
        ET.SubElement(self.doc, "author").text = self.author
        ET.SubElement(self.doc, "hash").text = self.hash
        ET.SubElement(self.doc, "date").text = self.date
        ET.SubElement(self.doc, "baseimage").text = self.baseimage
        ET.SubElement(self.doc, "basehash").text = self.basehash

        self.doc = ET.SubElement(self.root, "mails")
        for mail in self.mails:
            ET.SubElement(self.doc, "mail").text = mail

        self.doc = ET.SubElement(self.root, "downloads")
        for download in self.downloads:
            ET.SubElement(self.doc, "download").text = download

        self.doc = ET.SubElement(self.root, "browsings")
        for browsing in self.browsings:
            ET.SubElement(self.doc, "browsing").text = browsing

        self.doc = ET.SubElement(self.root, "container")
        for cont in self.container:
            ET.SubElement(self.doc, "veracrypt").text = cont

    def generate(self):
        self.generateTags()
        tree = ET.ElementTree(self.root)
        tree.write("reports/report_" + self.imagename + "_" + self.date + ".xml")
        os.chmod("reports/report_" + self.imagename + "_" + self.date + ".xml", 0o777)
        self.logger.info("Report has been generated.")
