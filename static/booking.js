
init()

function init() {
    check_signin()
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