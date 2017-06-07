# coding: utf-8
from sqlalchemy import BigInteger, Column, Float, Index, Integer, Numeric, SmallInteger, String, Table, Text, text
from sqlalchemy.dialects.mysql.types import BIT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class BgpLinkInfo(Base):
    __tablename__ = 'bgp_link_info'

    id = Column(Integer, primary_key=True)
    as_num = Column(SmallInteger, nullable=False)
    router_id = Column(String(15), nullable=False)
    interface_ip = Column(String(15), nullable=False)
    n_as_num = Column(SmallInteger, nullable=False)
    n_router_id = Column(String(15), nullable=False)
    n_interface_ip = Column(String(15), nullable=False)
    mask = Column(String(15), nullable=False)
    metric = Column(Integer, nullable=False)


class BgpPathInfo(Base):
    __tablename__ = 'bgp_path_info'

    id = Column(BigInteger, primary_key=True)
    n_routerID = Column(String(15))
    n_asNum = Column(Integer)
    n_peerIP = Column(String(15))
    prefixLen = Column(Integer)
    networkNum = Column(String(15))
    asPath = Column(String(30))
    nextHop = Column(String(15))
    origin = Column(Integer)
    weight = Column(Integer)
    med = Column(Integer)
    local_pref = Column(Integer)
    create_time = Column(Numeric(13, 0), nullable=False)
    end_time = Column(Numeric(13, 0), nullable=False)


class Department(Base):
    __tablename__ = 'department'

    dptid = Column(Integer, primary_key=True)
    dptname = Column(String(30), nullable=False)
    description = Column(String(127), server_default=text("''"))


class HzBgpPathInfo(Base):
    __tablename__ = 'hz_bgp_path_info'

    id = Column(BigInteger, primary_key=True, nullable=False)
    as_num = Column(SmallInteger, primary_key=True, nullable=False)
    n_routerID = Column(String(15))
    n_asNum = Column(Integer)
    n_peerIP = Column(String(15))
    prefixLen = Column(Integer)
    networkNum = Column(String(15))
    asPath = Column(String(30))
    nextHop = Column(String(15))
    origin = Column(Integer)
    weight = Column(Integer)
    med = Column(Integer)
    local_pref = Column(Integer)
    create_time = Column(Numeric(13, 0), nullable=False)
    end_time = Column(Numeric(13, 0), nullable=False)


class HzOspfAsexternallsa(Base):
    __tablename__ = 'hz_ospf_asexternallsa'

    id = Column(BigInteger, primary_key=True, nullable=False)
    as_num = Column(SmallInteger, primary_key=True, nullable=False, server_default=text("'0'"))
    routerID = Column(String(15))
    areaID = Column(String(15))
    timeStamp = Column(Numeric(13, 0))
    lsAge = Column(SmallInteger)
    lsaType = Column(Integer)
    linkStateID = Column(String(15))
    adRouter = Column(String(15))
    networkMask = Column(String(15))
    externalType = Column(Integer)
    metric = Column(Integer)
    forwardAddress = Column(String(15))
    eRouterTag = Column(Integer)
    isUseful = Column(BIT(1))


class HzOspfLinkAttr(Base):
    __tablename__ = 'hz_ospf_link_attr'

    id = Column(Integer, primary_key=True)
    as_num = Column(SmallInteger, nullable=False)
    router_id = Column(String(15), nullable=False)
    interface_ip = Column(String(15), server_default=text("''"))
    n_as_num = Column(SmallInteger)
    n_router_id = Column(String(15))
    bandwidth = Column(Integer, server_default=text("'0'"))
    description = Column(String(127), server_default=text("''"))
    timestamp = Column(Numeric(10, 0), nullable=False)


class HzOspfLinkInfo(Base):
    __tablename__ = 'hz_ospf_link_info'

    id = Column(BigInteger, primary_key=True, nullable=False)
    as_num = Column(SmallInteger, primary_key=True, nullable=False)
    router_id = Column(String(15), nullable=False)
    interface_ip = Column(String(15), server_default=text("''"))
    mask = Column(String(15), server_default=text("''"))
    n_as_num = Column(SmallInteger)
    n_router_id = Column(String(15))
    area_id = Column(String(15), server_default=text("''"))
    link_type = Column(Integer, server_default=text("'0'"))
    is_static = Column(Integer, server_default=text("'0'"))
    metric = Column(Integer, server_default=text("'0'"))
    create_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False, server_default=text("'9999999999'"))

    def __repr__(self):
        return "<OspfLinkInfo(id='%s', area_id='%s')>"%(self.id, self.area_id)


class HzOspfRouterAttr(Base):
    __tablename__ = 'hz_ospf_router_attr'
    __table_args__ = (
        Index('as_router', 'as_num', 'router_id'),
    )

    id = Column(Integer, primary_key=True)
    as_num = Column(SmallInteger, nullable=False)
    router_id = Column(String(15), nullable=False)
    alias = Column(String(30), server_default=text("''"))
    description = Column(String(127), server_default=text("''"))
    dptid = Column(Integer, server_default=text("'0'"))
    x = Column(Numeric(16, 12), server_default=text("'0.000000000000'"))
    y = Column(Numeric(16, 12), server_default=text("'0.000000000000'"))
    timestamp = Column(Numeric(10, 0), nullable=False)


class HzOspfRouterInfo(Base):
    __tablename__ = 'hz_ospf_router_info'
    __table_args__ = (
        Index('time', 'create_time', 'end_time'),
        Index('as_router', 'as_num', 'router_id')
    )

    id = Column(BigInteger, primary_key=True, nullable=False)
    as_num = Column(SmallInteger, primary_key=True, nullable=False)
    router_id = Column(String(15), nullable=False)
    router_type = Column(Integer, nullable=False)
    create_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False, server_default=text("'9999999999'"))


class HzOspfTrafficTopo(Base):
    __tablename__ = 'hz_ospf_traffic_topo'

    id = Column(BigInteger, primary_key=True)
    pid = Column(BigInteger, nullable=False, index=True)
    link_id = Column(BigInteger, nullable=False)
    as_num = Column(SmallInteger, nullable=False)
    period_interval = Column(Integer)
    bytes = Column(BigInteger, server_default=text("'0'"))
    protocol_bytes = Column(Text)


class HzWarning(Base):
    __tablename__ = 'hz_warning'

    id = Column(BigInteger, primary_key=True, nullable=False)
    as_num = Column(SmallInteger, primary_key=True, nullable=False)
    code = Column(SmallInteger, nullable=False, index=True)
    parse_time = Column(Integer)
    snmp_time = Column(Integer)
    text_params = Column(String(127), server_default=text("''"))
    relate_id = Column(BigInteger)
    solved = Column(Integer, nullable=False, server_default=text("'0'"))
    timestamp = Column(BigInteger, nullable=False)


class IpFlowIn(Base):
    __tablename__ = 'ip_flow_in'

    ip = Column(BigInteger, primary_key=True, nullable=False)
    pid = Column(BigInteger, primary_key=True, nullable=False)
    hour_0 = Column(BigInteger)
    hour_1 = Column(BigInteger)
    hour_2 = Column(BigInteger)
    hour_3 = Column(BigInteger)
    hour_4 = Column(BigInteger)
    hour_5 = Column(BigInteger)
    hour_6 = Column(BigInteger)
    hour_7 = Column(BigInteger)
    hour_8 = Column(BigInteger)
    hour_9 = Column(BigInteger)
    hour_10 = Column(BigInteger)
    hour_11 = Column(BigInteger)
    hour_12 = Column(BigInteger)
    hour_13 = Column(BigInteger)
    hour_14 = Column(BigInteger)
    hour_15 = Column(BigInteger)
    hour_16 = Column(BigInteger)
    hour_17 = Column(BigInteger)
    hour_18 = Column(BigInteger)
    hour_19 = Column(BigInteger)
    hour_20 = Column(BigInteger)
    hour_21 = Column(BigInteger)
    hour_22 = Column(BigInteger)
    hour_23 = Column(BigInteger)
    Total = Column(BigInteger)


class IpFlowOut(Base):
    __tablename__ = 'ip_flow_out'

    ip = Column(BigInteger, primary_key=True, nullable=False)
    pid = Column(BigInteger, primary_key=True, nullable=False)
    hour_0 = Column(BigInteger)
    hour_1 = Column(BigInteger)
    hour_2 = Column(BigInteger)
    hour_3 = Column(BigInteger)
    hour_4 = Column(BigInteger)
    hour_5 = Column(BigInteger)
    hour_6 = Column(BigInteger)
    hour_7 = Column(BigInteger)
    hour_8 = Column(BigInteger)
    hour_9 = Column(BigInteger)
    hour_10 = Column(BigInteger)
    hour_11 = Column(BigInteger)
    hour_12 = Column(BigInteger)
    hour_13 = Column(BigInteger)
    hour_14 = Column(BigInteger)
    hour_15 = Column(BigInteger)
    hour_16 = Column(BigInteger)
    hour_17 = Column(BigInteger)
    hour_18 = Column(BigInteger)
    hour_19 = Column(BigInteger)
    hour_20 = Column(BigInteger)
    hour_21 = Column(BigInteger)
    hour_22 = Column(BigInteger)
    hour_23 = Column(BigInteger)
    Total = Column(BigInteger)


class IpOnlineInfo(Base):
    __tablename__ = 'ip_online_info'

    ip = Column(BigInteger, primary_key=True, nullable=False)
    pid = Column(BigInteger, primary_key=True, nullable=False)
    hour_0 = Column(Integer, server_default=text("'0'"))
    hour_1 = Column(Integer, server_default=text("'0'"))
    hour_2 = Column(Integer, server_default=text("'0'"))
    hour_3 = Column(Integer, server_default=text("'0'"))
    hour_4 = Column(Integer)
    hour_5 = Column(Integer, server_default=text("'0'"))
    hour_6 = Column(Integer, server_default=text("'0'"))
    hour_7 = Column(Integer, server_default=text("'0'"))
    hour_8 = Column(Integer, server_default=text("'0'"))
    hour_9 = Column(Integer, server_default=text("'0'"))
    hour_10 = Column(Integer, server_default=text("'0'"))
    hour_11 = Column(Integer, server_default=text("'0'"))
    hour_12 = Column(Integer, server_default=text("'0'"))
    hour_13 = Column(Integer, server_default=text("'0'"))
    hour_14 = Column(Integer, server_default=text("'0'"))
    hour_15 = Column(Integer, server_default=text("'0'"))
    hour_16 = Column(Integer, server_default=text("'0'"))
    hour_17 = Column(Integer, server_default=text("'0'"))
    hour_18 = Column(Integer, server_default=text("'0'"))
    hour_19 = Column(Integer, server_default=text("'0'"))
    hour_20 = Column(Integer, server_default=text("'0'"))
    hour_21 = Column(Integer, server_default=text("'0'"))
    hour_22 = Column(Integer, server_default=text("'0'"))
    hour_23 = Column(Integer, server_default=text("'0'"))
    Total = Column(Integer, server_default=text("'0'"))


class IpProtocolFlow(Base):
    __tablename__ = 'ip_protocol_flow'

    ip = Column(BigInteger, primary_key=True, nullable=False)
    date = Column(BigInteger, primary_key=True, nullable=False)
    protocol = Column(String(12), primary_key=True, nullable=False)
    inflow = Column(BigInteger)
    outflow = Column(BigInteger)


class IsisInterfaceInfo(Base):
    __tablename__ = 'isis_interface_info'

    id = Column(BigInteger, primary_key=True)
    area_id = Column(String(25), server_default=text("''"))
    sys_id = Column(String(20), nullable=False, server_default=text("''"))
    interface_ip = Column(String(20), nullable=False)


class IsisLinkAttr(Base):
    __tablename__ = 'isis_link_attr'

    id = Column(Integer, primary_key=True)
    area_id = Column(String(25), server_default=text("''"))
    sys_id = Column(String(20), nullable=False, server_default=text("''"))
    interface_ip = Column(String(15), server_default=text("''"))
    n_area_id = Column(String(25), server_default=text("''"))
    n_sys_id = Column(String(20), server_default=text("''"))
    bandwidth = Column(Integer, server_default=text("'0'"))
    description = Column(String(127), server_default=text("''"))
    timestamp = Column(Numeric(10, 0), nullable=False)


class IsisLinkInfo(Base):
    __tablename__ = 'isis_link_info'

    id = Column(BigInteger, primary_key=True)
    area_id = Column(String(25), server_default=text("''"))
    sys_id = Column(String(20), nullable=False, server_default=text("''"))
    interface_ip = Column(String(15), server_default=text("''"))
    mask = Column(String(15), server_default=text("''"))
    n_area_id = Column(String(25), server_default=text("''"))
    n_sys_id = Column(String(20), server_default=text("''"))
    link_type = Column(Integer, server_default=text("'0'"))
    is_static = Column(Integer, server_default=text("'0'"))
    metric = Column(Integer, server_default=text("'0'"))
    create_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False, server_default=text("'9999999999'"))


class IsisRouterAttr(Base):
    __tablename__ = 'isis_router_attr'

    id = Column(Integer, primary_key=True)
    area_id = Column(String(25), server_default=text("''"))
    sys_id = Column(String(20), nullable=False, server_default=text("''"))
    alias = Column(String(30), server_default=text("''"))
    description = Column(String(127), server_default=text("''"))
    dptid = Column(Integer, server_default=text("'0'"))
    x = Column(Numeric(16, 12), server_default=text("'0.000000000000'"))
    y = Column(Numeric(16, 12), server_default=text("'0.000000000000'"))
    timestamp = Column(Numeric(10, 0), nullable=False)


class IsisRouterInfo(Base):
    __tablename__ = 'isis_router_info'

    id = Column(BigInteger, primary_key=True)
    area_id = Column(String(25), server_default=text("''"))
    sys_id = Column(String(20), nullable=False, server_default=text("''"))
    hostname = Column(String(20), server_default=text("''"))
    router_type = Column(Integer, nullable=False)
    create_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False, server_default=text("'9999999999'"))


class IsisRouterReachability(Base):
    __tablename__ = 'isis_router_reachability'

    id = Column(Integer, primary_key=True)
    area_id = Column(String(25), server_default=text("''"))
    sys_id = Column(String(20), nullable=False, server_default=text("''"))
    prefix = Column(String(20), nullable=False, server_default=text("''"))
    metric = Column(Integer, nullable=False)
    create_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False)


class IsisTrafficTopo(Base):
    __tablename__ = 'isis_traffic_topo'

    id = Column(BigInteger, primary_key=True)
    pid = Column(BigInteger, nullable=False)
    link_id = Column(BigInteger, nullable=False)
    period_interval = Column(Integer)
    bytes = Column(BigInteger, server_default=text("'0'"))
    protocol_bytes = Column(Text)


class IsisWarning(Base):
    __tablename__ = 'isis_warning'

    id = Column(BigInteger, primary_key=True)
    code = Column(SmallInteger, nullable=False, index=True)
    parse_time = Column(Integer)
    snmp_time = Column(Integer)
    text_params = Column(String(127), server_default=text("''"))
    relate_id = Column(BigInteger)
    solved = Column(Integer, nullable=False, server_default=text("'0'"))
    timestamp = Column(BigInteger, nullable=False)


class OspfAsexternallsa(Base):
    __tablename__ = 'ospf_asexternallsa'

    id = Column(BigInteger, primary_key=True)
    asNum = Column(SmallInteger)
    routerID = Column(String(15))
    areaID = Column(String(15))
    timeStamp = Column(Numeric(13, 0))
    lsAge = Column(SmallInteger)
    lsaType = Column(Integer)
    linkStateID = Column(String(15))
    adRouter = Column(String(15))
    networkMask = Column(String(15))
    externalType = Column(Integer)
    metric = Column(Integer)
    forwardAddress = Column(String(15))
    eRouterTag = Column(Integer)
    isUseful = Column(BIT(1))


class OspfDataBackup(Base):
    __tablename__ = 'ospf_data_backup'

    id = Column(BigInteger, primary_key=True)
    type = Column(Integer, nullable=False)
    tableName = Column(String(40), nullable=False, server_default=text("''"))
    hz_tableName = Column(String(40), nullable=False)
    relate_id = Column(BigInteger, nullable=False)
    timestamp = Column(BigInteger, nullable=False)


class OspfLinkAttr(Base):
    __tablename__ = 'ospf_link_attr'

    id = Column(Integer, primary_key=True)
    as_num = Column(SmallInteger, nullable=False)
    router_id = Column(String(15), nullable=False)
    interface_ip = Column(String(15), server_default=text("''"))
    n_as_num = Column(SmallInteger)
    n_router_id = Column(String(15))
    bandwidth = Column(Integer, server_default=text("'0'"))
    description = Column(String(127), server_default=text("''"))
    timestamp = Column(Numeric(10, 0), nullable=False)


class OspfLinkInfo(Base):
    __tablename__ = 'ospf_link_info'

    id = Column(BigInteger, primary_key=True)
    as_num = Column(SmallInteger, nullable=False)
    router_id = Column(String(15), nullable=False)
    interface_ip = Column(String(15), server_default=text("''"))
    mask = Column(String(15), server_default=text("''"))
    n_as_num = Column(SmallInteger)
    n_router_id = Column(String(15))
    area_id = Column(String(15), server_default=text("''"))
    link_type = Column(Integer, server_default=text("'0'"))
    is_static = Column(Integer, server_default=text("'0'"))
    metric = Column(Integer, server_default=text("'0'"))
    create_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False, server_default=text("'9999999999'"))


class OspfNetworklsa(Base):
    __tablename__ = 'ospf_networklsa'

    id = Column(BigInteger, primary_key=True)
    asNum = Column(SmallInteger)
    routerID = Column(String(15))
    areaID = Column(String(15))
    timeStamp = Column(Numeric(13, 0))
    lsAge = Column(SmallInteger)
    linkStateID = Column(String(15))
    adRouter = Column(String(15))
    networkMask = Column(String(15))
    attachedRouter = Column(String(15))
    isUseful = Column(BIT(1))


class OspfRouterAttr(Base):
    __tablename__ = 'ospf_router_attr'
    __table_args__ = (
        Index('as_router', 'as_num', 'router_id'),
    )

    id = Column(Integer, primary_key=True)
    as_num = Column(SmallInteger, nullable=False)
    router_id = Column(String(15), nullable=False)
    alias = Column(String(30), server_default=text("''"))
    description = Column(String(127), server_default=text("''"))
    dptid = Column(Integer, server_default=text("'0'"))
    x = Column(Numeric(16, 12), server_default=text("'0.000000000000'"))
    y = Column(Numeric(16, 12), server_default=text("'0.000000000000'"))
    timestamp = Column(Numeric(10, 0), nullable=False)


class OspfRouterInfo(Base):
    __tablename__ = 'ospf_router_info'
    __table_args__ = (
        Index('time', 'create_time', 'end_time'),
        Index('as_router', 'as_num', 'router_id')
    )

    id = Column(BigInteger, primary_key=True)
    as_num = Column(SmallInteger, nullable=False)
    router_id = Column(String(15), nullable=False)
    router_type = Column(Integer, nullable=False)
    create_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False, server_default=text("'9999999999'"))


class OspfRouterlsa(Base):
    __tablename__ = 'ospf_routerlsa'

    id = Column(BigInteger, primary_key=True)
    asNum = Column(SmallInteger)
    routerID = Column(String(15))
    areaID = Column(String(15))
    timeStamp = Column(Numeric(13, 0))
    lsAge = Column(SmallInteger)
    linkStateID = Column(String(15))
    adRouter = Column(String(15))
    zeroVEB = Column(Integer)
    linkID = Column(String(15))
    linkData = Column(String(15))
    linkType = Column(Integer)
    metric = Column(SmallInteger)
    isUseful = Column(BIT(1))


class OspfSummarylsa(Base):
    __tablename__ = 'ospf_summarylsa'

    id = Column(BigInteger, primary_key=True)
    asNum = Column(SmallInteger)
    routerID = Column(String(15))
    areaID = Column(String(15))
    timeStamp = Column(Numeric(13, 0))
    lsAge = Column(SmallInteger)
    lsaType = Column(Integer)
    linkStateID = Column(String(15))
    adRouter = Column(String(15))
    networkMask = Column(String(15))
    metric = Column(Integer)
    isUseful = Column(BIT(1))


class OspfTrafficTopo(Base):
    __tablename__ = 'ospf_traffic_topo'

    id = Column(BigInteger, primary_key=True)
    pid = Column(BigInteger, nullable=False, index=True)
    link_id = Column(BigInteger, nullable=False)
    period_interval = Column(Integer)
    bytes = Column(BigInteger, server_default=text("'0'"))
    protocol_bytes = Column(Text)


class PrefixFlowIn(Base):
    __tablename__ = 'prefix_flow_in'

    ip = Column(BigInteger, primary_key=True, nullable=False)
    pid = Column(BigInteger, primary_key=True, nullable=False)
    hour_0 = Column(BigInteger)
    hour_1 = Column(BigInteger)
    hour_2 = Column(BigInteger)
    hour_3 = Column(BigInteger)
    hour_4 = Column(BigInteger)
    hour_5 = Column(BigInteger)
    hour_6 = Column(BigInteger)
    hour_7 = Column(BigInteger)
    hour_8 = Column(BigInteger)
    hour_9 = Column(BigInteger)
    hour_10 = Column(BigInteger)
    hour_11 = Column(BigInteger)
    hour_12 = Column(BigInteger)
    hour_13 = Column(BigInteger)
    hour_14 = Column(BigInteger)
    hour_15 = Column(BigInteger)
    hour_16 = Column(BigInteger)
    hour_17 = Column(BigInteger)
    hour_18 = Column(BigInteger)
    hour_19 = Column(BigInteger)
    hour_20 = Column(BigInteger)
    hour_21 = Column(BigInteger)
    hour_22 = Column(BigInteger)
    hour_23 = Column(BigInteger)
    Total = Column(BigInteger)


class PrefixFlowOut(Base):
    __tablename__ = 'prefix_flow_out'

    ip = Column(BigInteger, primary_key=True, nullable=False)
    pid = Column(BigInteger, primary_key=True, nullable=False)
    hour_0 = Column(BigInteger)
    hour_1 = Column(BigInteger)
    hour_2 = Column(BigInteger)
    hour_3 = Column(BigInteger)
    hour_4 = Column(BigInteger)
    hour_5 = Column(BigInteger)
    hour_6 = Column(BigInteger)
    hour_7 = Column(BigInteger)
    hour_8 = Column(BigInteger)
    hour_9 = Column(BigInteger)
    hour_10 = Column(BigInteger)
    hour_11 = Column(BigInteger)
    hour_12 = Column(BigInteger)
    hour_13 = Column(BigInteger)
    hour_14 = Column(BigInteger)
    hour_15 = Column(BigInteger)
    hour_16 = Column(BigInteger)
    hour_17 = Column(BigInteger)
    hour_18 = Column(BigInteger)
    hour_19 = Column(BigInteger)
    hour_20 = Column(BigInteger)
    hour_21 = Column(BigInteger)
    hour_22 = Column(BigInteger)
    hour_23 = Column(BigInteger)
    Total = Column(BigInteger)


class PrefixProtocolFlow(Base):
    __tablename__ = 'prefix_protocol_flow'

    prefix = Column(BigInteger, primary_key=True, nullable=False)
    date = Column(BigInteger, primary_key=True, nullable=False)
    protocol = Column(String(12), primary_key=True, nullable=False)
    inflow = Column(BigInteger)
    outflow = Column(BigInteger)


class RtaAlarm(Base):
    __tablename__ = 'rta_alarm'

    id = Column(Integer, primary_key=True)
    alarmId = Column(String(255))
    alarmName = Column(String(255))
    alarmLevel = Column(String(255))
    alarmLevelCode = Column(String(255))
    alarmType = Column(String(255))
    alarmTypeCode = Column(String(255))
    alarmTime = Column(String(255))
    alarmLocation = Column(String(255))
    alarmInfo = Column(String(1000))
    deviceId = Column(String(255))
    deviceIp = Column(String(255))
    deviceName = Column(String(255))
    collectTime = Column(String(255))
    messageType = Column(String(255))


class RtaAlarmhistory(Base):
    __tablename__ = 'rta_alarmhistory'

    id = Column(Integer, primary_key=True)
    alarmName = Column(String(255))
    alarmLevel = Column(String(255))
    alarmLevelCode = Column(String(255))
    alarmType = Column(String(255))
    alarmTypeCode = Column(String(255))
    alarmTime = Column(String(255))
    alarmLocation = Column(String(255))
    affirmTime = Column(String(255))
    alarmId = Column(String(255))
    alarmInfo = Column(String(1000))
    deviceId = Column(String(255))
    deviceName = Column(String(255))
    deviceIp = Column(String(255))
    collectTime = Column(String(255))
    messageType = Column(String(255))


t_rta_config = Table(
    'rta_config', metadata,
    Column('configName', String(255)),
    Column('configValue', String(255))
)


t_rta_device_parameter = Table(
    'rta_device_parameter', metadata,
    Column('device_id', Integer),
    Column('device_ip', String(15)),
    Column('device_name', String(255)),
    Column('dev_type_id', Integer),
    Column('area_id', String(255)),
    Column('device_version', String(255)),
    Column('parent_dev_id', Integer),
    Column('sys_running_time', Integer),
    Column('run_status', SmallInteger)
)


t_rta_device_record = Table(
    'rta_device_record', metadata,
    Column('device_id', Integer),
    Column('cpu_util_ratio', Float),
    Column('phy_util_ratio', Float),
    Column('phy_memory_size', Integer),
    Column('service_number', Integer),
    Column('collect_time', Integer)
)


t_rta_device_type = Table(
    'rta_device_type', metadata,
    Column('type_id', Integer),
    Column('type_name', String(255))
)


class RtaDictionary(Base):
    __tablename__ = 'rta_dictionary'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    ncode = Column(String(10))
    type = Column(String(10))
    tcode = Column(String(10))
    englishname = Column(String(30))
    handleInfo = Column(String(250))


t_rta_dm_rount = Table(
    'rta_dm_rount', metadata,
    Column('interface_ip', String(30)),
    Column('device_id', Integer),
    Column('run_status', Integer),
    Column('offline_time', Integer),
    Column('collect_time', Integer)
)


t_rta_process_record = Table(
    'rta_process_record', metadata,
    Column('process_id', Integer),
    Column('process_name', String(255)),
    Column('device_id', Integer),
    Column('cpu_util_ratio', Float),
    Column('phy_util_ratio', Float),
    Column('collect_time', BigInteger)
)


class Syslog(Base):
    __tablename__ = 'syslog'

    id = Column(BigInteger, primary_key=True)
    code = Column(Integer, nullable=False, index=True)
    text_params = Column(Text)
    timestamp = Column(Integer, nullable=False)


class SyslogDictionary(Base):
    __tablename__ = 'syslog_dictionary'

    code = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    text_template = Column(String(127), server_default=text("''"))


class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True)
    username = Column(String(15), nullable=False)
    password = Column(String(32), nullable=False)
    usertype = Column(Integer, nullable=False, server_default=text("'2'"))
    dptid = Column(Integer, server_default=text("'0'"))


t_view_bgp_path_info = Table(
    'view_bgp_path_info', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('n_routerID', String(15)),
    Column('n_asNum', Integer),
    Column('n_peerIP', String(15)),
    Column('prefixLen', Integer),
    Column('networkNum', String(15)),
    Column('asPath', String(30)),
    Column('nextHop', String(15)),
    Column('origin', Integer),
    Column('weight', Integer),
    Column('med', Integer),
    Column('local_pref', Integer),
    Column('create_time', Numeric(13, 0)),
    Column('end_time', Numeric(13, 0))
)


t_view_hz_bgp_path_info = Table(
    'view_hz_bgp_path_info', metadata,
    Column('id', BigInteger),
    Column('as_num', SmallInteger),
    Column('n_routerID', String(15)),
    Column('n_asNum', Integer),
    Column('n_peerIP', String(15)),
    Column('prefixLen', Integer),
    Column('networkNum', String(15)),
    Column('asPath', String(30)),
    Column('nextHop', String(15)),
    Column('origin', Integer),
    Column('weight', Integer),
    Column('med', Integer),
    Column('local_pref', Integer),
    Column('create_time', Numeric(13, 0)),
    Column('end_time', Numeric(13, 0))
)


t_view_hz_ospf_asexternallsa = Table(
    'view_hz_ospf_asexternallsa', metadata,
    Column('id', BigInteger),
    Column('as_num', SmallInteger, server_default=text("'0'")),
    Column('routerID', String(15)),
    Column('areaID', String(15)),
    Column('timeStamp', Numeric(13, 0)),
    Column('lsAge', SmallInteger),
    Column('lsaType', Integer),
    Column('linkStateID', String(15)),
    Column('adRouter', String(15)),
    Column('networkMask', String(15)),
    Column('externalType', Integer),
    Column('metric', Integer),
    Column('forwardAddress', String(15)),
    Column('eRouterTag', Integer),
    Column('isUseful', BIT(1))
)


t_view_hz_ospf_link_info = Table(
    'view_hz_ospf_link_info', metadata,
    Column('id', BigInteger),
    Column('as_num', SmallInteger),
    Column('router_id', String(15)),
    Column('interface_ip', String(15)),
    Column('mask', String(15)),
    Column('n_as_num', SmallInteger),
    Column('n_router_id', String(15)),
    Column('area_id', String(15)),
    Column('link_type', Integer, server_default=text("'0'")),
    Column('is_static', Integer, server_default=text("'0'")),
    Column('metric', Integer, server_default=text("'0'")),
    Column('create_time', BigInteger),
    Column('end_time', BigInteger, server_default=text("'9999999999'"))
)


t_view_hz_ospf_router_info = Table(
    'view_hz_ospf_router_info', metadata,
    Column('id', BigInteger),
    Column('as_num', SmallInteger),
    Column('router_id', String(15)),
    Column('router_type', Integer),
    Column('create_time', BigInteger),
    Column('end_time', BigInteger, server_default=text("'9999999999'"))
)


t_view_hz_warning = Table(
    'view_hz_warning', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('as_num', SmallInteger),
    Column('code', SmallInteger),
    Column('parse_time', Integer),
    Column('snmp_time', Integer),
    Column('text_params', String(127)),
    Column('relate_id', BigInteger),
    Column('solved', Integer, server_default=text("'0'")),
    Column('timestamp', BigInteger)
)


t_view_ospf_asexternallsa = Table(
    'view_ospf_asexternallsa', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('asNum', SmallInteger),
    Column('routerID', String(15)),
    Column('areaID', String(15)),
    Column('timeStamp', Numeric(13, 0)),
    Column('lsAge', SmallInteger),
    Column('lsaType', Integer),
    Column('linkStateID', String(15)),
    Column('adRouter', String(15)),
    Column('networkMask', String(15)),
    Column('externalType', Integer),
    Column('metric', Integer),
    Column('forwardAddress', String(15)),
    Column('eRouterTag', Integer),
    Column('isUseful', BIT(1))
)


t_view_ospf_link_info = Table(
    'view_ospf_link_info', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('as_num', SmallInteger),
    Column('router_id', String(15)),
    Column('interface_ip', String(15)),
    Column('mask', String(15)),
    Column('n_as_num', SmallInteger),
    Column('n_router_id', String(15)),
    Column('area_id', String(15)),
    Column('link_type', Integer, server_default=text("'0'")),
    Column('is_static', Integer, server_default=text("'0'")),
    Column('metric', Integer, server_default=text("'0'")),
    Column('create_time', BigInteger),
    Column('end_time', BigInteger, server_default=text("'9999999999'"))
)


t_view_ospf_networklsa = Table(
    'view_ospf_networklsa', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('asNum', SmallInteger),
    Column('routerID', String(15)),
    Column('areaID', String(15)),
    Column('timeStamp', Numeric(13, 0)),
    Column('lsAge', SmallInteger),
    Column('linkStateID', String(15)),
    Column('adRouter', String(15)),
    Column('networkMask', String(15)),
    Column('attachedRouter', String(15)),
    Column('isUseful', BIT(1))
)


t_view_ospf_router_info = Table(
    'view_ospf_router_info', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('as_num', SmallInteger),
    Column('router_id', String(15)),
    Column('router_type', Integer),
    Column('create_time', BigInteger),
    Column('end_time', BigInteger, server_default=text("'9999999999'"))
)


t_view_ospf_routerlsa = Table(
    'view_ospf_routerlsa', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('asNum', SmallInteger),
    Column('routerID', String(15)),
    Column('areaID', String(15)),
    Column('timeStamp', Numeric(13, 0)),
    Column('lsAge', SmallInteger),
    Column('linkStateID', String(15)),
    Column('adRouter', String(15)),
    Column('zeroVEB', Integer),
    Column('linkID', String(15)),
    Column('linkData', String(15)),
    Column('linkType', Integer),
    Column('metric', SmallInteger),
    Column('isUseful', BIT(1))
)


t_view_ospf_summarylsa = Table(
    'view_ospf_summarylsa', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('asNum', SmallInteger),
    Column('routerID', String(15)),
    Column('areaID', String(15)),
    Column('timeStamp', Numeric(13, 0)),
    Column('lsAge', SmallInteger),
    Column('lsaType', Integer),
    Column('linkStateID', String(15)),
    Column('adRouter', String(15)),
    Column('networkMask', String(15)),
    Column('metric', Integer),
    Column('isUseful', BIT(1))
)


t_view_warning = Table(
    'view_warning', metadata,
    Column('id', BigInteger, server_default=text("'0'")),
    Column('code', SmallInteger),
    Column('parse_time', Integer),
    Column('snmp_time', Integer),
    Column('text_params', String(127)),
    Column('relate_id', BigInteger),
    Column('solved', Integer, server_default=text("'0'")),
    Column('timestamp', BigInteger)
)


class Warning(Base):
    __tablename__ = 'warning'

    id = Column(BigInteger, primary_key=True)
    code = Column(SmallInteger, nullable=False, index=True)
    parse_time = Column(Integer)
    snmp_time = Column(Integer)
    text_params = Column(String(127), server_default=text("''"))
    relate_id = Column(BigInteger)
    solved = Column(Integer, nullable=False, server_default=text("'0'"))
    timestamp = Column(BigInteger, nullable=False)


class WarningDictionary(Base):
    __tablename__ = 'warning_dictionary'

    code = Column(SmallInteger, primary_key=True)
    name = Column(String(30), nullable=False)
    _class = Column('class', Integer, nullable=False)
    type = Column(Integer, nullable=False)
    text_template = Column(String(127), server_default=text("''"))
    level = Column(Integer, nullable=False)
    handle_info = Column(String(127), server_default=text("''"))
