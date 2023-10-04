let date = new Date().getDate();
let current = (new Date().getFullYear()) + "-" + (new Date().getMonth()) + "-" + (new Date().getDate()) ;
console.log(current)


// new AirDatepicker('#myDatepicker');

//載入網頁, 連接後端取得景點資料

get_attraction_data_by_currentUrl_and_reflush_attraction_info()
create_radio_eventListener()
select_travel_date_add_min_max_date()


//add radio event listener
function create_radio_eventListener() {
    document.querySelectorAll(".select_plan_radio").forEach(item => {
        item.addEventListener('click', event => {
            let target_value = event.target.value

            let price_span = document.getElementsByClassName("price_span")[0];

            if (target_value == 'morning') {
                price_span.textContent = "新台幣 2OOO 元"
                price_span.value = 2000
            };
            if (target_value == 'afternoon') {
                price_span.textContent = "新台幣 25OO 元"
                price_span.value = 2500
            };
        })
    })
}


//載入網頁, 連接後端取得景點資料
async function get_attraction_data_by_currentUrl_and_reflush_attraction_info() {
    let current_url = window.location.href;
    let host_url = current_url.split('attraction/')[0]
    let attraction_id = current_url.split('attraction/')[1]
    let fetch_url = `${host_url}/api/attraction/${attraction_id}`
    try {
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



    } catch (error) {
        console.log(error)
        console.log("fetech url error!")
        window.location.href = host_url
    }



}


function switch_attraction_info_img_dot(switch_index) {
    if (switch_index == 0) return;
    switch_index = parseInt(switch_index)

    //get img location index
    let current_img_location = parseInt(document.getElementsByClassName("attraction-img-display")[0].id);
    let img_collection = document.getElementsByClassName("attraction-img")
    let img_collection_len = img_collection.length;

    //get dot locatiob_index
    let current_dot_location = parseInt(document.getElementsByClassName("img_navbar_circle_button-current")[0].id);
    let dot_collection = document.getElementsByClassName("img_navbar_circle_button")

    //編碼錯誤刷新頁面
    if (current_dot_location != current_img_location) {
        location.reload()
    }

    let target_value = (current_img_location + switch_index) % img_collection_len
    let non_display_index = current_img_location;
    let display_index = target_value;
    //重新設定 element class 來處理display狀態
    img_collection[display_index].className = "attraction-img-display attraction-img"
    img_collection[non_display_index].className = "attraction-img-non-display attraction-img"
    dot_collection[display_index].className = "img_navbar_circle_button-current img_navbar_circle_button"
    dot_collection[non_display_index].className = "img_navbar_circle_button-non-current img_navbar_circle_button"


}



async function booking_select_plan() {
    //check login
    let jwt_token = localStorage.getItem("jwt_token")
    if (jwt_token == null) {
        show_sign()
        return
    } else {
        check_user_login_status()
    }

    //user input status
    let select_date = document.getElementsByClassName("select_travel_date")[0].value
    if (select_date == "") { alert("請選擇日期"); return }

    let select_plan
    document.querySelectorAll("#select_plan_radio").forEach(Element => {
        if (Element.checked == true) { select_plan = Element.defaultValue }
    })
    if (select_plan == undefined) { alert("請選擇行程"); return }
    let price = document.getElementsByClassName("price_span")[0].value

    let booking_data = {
        "attractionId": parseInt(window.location.href.split('attraction/')[1]),
        "date": select_date,
        "time": select_plan,
        "price": price
    }
    let request_para = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("jwt_token")}`
        },
        body: JSON.stringify(booking_data)

    }


    //create a post reqeust into webn server
    let fetch_data = await fetch("/api/booking", request_para)
    let parseData = await fetch_data.json()
    console.log(parseData)
    if (parseData['ok']) {
        window.location.href = window.location.origin+"/booking"
    }
    else {
        alert("預定失敗")
    }

}

async function check_user_login_status() {

    if (localStorage.getItem("jwt_token") != null) {
        let request_obj = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("jwt_token")}`
            }
        }
        try {
            let fetch_data = await fetch("/api/user/auth", request_obj)
            let parseData = await fetch_data.json()
            if (parseData == null) {
                localStorage.removeItem("jwt_token");
                //如果會員認證失敗，重新整理頁面
                window.location.href = window.location.origin
            } else {
                return true
            }


        } catch (err) {
            console.log("login failed")
            console.log(err)

        }



    }

};

function select_travel_date_add_min_max_date(){
    let today = new Date()
    let year = today.getFullYear()
    let month = today.getMonth()+1 < 10 ? "0"+(today.getMonth()+1) : today.getMonth()+1
    let date = today.getDate() <10 ? "0"+today.getDate() : today.getDate()
    let min_date = `${year}-${month}-${date}`
    let max_date = `${year+1}-${month}-${date}`

    let input_date = document.getElementsByClassName("select_travel_date")[0]
    input_date.min = min_date
    input_date.max = max_date

}








