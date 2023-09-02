
import json
import os
import attraction_model


##read json data from file
def read_json_file(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        data = json.load(file)
        
    return data

##current file path
current_path = os.path.dirname(__file__)
taipei_attractions_collection = read_json_file(current_path + "/taipei-attractions.json")["result"]["results"]


##get mrt set
def get_mrt_set(arrtactions_collection)->set:
    mrt_set = set()
    for attraction in arrtactions_collection:
        mrt_set.add(attraction["MRT"])
    return mrt_set


def get_category_set(arrtactions_collection)->set:
    category_set = set()
    for attraction in arrtactions_collection:
        category_set.add(attraction["CAT"])
    return category_set

def split_file_scr_from_string(str)->[str]:
    resutls = []
    for item in str.split("https:"):
        test_str = item.upper()
        if test_str.find(".JPG")== -1 and test_str.find(".PNG")== -1:
            continue
        resutls.append("https:" + item)
    return resutls
def inset_all_mrt_data(mrt_set):
    for mrt in mrt_set:
        attraction_model.insert_mrt_data_into_taipei_travel(mrt=mrt)

def insert_all_category_data(category_set):
    for item in category_set:
        attraction_model.insert_category_data_into_taipei_travel(category=item)
##insert_all_category_data(get_category_set(taipei_attractions_collection))

def get_all_mrt_data():
    temp_data= attraction_model.get_all_mrt_data_from_taipei_travel()

    mrt_dict = {}
    for mrt in temp_data:
        mrt_dict[mrt["mrt"]] = mrt["mrt_id"]
    return mrt_dict


def get_all_category_data():
    temp_data= attraction_model.get_all_category_data_from_taipei_travel()

    category_dict = {}
    for item in temp_data:
        category_dict[item["category"]] = item["category_id"]
    return category_dict

##inset_all_mrt_data(get_mrt_set(taipei_attractions_collection))
##insert_all_category_data(get_category_set(taipei_attractions_collection))

##get data dic
category_dict = get_all_category_data()
mrt_dict = get_all_mrt_data()



#plan insert data
def insert_all_attraction_data(attractions_collection):
    mrt_dict = get_all_mrt_data()
    category_dict = get_all_category_data()
    for attraction in attractions_collection:
        try:
            attraction_object = {
                "attraction_id":attraction["_id"],
                "rate":attraction["rate"],
                "transport":attraction["direction"],
                "name":attraction["name"],
                "av_end":attraction["avEnd"],
                "av_begin":attraction["avBegin"],
                "address":attraction["address"],
                "description":attraction["description"],
                "mrt_id":mrt_dict[attraction["MRT"]],
                "category_id":category_dict[attraction["CAT"]],
                "date":attraction["date"],
                "serial_no":attraction["SERIAL_NO"],
                "memo_time":attraction["MEMO_TIME"],
                "poi": attraction["POI"],
                "file": split_file_scr_from_string(attraction["file"]),
                'idpt': attraction["idpt"],
                "lat": attraction["latitude"],
                "lng": attraction["longitude"],
                "ref_wp": attraction["REF_WP"]
            }
        except Exception as err:
            print(err)
            continue   
        attraction_model.insert_into_attraction(attraction_object)
        attraction_model.insert_attraction_info(attraction_object)
        for item in attraction_object["file"]:
            attraction_model.insert_image(
                attraction_id=attraction_object["attraction_id"],
                src=item
                )
#insert_all_attraction_data(taipei_attractions_collection)

if __name__ == '__main__':
    
    inset_all_mrt_data(get_mrt_set(taipei_attractions_collection))
    insert_all_category_data(get_category_set(taipei_attractions_collection))
    insert_all_attraction_data(taipei_attractions_collection)
    