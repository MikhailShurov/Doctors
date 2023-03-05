import requests
import json
from bs4 import BeautifulSoup

import xlsxwriter


class BarbUA:
    def __init__(self):
        self.links_with_subdirectories = []
        self.doctors = set()

    def save_subdirectory_links(self):
        response = requests.get("https://barb.ua/")
        soup = BeautifulSoup(response.text, "lxml")
        main_section = soup.find("section", {"id": "mainpage"})

        uls = main_section.findAll("ul")
        uls = uls[-2:]

        for val in uls:
            a = val.findAll("a")
            for aa in a:
                self.links_with_subdirectories.append(aa.get("href"))

        print(self.links_with_subdirectories)

    def parse(self):
        self.save_subdirectory_links()
        for link in self.links_with_subdirectories:
            print(link)
            try:
                doctors = []
                counter = 1
                while True:
                    if "page" not in link:
                        link += f"?page={counter}"
                    else:
                        counter += 1
                        link = link[:-1] + str(counter)
                    print("***************** NEXT PAGE *****************")
                    print(link)
                    print("*********************************************")
                    response = requests.get(link)
                    soup = BeautifulSoup(response.text, "lxml")
                    main_window = soup.find("div", {"id": "filters-result"})
                    a_tags = main_window.findAll("a")

                    for c_link in a_tags:
                        a_tag = c_link.get("href")
                        if "master" in a_tag:
                            if len(doctors) == 0 or (str(doctors[-1]) not in str(a_tag)):
                                print(a_tag)
                                doctors.append(a_tag)
                                self.doctors.add(a_tag)

            except Exception as ex:
                print("All is ok, here is exception")
                print("***********************************************************")
                print(ex)
                print("***********************************************************\n")

        print(self.doctors)