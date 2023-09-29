
//page init 
init();


function init() {
    check_user_login_status_control_element();
}


async function check_user_login_status_control_element() {
    if (localStorage.getItem("jwt_token") == null) {
        document.querySelectorAll("#header_div_div_li_sign").forEach(element => {
            element.className = "header_div_div_li flex";
        })
        document.querySelectorAll("header_div_div_li_logout").forEach(element => {
            element.className = "header_div_div_li flex non-display";
        })
    }

    if (localStorage.getItem("jwt_token") != null || parseData["error"] != true) {
        let request_obj = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("jwt_token")}`
            }
        }

        try {
            fetch_data = await fetch("/api/user/auth", request_obj)
            parseData = await fetch_data.json()
            if (parseData == null) {
                localStorage.removeItem("jwt_token");
                window.location.reload()
            } else {
                //修改成登入狀態
                document.querySelectorAll("#header_div_div_li_sign").forEach(element => {
                    element.className = "header_div_div_li flex non-display";
                })
                document.querySelectorAll("#header_div_div_li_logout").forEach(element => {
                    element.className = "header_div_div_li flex";
                })
            }


        } catch (err) {
            console.log("login failed")
            console.log(err)

        }



    }



};

async function login_account() {
    //check form input
    if (document.querySelector("#signin_form").checkValidity() == false) {
        controll_sign_message(message = "輸入錯誤格式，請重新登入")
        return
    }



    let data = {
        "email": document.querySelector("#user_account_signin").value,
        "password": document.querySelector("#user_password_signin").value
    }

    //fetch and check account and password
    request_obj = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    try {
        fetch_data = await fetch("/api/user/auth", request_obj)
        parseData = await fetch_data.json()


    } catch (err) {
        console.log("login failed")
        console.log(err)
        controll_sign_message(message = "登入失敗，請重新登入")
        // window.location.reload()
    }


    // console.log(parseData)
    //check login status
    if (parseData["error"] == true) {
        console.log("login failed")
        controll_sign_message(message = "登入失敗，請重新登入")
        // setTimeout(function(){
        //     window.location.reload()
        // }, 1000)
    }

    //login sucessfully save token
    if (parseData["error"] != true) {
        localStorage.setItem("jwt_token", parseData["token"])
        controll_sign_message(message = "登入成功")
        setTimeout(function () {
            window.location.reload()
        }, 1000)
    }




}
async function signup_account() {
    //check form input
    if (document.querySelector("#signup_form").checkValidity() == false) {
        controll_sign_message(message = "輸入錯誤格式，請重新註冊")
        return
    }

    let data = {
        "name": document.querySelector("#user_username_signup").value,
        "email": document.querySelector("#user_account_singup").value,
        "password": document.querySelector("#user_password_signup").value
    }

    //fetch and check account and password
    let request_obj = {
        method: "post",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    try {
        fetch_data = await fetch("/api/user/", request_obj)
        parseData = await fetch_data.json()

    } catch (err) {
        console.log("signup failed")
        console.log(err)
    }


    //check signup status
    if (parseData["error"] == true) {
        console.log("signup failed")
        controll_sign_message(message = parseData["message"])
        // setTimeout(function(){
        //     window.location.reload()
        // }, 1000)

    }

    //if scucessfully signup
    if (parseData["ok"] == true) {
        controll_sign_message(message = "註冊成功")
        //auth account and get token
        //fetch and check account and password
        let obj = {
            "email": data["email"],
            "password": data["password"]
        }
        let request_obj = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(obj)
        }
        try {
            fetch_data = await fetch("/api/user/auth", request_obj)
            parseData = await fetch_data.json()

        } catch (err) {
            console.log("login failed")
            console.log(err)
            window.location.reload()
        }

        localStorage.setItem("jwt_token", parseData["token"])

        setTimeout(function () {
            window.location.reload()
        }, 1000)
    }
}

function left_sign() {
    document.querySelectorAll(".mask").forEach(element => {
        element.className = "mask non-display";
    })

}

function show_sign() {
    document.querySelectorAll("#signin").forEach(element => {
        element.className = "mask display";
    })
    controll_sign_message(message = "")
}

function change_element_to_signup() {
    controll_sign_message(message = "")
    document.querySelectorAll(".mask").forEach(element => {
        element.className = "mask non-display";
    })
    document.querySelectorAll("#signup").forEach(element => {
        element.className = "mask display";
    })
}

function change_element_to_login() {
    controll_sign_message(message = "")
    document.querySelectorAll(".mask").forEach(element => {
        element.className = "mask non-display";
    })
    document.querySelectorAll("#signin").forEach(element => {
        element.className = "mask display";
    })
}

function logout_account() {
    localStorage.removeItem("jwt_token")
    window.location.reload()
}

function controll_sign_message(message) {
    document.querySelectorAll("#sign_message").forEach(element => {
        element.innerText = "";
        setTimeout(function () {
            element.innerText = message;
        }, 153)
    })

}


function redirect_booking_and_check_signin() {

    try {
        let jwt_token = localStorage.getItem("jwt_token")
        if (jwt_token == null) {
            show_sign()
            return
        }

 
        window.location.href = window.location.origin + "/booking"


    } catch (err) {
        console.log(err)
    }
}