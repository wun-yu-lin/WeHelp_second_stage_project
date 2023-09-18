function left_sign(){
    document.querySelectorAll(".mask").forEach(element => {
        element.className = "mask non-display";
    })
    
}

function show_sign(){
    document.querySelectorAll("#signin").forEach(element => {
        element.className = "mask display";
    })
}

function change_element_to_signup(){
    document.querySelectorAll(".mask").forEach(element => {
        element.className = "mask non-display";
    })
    document.querySelectorAll("#signup").forEach(element => {
        element.className = "mask display";
    })
}

function change_element_to_login(){
    document.querySelectorAll(".mask").forEach(element => {
        element.className = "mask non-display";
    })
    document.querySelectorAll("#signin").forEach(element => {
        element.className = "mask display";
    })
}