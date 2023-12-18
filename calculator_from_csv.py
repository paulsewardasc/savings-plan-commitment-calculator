# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import csv
import core
import datetime

# csv input and output files
file_input = open('input.csv')
file_output = open('output.csv', 'w', newline='')

#input reader
csvreader = csv.reader(file_input)
header = next(csvreader)
# Delete Type from Columns
del header[5]

#output writer
writer = csv.writer(file_output)
header.append("Compute Savings Plan Rate ($)")
header.append("EC2 Instance Savings Plan Rate ($)")
header.append("OnDemand Rate ($)")
header.append("% Saving CSP")
header.append("% Saving EC2 ISP")
header.append("CSP Break Even Date")
header.append("EC2ISP Break Even Date")
header.append("Total Hourly Compute Savings Plan Cost ($)")
header.append("Total Hourly EC2 Instance Savings Plan Cost ($)")
header.append("Total Hourly OnDemand Cost ($)")
header.append("Monthly Compute Savings Plan Cost ($)")
header.append("Monthly EC2 Instance Savings Plan Cost ($)")
header.append("Monthly OnDemand Cost ($)")

writer.writerow(header)

#summary savings plan to purchase
summary_sp = {}
summary_sp1 = {}

def main_handler():
    #elaborate csv input rows
    for csv_row in csvreader:
        elaborate_item(csv_row)

    #write summary savings plan to purchase
    write_summary()

def elaborate_item(csv_row):
    region_code = csv_row[0]
    usage_operation = core.operation_by_platform_dict[csv_row[1]]
    instance_type = csv_row[2]
    tenancy = csv_row[3]
    n_instances = int(csv_row[4])
    # Ignoring this column as we do both
    sp_type = csv_row[5]
    del csv_row[5]
    term = csv_row[5]
    purchasing_option = csv_row[6]
    try:
      start_date = csv_row[7]
    except:
      start_date = datetime.date.today().strftime('%d/%m/%Y')
    instance_family = instance_type.split('.')[0]

    #check parameters
    core.check_input_parameters(usage_operation, tenancy, sp_type, term, purchasing_option)
    
    print(region_code, usage_operation, instance_family, instance_type, tenancy, sp_type, term, purchasing_option, start_date)

    # eu-west-2,Linux/UNIX,t4g.medium,Shared,1,ComputeSavingsPlans,1yr,No Upfront
    # eu-west-2,Linux/UNIX,t4g.medium,Shared,1,EC2InstanceSavingsPlans,1yr,No Upfront

    sp_rate = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'ComputeSavingsPlans', term, purchasing_option)
    sp_rate1 = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'EC2InstanceSavingsPlans', term, purchasing_option)
    ondemand_rate = core.get_ondemand_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'OnDemand', term, purchasing_option)
    pcSavingCSP = 100-(sp_rate/ondemand_rate*100)
    pcSavingEC2ISP = 100-(sp_rate1/ondemand_rate*100)
    csv_row.append(f'{sp_rate}')
    csv_row.append(f'{sp_rate1}')
    csv_row.append(f'{ondemand_rate}')

    total_hourly_rate = sp_rate * n_instances
    total_hourly_rate1 = sp_rate1 * n_instances
    total_hourly_rate_ondemand = ondemand_rate * n_instances
    breakeven_csp = (100-pcSavingCSP)
    breakeven_csp = breakeven_csp*730/100*12/24
    date_1 = datetime.datetime.strptime(start_date, "%d/%m/%Y")
    end_date = date_1 + datetime.timedelta(days=breakeven_csp)
    end_date_csp = end_date.strftime('%d/%m/%Y')
    breakeven_ec2isp = (100-pcSavingEC2ISP)
    breakeven_ec2isp = breakeven_ec2isp*730/100*12/24
    date_1 = datetime.datetime.strptime(start_date, "%d/%m/%Y")
    end_date = date_1 + datetime.timedelta(days=breakeven_ec2isp)
    end_date_ec2isp = end_date.strftime('%d/%m/%Y')

    csv_row.append(f'{pcSavingCSP:0.2f}')
    csv_row.append(f'{pcSavingEC2ISP:0.2f}')
    csv_row.append(f'{end_date_csp}')
    csv_row.append(f'{end_date_ec2isp}')
    csv_row.append(f'{total_hourly_rate:0.2f}')
    csv_row.append(f'{total_hourly_rate1:0.2f}')
    csv_row.append(f'{total_hourly_rate_ondemand:0.2f}')
    csv_row.append(f'{total_hourly_rate*730:0.2f}')
    csv_row.append(f'{total_hourly_rate1*730:0.2f}')
    csv_row.append(f'{total_hourly_rate_ondemand*730:0.2f}')
    csv_row.append(f'{end_date}')

    writer.writerow(csv_row)

    # savings plan description for summary
    sp_description = "ComputeSavingsPlans (" + term + " - " + purchasing_option + ")"
    sp_description1 =  "EC2InstanceSavingsPlans (" + term + " - " + purchasing_option + "); family: " + instance_family + "; region: " + region_code

    # register commitment for the summary
    if (sp_description not in summary_sp):
        summary_sp[sp_description] = total_hourly_rate
    else:
        summary_sp[sp_description] += total_hourly_rate
    if (sp_description1 not in summary_sp1):
        summary_sp1[sp_description1] = total_hourly_rate1
    else:
        summary_sp1[sp_description1] += total_hourly_rate1

def write_summary():
    writer.writerow([]) #empty row as separator
    writer.writerow(["Summary Savings Plans to purchase:", "Hourly Commitment ($)"])
    for sp_description in summary_sp:
        writer.writerow([sp_description, summary_sp[sp_description]])
    for sp_description1 in summary_sp1:
        writer.writerow([sp_description1, summary_sp1[sp_description1]])

main_handler()

print("COMPLETED SUCCESSFULLY")

file_input.close()
file_output.close()
