

async function init_booking() {
    check_signin()
    await check_user_login_status_flush_item()//async function
    //get booking item length
    let booking_count = document.getElementsByClassName("atrraction_travel_info_div").length
    if (booking_count == 0) {
            clean_page()
            return
        }
    add_contact_and_payment_form()
    console.log("init_booking")
    update_total_price_message(calculated_total_price()) //計算總價並更新上去
    //create_multi_year_option()
}

function clean_page(){
    let content_div = document.querySelector(".content")
    content_div.innerHTML =""

    content_div.innerHTML=`
        <div class="booking_message_div">
            <p class="booking_message_p">您好，林文昱，待預訂行程如下：</p>
        </div>
        <div class="booking_message_div">
            <p class="booking_message_status_p">目前沒有任何待預訂的行程</p>
        </div>
    `
}

function check_signin() {
    try{
        let jwt_token = localStorage.getItem("jwt_token")
        if (jwt_token == null) {
            localStorage.removeItem("jwt_token")
            window.location.href = window.location.origin
            return
        }
        return true
    }catch (err){
        localStorage.removeItem("jwt_token")
        window.location.href = window.location.origin
        return

    }
}

//動態生成信用卡有效期限選項
function create_multi_year_option(){
    let year = new Date().getFullYear() -2000
    let year_option = document.getElementById("multi_year")
    year_option.innerHTML = ""
    let option = document.createElement("option")
    option.value = ""
    option.innerText = "YY"
    year_option.appendChild(option)
    for (let i = 0; i <= 20; i++) {
        let option = document.createElement("option")
        option.value = year + i
        option.innerText = year + i
        year_option.appendChild(option)
    }
}

async function delete_booking_item_and_reflush_page(event){
    //preparation request data
    id_arr = [event.target.id]
    delete_para = {
        method: "DELETE",
        headers:{
            "Content-type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("jwt_token")}`
            
        },
        body: JSON.stringify({"booking_id": id_arr})
    }

    //send delete request
    let fetch_data = await fetch("/api/booking", delete_para)
    let parseData = await fetch_data.json()
    console.log(parseData)
    
    //reflush page
    setTimeout(() => {
        window.location.reload()
    }, 1000);
    
}


function add_booking_message_p(content_text){
    document.getElementsByClassName("booking_message_p")[0].innerText = content_text
    
}

async function check_user_login_status_flush_item() {
    let parseData

    //確認登入狀態＆認證，並拿到會員資料
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
            parseData = await fetch_data.json()
            if (parseData == null) {
                localStorage.removeItem("jwt_token");
                //如果會員認證失敗，重新整理頁面
                window.location.href = window.location.origin
            }


        } catch (err) {
            console.log("login failed")
            console.log(err)

        }
    


    }

    //客製化頁面
    add_booking_message_p(`您好，${parseData["data"]["name"]}，待預訂行程如下：`)

    //拿到user預定行程資料
    get_booking_request_para = {
        method: "GET",
        headers:{
            "Authorization": `Bearer ${localStorage.getItem("jwt_token")}`,
            "Content-Type": "application/json"
        }
    }

    let fetch_booking_data = await fetch("/api/booking", get_booking_request_para)
    let parse_booking_data = await fetch_booking_data.json()
    booking_data_arr = parse_booking_data["data"]
    booking_data_arr.forEach(item=>{
        add_booking_item_div(item)
    })


};

function add_booking_item_div(booking_data_obj){
    let content_div = document.querySelector(".booking_item_div")
    let booking_item_div = document.createElement("div")
    booking_item_div.className = "atrraction_travel_info_div"

    let booking_item_div_img_div= document.createElement("div")
    booking_item_div_img_div.className = "img_div"
    booking_item_div_img_div.innerHTML =  `        
        <img class="attraction_travel_info_img"
            src=${booking_data_obj["attraction"]["image"]}
        alt="無法顯示照片">
        `
    booking_item_div.appendChild(booking_item_div_img_div)
    
    let travel_booking_info_div = document.createElement("div")
    travel_booking_info_div.className = "travel_booking_info_div"
    let booking_travel_title_div = document.createElement("div")
    booking_travel_title_div.className = "booking_travel_title_div"
    booking_travel_title_div.innerHTML = `
        <span class="booking_item">台北一日遊:</span>
        <span class="booking_value">${booking_data_obj["attraction"]["name"]}</span>
        `
    travel_booking_info_div.appendChild(booking_travel_title_div)

    let booking_travel_date_div = document.createElement("div")
    booking_travel_date_div.className = "booking_travel_date_div"
    booking_travel_date_div.innerHTML = `
        <span class="booking_item">日期：</span>
        <span class="booking_value">${booking_data_obj["date"]}</span>
        `
    travel_booking_info_div.appendChild(booking_travel_date_div)

    let booking_travel_time_div = document.createElement("div")
    booking_travel_time_div.className = "booking_travel_time_div"
    booking_travel_time_div.innerHTML = `
        <span class="booking_item">時間：</span>
        <span class="booking_value">${booking_data_obj["time"]}</span>
        `
    travel_booking_info_div.appendChild(booking_travel_time_div)
    
    let booking_travel_price_div = document.createElement("div")
    booking_travel_price_div.className = "booking_travel_price_div"
    let booking_price_span1 = document.createElement("span")
    booking_price_span1.className = "booking_item"
    booking_price_span1.innerText = "費用："
    let booking_price_span2 = document.createElement("span")
    booking_price_span2.className = "booking_value booking_price"
    booking_price_span2.innerText = `新台幣 ${booking_data_obj["price"]} 元`
    booking_price_span2.value = booking_data_obj["price"]
    booking_travel_price_div.appendChild(booking_price_span1)
    booking_travel_price_div.appendChild(booking_price_span2)
    travel_booking_info_div.appendChild(booking_travel_price_div)

    let booking_travel_address_div = document.createElement("div")
    booking_travel_address_div.className = "booking_travel_address_div"
    booking_travel_address_div.innerHTML = `
        <span class="booking_item">地點：</span>
        <span class="booking_value">${booking_data_obj["attraction"]["address"]}</span>
        `
    travel_booking_info_div.appendChild(booking_travel_address_div)

    let booking_item_delete_div = document.createElement("div")
    booking_item_delete_div.className = "booking_item_delete_div"
    let booking_item_delete_button = document.createElement("button")
    booking_item_delete_button.className = "booking_item_delete_button"
    booking_item_delete_button.id = booking_data_obj["booking_id"]
    booking_item_delete_button.onclick = delete_booking_item_and_reflush_page
    booking_item_delete_div.appendChild(booking_item_delete_button)
    travel_booking_info_div.appendChild(booking_item_delete_div)

    booking_item_div.appendChild(travel_booking_info_div)

    // booking_item_div.innerHTML = `
    // <div class="travel_booking_info_div">
    //     <div class="booking_item_delete_div">
    //         <button class="booking_item_delete_button" id=${booking_data_obj["booking_id"]} ></button> 
    //     </div>
    // </div>
    // `
    content_div.appendChild(booking_item_div)
}

function calculated_total_price(){
    let total_price = 0
    document.querySelectorAll(".booking_price").forEach(item=>{
        
        total_price += parseInt(item.value)
    })
    return total_price
}

function update_total_price_message(total_price){
    let total_price_parse = parseInt(total_price)
    document.querySelector(".confirm_price_span").innerText = `總價：新台幣 ${total_price_parse} 元`
}

function add_contact_and_payment_form(){
    let content_div = document.querySelector(".content")
    content_div.appendChild(document.createElement("hr")) //分隔線

    let booking_form = document.createElement("form")
    booking_form.className = "booking_form"
    booking_form.id = "booking_form"
    booking_form.action = "javascript:void(0);" //不重新整理頁面
    
    booking_form.innerHTML= `
        <div class="contact_div">
            <div class="contact_div_div booking_div">
                <p class="booking_contact_title">您的聯絡資訊</p>
                <div class="booking_contact_name_div">
                    <label class="label" for="name">聯絡姓名：</label>
                    <input class="input" type="text" id="name" placeholder="請輸入姓名" required>
                </div>
                <div class="booking_contact_email_div">
                    <label class="label" for="email">連絡信箱：</label>
                    <input class="input" type="email" id="email" placeholder="請輸入電子信箱" required>
                </div>
                <div class="booking_contact_phone_div">
                    <label class="label" for="phone">手機號碼：</label>
                    <input class="input" type="text" id="phone" minlength="10" maxlength="10" placeholder="請輸入手機號碼" required>
                </div>
                <p class="booking_contact_footer">請保持手機暢通，準時到達，導覽人員將用手機與您聯繫，務必留下正確的聯絡方式。</p>
            </div>
        </div>
        <hr>
        <div class="payment_div">
            <div class="payment_div_div">
                <p class="booking_payment_title">信用卡付款資訊</p>
                <div class="booking_payment_div">
                    <label class="label" for="card_number">卡片號碼：</label>
                    <div class="tpfield input" id="card-number"></div>
                </div>
                <div class="booking_payment_exp_date_div">
                    <label class="label" for="exp_date">過期時間：</label>
                    <div class="tpfield input" id="card-expiration-date"></div>
                </div>
                <div class="booking_payment_validation_number_div">
                    <label class="label" for="validation_number">驗證密碼：</label>
                    <div class="tpfield input" id="card-ccv"></div>

                </div>
            </div>
        </div>
        <hr>
        <div class="confirm">
            <div class="confirm_div">
                <span class="confirm_price_span"></span>
                <p class="comfirm_submit_message" id="comfirm_submit_message"></p>
                <button class="confirm_submit_button" onclick=booking_travel_submit() id=confirm_submit_button>確認訂購並付款</button>
            </div>
        </div>
    `
    content_div.appendChild(booking_form)

}

