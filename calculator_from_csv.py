# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import csv
import core
import datetime
import sys

def get_costs(a,b,c,d,e,f,g):
  #print(f'[+] {a},{b},{c},{d},{e},{f},{g}')
  row = []
  row.extend(a)
  row.append(g)
  t1 = row[4]
  t2 = row[3]
  row[3] = t1
  row[4] = t2
  colf = b
  colg = colf * c
  colh = d * 730
  coli = colh * 12
  colj = (b / e) + (d * 730 * 12)
  colk = d * 730 * c
  coll = ((colf / e) + (colh * 12)) * c
  colm = coll * e
  coln = f
  row.append(f'{colf:0.3f}')
  row.append(f'{colg:0.3f}')
  row.append(f'{colh:0.3f}')
  row.append(f'{coli:0.3f}')
  row.append(f'{colj:0.3f}')
  row.append(f'{colk:0.3f}')
  row.append(f'{coll:0.3f}')
  row.append(f'{colm:0.3f}')
  row.append(coln)
  return row

# csv input and output files
file_input = open('input.csv')
file_output = open('output.csv', 'w', newline='')

if len(sys.argv) == 1:
  savingsPlanType = 1
  savingsPlanTypeStr = "Reserved Instances" 
else:
  argument = sys.argv[1]
  if argument == "1":
    savingsPlanType = 1
    savingsPlanTypeStr = "Reserved Instances"
  if argument == "2":
    savingsPlanType = 2
    savingsPlanTypeStr = "Compute Savings Plan"
  if argument == "3":
    savingsPlanType = 3
    savingsPlanTypeStr = "EC2 Savings Plan"

#input reader
csvreader = csv.reader(file_input)
header = next(csvreader)
# Delete Type from Columns
del header[5]
# Change the order of the header
newheader = header.copy()
newheader[0] = header[2]
newheader[1] = header[1]
newheader[2] = header[0]
newheader[3] = header[6]
newheader[4] = header[4]
newheader[5] = "fred"

del newheader[7]
del newheader[6]
del newheader[5]
header = newheader

csv_row1 = []
csv_row2 = []
csv_row3 = []
csv_row4 = []
csv_1 = {}
csv_2 = {}
csv_3 = {}
csv_4 = {}
row_count = 1

#output writer
writer = csv.writer(file_output)

topheader = [savingsPlanTypeStr]
writer.writerow(topheader)

header.append("Upfront / Instance")
header.append("Total Upfront")
header.append("Monthly / Instance")
header.append("Yearly / Instance")
header.append("Yearly / Instance + Upfront")
header.append("Monthly Total (All Instances)")
header.append("Yearly Total (All Instances + Upfront)")
header.append("Total")
header.append("Term")

writer.writerow(header)

#summary savings plan to purchase
summary_sp = {}
summary_sp1 = {}

def main_handler():
    for csv_row in csvreader:
      elaborate_item(csv_row)

    csv_total_1_u = 0
    csv_total_2_u = 0
    csv_total_3_u = 0
    csv_total_4_u = 0
    csv_total_5_u = 0
    csv_total_6_u = 0
    csv_total_7_u = 0
    csv_total_8_u = 0
    csv_total_9_u = 0
    for i,j in csv_1.items():
      csv = ",".join(j)
      print(f'{csv}')
      writer.writerow(j)
      csv_total_1_u += float(j[4])
      csv_total_2_u += float(j[5])
      csv_total_3_u += float(j[6])
      csv_total_4_u += float(j[7])
      csv_total_5_u += float(j[8])
      csv_total_6_u += float(j[9])
      csv_total_7_u += float(j[10])
      csv_total_8_u += float(j[11])
      csv_total_9_u += float(j[12])
    row=f'Total,,,,{csv_total_1_u},{csv_total_2_u},{csv_total_3_u},{csv_total_4_u},{csv_total_5_u},{csv_total_6_u},{csv_total_7_u},{csv_total_8_u},{csv_total_9_u}'
    print(row)
    writer.writerow(row.split(","))
    

    csv_total_1 = 0
    csv_total_2 = 0
    csv_total_3 = 0
    csv_total_4 = 0
    csv_total_5 = 0
    csv_total_6 = 0
    csv_total_7 = 0
    csv_total_8 = 0
    csv_total_9 = 0
    for i,j in csv_2.items():
      csv = ",".join(j)
      print(f'{csv}')
      writer.writerow(j)
      csv_total_1 += float(j[4])
      csv_total_2 += float(j[5])
      csv_total_3 += float(j[6])
      csv_total_4 += float(j[7])
      csv_total_5 += float(j[8])
      csv_total_6 += float(j[9])
      csv_total_7 += float(j[10])
      csv_total_8 += float(j[11])
      csv_total_9 += float(j[12])
    row=f'Total,,,,{csv_total_1},{csv_total_2},{csv_total_3},{csv_total_4},{csv_total_5},{csv_total_6},{csv_total_7},{csv_total_8},{csv_total_9}'
    print(row)
    writer.writerow(row.split(","))
    row=f',,,Total vs On Demand,,,,{csv_total_4_u-csv_total_4:0.2f},{csv_total_5_u-csv_total_5:0.2f},{csv_total_6_u-csv_total_6:0.2f},{csv_total_7_u-csv_total_7:0.2f},{csv_total_8_u-csv_total_8:0.2f},{csv_total_9_u-csv_total_9:0.2f}'
    print(row)
    writer.writerow(row.split(","))

    csv_total_1 = 0
    csv_total_2 = 0
    csv_total_3 = 0
    csv_total_4 = 0
    csv_total_5 = 0
    csv_total_6 = 0
    csv_total_7 = 0
    csv_total_8 = 0
    csv_total_9 = 0
    for i,j in csv_3.items():
      csv = ",".join(j)
      print(f'{csv}')
      writer.writerow(j)
      csv_total_1 += float(j[4])
      csv_total_2 += float(j[5])
      csv_total_3 += float(j[6])
      csv_total_4 += float(j[7])
      csv_total_5 += float(j[8])
      csv_total_6 += float(j[9])
      csv_total_7 += float(j[10])
      csv_total_8 += float(j[11])
      csv_total_9 += float(j[12])
    row=f'Total,,,,{csv_total_1},{csv_total_2},{csv_total_3},{csv_total_4},{csv_total_5},{csv_total_6},{csv_total_7},{csv_total_8},{csv_total_9}'
    print(row)
    writer.writerow(row.split(","))
    row=f',,,Total vs On Demand,,,,{csv_total_4_u-csv_total_4:0.2f},{csv_total_5_u-csv_total_5:0.2f},{csv_total_6_u-csv_total_6:0.2f},{csv_total_7_u-csv_total_7:0.2f},{csv_total_8_u-csv_total_8:0.2f},{csv_total_9_u-csv_total_9:0.2f}'
    print(row)
    writer.writerow(row.split(","))

    csv_total_1 = 0
    csv_total_2 = 0
    csv_total_3 = 0
    csv_total_4 = 0
    csv_total_5 = 0
    csv_total_6 = 0
    csv_total_7 = 0
    csv_total_8 = 0
    csv_total_9 = 0
    for i,j in csv_4.items():
      csv = ",".join(j)
      print(f'{csv}')
      writer.writerow(j)
      csv_total_1 += float(j[4])
      csv_total_2 += float(j[5])
      csv_total_3 += float(j[6])
      csv_total_4 += float(j[7])
      csv_total_5 += float(j[8])
      csv_total_6 += float(j[9])
      csv_total_7 += float(j[10])
      csv_total_8 += float(j[11])
      csv_total_9 += float(j[12])
    row=f'Total,,,,{csv_total_1},{csv_total_2},{csv_total_3},{csv_total_4},{csv_total_5},{csv_total_6},{csv_total_7},{csv_total_8},{csv_total_9}'
    print(row)
    writer.writerow(row.split(","))
    row=f',,,Total vs On Demand,,,,{csv_total_4_u-csv_total_4:0.2f},{csv_total_5_u-csv_total_5:0.2f},{csv_total_6_u-csv_total_6:0.2f},{csv_total_7_u-csv_total_7:0.2f},{csv_total_8_u-csv_total_8:0.2f},{csv_total_9_u-csv_total_9:0.2f}'
    print(row)
    writer.writerow(row.split(","))

    #write summary savings plan to purchase
    write_summary()

def elaborate_item(csv_row):
    global row_count
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
    del csv_row[6]
    try:
      start_date = csv_row[6]
      del csv_row[6]
    except:
      start_date = datetime.date.today().strftime('%d/%m/%Y')
    instance_family = instance_type.split('.')[0]

    #check parameters
    core.check_input_parameters(usage_operation, tenancy, sp_type, term, purchasing_option)
   
    #print('') 
    #print('[INFO] ------------------------------------------------------------------------------------------')
    #print('[INFO]',region_code, usage_operation, instance_family, instance_type, tenancy, term, start_date)

    # eu-west-2,Linux/UNIX,t4g.medium,Shared,1,ComputeSavingsPlans,1yr,No Upfront
    # eu-west-2,Linux/UNIX,t4g.medium,Shared,1,EC2InstanceSavingsPlans,1yr,No Upfront

    sp_rate_nu = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'ComputeSavingsPlans', term, purchasing_option)
    sp_rate_pu = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'ComputeSavingsPlans', term, 'Partial Upfront')
    sp_rate_au = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'ComputeSavingsPlans', term, 'All Upfront')
    sp_rate1_nu = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'EC2InstanceSavingsPlans', term, purchasing_option)
    sp_rate1_pu = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'EC2InstanceSavingsPlans', term, 'Partial Upfront')
    sp_rate1_au = core.get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'EC2InstanceSavingsPlans', term, 'All Upfront')
    #print(region_code, usage_operation, instance_family, instance_type, tenancy, 'OnDemand', term, purchasing_option)
    ondemand_rate = core.get_ondemand_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'OnDemand', term, purchasing_option)
    reserved_rate_nu,reserved_upfront_nu = core.get_reserved_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'OnDemand', term, 'No Upfront')
    reserved_rate_pu,reserved_upfront_pu = core.get_reserved_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'OnDemand', term, 'Partial Upfront')
    reserved_rate_au,reserved_upfront_au = core.get_reserved_rate(region_code, usage_operation, instance_family, instance_type, tenancy, 'OnDemand', term, 'All Upfront')

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

    t1 = csv_row[2]
    t2 = csv_row[0]
    csv_row[0] = t1
    csv_row[2] = t2
    # Delete Shared
    del csv_row[3]
    # Delete Term as we only use 1 year
    termtime = csv_row[4]
    del csv_row[4]

    # Reserved Instance
    if savingsPlanType == 1:
      # On Demand
      csv_row1 = get_costs(csv_row, 0, n_instances, ondemand_rate, termno, termtime,'On Demand')
      csv_1[row_count] = csv_row1
      
      # No Upfront
      csv_row2 = get_costs(csv_row, reserved_upfront_nu, n_instances, reserved_rate_nu,termno, termtime,'No Upfront')
      csv_2[row_count] = csv_row2
  
      # Partial Upfront
      csv_row3 = get_costs(csv_row, reserved_upfront_pu, n_instances, reserved_rate_pu, termno, termtime,'Partial Upfront')
      csv_3[row_count] = csv_row3
  
      # All Upfront
      csv_row4 = get_costs(csv_row, reserved_upfront_au, n_instances, reserved_rate_au, termno, termtime,'All Upfront')
      csv_4[row_count] = csv_row4
      row_count += 1

    if savingsPlanType == 2:
      # On Demand
      csv_row1 = get_costs(csv_row, 0, n_instances, ondemand_rate, termno, termtime,'On Demand')
      csv_1[row_count] = csv_row1
      
      # No Upfront
      csv_row2 = get_costs(csv_row, upfront_nu, n_instances, hourly_cost_nu,termno, termtime,'No Upfront')
      csv_2[row_count] = csv_row2
  
      # Partial Upfront
      csv_row3 = get_costs(csv_row, upfront_pu, n_instances, hourly_cost_pu, termno, termtime,'Partial Upfront')
      csv_3[row_count] = csv_row3
  
      # All Upfront
      csv_row4 = get_costs(csv_row, upfront_au, n_instances, hourly_cost_au, termno, termtime,'All Upfront')
      csv_4[row_count] = csv_row4
      row_count += 1
 
    if savingsPlanType == 3:
      # On Demand
      csv_row1 = get_costs(csv_row, 0, n_instances, ondemand_rate, termno, termtime,'On Demand')
      csv_1[row_count] = csv_row1
      
      # No Upfront
      csv_row2 = get_costs(csv_row, upfront1_nu, n_instances, hourly_cost1_nu,termno, termtime,'No Upfront')
      csv_2[row_count] = csv_row2
  
      # Partial Upfront
      csv_row3 = get_costs(csv_row, upfront1_pu, n_instances, hourly_cost1_pu, termno, termtime,'Partial Upfront')
      csv_3[row_count] = csv_row3
  
      # All Upfront
      csv_row4 = get_costs(csv_row, upfront1_au, n_instances, hourly_cost1_au, termno, termtime,'All Upfront')
      csv_4[row_count] = csv_row4
      row_count += 1
 
def write_summary():
    writer.writerow([]) #empty row as separator


main_handler()

file_input.close()
file_output.close()

print("COMPLETED SUCCESSFULLY")

