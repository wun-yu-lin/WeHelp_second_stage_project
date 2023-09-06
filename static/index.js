const listBar = document.getElementsByClassName("list-bar")[0];
var pageIndex = 0;

get_attractions_data_and_reflush_attraction_grid();
get_mrt_data_and_reflush_mrt_navbar();


function navbar_scroll_left() {
    listBar.scrollBy({ left: -300, behavior: 'smooth' }); 
   
}

function navbar_scroll_right() {
    listBar.scrollBy({ left: 300, behavior: 'smooth' });
}


function add_attraction_card(attraction_object){
    const attraction_name = attraction_object["name"];
    const attraction_mrt = attraction_object["mrt"];
    const attraction_category = attraction_object["category"];
    const attraction_src = attraction_object["images"][0];
    const attractions_container = document.getElementsByClassName("attraction_grid")[0];
    

    const attraction_card = document.createElement("div");
    attraction_card.className = "attraction_card content_div_div";
    const attraction_card_cotent = `
        <div class="attraction_card content_div_div">
            <img class="attraction_img card-body" src=${attraction_src} alt="">
            <div class="card-body content_div_div_div div_attraction_name">
                <p class="p_attraction_name" id ="p_attraction_name">${attraction_name}</p>
            </div>
            <div class="card-body content_div_div_div div_category">
                <p class="p_mrt" id="p_mrt">${attraction_mrt}</p>
                <p class="p_category" id="p_category">${attraction_category}</p>
            </div>
        </div>
            `
    attraction_card.innerHTML = attraction_card_cotent;
    attractions_container.appendChild(attraction_card);
    
}

function mrt_button_search(){
    console.log("mrt_button_search");
}

function add_mrt_navbar(mrt_name){
    const mrt_listbar_div = document.getElementsByClassName("list-bar")[0];
    const mrt_button = document.createElement("button");
    mrt_button.className = `mrt_search_button ${mrt_name}`;
    mrt_button.onclick = mrt_button_search; //setting function
    mrt_button.textContent = mrt_name;
    mrt_button.id = mrt_name;
    mrt_listbar_div.appendChild(mrt_button);
}
    


//初次載入頁面時，取得景點資料
function get_attractions_data_and_reflush_attraction_grid() {
    const attractions_container = document.getElementsByClassName("attraction_grid")[0];
    //clean the container
    attractions_container.innerHTML = "";

    //get data from server
    currentUrl = window.location.href; 
    console.log(currentUrl);
    url = currentUrl + "api/attractions?page=" + pageIndex;
    data = fetch(url)
        .then((response)=>{
            return response.json();
        })
        .then((result)=>{
            if (result["nextPage"] != null){
                const attraction_arr =result["data"]
                attraction_arr.forEach(element => {
                    add_attraction_card(element);
                });
            }
            return result;
            
        }) 
        .catch((error)=>{
            console.log(error);
            return null;
        })

}

//初次連入頁面時，取得捷運資料
function get_mrt_data_and_reflush_mrt_navbar(){
    const mrt_navbar = document.getElementsByClassName("list-bar")[0];
    //clean the container
    mrt_navbar.innerHTML = "";

    //get url //api/mrts
    currentUrl = window.location.href;
    url = currentUrl + "api/mrts";

    //fetch data from server
    fetch(url)
        .then((response)=>{
            return response.json();
        })
        .then(result=>{
            const mrt_arr = result["data"];
            mrt_arr.forEach(element => {
                add_mrt_navbar(element);
            })
        })
        .catch(error=>{
            console.log(error);
        })

}







