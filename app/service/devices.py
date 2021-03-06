from pymongo.database import Database
from bson.objectid import ObjectId
from datetime import datetime
from dateutil import parser
from loguru import logger
from bson.errors import InvalidDocument, InvalidId


def list_oldest_records(db: Database, max_register: int = 1000, synchronized: bool = False) -> (list, list):
    sensors = db.get_collection("devices").find({},{'sensors.type':1})
    registers = []
    list_sensors = []
    # type-relative-humidity
    for sensor in sensors:
        for type_sensor in sensor['sensors']:
            list_sensors.append(type_sensor['type'])
            data_sensor = list(db.get_collection(type_sensor['type'])
                                                .find({
                                                    "$or":[
                                                        {"synchronized": {"$exists": False}},
                                                        {"synchronized": synchronized}
                                                    ]})
                                                .sort("date",1)
                                                .limit(max_register))

            registers += list(map(lambda data: update_data(data, type_sensor['type']) , data_sensor))
    # registers.sort(key = lambda device: device["date"], reverse = True)
    registers.sort(key = lambda device: device["date"])
    logger.info(f"total records read {len(registers)} of {len(list_sensors)} sensors")
    return registers[0:max_register], list_sensors

def update_data(data, type_sensor):
    data_update = data["date"]
    if type(data["date"]) == str:
        data_update = parser.parse(data_update)
        # data_update = datetime.strptime(data_update, '%d/%m/%y %H:%M:%S')
    data.update({
        "type":  type_sensor,
        "date": data_update
        })
    return data


def update_sensors(db: Database, device: str, ids: list, new_value: dict = { "$set": { "synchronized": True } }) -> bool:
    try:
        result = db.get_collection(device).update_many({"_id": {"$in": ids}}, new_value)
        # logger.info(f"updated records: {result.raw_result} -> {ids}")
        return True
    except InvalidId as invalId:
        logger.error(str(invalId))
    except InvalidDocument as invalDoc:
        logger.error(str(invalDoc))
    return False

def delete_sensors(db: Database, device: str, ids: list) -> bool:
    try:
        result = db.get_collection(device).delete_many({"_id": {"$in": ids}})
        logger.info(f"deleted records: {result.raw_result['n']}")
        return True
    except InvalidId as invalId:
        logger.error(str(invalId))
    except InvalidDocument as invalDoc:
        logger.error(str(invalDoc))
    return False