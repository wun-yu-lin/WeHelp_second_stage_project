
let orderNumber_str = window.location.href.split('?number=')[1];
main();





async function main() {
    getOrder_data_by_ordernNumber(orderNumber_str);

    
}


async function getOrder_data_by_ordernNumber(orderNumber_str) {

    let request_para = {
        methods: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + localStorage.getItem('jwt_token')
        }
    }
    let url_search_para = new URLSearchParams({
        number: orderNumber_str,
    });
    let response = await fetch('/api/order/?'+url_search_para , request_para);
    let data = await response.json();
    console.log(data);
    if(data["data"]==null){
        document.getElementById("order_price_item_span").textContent = "訂單編號：查無此訂單";
       return;
    }

    document.getElementById("order_price_item_span").textContent = `訂單編號：${data["data"]["number"]}`;
    document.getElementById("order_price_value_span").textContent = `新台幣 ${data["data"]["price"]} 元`;

    if(data["data"]["status"]=="0"){
        document.getElementById("order_status_value_span").textContent = "已付款";
    }
    if(data["data"]["status"]=="1"){
        document.getElementById("order_status_value_span").textContent = "未付款";
    }
    if(data["data"]["status"]=="2"){
        document.getElementById("order_status_value_span").textContent = "交易失敗";
    }

    document.getElementById("order_contact_name_span").textContent = `聯絡姓名：${data["data"]["contact"]["name"]}`;
    document.getElementById("order_contact_email_span").textContent = `聯絡信箱：${data["data"]["contact"]["email"]}`;
    document.getElementById("order_contact_phone_span").textContent = `聯絡電話：${data["data"]["contact"]["phone"]}`;


    //add attraction item into order_div
    let order_div = document.querySelector("#order_div");
    data["data"]["trip"].forEach(element => {
        let order_attraction_item_div = document.createElement("div");
        order_attraction_item_div.className = "order_attraction_item_div";
        order_attraction_item_div.innerHTML = `
            <div class="order_attraction_item_div">
                <span class="order_attraction_name_span" id="order_attraction_name_span">旅遊景點：${element["attraction"]["name"]}</span>
                <span class="order_attraction_date_span" id="order_attraction_date_span">旅遊日期：${element["date"]}</span>
                <span class="order_attraction_time_span" id="order_attraction_time_span">旅遊時間：${element["time"]}</span>
            </div>
        
            `
        order_div.appendChild(order_attraction_item_div);
    });


};
