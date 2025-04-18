import json
import re
import os

# --- INSERT Statements (without 'rawdata.' prefix) ---
# Dictionary mapping table names to their INSERT statements
inserts_dict = {
    "sites": [
        'INSERT INTO sites ("SITE_ID", "SITE_NAME", "LONGITUDE", "LATITUDE", "DISTRICT", "ADDRESS", "CIVICO", "CITY_NAME", "SITE_TYPE", "CUSTOMER", "SHORT_NAME", "ALTERNATIVE_NAME", "PROVINCE", "BUILDING_UNIQUE_ID", "CODICE_ISTAT", "REGIONE", "PROVINCIA") VALUES (\'Site_Milan_001\', \'Central Office Milan\', \'9.1900\', \'45.4642\', \'Milan\', \'Via Roma\', \'10\', \'Milan\', \'POP\', \'Telecom Italia\', \'MIL_01\', \'Milano Centrale\', \'MI\', \'BLD_MI_001\', 20154.0, \'Lombardy\', \'MI\');',
        'INSERT INTO sites ("SITE_ID", "SITE_NAME", "LONGITUDE", "LATITUDE", "DISTRICT", "ADDRESS", "CIVICO", "CITY_NAME", "SITE_TYPE", "CUSTOMER", "SHORT_NAME", "ALTERNATIVE_NAME", "PROVINCE", "BUILDING_UNIQUE_ID", "CODICE_ISTAT", "REGIONE", "PROVINCIA") VALUES (\'Site_Lazio_001\', \'Regional Hub Lazio\', \'12.4964\', \'41.9028\', \'Rome\', \'Piazza Venezia\', \'1\', \'Rome\', \'Hub\', \'Customer B\', \'ROM_01\', \'Roma Hub\', \'RM\', \'BLD_RM_001\', 58091.0, \'Lazio\', \'RM\');'
    ],
    "network_elements": [
        'INSERT INTO network_elements (index, "LOCATION", "NODE_NAME", "NETWORK_ELEMENT_ID", "NETWORK_ELEMENT_TYPE_CODE", "SERIAL_NUMBER", "ACTIVITY_STATUS_CODE", "MODEL_CODE", "VENDOR_NAME", "ELEMENT_CLASS_CODE", "ELEMENT_CLASS_DESC", "CARD_TYPE_ID", "SYSTEM_NAME", "LOCATION_SHORT_NAME") VALUES (1, \'Milan Datacenter\', \'ROUTER_MILAN_CORE_1\', 1001, \'Router\', 987654321, \'active\', \'CISCO_ASR9K\', \'Cisco\', \'Core Router\', \'Core Network Router\', 101.0, \'Core Network\', \'MIL_01\');',
        'INSERT INTO network_elements (index, "LOCATION", "NODE_NAME", "NETWORK_ELEMENT_ID", "NETWORK_ELEMENT_TYPE_CODE", "SERIAL_NUMBER", "ACTIVITY_STATUS_CODE", "MODEL_CODE", "VENDOR_NAME", "ELEMENT_CLASS_CODE", "ELEMENT_CLASS_DESC", "CARD_TYPE_ID", "SYSTEM_NAME", "LOCATION_SHORT_NAME") VALUES (2, \'Rome POP\', \'SWITCH_ROME_EDGE_1\', 1002, \'Switch\', 123456789, \'inactive\', \'JUNOS_MX240\', \'Juniper\', \'Edge Router\', \'Edge Network Router\', 102.0, \'Edge Network\', \'ROM_01\');'
    ],
    "incident": [
        'INSERT INTO incident (incident_number, affected_service, assignment_group, assigned_to, assignment_count, business_service, caller, category, closed, configuration_item, contact_type, correlation_id, created_date, customer_type, description, domain, end_fault, end_inefficiency, expected_resolution_date, first_configuration_item, impact, in_validation, incident_alert, incident_parent, inefficiency, inefficiency_type, level1, level2, level3, level4, msisdn, network_element_type, opened_by, originating_system, owner_group, process_cause, product_type, reopen_count, resolution_code, resolution_entity, resolved, root_cause, sequence_id, short_description, source, start_fault, start_inefficiency, status, updated, updated_by, urgency, vendor, wfm_id) VALUES (\'INC0012345\', \'Mobile Data\', \'Network Operations\', \'john.doe\', 1, \'Mobile Services\', \'Customer Support\', \'Fiber Cut\', NULL, \'ROUTER_MILAN_CORE_1\', \'Phone\', \'ALM_556677\', \'2025-04-17 10:00:00\', \'Business\', \'Fiber cut reported in Milan area\', \'Network\', NULL, NULL, \'2025-04-19 10:00:00\', \'ROUTER_MILAN_CORE_1\', 3, false, true, NULL, false, NULL, \'Network\', \'Transmission\', \'Fiber\', NULL, \'3331234567\', \'Router\', \'system_monitor\', \'Monitoring Tool X\', \'NOC Level 2\', \'External Damage\', \'Connectivity\', 0, NULL, NULL, NULL, \'Fiber Damage\', 101, \'Mobile Data Outage Milan\', \'Monitoring\', \'2025-04-17 09:55:00\', NULL, 2, \'2025-04-17 11:30:00\', \'analyst1\', 3, \'Cisco\', \'WFM_9876\');',
        'INSERT INTO incident (incident_number, affected_service, assignment_group, assigned_to, assignment_count, business_service, caller, category, closed, configuration_item, contact_type, correlation_id, created_date, customer_type, description, domain, end_fault, end_inefficiency, expected_resolution_date, first_configuration_item, impact, in_validation, incident_alert, incident_parent, inefficiency, inefficiency_type, level1, level2, level3, level4, msisdn, network_element_type, opened_by, originating_system, owner_group, process_cause, product_type, reopen_count, resolution_code, resolution_entity, resolved, root_cause, sequence_id, short_description, source, start_fault, start_inefficiency, status, updated, updated_by, urgency, vendor, wfm_id) VALUES (\'INC0012346\', \'VOIP Service\', \'Service Desk\', \'jane.smith\', 2, \'Voice Services\', \'Internal User\', \'Service Degradation\', \'2025-04-18 09:00:00\', \'SWITCH_ROME_EDGE_1\', \'Email\', \'ALM_556678\', \'2025-04-17 14:00:00\', \'Residential\', \'Poor voice quality reported\', \'Voice\', \'2025-04-18 08:55:00\', NULL, \'2025-04-17 18:00:00\', \'SWITCH_ROME_EDGE_1\', 4, true, false, \'INC0012300\', true, \'Configuration Error\', \'Voice\', \'Platform\', \'Core\', NULL, \'N/A\', \'Switch\', \'user_report\', \'Ticketing System\', \'Voice Operations\', \'Software Bug\', \'VOIP\', 1, \'No Fault Found\', \'Vendor Support\', \'2025-04-18 08:55:00\', \'Configuration Mismatch\', 102, \'VOIP Quality Issues Rome\', \'User\', \'2025-04-17 13:50:00\', NULL, 1, \'2025-04-18 09:05:00\', \'jane.smith\', 2, \'Juniper\', \'WFM_9877\');'
    ],
    "cable_system": [
        'INSERT INTO cable_system (index, "CABLE_SYSTEM_ID", "CABLE_SYSTEM_NAME", "CABLE_TYPE", "SITE_A_ID", "SITE_B_ID") VALUES (1, \'CS_WEST_001\', \'CS_WEST\', \'Submarine\', \'SITE_A_NAPLES\', \'SITE_B_PALERMO\');',
        'INSERT INTO cable_system (index, "CABLE_SYSTEM_ID", "CABLE_SYSTEM_NAME", "CABLE_TYPE", "SITE_A_ID", "SITE_B_ID") VALUES (2, \'CS_NORTH_001\', \'Undersea Cable 1\', \'Terrestrial\', \'SITE_A_MILAN\', \'SITE_B_TURIN\');'
    ],
    "alarm": [
        'INSERT INTO alarm (id, ack_user_id, additional_text, alarm_primary_key, area, base_alarm_ack_state, base_probable_alarm_cause, comments, detail, device_name, device_type, district, ems_name, eqp_name, from_site, keyword, notification_id, origin, outcome, proposed_repair_actions, raw_probable_alarm_cause, remote_eqp_name, repeated_count, severity, specific_problem, status, time_ack, time_cleared, time_down, time_raised, time_up, time_update, type, vendor, parent_alarm_primary_key, tt_id, module_name, inhibit, comment_user_id, raw_alarm_type, time_comment, tt_status, time_tt_last_update, planned_work, access_id, access_type, action_code, element_status, eqp_name2, eqp_type, topology, tt_association_type) VALUES (12345, \'john.doe\', \'PSU 1 Failure\', \'ALM_CRITICAL_001\', \'North Area\', \'acknowledged\', \'Equipment Failure\', \'Power supply unit 1 failed. PSU 2 is active.\', \'Device reported PSU failure alarm.\', \'ROUTER_MILAN_CORE_1\', \'Router\', \'Milan\', \'EMS_Alpha\', \'ROUTER_MILAN_01\', \'MIL_01\', \'Power,Failure,Critical\', \'NOTIF_555\', \'Device Poll\', \'Service Impacted\', \'Replace PSU 1\', 5001, NULL, 3, \'critical\', \'Power Supply Failure\', \'Active\', \'2025-04-18 08:15:00\', NULL, \'2025-04-18 08:00:00\', \'2025-04-18 08:00:00\', NULL, \'2025-04-18 08:15:00\', \'EquipmentAlarm\', \'Cisco\', NULL, \'TT_123456\', \'Power Module 1\', false, \'system\', \'PowerFailure\', NULL, \'Open\', \'2025-04-18 09:00:00\', \'No\', \'ACC_001\', \'Physical\', \'REP\', 1, \'PSU_1\', \'Power Supply\', \'Core Network\', \'Direct\');',
        'INSERT INTO alarm (id, ack_user_id, additional_text, alarm_primary_key, area, base_alarm_ack_state, base_probable_alarm_cause, comments, detail, device_name, device_type, district, ems_name, eqp_name, from_site, keyword, notification_id, origin, outcome, proposed_repair_actions, raw_probable_alarm_cause, remote_eqp_name, repeated_count, severity, specific_problem, status, time_ack, time_cleared, time_down, time_raised, time_up, time_update, type, vendor, parent_alarm_primary_key, tt_id, module_name, inhibit, comment_user_id, raw_alarm_type, time_comment, tt_status, time_tt_last_update, planned_work, access_id, access_type, action_code, element_status, eqp_name2, eqp_type, topology, tt_association_type) VALUES (12346, NULL, \'High Temperature Threshold\', \'ALM_MAJOR_002\', \'South Area\', \'unacknowledged\', \'Environmental Alarm\', NULL, \'Temperature sensor reading 55C.\', \'SWITCH_ROME_EDGE_1\', \'Switch\', \'Rome\', \'EMS_Beta\', \'SWITCH_ROME_EDGE_1\', \'ROM_01\', \'Temperature,High,Major\', \'NOTIF_556\', \'Sensor Reading\', \'Potential Overheating\', \'Check HVAC system\', 6002, NULL, 1, \'major\', \'High Temperature\', \'Active\', NULL, NULL, \'2025-04-18 10:05:00\', \'2025-04-18 10:05:00\', NULL, \'2025-04-18 10:05:00\', \'EnvironmentalAlarm\', \'Juniper\', NULL, NULL, \'Temp Sensor 1\', false, NULL, \'TempHigh\', NULL, NULL, NULL, \'No\', \'ACC_002\', \'Remote\', \'CHK\', 1, \'Sensor_1\', \'Sensor\', \'Edge Network\', NULL);'
    ],
    "service": [
        'INSERT INTO service ("SERVICE_ID", "HIERARCHY_ID", "SERVICE_NAME", "STATUS", "A_NETWORK_ADDRESS", "B_NETWORK_ADDRESS", "V52_NUMBER", "LINK_ID", "NA_IMA_GROUP", "CIRCUIT_COUNT", "CHANNEL_COUNT", "MARKET_DESTINATION", "ACCESS_TYPE", "ASSOCIATED_SERVICE", "PROVISIONING_STATUS", "CLI", "DOMAIN") VALUES (\'SVC_MPLS_001\', 10.0, \'MPLS VPN Milan\', \'Active\', \'10.0.0.1\', \'10.0.0.2\', NULL, 5001.0, NULL, 1, 1.0, \'Enterprise\', \'Fiber\', NULL, \'Provisioned\', \'N/A\', 1);',
        'INSERT INTO service ("SERVICE_ID", "HIERARCHY_ID", "SERVICE_NAME", "STATUS", "A_NETWORK_ADDRESS", "B_NETWORK_ADDRESS", "V52_NUMBER", "LINK_ID", "NA_IMA_GROUP", "CIRCUIT_COUNT", "CHANNEL_COUNT", "MARKET_DESTINATION", "ACCESS_TYPE", "ASSOCIATED_SERVICE", "PROVISIONING_STATUS", "CLI", "DOMAIN") VALUES (\'SVC_VOIP_002\', 20.0, \'Business VOIP Rome\', \'Inactive\', \'192.168.1.1\', \'192.168.1.2\', 12345.0, 5002.0, \'IMA_Group_1\', 10, 10.0, \'Business\', \'Copper\', \'SVC_MPLS_002\', \'Decommissioned\', \'061234567\', 2);'
    ],
    "outage": [
        'INSERT INTO outage (outage_id, site_id, ts_start_disruption, equipment_list, status, username, latitude, longitude) VALUES (1, \'SITE_123\', \'2025-04-18 05:00:00\', \'Router R1, Switch S1\', \'active\', \'system\', 42.123456, 12.123456);',
        'INSERT INTO outage (outage_id, site_id, ts_start_disruption, equipment_list, status, username, latitude, longitude) VALUES (2, \'SITE_456\', \'2025-04-17 23:30:00\', \'Firewall F1\', \'resolved\', \'tech1\', 45.654321, 9.654321);'
    ],
    "rmm_equipment_details": [
        'INSERT INTO rmm_equipment_details ("NETWORK_ELEMENT_NAME", "NETWORK_ELEMENT_MODEL", "NODE_NAME", "SLOT_NAME", "SLOT_NUMBER", "SHELF_NAME", "SHELF_DESCRIPTION", "CARD_TYPE", "CARD_NAME", "VENDOR_CARD_CODE", "CARD_STATUS_CODE", "CARD_VENDOR_NAME") VALUES (\'RouterMilan1\', \'ASR9K\', \'ROUTER_MILAN_CORE_1\', \'Slot 3\', 3.0, \'Shelf 1\', \'Main Shelf\', \'Line Card 100G\', \'LC100G-1\', \'PID-LC100G\', \'Active\', \'Cisco\');',
        'INSERT INTO rmm_equipment_details ("NETWORK_ELEMENT_NAME", "NETWORK_ELEMENT_MODEL", "NODE_NAME", "SLOT_NAME", "SLOT_NUMBER", "SHELF_NAME", "SHELF_DESCRIPTION", "CARD_TYPE", "CARD_NAME", "VENDOR_CARD_CODE", "CARD_STATUS_CODE", "CARD_VENDOR_NAME") VALUES (\'SwitchRome1\', \'MX240\', \'SWITCH_ROME_EDGE_1\', \'Slot 1\', 1.0, \'Shelf 0\', \'Control Shelf\', \'Routing Engine\', \'RE-S-1800X4\', \'PID-RES1800\', \'Standby\', \'Juniper\');'
    ],
    "equipment_ip_address": [
        'INSERT INTO equipment_ip_address (index, "NODE_NAME", "MODEL_CODE", "NETWORK_ELEMENT_ID", "CODE", "IP_ADDRESS") VALUES (1, \'ROUTER_MILAN_CORE_1\', \'CISCO_ASR9K\', 1001, \'Management\', \'192.168.10.1\');',
        'INSERT INTO equipment_ip_address (index, "NODE_NAME", "MODEL_CODE", "NETWORK_ELEMENT_ID", "CODE", "IP_ADDRESS") VALUES (2, \'SWITCH_ROME_EDGE_1\', \'MODEL_XYZ\', 1002, \'Loopback\', \'10.10.10.1\');'
    ],
    "alarm_label": [
        'INSERT INTO alarm_label (id, domain_id, slogan, alarmtrigger) VALUES (12345, \'Power\', \'Critical Power Failure\', \'PSU Down\');',
        'INSERT INTO alarm_label (id, domain_id, slogan, alarmtrigger) VALUES (12346, \'Environment\', \'High Temperature Warning\', \'Temp > 50C\');'
    ],
    "path_ethernet": [
        'INSERT INTO path_ethernet (index, "VLAN_ID", "VPLS_ID", "PATH_ETHERNET_ID", "PATH_ETHERNET_STATUS", "NAME") VALUES (1, 100, 500.0, 9001, \'Up\', \'Path_CustomerA_VLAN100\');',
        'INSERT INTO path_ethernet (index, "VLAN_ID", "VPLS_ID", "PATH_ETHERNET_ID", "PATH_ETHERNET_STATUS", "NAME") VALUES (2, 200, 501.0, 9002, \'Down\', \'Path_CustomerB_VLAN200\');'
    ],
    "cl_clsegm_rel": [
        'INSERT INTO cl_clsegm_rel (index, "CABLE_SYSTEM_ID", "CABLE_SEGMENT_ID") VALUES (1, \'CS_WEST_001\', \'SEG_W_001\');',
        'INSERT INTO cl_clsegm_rel (index, "CABLE_SYSTEM_ID", "CABLE_SEGMENT_ID") VALUES (2, \'CS_NORTH_001\', \'SEG_N_001\');'
    ],
    "cablesegment": [
        'INSERT INTO cablesegment (index, "CABLE_SEGMENT_ID", "CABLE_SEGMENT_NAME", "CABLE_TYPE", "STATUS", "SITE_CABINET_A_ID", "SITE_CABINET_B_ID", "SYNTHETIC_NAME") VALUES (1, \'SEG_W_001\', \'West Segment 1\', \'Submarine\', 1.0, \'CAB_NAPLES_01\', \'CAB_PALERMO_01\', \'Naples-Palermo-Seg1\');',
        'INSERT INTO cablesegment (index, "CABLE_SEGMENT_ID", "CABLE_SEGMENT_NAME", "CABLE_TYPE", "STATUS", "SITE_CABINET_A_ID", "SITE_CABINET_B_ID", "SYNTHETIC_NAME") VALUES (2, \'SEG_N_001\', \'North Segment 1 (Undersea Cable 1)\', \'Terrestrial\', 1.0, \'CAB_MILAN_02\', \'CAB_TURIN_02\', \'Milan-Turin-Seg1\');'
    ]
}

# Input and Output file names
input_filename = 'data/generated-sql.jsonl'
output_filename = 'data/generated-sql-with-inserts.jsonl'

# Check if input file exists
if not os.path.exists(input_filename):
    print(f"Error: Input file '{input_filename}' not found.")
else:
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile, \
             open(output_filename, 'w', encoding='utf-8') as outfile:

            for line in infile:
                try:
                    # Load the JSON object from the line
                    data = json.loads(line.strip())
                    sql_context = data.get('sql_context', '')

                    # Find all table names mentioned in CREATE TABLE statements
                    # Regex looks for 'CREATE TABLE rawdata.' followed by the table name (alphanumeric + _)
                    table_names = re.findall(r'CREATE TABLE rawdata\.(\w+)', sql_context)

                    inserts_to_append = ""
                    appended_tables_for_line = set() # Track tables appended for this line

                    # Append INSERT statements for each unique table found
                    for table_name in table_names:
                        if table_name in inserts_dict and table_name not in appended_tables_for_line:
                            inserts_to_append += "\n".join(inserts_dict[table_name])
                            appended_tables_for_line.add(table_name) # Mark as appended for this line

                    # Append the collected INSERT statements to the original sql_context
                    data['sql_context'] = sql_context + inserts_to_append

                    # Write the modified JSON object back to the output file
                    outfile.write(json.dumps(data) + '\n')

                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line.strip()}")
                except Exception as e:
                    print(f"An error occurred processing line: {line.strip()} - Error: {e}")

        print(f"Processing complete. Output written to '{output_filename}'")

    except IOError as e:
        print(f"Error opening or writing to files: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")