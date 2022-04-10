import csv, os

device_1_path = "/Users/marynavek/Projects/LoRa_fingerprinting/csv_files/uplinks_260C96BF.csv"
device_2_path = "/Users/marynavek/Projects/LoRa_fingerprinting/csv_files/uplinks_260CC1A1.csv"

mean_interarrival_time_d1 = 0
mean_interarrival_time_d2 = 0

mean_channel_rsi_d1 = 0
mean_channel_rsi_d2 = 0

mean_rssi_d1 = 0
mean_rssi_d2 = 0

mean_snr_d1 = 0
mean_snr_d2 = 0

total_interarrival_time = 0
total_channel_rsi = 0
total_rssi = 0
total_snr = 0
total_items = 0
with open(device_1_path) as device1_csv:
    reader_d1 = csv.DictReader(device1_csv)
    for row in reader_d1:
        total_interarrival_time = total_interarrival_time + float(row["inter_arrival_time_ms"])
        total_channel_rsi = total_channel_rsi + float(row["channel_rssi"])
        total_rssi = total_rssi + float(row["rssi"])
        total_snr = total_snr + float(row["snr"])
        total_items += 1

    mean_interarrival_time_d1 = total_interarrival_time/total_items
    mean_channel_rsi_d1 = total_channel_rsi/total_items
    mean_rssi_d1 = total_rssi/total_items
    mean_snr_d1 = total_snr/total_items

    print(f"For device one, total # of uplinks {total_items}")
    print(f"Mean interarrival_time {mean_interarrival_time_d1}")
    print(f"Mean channel rssi {mean_channel_rsi_d1}")
    print(f"Mean rssi {mean_rssi_d1}")
    print(f"Mean snr {mean_snr_d1}")
    

total_interarrival_time = 0
total_channel_rsi = 0
total_rssi = 0
total_snr = 0
total_items = 0
with open(device_2_path) as device2_csv:
    reader_d1 = csv.DictReader(device2_csv)
    for row in reader_d1:
        total_interarrival_time = total_interarrival_time + float(row["inter_arrival_time_ms"])
        total_channel_rsi = total_channel_rsi + float(row["channel_rssi"])
        total_rssi = total_rssi + float(row["rssi"])
        total_snr = total_snr + float(row["snr"])
        total_items += 1

    mean_interarrival_time_d2 = total_interarrival_time/total_items
    mean_channel_rsi_d2 = total_channel_rsi/total_items
    mean_rssi_d2 = total_rssi/total_items
    mean_snr_d2 = total_snr/total_items

    print(f"For device one, total # of uplinks {total_items}")
    print(f"Mean interarrival_time {mean_interarrival_time_d2}")
    print(f"Mean channel rssi {mean_channel_rsi_d2}")
    print(f"Mean rssi {mean_rssi_d2}")
    print(f"Mean snr {mean_snr_d2}")
    

    
    
