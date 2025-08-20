import hashlib
import json
import os
import time

from curl_cffi import requests
from pathlib import Path

from pydash import times

final_data = []


#TODO:: Pagesave conection path
try:
    # PAGESAVE_PATH = Path("D:/Sharma Danesh/Pagesave/PolicyBazaar_feasiblity/09_07_2025")
    PAGESAVE_PATH = Path("D:/Sharma Danesh/Pagesave/PolicyBazaar_feasiblity/19_08_2025_1")
    PAGESAVE_PATH.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(e)

def pagesave_portion(join_path, table_section,car_number):
    # Headers — adjust as needed
    headers = {
        "accept": "application/json",
        "Accept-Encoding": "gzip",
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJNb2JpbGVObyI6Ijk3MjYxNDkwNjgiLCJJc0N1c3RvbWVyIjoidHJ1ZSIsInJvbGUiOiJDdXN0b21lciIsIkxvZ2luSUQiOiI5MTUxNDM3MCIsIlN1YlNvdXJjZSI6Ik1ZQUNDQVBQIiwiQ3VzdG9tZXJJRCI6IjEzNDcwMjg1MyIsIkxvZ2luTWVkaXVtIjoiT1RQIiwiU291cmNlIjoiTVlBQ0NBUFAiLCJJc0FwcEZsb3ciOiJ0cnVlIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbW9iaWxlcGhvbmUiOiI5NzI2MTQ5MDY4IiwidW5pcXVlX25hbWUiOiJEYW5lc2giLCJuYmYiOjE3NTIwNDA0NjcsIkFnZW50SUQiOjAsIkdtYWlsSUQiOiIiLCJDb3VudHJ5Q29kZSI6IjkxIiwiZXhwIjoxNzgzNTc2NDY3LCJTZXNzaW9uSUQiOiI2ODZlMDQxM2U1OWE5ODI1MmNhNzEwMDgiLCJpYXQiOjE3NTIwNDA0NjcsImVtYWlsIjoiZGFuZXNoLnNoYXJtYS5hY3Rvd2l6QGdtYWlsLmNvbSJ9.EEY_Ksq_VMbPjlAqM5diQPPzmG7IusFc2bYlg3Mlvmo",
        "Connection": "Keep-Alive",
        "Host": "api.policybazaar.com",
        "origin": "",
        "os": "android",
        "user-agent": "PBApp-android/5.2.6 (android 9)",
        "x-pb-source": "MYACCAPP",
    }

    # TODO:: For getting visitor ID content ......
    try:
        url = "https://api.policybazaar.com/mobile/motorprequote/CreateVisit"
        payload = {
            "landingPageName": "PreLanding",
            "referrer": "",
            "UtmSource": "organic",
            "UtmCampaign": "organic",
            "UtmTerm": "AND_5.2.6-1_v2",
            "UtmContent": "",
            "UtmMedium": "app_grid_car_v1"
        }
        response = requests.post(url, json=payload, headers=headers, impersonate='chrome120')
        my_main_json = response.json()
        visitor_id = my_main_json.get('data').get("visitId")
    except Exception as e:
        print("Something issue in the first request", e)

    # TODO:: For getting rtoId content ......
    try:
        rtoId_url = "https://api.policybazaar.com/mobile/motorprequote/RcDetails"
        rtoId_payload = {
            "registrationNumber": f"{car_number.replace('-', '')}",
            "visitData": {
                "landingPageName": "PreLanding",
                "referrer": "",
                "utmMedium": "app_grid_car_v1"
            },
            "visitId": visitor_id
        }

        rtoId_response = requests.post(rtoId_url, json=rtoId_payload, headers=headers, impersonate='chrome120')
        if rtoId_response.ok and rtoId_response.status_code == 200 and "visitId" in rtoId_response.text:
            my_f1json = rtoId_response.json()
            f1_visitId = my_f1json.get('data').get("visitId")
            f1_rtoId = my_f1json.get('data').get("rtoId")
            f1_makeId = my_f1json.get('data').get("makeId")
            f1_modelId = my_f1json.get('data').get("modelId")
            f1_fuelTypeId = my_f1json.get('data').get("fuelTypeId")
            f1_vehicleCode = my_f1json.get('data').get("vehicleCode")
            f1_registrationDate = my_f1json.get('data').get("registrationDate")
        else:
            print(f"Error {response.status_code}")
    except Exception as e:
        print("Something issue in the second request", e)

    # TODO:: For getting enquiryId content ......
    try:
        CreateEnquiry_URl = "https://api.policybazaar.com/mobile/motorprequote/CreateEnquiry"
        CreateEnquiry_payload = {
            "visitId": f1_visitId,
            "rtoId": f1_rtoId,
            "makeId": f1_makeId,
            "modelId": f1_modelId,
            "fuelTypeId": f1_fuelTypeId,
            "vehicleCode": f1_vehicleCode,
            "registrationDate": f"{f1_registrationDate}",
            "isNewCar": False,
            "registrationNumber": f"{car_number.replace('-', '')}",
            "UtmSource": "organic",
            "UtmCampaign": "organic",
            "UtmTerm": "AND_5.2.6-1_v2",
            "UtmContent": "",
            "UtmMedium": "app_grid_car_v1"
        }
        CreateEnquiry_req = requests.post(CreateEnquiry_URl, json=CreateEnquiry_payload, headers=headers,
                                          impersonate='chrome120')
        CreateEnquiry_req_json = CreateEnquiry_req.json()
        enquiryId = CreateEnquiry_req_json.get("data").get("enquiryId")
        # print(enquiryId)
    except Exception as e:
        print("Something issue in enquiryId request...", e)

    # TODO:: For getting re-direct url ......
    try:
        re_direct_url = "https://api.policybazaar.com/mobile/motorprequote/CreateLead"
        re_direct_payload = {
            "name": "Danesh",
            "email": "danesh.sharma.actowiz@gmail.com",
            "custDataSrc": "",
            "enquiryId": f"{enquiryId}",
            "encName": None,
            "encEmail": None,
            "encMobile": None,
            "isEdited": True,
            "UtmSource": "adtiming_int",
            "UtmCampaign": "automatetech",
            "UtmTerm": "AND_5.2.6-1_v2",
            "UtmContent": "",
            "UtmMedium": "app_grid_car_v1"
        }
        re_direct_req = requests.post(re_direct_url, json=re_direct_payload, headers=headers, impersonate='chrome120')
        re_direct_req_json = re_direct_req.json()
        redirectUrl = re_direct_req_json.get("data").get("redirectUrl")
    except Exception as e:
        print("Something issue in the re-drect request", e)

    # TODO:: For getting car all prices ......
    try:
        enId = f"{redirectUrl.split('?id=')[-1].split('%3d&id2=')[0]}"
        car_price_url = "https://api.policybazaar.com/mobile/motorquotes/Quotes"
        car_price_payload = {
            "enquiryId": enId,
            "enquiryId2": "dmZoWVBlVmJNNWhDcnJTVURyZ1dOZz09",
            "filters": [
                {
                    "sectionName": "Addons",
                    "sectionId": 51,
                    "filterId": 101,
                    "filterText": "Zero Depreciation",
                    "selectedAmount": None,
                    "isPremiumFactor": False,
                    "isPremiumCover": False,
                    "isAmountApplicable": False,
                    "sectionType": "ADDONS",
                    "typeSelection": "checkbox"
                },
                {
                    "sectionName": "Addons",
                    "sectionId": 51,
                    "filterId": 102,
                    "filterText": "24x7 Roadside Assistance",
                    "selectedAmount": None,
                    "isPremiumFactor": False,
                    "isPremiumCover": False,
                    "isAmountApplicable": False,
                    "sectionType": "ADDONS",
                    "typeSelection": "checkbox"
                },
                {
                    "sectionName": "Addons",
                    "sectionId": 51,
                    "filterId": 103,
                    "filterText": "Engine Protection Cover",
                    "selectedAmount": None,
                    "isPremiumFactor": False,
                    "isPremiumCover": False,
                    "isAmountApplicable": False,
                    "sectionType": "ADDONS",
                    "typeSelection": "checkbox"
                }
            ],
            "isAppliedFilter": True,
            "tabSectionId": table_section,
            "enableTabs": True
        }
        car_price_req = requests.post(car_price_url, json=car_price_payload, headers=headers, impersonate='chrome120')
        car_price_json = car_price_req.json()
        # print(car_price_json)
    except Exception as e:
        print("Something issue in the car prices request", e)

    if car_price_req.status_code == 200 and "idv" in car_price_req.text:
        try:
            with open(join_path, "w") as file:
                file.write(json.dumps(car_price_json))  # Convert dict to string
            my_selector = car_price_json
        except Exception as e:
            print(f"File write error: {e}")
    else:
        my_selector = ""

    return json.dumps(car_price_json)

def main_final(car_number):
    table_sections = [1001,1002,1003]
    for table_section in table_sections:
        page_name = f"{car_number.replace('-','')}_{table_section}.json"
        join_path = PAGESAVE_PATH / page_name

        if os.path.exists(join_path):
            my_selector = open(join_path, "r", encoding="utf-8").read()
        else:
            my_selector = pagesave_portion(join_path, table_section,car_number)

        if my_selector:
            my_json = json.loads(my_selector)
            main_loop  = my_json.get('data').get('bucketList')
            for sub_loop in main_loop:
                looping = sub_loop.get("plans")
                for min_loop in looping:


                    item = {}
                    Insurer_Name = min_loop.get('insurerName')
                    if Insurer_Name:
                        Plan_type = min_loop.get('planDetails')[0].get('planName')
                        IDV = min_loop.get('idv')
                        Premium_Amount = min_loop.get('planDetails')[0].get('basePremium')
                        Discount = ""
                        Add_ons_Included_loop_list = [
                            addon.get('title')
                            for addon in (
                                    (((min_loop.get('planDetails') or [{}])[0])
                                     .get('addonHighlightsSection') or {})
                                    .get('customerSelectedAddons') or []
                            )
                        ]

                        item['Car Number'] = car_number
                        item['Insurer Name'] = Insurer_Name
                        item['Plan Type'] = Plan_type
                        item['IDV'] = IDV
                        item['Premium Amount'] = Premium_Amount
                        item['Discount'] = Discount
                        item['Add-ons Included'] = Add_ons_Included_loop_list
                        item['Table Section'] = table_section
                        final_data.append(item)

if __name__ == '__main__':
    st_tm = time.time()
    # car_number = "GJ-27-EE-4956"
    # car_number = "GJ-05-JD-9759"
    car_number_list = [
        "MH-46-CR-3636",
        "GJ-27-EE-4956"
    ]
    for car_number in car_number_list:
        main_final(car_number)

    import pandas as pd
    print(final_data)
    df = pd.DataFrame(final_data)
    output_path = "policybazaar_sample_19082025.xlsx"
    df.to_excel(output_path, index=False)
    # print(json.dumps(final_data))

    print(time.time() - st_tm)