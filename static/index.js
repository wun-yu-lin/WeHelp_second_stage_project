const listBar = document.getElementsByClassName("list-bar")[0];


////Gobal variable, 頁面有做更動時，務必注意變數的使用
var keyword = null; //搜尋關鍵字參數
var nextPage = undefined //網頁是否有下一頁

get_attractions_data_and_reflush_attraction_grid();
get_mrt_data_and_reflush_mrt_navbar();


let scrolldown_observer = new IntersectionObserver(async(entries, observe)=>{
    if(entries[0].isIntersecting){
        targetElement = entries[0].target;
        observe.unobserve(entries[0].target);
        //add more atrraction card
        if (keyword == null ){
            url = `${currentUrl}/api/attractions?page=${nextPage}`
        }else{
            url = `${currentUrl}/api/attractions?page=${nextPage}&keyword=${keyword}`
        }
        

        if (nextPage !== undefined && nextPage !== null){
            
            data = await fetch(url)
            .then((response)=>{
                return response.json();
            })
            .then((result)=>{
                const attraction_arr =result["data"]
                if (attraction_arr !== undefined){
                    attraction_arr.forEach(element => {
                        add_attraction_card(element);
                    });
                   }
                nextPage = result["nextPage"];
                return result;
            }) 
            .catch((error)=>{
                console.log(error);
            });
       }
       observe.observe(targetElement);
       
    }

    })
scrolldown_observer.observe(document.querySelector(".footer"));


function navbar_scroll_left() {
    listBar.scrollBy({ left: -200, behavior: 'smooth' }); 
   
}

function navbar_scroll_right() {
    listBar.scrollBy({ left: 200, behavior: 'smooth' });
}


function add_attraction_card(attraction_object){
    const attraction_name = attraction_object["name"];
    const attraction_mrt = attraction_object["mrt"];
    const attraction_category = attraction_object["category"];
    const attraction_src = attraction_object["images"][0];
    const attractions_container = document.getElementsByClassName("attraction_grid")[0];
    const attraction_id = attraction_object["id"];
    

    const attraction_card = document.createElement("div");
    attraction_card.className = "attraction_card content_div_div";
    attraction_card.onclick = redirect_to_attraction_id_page;
    attraction_card.id = attraction_id;
    const attraction_card_cotent = `
            <img class="attraction_img card-body" src=${attraction_src} alt="" id=${attraction_id}>
            <div class="card-body content_div_div_div div_attraction_name" id=${attraction_id}>
                <p class="p_attraction_name" id =${attraction_id}>${attraction_name}</p>
            </div>
            <div class="card-body content_div_div_div div_category" id=${attraction_id}>
                <p class="p_mrt" id=${attraction_id}>${attraction_mrt}</p>
                <p class="p_category" id=${attraction_id}>${attraction_category}</p>
            </div>

            `
    attraction_card.innerHTML = attraction_card_cotent;
    attractions_container.appendChild(attraction_card);
    
}

//nav-bar 按下去後觸發, 可以按照mrt來搜尋台北景點
function mrt_button_search(event){
    const mrt_name = event.target.id;
    const search_input_element = document.getElementsByClassName("search_input")[0];
    search_input_element.value = mrt_name;
    search_keyword_reflush_attraction_card();
    
    
}

// 從search bar取得關鍵字，並且搜尋景點, 
function search_keyword_reflush_attraction_card(){
    const search_input_element = document.getElementsByClassName("search_input")[0];
    const search_keyword = search_input_element.value;

    if (search_keyword == undefined || search_keyword == ""){
        console.log("search_keyword is empty");
        return;
    }
    //clean the container
    const attractions_container = document.getElementsByClassName("attraction_grid")[0];
    attractions_container.innerHTML = "";
    nextPage = 0;
    
    //settign url
    const currentUrl = window.location.href;
    const url = `${currentUrl}/api/attractions?page=0&keyword=${search_keyword}`;

    //get data from server
    data = fetch(url)
            .then((response)=>{
                return response.json();
            })
            .then((result)=>{
                const attraction_arr =result["data"]
                attraction_arr.forEach(element => {
                    add_attraction_card(element);
                });
                nextPage = result["nextPage"];
                return result;
            }) 
            .catch((error)=>{
                console.log(error);
            });

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
    url = currentUrl + "api/attractions?page=0"
    data = fetch(url)
        .then((response)=>{
            return response.json();
        })
        .then((result)=>{

            const attraction_arr =result["data"]
            attraction_arr.forEach(element => {
                add_attraction_card(element);
            });
            nextPage = result["nextPage"];
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

function redirect_to_attraction_id_page(event){
    let attraction_id = event.target.id;
    let currentUrl = window.location.href;
    let redirect_url = `${currentUrl}attraction/${attraction_id}`;
    window.location.href = redirect_url;
}






