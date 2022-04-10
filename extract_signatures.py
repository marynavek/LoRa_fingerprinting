import csv, os
import random
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

file_path = "/Users/marynavek/Projects/LoRa_fingerprinting/uplinks_ds.csv"
with open(file_path, newline='') as csvfile:
    uplinks_reader = csv.DictReader(csvfile)
    signature_dictionary_train_dataset = []
    signature_dictionary_test_dataset = []
    list_of_devAddresses = []
    new_dict = []
    
    for item in uplinks_reader:
        new_dict.append(item)
        if item["dev_addr"] not in list_of_devAddresses:
                list_of_devAddresses.append(item["dev_addr"])
    dictionary_of_addresses = []
    print(len(new_dict))
    for address in list_of_devAddresses:
        if address != "1":
            temp_dictionary = []
            for new_item in new_dict:
                if new_item["dev_addr"] == address:
                    temp_dictionary.append(new_item)
            temp_dictionary = sorted(temp_dictionary,  key=lambda x: x["f_cnt"])

            addItem = {address: temp_dictionary}
            dictionary_of_addresses.append(addItem)

    dictionary_of_addresses
    for address in list_of_devAddresses:
        if address != "1":
            uplinks = []
            temp_signarure_array = []
            for item in dictionary_of_addresses:
                if address in item.keys():
                    for link in item[address]:
                        uplinks.append(link)
            bins_count = 0
            signature_array = []
            stride = 1
            first_position_for_iat = 0

            for first_position_for_iat in range(len(uplinks)-20):
                for link_index in range(first_position_for_iat, 20+first_position_for_iat):
                    
                    signature_array.append(float(uplinks[link_index]["inter_arrival_time_ms"]))
                # normalized signature
                # signature, _ = np.histogram(signature_array, bins=300)
                # non-normalized signature
                # print(len(signature_array))
                signature, _ = np.histogram(signature_array,range=(0,20000), bins=500)
                addItem = {"dev_addr": address, "signature": signature}
                temp_signarure_array.append(addItem)
                signature_array = []

            random.shuffle(temp_signarure_array)
            test_signatures_amount = len(temp_signarure_array)*0.3
            train_signatures_amount = len(temp_signarure_array) - test_signatures_amount
            # train_signatures_amount = 70
            # test_signatures_amount = 30
            i = test_signatures_amount - 1
            while i >= 0:
                signature_dictionary_test_dataset.append(temp_signarure_array.pop())
                random.shuffle(temp_signarure_array)
                i -= 1
            d = 0
            for signature in temp_signarure_array: 
                if d <= train_signatures_amount:
                    signature_dictionary_train_dataset.append(signature)
                    d += 1
                
    file_name_test = 'signatures_test.csv'
    csv_path_test = os.path.join("/Users/marynavek/Projects/LoRa_fingerprinting/", file_name_test)
    with open(csv_path_test, 'w') as csvfile:
        fieldnames=["dev_addr", "signature"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in signature_dictionary_test_dataset:
            writer.writerow(data)
    
    file_name_train = 'signatures_train.csv'
    csv_path_train = os.path.join("/Users/marynavek/Projects/LoRa_fingerprinting/", file_name_train)
    with open(csv_path_train, 'w') as csvfile:
        fieldnames=["dev_addr", "signature"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in signature_dictionary_train_dataset:
            writer.writerow(data)
            
