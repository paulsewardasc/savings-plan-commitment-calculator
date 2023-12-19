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

header.append("Compute Savings Plan Rate - NU ($)")
header.append("Compute Savings Plan Rate - PU ($)")
header.append("Compute Savings Plan Rate - AU ($)")
header.append("EC2 Instance Savings Plan Rate - NU ($)")
header.append("EC2 Instance Savings Plan Rate - PU ($)")
header.append("EC2 Instance Savings Plan Rate - AU ($)")
header.append("OnDemand Rate ($)")
header.append("% Saving CSP - NU")
header.append("% Saving CSP - PU")
header.append("% Saving CSP - AU")
header.append("% Saving EC2 ISP - NU")
header.append("% Saving EC2 ISP - PU")
header.append("% Saving EC2 ISP - AU")
header.append("CSP Break Even Months- NU")
header.append("CSP Break Even Months - PU")
header.append("CSP Break Even Months - AU")
header.append("EC2ISP Break Even Months - NU")
header.append("EC2ISP Break Even Months - PU")
header.append("EC2ISP Break Even Months - AU")
header.append("Total Upfront Cost CSP ($) - NU")
header.append("Total Upfront Cost CSP ($) - PU")
header.append("Total Upfront Cost CSP ($) - AU")
header.append("Total Monthly Cost CSP ($) - NU")
header.append("Total Monthly Cost CSP ($) - PU")
header.append("Total Monthly Cost CSP ($) - AU")
header.append("Total Upfront Cost EC2 ISP ($) - NU")
header.append("Total Upfront Cost EC2 ISP ($) - PU")
header.append("Total Upfront Cost EC2 ISP ($) - AU")
header.append("Total Monthly Cost EC2 ISP ($) - NU")
header.append("Total Monthly Cost EC2 ISP ($) - PU")
header.append("Total Monthly Cost EC2 ISP ($) - AU")
header.append("Total Monthly OnDemand Cost ($)")
header.append("Yearly CSP Saving - NU ($)")
header.append("Yearly CSP Saving - PU ($)")
header.append("Yearly CSP Saving - AU ($)")
header.append("Yearly EC2 ISP Saving - NU ($)")
header.append("Yearly EC2 ISP Saving - PU ($)")
header.append("Yearly EC2 ISP Saving - AU ($)")

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
    if term == '1yr':
      termno = 1
    else:
      termno = 3
    purchasing_option = csv_row[6]
    try:
      start_date = csv_row[7]
    except:
      start_date = datetime.date.today().strftime('%d/%m/%Y')
    instance_family = instance_type.split('.')[0]

    #check parameters
    core.check_input_parameters(usage_operation, tenancy, sp_type, term, purchasing_option)
    
    print('[INFO]',region_code, usage_operation, instance_family, instance_type, tenancy, term, start_date)

    # eu-west-2,Linux/UNIX,t4g.medium,Shared,1,ComputeSavingsPlans,1yr,No Upfront
    # eu-west-2,Linux/UNIX,t4g.medium,Shared,1,EC2InstanceSavingsPlans,1yr,No Upfront

    sp_rate_nu = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'ComputeSavingsPlans', term, purchasing_option)
    sp_rate_pu = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'ComputeSavingsPlans', term, 'Partial Upfront')
    sp_rate_au = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'ComputeSavingsPlans', term, 'All Upfront')
    sp_rate1_nu = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'EC2InstanceSavingsPlans', term, purchasing_option)
    sp_rate1_pu = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'EC2InstanceSavingsPlans', term, 'Partial Upfront')
    sp_rate1_au = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'EC2InstanceSavingsPlans', term, 'All Upfront')
    ondemand_rate = core.get_ondemand_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'OnDemand', term, purchasing_option)
    pcSavingCSP_nu = 100-(sp_rate_nu/ondemand_rate*100)
    pcSavingCSP_pu = 100-(sp_rate_pu/ondemand_rate*100)
    pcSavingCSP_au = 100-(sp_rate_au/ondemand_rate*100)
    pcSavingEC2ISP_nu = 100-(sp_rate1_nu/ondemand_rate*100)
    pcSavingEC2ISP_pu = 100-(sp_rate1_pu/ondemand_rate*100)
    pcSavingEC2ISP_au = 100-(sp_rate1_au/ondemand_rate*100)

    hours_in_the_commitment = 365*24*termno
    months_in_term = termno * 12
    total_commitment_nu = hours_in_the_commitment*sp_rate_nu
    total_commitment_pu = hours_in_the_commitment*sp_rate_pu
    total_commitment_au = hours_in_the_commitment*sp_rate_au
    total_commitment1_nu = hours_in_the_commitment*sp_rate1_nu
    total_commitment1_pu = hours_in_the_commitment*sp_rate1_pu
    total_commitment1_au = hours_in_the_commitment*sp_rate1_au
    upfront_nu = 0
    upfront_pu = total_commitment_pu * 0.5
    upfront_au = total_commitment_au
    upfront1_nu = 0
    upfront1_pu = total_commitment1_pu * 0.5
    upfront1_au = total_commitment1_au
    hourly_cost_nu = (total_commitment_nu - upfront_nu)/hours_in_the_commitment
    hourly_cost_pu = (total_commitment_pu - upfront_pu)/hours_in_the_commitment
    hourly_cost_au = (total_commitment_au - upfront_au)/hours_in_the_commitment
    hourly_cost1_nu = (total_commitment1_nu - upfront1_nu)/hours_in_the_commitment
    hourly_cost1_pu = (total_commitment1_pu - upfront1_pu)/hours_in_the_commitment
    hourly_cost1_au = (total_commitment1_au - upfront1_au)/hours_in_the_commitment
    norm_cost_nu = (upfront_nu / months_in_term) + (hourly_cost_nu * 730)
    norm_cost_pu = (upfront_pu / months_in_term) + (hourly_cost_pu * 730)
    norm_cost_au = (upfront_au / months_in_term) + (hourly_cost_au * 730)
    norm_cost1_nu = (upfront1_nu / months_in_term) + (hourly_cost1_nu * 730)
    norm_cost1_pu = (upfront1_pu / months_in_term) + (hourly_cost1_pu * 730)
    norm_cost1_au = (upfront1_au / months_in_term) + (hourly_cost1_au * 730)
    norm_ondemand_rate = ondemand_rate * 730
    bep_nu = norm_cost_nu / norm_ondemand_rate
    bep_pu = norm_cost_pu / norm_ondemand_rate
    bep_au = norm_cost_au / norm_ondemand_rate
    bep1_nu = norm_cost1_nu / norm_ondemand_rate
    bep1_pu = norm_cost1_pu / norm_ondemand_rate
    bep1_au = norm_cost1_au / norm_ondemand_rate
    bept_nu = bep_nu * 730
    bept_pu = bep_pu * 730
    bept_au = bep_au * 730
    bept1_nu = bep1_nu * 730
    bept1_pu = bep1_pu * 730
    bept1_au = bep1_au * 730
    t_ufc_nu = upfront_nu * n_instances
    t_ufc_pu = upfront_pu * n_instances
    t_ufc_au = upfront_au * n_instances
    t_ufc1_nu = upfront1_nu * n_instances
    t_ufc1_pu = upfront1_pu * n_instances
    t_ufc1_au = upfront1_au * n_instances
    t_mc_nu = hourly_cost_nu * 730 * n_instances
    t_mc_pu = hourly_cost_pu * 730 * n_instances
    t_mc_au = hourly_cost_au * 730 * n_instances
    t_mc1_nu = hourly_cost1_nu * 730 * n_instances
    t_mc1_pu = hourly_cost1_pu * 730 * n_instances
    t_mc1_au = hourly_cost1_au * 730 * n_instances
    t_yc_nu = (t_ufc_nu/termno)+(t_mc_nu*12)
    t_yc_pu = (t_ufc_pu/termno)+(t_mc_pu*12)
    t_yc_au = (t_ufc_au/termno)+(t_mc_au*12)
    t_yc1_nu = (t_ufc1_nu/termno)+(t_mc1_nu*12)
    t_yc1_pu = (t_ufc1_pu/termno)+(t_mc1_pu*12)
    t_yc1_au = (t_ufc1_au/termno)+(t_mc1_au*12)
    t_ycs_nu = (norm_ondemand_rate*12*n_instances) - t_yc_nu
    t_ycs_pu = (norm_ondemand_rate*12*n_instances) - t_yc_pu
    t_ycs_au = (norm_ondemand_rate*12*n_instances) - t_yc_au
    t_ycs1_nu = (norm_ondemand_rate*12*n_instances) - t_yc1_nu
    t_ycs1_pu = (norm_ondemand_rate*12*n_instances) - t_yc1_pu
    t_ycs1_au = (norm_ondemand_rate*12*n_instances) - t_yc1_au
    sd = datetime.datetime.strptime(start_date, "%d/%m/%Y")
    ed_nu = (sd + datetime.timedelta(days=bept_nu * 12 * termno / 24)).strftime('%d/%m/%Y')
    ed_pu = (sd + datetime.timedelta(days=bept_pu * 12 * termno / 24)).strftime('%d/%m/%Y')
    ed_au = (sd + datetime.timedelta(days=bept_au * 12 * termno / 24)).strftime('%d/%m/%Y')
    ed1_nu = (sd + datetime.timedelta(days=bept1_nu * 12 * termno / 24)).strftime('%d/%m/%Y')
    ed1_pu = (sd + datetime.timedelta(days=bept1_pu * 12 * termno / 24)).strftime('%d/%m/%Y')
    ed1_au = (sd + datetime.timedelta(days=bept1_au * 12 * termno / 24)).strftime('%d/%m/%Y')


    print(f'[INFO] CSP Rate NU: {sp_rate_nu}')
    print(f'[INFO] CSP Rate PU: {sp_rate_pu}')
    print(f'[INFO] CSP Rate AU: {sp_rate_au}')
    print(f'[INFO] EC2 ISP Rate NU: {sp_rate1_nu}')
    print(f'[INFO] EC2 ISP Rate PU: {sp_rate1_pu}')
    print(f'[INFO] EC2 ISP Rate AU: {sp_rate1_au}')
    print(f'[INFO] Hours in the commitment: {hours_in_the_commitment}')
    print(f'[INFO] Total commitment CSP NU: {hours_in_the_commitment}*{sp_rate_nu}={total_commitment_nu}')
    print(f'[INFO] Total commitment CSP PU: {hours_in_the_commitment}*{sp_rate_pu}={total_commitment_pu}')
    print(f'[INFO] Total commitment CSP AU: {hours_in_the_commitment}*{sp_rate_au}={total_commitment_au}')
    print(f'[INFO] Total commitment EC2 ISP NU: {hours_in_the_commitment}*{sp_rate1_nu}={total_commitment1_nu}')
    print(f'[INFO] Total commitment EC2 ISP PU: {hours_in_the_commitment}*{sp_rate1_pu}={total_commitment1_pu}')
    print(f'[INFO] Total commitment EC2 ISP AU: {hours_in_the_commitment}*{sp_rate1_au}={total_commitment1_au}')
    print(f'[INFO] Upfront CSP NU: {upfront_nu}')
    print(f'[INFO] Upfront CSP PU: {upfront_pu}')
    print(f'[INFO] Upfront CSP AU: {upfront_au}')
    print(f'[INFO] Upfront EC2 ISP NU: {upfront1_nu}')
    print(f'[INFO] Upfront EC2 ISP PU: {upfront1_pu}')
    print(f'[INFO] Upfront EC2 ISP AU: {upfront1_au}')
    print(f'[INFO] Hourly Cost CSP NU: ({total_commitment_nu}-{upfront_nu})/{hours_in_the_commitment}={hourly_cost_nu}')
    print(f'[INFO] Hourly Cost CSP PU: ({total_commitment_pu}-{upfront_pu})/{hours_in_the_commitment}={hourly_cost_pu}')
    print(f'[INFO] Hourly Cost CSP AU: ({total_commitment_au}-{upfront_au})/{hours_in_the_commitment}={hourly_cost_au}')
    print(f'[INFO] Hourly Cost EC2 ISP NU: ({total_commitment1_nu}-{upfront1_nu})/{hours_in_the_commitment}={hourly_cost1_nu}')
    print(f'[INFO] Hourly Cost EC2 ISP PU: ({total_commitment1_pu}-{upfront1_pu})/{hours_in_the_commitment}={hourly_cost1_pu}')
    print(f'[INFO] Hourly Cost EC2 ISP AU: ({total_commitment1_au}-{upfront1_au})/{hours_in_the_commitment}={hourly_cost1_au}')
    print(f'[INFO] Normalized monthly price CSP NU: ({upfront_nu} / {months_in_term}) + ({hourly_cost_nu} * 730)={norm_cost_nu}')
    print(f'[INFO] Normalized monthly price CSP PU: ({upfront_pu} / {months_in_term}) + ({hourly_cost_pu} * 730)={norm_cost_pu}')
    print(f'[INFO] Normalized monthly price CSP AU: ({upfront_au} / {months_in_term}) + ({hourly_cost_au} * 730)={norm_cost_au}')
    print(f'[INFO] Normalized monthly price EC2 ISP NU: ({upfront1_nu} / {months_in_term}) + ({hourly_cost1_nu} * 730)={norm_cost1_nu}')
    print(f'[INFO] Normalized monthly price EC2 ISP PU: ({upfront1_pu} / {months_in_term}) + ({hourly_cost1_pu} * 730)={norm_cost1_pu}')
    print(f'[INFO] Normalized monthly price EC2 ISP AU: ({upfront1_au} / {months_in_term}) + ({hourly_cost1_au} * 730)={norm_cost1_au}')
    print(f'[INFO] On-Demand hourly price: {ondemand_rate}')
    print(f'[INFO] Normalized On-Demand hourly price: {ondemand_rate}*730={norm_ondemand_rate}')
    print(f'[INFO] Breakeven percentage CSP NU: {norm_cost_nu} / {norm_ondemand_rate}={bep_nu}')
    print(f'[INFO] Breakeven percentage CSP PU: {norm_cost_pu} / {norm_ondemand_rate}={bep_pu}')
    print(f'[INFO] Breakeven percentage CSP AU: {norm_cost_au} / {norm_ondemand_rate}={bep_au}')
    print(f'[INFO] Breakeven percentage EC2 ISP NU: {norm_cost1_nu} / {norm_ondemand_rate}={bep1_nu}')
    print(f'[INFO] Breakeven percentage EC2 ISP PU: {norm_cost1_pu} / {norm_ondemand_rate}={bep1_pu}')
    print(f'[INFO] Breakeven percentage EC2 ISP AU: {norm_cost1_au} / {norm_ondemand_rate}={bep1_au}')
    print(f'[INFO] Breakeven point: {bep_nu} * 730={bept_nu}')
    print(f'[INFO] Breakeven point: {bep_pu} * 730={bept_pu}')
    print(f'[INFO] Breakeven point: {bep_au} * 730={bept_au}')
    print(f'[INFO] Breakeven point: {bep1_nu} * 730={bept1_nu}')
    print(f'[INFO] Breakeven point: {bep1_pu} * 730={bept1_pu}')
    print(f'[INFO] Breakeven point: {bep1_au} * 730={bept1_au}')
    print(f'[INFO] Total Upfront Cost CSP NU: {t_ufc_nu}')
    print(f'[INFO] Total Upfront Cost CSP PU: {t_ufc_pu}')
    print(f'[INFO] Total Upfront Cost CSP AU: {t_ufc_au}')
    print(f'[INFO] Total Upfront Cost EC2 ISP NU: {t_ufc1_nu}')
    print(f'[INFO] Total Upfront Cost EC2 ISP PU: {t_ufc1_pu}')
    print(f'[INFO] Total Upfront Cost EC2 ISP AU: {t_ufc1_au}')
    print(f'[INFO] Total Monthly Cost CSP NU: {t_mc_nu}')
    print(f'[INFO] Total Monthly Cost CSP PU: {t_mc_pu}')
    print(f'[INFO] Total Monthly Cost CSP AU: {t_mc_au}')
    print(f'[INFO] Total Monthly Cost EC2 ISP NU: {t_mc1_nu}')
    print(f'[INFO] Total Monthly Cost EC2 ISP PU: {t_mc1_pu}')
    print(f'[INFO] Total Monthly Cost EC2 ISP AU: {t_mc1_au}')
    print(f'[INFO] Total Yearly Cost CSP NU: {t_yc_nu}')
    print(f'[INFO] Total Yearly Cost CSP PU: {t_yc_pu}')
    print(f'[INFO] Total Yearly Cost CSP AU: {t_yc_au}')
    print(f'[INFO] Total Yearly Cost EC2 ISP NU: {t_yc1_nu}')
    print(f'[INFO] Total Yearly Cost EC2 ISP PU: {t_yc1_pu}')
    print(f'[INFO] Total Yearly Cost EC2 ISP AU: {t_yc1_au}')
    print(f'[INFO] Total Yearly Cost Saving CSP NU: {t_ycs_nu}')
    print(f'[INFO] Total Yearly Cost Saving CSP PU: {t_ycs_pu}')
    print(f'[INFO] Total Yearly Cost Saving CSP AU: {t_ycs_au}')
    print(f'[INFO] Total Yearly Cost Saving EC2 ISP NU: {t_ycs1_nu}')
    print(f'[INFO] Total Yearly Cost Saving EC2 ISP PU: {t_ycs1_pu}')
    print(f'[INFO] Total Yearly Cost Saving EC2 ISP AU: {t_ycs1_au}')
    print(f'[INFO] Start Date: {start_date}')
    print(f'[INFO] End Date CSP NU: {ed_nu}')
    print(f'[INFO] End Date CSP PU: {ed_pu}')
    print(f'[INFO] End Date CSP AU: {ed_au}')
    print(f'[INFO] End Date EC2 ISP NU: {ed1_nu}')
    print(f'[INFO] End Date EC2 ISP PU: {ed1_pu}')
    print(f'[INFO] End Date EC2 ISP AU: {ed1_au}')
   
    csv_row.append(f'{sp_rate_nu}')
    csv_row.append(f'{sp_rate_pu}')
    csv_row.append(f'{sp_rate_au}')
    csv_row.append(f'{sp_rate1_nu}')
    csv_row.append(f'{sp_rate1_pu}')
    csv_row.append(f'{sp_rate1_au}')
    csv_row.append(f'{ondemand_rate}')
    csv_row.append(f'{(1-bep_nu)*100:0.2f}')
    csv_row.append(f'{(1-bep_pu)*100:0.2f}')
    csv_row.append(f'{(1-bep_au)*100:0.2f}')
    csv_row.append(f'{(1-bep1_nu)*100:0.2f}')
    csv_row.append(f'{(1-bep1_pu)*100:0.2f}')
    csv_row.append(f'{(1-bep1_au)*100:0.2f}')
    csv_row.append(f'{bept_nu/730*12*termno:0.0f}')
    csv_row.append(f'{bept_pu/730*12*termno:0.0f}')
    csv_row.append(f'{bept_au/730*12*termno:0.0f}')
    csv_row.append(f'{bept1_nu/730*12*termno:0.0f}')
    csv_row.append(f'{bept1_pu/730*12*termno:0.0f}')
    csv_row.append(f'{bept1_au/730*12*termno:0.0f}')
    csv_row.append(f'{t_ufc_nu:0.2f}')
    csv_row.append(f'{t_ufc_pu:0.2f}')
    csv_row.append(f'{t_ufc_au:0.2f}')
    csv_row.append(f'{t_mc_nu:0.2f}')
    csv_row.append(f'{t_mc_pu:0.2f}')
    csv_row.append(f'{t_mc_au:0.2f}')
    csv_row.append(f'{t_ufc1_nu:0.2f}')
    csv_row.append(f'{t_ufc1_pu:0.2f}')
    csv_row.append(f'{t_ufc1_au:0.2f}')
    csv_row.append(f'{t_mc1_nu:0.2f}')
    csv_row.append(f'{t_mc1_pu:0.2f}')
    csv_row.append(f'{t_mc1_au:0.2f}')
    csv_row.append(f'{norm_ondemand_rate*n_instances:0.2f}')
    csv_row.append(f'{t_ycs_nu:0.2f}')
    csv_row.append(f'{t_ycs_pu:0.2f}')
    csv_row.append(f'{t_ycs_au:0.2f}')
    csv_row.append(f'{t_ycs1_nu:0.2f}')
    csv_row.append(f'{t_ycs1_pu:0.2f}')
    csv_row.append(f'{t_ycs1_au:0.2f}')
    




    writer.writerow(csv_row)


def write_summary():
    writer.writerow([]) #empty row as separator
    writer.writerow(["Information:"])
    writer.writerow(["NU:", "No Upfront"])
    writer.writerow(["PU:", "Partial Upfront"])
    writer.writerow(["AU:", "All Upfront"])

main_handler()

print("COMPLETED SUCCESSFULLY")

file_input.close()
file_output.close()
