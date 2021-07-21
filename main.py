from app.service import ( delete_sensors, 
                        update_sensors, 
                        list_oldest_records,
                        Synchonization,
                        GarbageCollector
                                )
from app.config import my_database 
from bson.objectid import ObjectId


if __name__ == "__main__":
    Synchonization().synchronize_records(my_database)
    #GarbageCollector().clear_memory(my_database)
    # r, l = list_oldest_records(my_database, synchronized=True)
    # print(r[0])
    # id =  [ObjectId('5e1362f67cb1853275270dcc'), ObjectId('5e1364690f35dc3695f897b3')]
    # update_sensors(my_database, "type-air-temperature", id)
