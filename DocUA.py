import requests
import json

import xlsxwriter


class DocUA:
    def __init__(self):
        self.data_ = {"method_name": "ListDoctors",
                      "param": {"language": 1, "city_id": 1, "offset": 10, "limit": 10, "sorting_mode": None,
                                "premium_on_top": False, "sorting_direction": 1, "metro_aliases": [],
                                "district_aliases": [],
                                "time_slots_for": None, "specialty_alias": None}}
        self.headers_ = {'Content-type': 'application/json',  # Определение типа данных
                         'Accept': 'text/plain',
                         'Content-Encoding': 'utf-8'}

        #  "Парикмахерская", "Салон красоты", "Лазерная эпиляция", "Барбершоп",
        #  "Студия наращивания ресниц и коррекции бровей", "SPA",  "Спорт и тренировки",
        #  "Тату и пирсинг", "Центр коррекции веса"

        self.category_ = ["Стоматолог", "Косметолог", "пластическ", "контурная", "Трихолог",
                          "косметолог", "педикюр", "маникюр", "массаж"]
        self.forbidden = ["ЛОР", "невролог"]

        self.parsed_doctors = []

    def check_specialities(self, doctor):

        print("checking doctor")
        string_to_check = ""
        string_to_check += doctor["short_about"] + " "
        for sp in range(len(doctor["specialities"])):
            string_to_check += doctor["specialities"][sp]["name"] + " "

        string_to_check.lower()

        for word in self.forbidden:
            if string_to_check.find(word) != -1:
                return False

        for word in self.category_:
            if string_to_check.find(word) != -1:
                print("success")
                return True
        print("failure")
        return False

    def save_doctor(self, doctor):
        f_i_o = []
        city = []
        description = []
        category = []
        speciality = []

        f_i_o.append(doctor["last_name"])
        f_i_o.append(doctor["name"])
        f_i_o.append(doctor["middle_name"])
        city.append(doctor["city"]["name"])
        description.append(doctor["short_about"])
        category.append(doctor["category"]["name"])

        for name in doctor["specialities"]:
            speciality.append(name["name"])
        self.parsed_doctors.append([f_i_o, description, city, category, speciality])
        return True

    def write_to_file(self):
        workbook = xlsxwriter.Workbook('doctors.xlsx')
        worksheet = workbook.add_worksheet()

        for doctor_info in range(len(self.parsed_doctors)):
            for group in range(len(self.parsed_doctors[doctor_info])):
                for cell in range(len(self.parsed_doctors[doctor_info][group])):
                    print(str(self.parsed_doctors[doctor_info][group][cell]))
                    worksheet.write(doctor_info+1, cell, str(self.parsed_doctors[doctor_info][group][cell]))
                print("\n\n")
                break

        workbook.close()

    def parse(self):
        try:
            while True:
                if len(self.parsed_doctors) == 10:
                    print(10 / 0)
                response = requests.post("https://api.doc.ua/", data=json.dumps(self.data_), headers=self.headers_)
                response = json.loads(response.text)
                self.data_["param"]["offset"] += 10
                for i in range(len(response["data"]["items"])):
                    if self.check_specialities(response["data"]["items"][i]["doctor"]) is True:
                        self.save_doctor(response["data"]["items"][i]["doctor"])
        except Exception as ex:
            self.write_to_file()
            print(ex)
