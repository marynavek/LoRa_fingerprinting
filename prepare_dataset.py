import numpy as np

import json, os, csv

file_names = ["ArduinoMega.json", "ArduinoPro.json", "expLoRaBLE.json", "device_dataset_1.json", "device_dataset_2.json", "device_dataset_3.json", "device_dataset_4.json"]
path = "/Users/marynavek/Projects/LoRa_fingerprinting"
final_dataset = []
# For now only devices with the following addresses are being analyzed.
dev_addresses = ['260CC099', '260C96BF', '260C60B0']
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
        if dev_addr in dev_addresses:
            uplinks_ds_device_1.append(addObject)

    print(list_of_devAddresses)
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

file_name = 'uplinks_ds.csv'
csv_path = os.path.join("/Users/marynavek/Projects/LoRa_fingerprinting/", file_name)
with open(csv_path, 'w') as csvfile:
    fieldnames=["dev_addr", "time", "m_hdr_type", "f_cnt", "f_port", "bandwidth", "sf", "coding_rate",
                "frequency", "rssi", "channel_rssi", "snr", "inter_arrival_time_ms"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in final_dataset:
        writer.writerow(data)

