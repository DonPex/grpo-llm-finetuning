
CREATE TABLE rawdata.alarm (
    id bigint,
    ack_user_id character varying(250),
    additional_text character varying(250),
    alarm_primary_key character varying(250),
    area character varying(250),
    base_alarm_ack_state character varying(250),
    base_probable_alarm_cause character varying(250),
    comments text,
    detail text,
    device_name character varying(250),
    device_type character varying(250),
    district character varying(250),
    ems_name character varying(250),
    eqp_name character varying(250),
    from_site character varying(250),
    keyword character varying(250),
    notification_id character varying(250),
    origin character varying(250),
    outcome character varying(250),
    proposed_repair_actions text,
    raw_probable_alarm_cause integer,
    remote_eqp_name character varying(250),
    repeated_count integer,
    severity character varying(250),
    specific_problem character varying(250),
    status character varying(250),
    time_ack timestamp without time zone,
    time_cleared timestamp without time zone,
    time_down timestamp without time zone,
    time_raised timestamp without time zone,
    time_up timestamp without time zone,
    time_update timestamp without time zone,
    type character varying(250),
    vendor character varying(250),
    parent_alarm_primary_key character varying(250),
    tt_id character varying(250),
    module_name character varying(250),
    inhibit boolean,
    comment_user_id character varying(250),
    raw_alarm_type character varying(250),
    time_comment timestamp without time zone,
    tt_status character varying(250),
    time_tt_last_update timestamp without time zone,
    planned_work character varying(250),
    access_id character varying(250),
    access_type character varying(250),
    action_code character varying(10),
    element_status integer,
    eqp_name2 character varying(250),
    eqp_type character varying(250),
    topology character varying(250),
    tt_association_type character varying(250)
);

CREATE TABLE rawdata.alarm_label (
    id bigint,
    domain_id character varying(250),
    slogan character varying(250),
    alarmtrigger character varying(250)
);

CREATE TABLE rawdata.cable_system (
    index bigint,
    "CABLE_SYSTEM_ID" text,
    "CABLE_SYSTEM_NAME" text,
    "CABLE_TYPE" text,
    "SITE_A_ID" text,
    "SITE_B_ID" text
);

CREATE TABLE rawdata.cablesegment (
    index bigint,
    "CABLE_SEGMENT_ID" text,
    "CABLE_SEGMENT_NAME" text,
    "CABLE_TYPE" text,
    "STATUS" double precision,
    "SITE_CABINET_A_ID" text,
    "SITE_CABINET_B_ID" text,
    "SYNTHETIC_NAME" text
);

CREATE TABLE rawdata.cl_clsegm_rel (
    index bigint,
    "CABLE_SYSTEM_ID" text,
    "CABLE_SEGMENT_ID" text
);

CREATE TABLE rawdata.equipment_details (
    index bigint,
    "SHORT_NAME" text,
    "LOCATION" text,
    "TRAIL_NAME" text,
    "NUMERO_TD" text,
    "CODE" text,
    "DESCRIPTION" text
);

CREATE TABLE rawdata.equipment_ip_address (
    index bigint,
    "NODE_NAME" text,
    "MODEL_CODE" text,
    "NETWORK_ELEMENT_ID" bigint,
    "CODE" text,
    "IP_ADDRESS" text
);

CREATE TABLE rawdata.incident (
    incident_number character varying(50),
    affected_service character varying(100),
    assignment_group character varying(100),
    assigned_to character varying(100),
    assignment_count integer,
    business_service character varying(100),
    caller character varying(100),
    category character varying(100),
    closed timestamp without time zone,
    configuration_item character varying(100),
    contact_type character varying(100),
    correlation_id character varying(100),
    created_date timestamp without time zone,
    customer_type character varying(100),
    description text,
    domain character varying(100),
    end_fault timestamp without time zone,
    end_inefficiency timestamp without time zone,
    expected_resolution_date timestamp without time zone,
    first_configuration_item character varying(100),
    impact integer,
    in_validation boolean,
    incident_alert boolean,
    incident_parent character varying(100),
    inefficiency boolean,
    inefficiency_type character varying(100),
    level1 character varying(100),
    level2 character varying(100),
    level3 character varying(100),
    level4 character varying(100),
    msisdn character varying(100),
    network_element_type character varying(100),
    opened_by character varying(100),
    originating_system character varying(100),
    owner_group character varying(100),
    process_cause character varying(100),
    product_type character varying(100),
    reopen_count integer,
    resolution_code character varying(100),
    resolution_entity character varying(100),
    resolved timestamp without time zone,
    root_cause character varying(100),
    sequence_id integer,
    short_description text,
    source character varying(100),
    start_fault timestamp without time zone,
    start_inefficiency timestamp without time zone,
    status integer,
    updated timestamp without time zone,
    updated_by character varying(100),
    urgency integer,
    vendor character varying(100),
    wfm_id character varying(100)
);

CREATE TABLE rawdata.leased_lines (
    index bigint,
    "SHORT_NAME" text,
    "LOCATION" text,
    "TRAIL_NAME" text,
    "NUMERO_TD" text,
    "CODE" text,
    "DESCRIPTION" text
);

CREATE TABLE rawdata.mobile_pe (
    index bigint,
    "VLAN_ID" double precision,
    "LOGICAL_LINK_ID" double precision,
    "PE_ID" bigint,
    "PE_NAME" text,
    "PE_STATUS" text,
    "ENTITY_TYPE" text,
    "POSITION" bigint
);

CREATE TABLE rawdata.mobile_peip (
    index bigint,
    "VLAN_ID" double precision,
    "PEIP_ID" bigint,
    "SUBNET" double precision,
    "TXP" text,
    "ENTITY_TYPE" text,
    "VPNL3_ID" double precision,
    "PEIP_MODEL" text,
    "POSITION" bigint,
    "STATUS" text
);

CREATE TABLE rawdata.network_elements (
    index bigint,
    "LOCATION" text,
    "NODE_NAME" text,
    "NETWORK_ELEMENT_ID" bigint,
    "NETWORK_ELEMENT_TYPE_CODE" text,
    "SERIAL_NUMBER" bigint,
    "ACTIVITY_STATUS_CODE" text,
    "MODEL_CODE" text,
    "VENDOR_NAME" text,
    "ELEMENT_CLASS_CODE" text,
    "ELEMENT_CLASS_DESC" text,
    "CARD_TYPE_ID" double precision,
    "SYSTEM_NAME" text,
    "LOCATION_SHORT_NAME" text
);

CREATE TABLE rawdata.outage (
    outage_id integer,
    site_id character varying(50),
    ts_start_disruption timestamp without time zone,
    equipment_list character varying(100),
    status character varying(50),
    username character varying(100),
    latitude numeric(9,6),
    longitude numeric(9,6)
);

CREATE TABLE rawdata.path_ethernet (
    index bigint,
    "VLAN_ID" bigint,
    "VPLS_ID" double precision,
    "PATH_ETHERNET_ID" bigint,
    "PATH_ETHERNET_STATUS" text,
    "NAME" text
);

CREATE TABLE rawdata.path_ethernet_serv (
    index bigint,
    "PATH_ETHERNET_ID" bigint,
    "PATH_ETHERNET_SECTION_ID" bigint,
    "POSITION_IN_PATH" bigint,
    "VLAN_IN_ID" bigint,
    "VPLS_ID" double precision,
    "VLAN_OUT_ID" bigint
);

CREATE TABLE rawdata.ports (
    index bigint,
    "NODE_NAME" text,
    "MODEL_CODE" text,
    "NETWORK_ELEMENT_ID" bigint,
    "CODE" text,
    "IP_ADDRESS" text
);

CREATE TABLE rawdata.raw_alarms (
    "ID" bigint,
    "ACK_USER_ID" text,
    "ADDITIONAL_TEXT" text,
    "ALARM_PRIMARY_KEY" text,
    "AREA" text,
    "BASE_ALARM_ACK_STATE" text,
    "BASE_PROBABLE_ALARM_CAUSE" text,
    "COMMENTS" text,
    "DETAIL" double precision,
    "DEVICE_NAME" text,
    "DEVICE_TYPE" text,
    "DISTRICT" text,
    "EMS_NAME" text,
    "EQP_NAME" text,
    "FROM_SITE" text,
    "KEYWORD" text,
    "NOTIFICATION_ID" text,
    "ORIGIN" text,
    "PROPOSED_REPAIR_ACTIONS" text,
    "RAW_PROBABLE_ALARM_CAUSE" bigint,
    "REMOTE_EQP_NAME" text,
    "REPEATED_COUNT" bigint,
    "SEVERITY" text,
    "SPECIFIC_PROBLEM" text,
    "STATUS" text,
    "TIME_ACK" text,
    "TIME_CLEARED" text,
    "TIME_DOWN" text,
    "TIME_RAISED" text,
    "TIME_UP" double precision,
    "TIME_UPDATE" text,
    "TYPE" text,
    "VENDOR" text,
    "PARENT_ALARM_PRIMARY_KEY" text,
    "TT_ID" text,
    "MODULE_NAME" text,
    "INHIBIT" text,
    "COMMENT_USER_ID" text,
    "RAW_ALARM_TYPE" text,
    "TIME_COMMENT" text,
    "TT_STATUS" text,
    "TIME_TT_LAST_UPDATE" text,
    "PLANNED_WORK" text,
    "ACCESS_ID" text,
    "ACCESS_TYPE" text,
    "ACTION_CODE" text,
    "ELEMENT_STATUS" double precision,
    "EQP_NAME2" text,
    "EQP_TYPE" double precision,
    "TOPOLOGY" text,
    "TT_ASSOCIATION_TYPE" text
);

CREATE TABLE rawdata.rmm_equipment_details (
    "NETWORK_ELEMENT_NAME" text,
    "NETWORK_ELEMENT_MODEL" text,
    "NODE_NAME" text,
    "SLOT_NAME" text,
    "SLOT_NUMBER" double precision,
    "SHELF_NAME" text,
    "SHELF_DESCRIPTION" text,
    "CARD_TYPE" text,
    "CARD_NAME" text,
    "VENDOR_CARD_CODE" text,
    "CARD_STATUS_CODE" text,
    "CARD_VENDOR_NAME" text
);

CREATE TABLE rawdata.routing (
    index bigint,
    "PARENT_LL_ID" text,
    "ROUTE_ORDER" bigint,
    "CHILD_LL_ID" text,
    "ROUTE_TYPE" text,
    "CHANNEL_IDENTIFIER" bigint,
    "VCI" double precision
);

CREATE TABLE rawdata.service (
    "SERVICE_ID" text,
    "HIERARCHY_ID" double precision,
    "SERVICE_NAME" text,
    "STATUS" text,
    "A_NETWORK_ADDRESS" text,
    "B_NETWORK_ADDRESS" text,
    "V52_NUMBER" double precision,
    "LINK_ID" double precision,
    "NA_IMA_GROUP" text,
    "CIRCUIT_COUNT" bigint,
    "CHANNEL_COUNT" double precision,
    "MARKET_DESTINATION" text,
    "ACCESS_TYPE" text,
    "ASSOCIATED_SERVICE" text,
    "PROVISIONING_STATUS" text,
    "CLI" text,
    "DOMAIN" bigint
);

CREATE TABLE rawdata.sites (
    "SITE_ID" text,
    "SITE_NAME" text,
    "LONGITUDE" text,
    "LATITUDE" text,
    "DISTRICT" text,
    "ADDRESS" text,
    "CIVICO" text,
    "CITY_NAME" text,
    "SITE_TYPE" text,
    "CUSTOMER" text,
    "SHORT_NAME" text,
    "ALTERNATIVE_NAME" text,
    "PROVINCE" text,
    "BUILDING_UNIQUE_ID" text,
    "CODICE_ISTAT" double precision,
    "REGIONE" text,
    "PROVINCIA" text
);

CREATE TABLE rawdata.synthetic_name_trail (
    "TRANSMEDIA_NAME" text,
    "TRATTA" text,
    "TRAIL_NAME" text,
    "ACTIVITY_STATUS_TRAIL" text,
    "TRAIL_DESCRIPTION" text,
    "FUNCTION_CODE" text
);

CREATE TABLE rawdata.topology_mbh_ip (
    "VPNL3_ID" double precision,
    "LOGICAL_LINK_ID" double precision,
    "MBH_IP_TOPOLOGY_ID" bigint,
    "NAME" text,
    "ALTERNATIVE_NAME" text,
    "SERIAL_NUMBER" bigint,
    "ID_PROCESSO" double precision,
    "DISTRICT" text,
    "TOPOLOGY_TYPE" text,
    "AREA_OSPF_BLK1" double precision,
    "AREA_OSPF_BLK2" double precision,
    "AREA_OSPF_BLK3" double precision,
    "AREA_OSPF_BLK4" double precision
);

CREATE TABLE rawdata.topology_wdm (
    "TOPOLOGYID" bigint,
    "TOPOLOGY_TYPE" text,
    "STATUS" double precision,
    "ALTERNATIVE_NAME" text,
    "CODE" text,
    "SERIAL_NUMBER" bigint,
    "DESCRIPTION" text,
    "LOGICAL_LINK_ID" bigint
);

CREATE VIEW rawdata.v_alarms AS
 SELECT a.id AS alarm_id,
    a.severity,
    a.eqp_name,
    a.from_site,
    a.remote_eqp_name,
    a.time_up,
    a.time_down,
    l.slogan AS description,
    a.additional_text,
    a.vendor,
    a.raw_alarm_type AS alarm_type,
    a.device_name,
    a.device_type,
    l.domain_id AS domain,
    a.tt_id,
    a.ems_name,
    a.time_cleared AS ts_cleared
   FROM (rawdata.alarm a
     JOIN rawdata.alarm_label l ON ((a.id = l.id)));

COMMENT ON VIEW rawdata.v_alarms IS 'vista contenente i dati di input per i modelli ML di MITO.AI';