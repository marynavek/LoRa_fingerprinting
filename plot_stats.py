import csv, os
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import json, os, csv

# file_names = ["device_dataset_1.json", "device_dataset_2.json", "device_dataset_3.json", "device_dataset_4.json"]
file_names = ["ArduinoMega.json", "ArduinoPro.json", "expLoRaBLE.json"]
path = "/Users/marynavek/Projects/LoRa_fingerprinting"
final_dataset = []
count = 0
array1 = []
array2 = []
array3 = []
for file in file_names:
    print(file)
    json_path = os.path.join(path, file)
    f = open(json_path)

    uplink_objects = list()
    downlink_objects = list()

    data = json.load(f)
    for item in data:
        link_name = item["name"]
        if link_name == "gs.up.receive":
            uplink_objects.append(item)
        elif link_name == "gs.down.send":
            downlink_objects.append(item)
    f.close()  

    uplinks_ds_device_1 = []
    list_of_devAddresses = []

    for link in uplink_objects:
        time = link["time"]
        payload = link["data"]["payload"] if "data" in link else None
        settings = link["data"]["settings"] if "data" in link else None
        rx_metadata = link["data"]["rx_metadata"] if "data" in link else None
        # print(link)
        if payload != None:
            m_hdr_type = payload["m_hdr"]["m_type"] if "m_hdr" in payload else None
            dev_addr = payload["mac_payload"]["f_hdr"]["dev_addr"] if "mac_payload" in payload else None
            f_cnt = payload["mac_payload"]["f_hdr"]["f_cnt"] if "mac_payload" in payload else None
            f_port = payload["mac_payload"]["f_port"] if "f_port" in payload["mac_payload"] else None
        if settings != None:
            bandwidth = settings["data_rate"]["lora"]["bandwidth"]
            sf = settings["data_rate"]["lora"]["spreading_factor"]
            coding_rate = settings["coding_rate"]
            frequency = settings["frequency"]
        else: 
            bandwidth = None
            sf = None
            coding_rate = None
            frequency = None
        if rx_metadata != None:
            rssi = rx_metadata[0]["rssi"]
            channel_rssi = rx_metadata[0]["channel_rssi"]
            snr = rx_metadata[0]["snr"] if "snr" in rx_metadata[0] else None
        else:
            rssi = None
            channel_rssi = None
            snr = None
        if dev_addr is None:
            dev_addr = "111111"
        if dev_addr not in list_of_devAddresses:
            list_of_devAddresses.append(dev_addr)
        
        addObject = {"dev_addr": dev_addr, "time": time, "m_hdr_type": m_hdr_type, "f_cnt": f_cnt, "f_port": f_port, "bandwidth": bandwidth, "sf": sf, "coding_rate": coding_rate,
                    "frequency":frequency, "rssi": rssi, "channel_rssi": channel_rssi, "snr": snr}
        
        uplinks_ds_device_1.append(addObject)

    for address in list_of_devAddresses:
        temp_dictionary = []
        for item in uplinks_ds_device_1:
            if item["dev_addr"] == address:
                temp_dictionary.append(item)
        temp_dictionary = sorted(temp_dictionary,  key=lambda x: x["f_cnt"])
        time_previous = 0
        for item in temp_dictionary:
            time = item["time"]
            year, month, day = time.split("-")
            day, time_values = day.split("T")
            hours, minutes, seconds = time_values.split(":")
            seconds, miliseconds = seconds.split(".")
            miliseconds, _ = miliseconds.split("Z")

            total_miliseconds = ((int(hours) * 60 * 60) + (int(minutes) * 60) + int(seconds)) * 1000 + (int(miliseconds) * 0.000001)

            if time_previous == 0:
                inter_arrival_time_ms = 0
            else:
                inter_arrival_time_ms = total_miliseconds - time_previous
            time_previous = total_miliseconds
            item["inter_arrival_time_ms"] = inter_arrival_time_ms
            if inter_arrival_time_ms != 0:
                final_dataset.append(item)

for item in final_dataset:
    if item["dev_addr"] not in list_of_devAddresses:
        list_of_devAddresses.append(item["dev_addr"])
dictionary_of_addresses = []   
print(list_of_devAddresses)     
for address in list_of_devAddresses:
        temp_dictionary = []
        for new_item in final_dataset:
            if new_item["dev_addr"] == address:
                temp_dictionary.append(new_item)
        temp_dictionary = sorted(temp_dictionary,  key=lambda x: x["f_cnt"])

        addItem = {address: temp_dictionary}
        dictionary_of_addresses.append(addItem)

for address in list_of_devAddresses:
    count +=1
    uplinks = []
    temp_signarure_array = []
    bins_count = 0
    signature_array = []
    for item in dictionary_of_addresses:
        if address in item.keys():
            for link in item[address]:
                uplinks.append(link)
    for link in uplinks:   
        bins_count += 1
        # if float(link["inter_arrival_time_ms"]) < 15000:
        #         iat = (float(link["inter_arrival_time_ms"]) - 10000) * 10000000000
        # else:
        #     iat = (float(link["inter_arrival_time_ms"]) - 16000) * 10000000000
        # signature_array.append(iat)
        signature_array.append(link["inter_arrival_time_ms"])
    # signature_array = np.asarray(signature_array)
    # plt.hist(signature_array, color = 'blue', edgecolor = 'black')
    if count == 1:
        array1 = signature_array
    if count == 2:
        array2 = signature_array
    if count == 3:
        array3 = signature_array
    # sns.set_style('whitegrid')
    # sns.kdeplot(np.array(signature_array), bw=0.1)

    # title = "Histogram of" + address
    # plt.title(title)
    # plt.xlabel('Time')
    # plt.ylabel('IAT Distribution')
    # plt.show()

data1 = {'signatures': array1}
data2 = {'signatures': array2}
data3 = {'signatures': array3}
 
# Create the pandas DataFrame

# print(len(array1))
# print(len(array2))
# print(len(array3))
# df = pd.DataFrame({
#     'signatures1': array1,
#     'signatures2': array2,
#     'signatures3': array3,
# })

# ax = df.plot.kde()
# sns.set_style('whitegrid')
fig, ax = plt.subplots()
sns.kdeplot(data=array1, ax=ax, color='red', fill=True, label='means TP')
sns.kdeplot(data=array2, ax=ax, color='green', fill=True, label='means TN')
sns.kdeplot(data=array3, ax=ax, color='purple', label='means FP')
# # sns.kdeplot(data=mc_means_FN.squeeze(), ax=ax, color='purple', label='means FN')
# # ax.legend(bbox_to_anchor=(1.02, 1.02), loc='upper left')
plt.tight_layout()
plt.show()
# # sns.kdeplot(np.array(array1), bw=0.1)
# # sns.kdeplot(np.array(array2), bw=0.1)
# # sns.kdeplot(np.array(array3), bw=0.1)
# # title = "Histogram of" 
# # plt.title(title)
# # plt.xlabel('Time')
# # plt.ylabel('IAT Distribution')
# # plt.show()