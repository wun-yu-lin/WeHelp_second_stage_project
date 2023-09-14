// new AirDatepicker('#myDatepicker');

//載入網頁, 連接後端取得景點資料

get_attraction_data_by_currentUrl_and_reflush_attraction_info()
create_radio_eventListener()


//add radio event listener
function create_radio_eventListener(){
    document.querySelectorAll(".select_plan_radio").forEach(item => {
        item.addEventListener('click', event =>{
            let target_value = event.target.value
            
            let price_span = document.getElementsByClassName("price_span")[0];

            if (target_value == 'morning') {price_span.textContent = "新台幣 2OOO 元"};
            if (target_value == 'afternoon') {price_span.textContent = "新台幣 25OO 元"};
        })
    })
}


//載入網頁, 連接後端取得景點資料
async function get_attraction_data_by_currentUrl_and_reflush_attraction_info(){
    let current_url = window.location.href;
    let host_url =current_url.split('attraction/')[0]
    let attraction_id = current_url.split('attraction/')[1]
    let fetch_url = `${host_url}/api/attraction/${attraction_id}`
    try{
        let data = await fetch(fetch_url);
        let parseData = await data.json();

        //if error in parseData redirect to index
        if (parseData['error']) {
            console.log("error in parseData")
            window.location.href = host_url
        } 
        let attraction_data = parseData['data']
        let img_src_arr = attraction_data['images']


        //insert img into img_div
        let index = 0;
        let img_div = document.getElementsByClassName("img_collector_div")[0];
        let dot_div = document.getElementsByClassName("img_navbar_circle")[0];
        img_div.innerHTML = "";
        dot_div.innerHTML = "";
        img_src_arr.forEach((item) => {
            let img = document.createElement("img");
            let dot_button = document.createElement("button");
            if (index == 0) {
                img.className = "attraction-img-display attraction-img"
                dot_button.className = "img_navbar_circle_button-current img_navbar_circle_button"
            }
            else {
                img.className = "attraction-img-non-display attraction-img"
                dot_button.className = "img_navbar_circle_button-non-current img_navbar_circle_button"
            }
            img.src = item
            img.alt = "無照片連結"
            img.id = index
            dot_button.id = index
            img_div.appendChild(img);
            dot_div.appendChild(dot_button);
            index++;

            //insert attraction info
            document.getElementsByClassName("span_attraction_name")[0].textContent = attraction_data['name']
            document.getElementsByClassName("span_category_and_mrt")[0].textContent = `${attraction_data['category']} at ${attraction_data['mrt']}`
            document.getElementsByClassName("attraction_description")[0].textContent = attraction_data['description']
            document.getElementsByClassName("attraction_address_span")[0].textContent = attraction_data['address']
            document.getElementsByClassName("attraction_direction_span")[0].textContent = attraction_data['transport']


            

        })



    }catch (error){
        console.log(error)
        console.log("fetech url error!")
        window.location.href = host_url
    }
  
    

}


function switch_attraction_info_img_dot(switch_index){
    if (switch_index == 0 ) return;
    switch_index = parseInt(switch_index)

    //get img location index
    let current_img_location = parseInt(document.getElementsByClassName("attraction-img-display")[0].id);
    let img_collection = document.getElementsByClassName("attraction-img")
    let img_collection_len = img_collection.length;
    let img_non_display_index, img_display_index;

    //get dot locatiob_index
    let current_dot_location = parseInt(document.getElementsByClassName("img_navbar_circle_button-current")[0].id);
    let dot_collection = document.getElementsByClassName("img_navbar_circle_button")
    let dot_non_current_index, dot_current_index;

    //編碼錯誤刷新頁面
    if (current_dot_location != current_img_location) {
        location.reload()
    }


    img_non_display_index=current_img_location;
    dot_non_current_index=current_img_location;
    //最後一個跳轉到第一個img
    if(current_img_location+1==img_collection_len && switch_index == 1){

        img_display_index=0;
        dot_current_index=0;

    //第一個跳轉到最後一個
    }else if (current_img_location==0 && switch_index==-1){
        img_display_index=img_collection_len-1;
        dot_current_index=img_collection_len-1;

    //正常情況跳轉
    }else {
        if (switch_index==1){
            img_display_index=current_img_location+1;
            dot_current_index=current_img_location+1;
        }
        if (switch_index==-1){
            img_display_index=current_img_location-1;
            dot_current_index=current_img_location-1;
        }
    }
    
    //重新設定 element class 來處理display狀態
    img_collection[img_display_index].className = "attraction-img-display attraction-img"
    img_collection[img_non_display_index].className = "attraction-img-non-display attraction-img"
    dot_collection[dot_current_index].className = "img_navbar_circle_button-current img_navbar_circle_button"
    dot_collection[dot_non_current_index].className = "img_navbar_circle_button-non-current img_navbar_circle_button"
    

}






