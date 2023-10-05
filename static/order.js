// init_order()

async function init_order(){
    console.log('init_order')
    //setupSDK
    TPDirect.setupSDK(137079, 'app_fBbQkIGAcfBEmUGFmTjqT4yJUYGbBBmFO3KTvGE4AJu3S1r3wuPFfsCOkAPm', 'sandbox')
    
    //setup TPDirect
    TPDirect.card.setup({
        // Display ccv field
        fields: {
            number: {
                // css selector
                element: document.getElementById('card-number'),
                placeholder: '**** **** **** ****'
            },
            expirationDate: {
                // DOM object
                element: document.getElementById('card-expiration-date'),
                placeholder: 'MM / YY'
            },
            ccv: {
                element: document.getElementById('card-ccv'),
                placeholder: 'CCV'
            }
        },
    
        styles: {
            // Style all elements
            'input': {
                'color': 'gray',
            },
            // Styling ccv field
            'input.ccv': {
                'font-size': '16px'
            },
            // Styling expiration-date field
            'input.expiration-date': {
                'font-size': '16px'
            },
            // Styling card-number field
            'input.card-number': {
                'font-size': '16px'
            },
            // style focus state
            ':focus': {
                // 'color': 'black'
            },
            // style valid state
            '.valid': {
                'color': 'green'
            },
            // style invalid state
            '.invalid': {
                'color': 'red'
            },
            // Media queries
            // Note that these apply to the iframe, not the root window.
            '@media screen and (max-width: 400px)': {
                'input': {
                    'color': 'orange'
                }
            }
        },
        // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
        isMaskCreditCardNumber: true,
        maskCreditCardNumberRange: {
            beginIndex: 6,
            endIndex: 11
        }
    })

    //check update
    // TPDirect.card.onUpdate(function (update) {
    //     // update.canGetPrime === true
    //     // --> you can call TPDirect.card.getPrime()
    //     if (update.canGetPrime) {
    //         // Enable submit Button to get prime.
    //         // submitButton.removeAttribute('disabled')
    //         document.querySelector('#confirm_submit_button').removeAttribute('disabled')
    //     } else {
    //         // Disable submit Button to get prime.
    //         // submitButton.setAttribute('disabled', true)
    //         document.querySelector('#confirm_submit_button').setAttribute('disabled', true)
    //         console.log('update.canGetPrime === false')            
    //     }
    
    //     // // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay','unknown']
    //     // if (update.cardType === 'visa') {
    //     //     // Handle card type visa.
    //     // }
    
    //     // // number 欄位是錯誤的
    //     // if (update.status.number === 2) {
    //     //     // setNumberFormGroupToError()
    //     //     alert('信用卡資料輸入錯誤')
    //     // } else if (update.status.number === 0) {
    //     //     // setNumberFormGroupToSuccess()
    //     // } else {
    //     //     // setNumberFormGroupToNormal()
    //     // }
    
    //     // if (update.status.expiry === 2) {
    //     //     // setNumberFormGroupToError()
    //     //     alert('信用卡資料輸入錯誤')
    //     // } else if (update.status.expiry === 0) {
    //     //     // setNumberFormGroupToSuccess()

    //     // } else {
    //     //     // setNumberFormGroupToNormal()
    //     // }
    
    //     // if (update.status.ccv === 2) {
    //     //     // setNumberFormGroupToError()
    //     //     alert('信用卡資料輸入錯誤')
    //     // } else if (update.status.ccv === 0) {
    //     //     // setNumberFormGroupToSuccess()

    //     // } else {
    //     //     // setNumberFormGroupToNormal()
    //     // }
    // })
    
   

    

}




async function booking_travel_submit(){
    document.querySelector("#confirm_submit_button").disabled = true
    if (document.querySelector("#confirm_submit_button").checkValidity() == false) {
        controll_sign_message(message = "輸入錯誤格式，請重新輸入")
        document.querySelector("#confirm_submit_button").disabled = false
        return
    }
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime, 如果不行就 show error
    if (tappayStatus.canGetPrime === false) {
        alert('信用卡資料認證錯誤')
        document.querySelector("#confirm_submit_button").disabled = false
        return
    }

    //get prime
    TPDirect.card.getPrime(async (result) => {
        if (result.status !== 0) {
            alert('get prime error: ' + result.msg)
            return
        }
        let prime = result.card.prime

        let booking_id_arr = []
        document.querySelectorAll(".booking_item_delete_button").forEach(item=>{
            booking_id_arr.push(parseInt(item.id))
        })
        //prepare order data in form
        let form_data_obj = {
            "contact_name": document.getElementById("name").value,
            "contact_email": document.getElementById("email").value,
            "contact_phone": document.getElementById("phone").value,
            "amount": document.getElementById("confirm_price_span").value,
            "booking_id_arr": booking_id_arr,
        }

        //prepare attraction data arr of order
        let trip_arr = []
        document.querySelectorAll(".atrraction_travel_info_div").forEach(item=>{
            trip_arr.push({
                "attraction": {
                    "id": item.children[1].children[5].children[0].id,
                    "name": item.children[1].children[0].children[1].textContent,
                    "address": item.children[1].children[4].children[1].textContent,
                    "image": item.children[0].children[0].src
                },
                "date": item.children[1].children[1].children[1].textContent,
                "time": item.children[1].children[2].children[1].textContent,
            })
        })

        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api

        order_obj = {
            "prime": prime,
            "order": {
                "price": form_data_obj['amount'],
                "booking_id_arr": form_data_obj['booking_id_arr'],
                "trip": trip_arr,
                "contact": {
                    "name": form_data_obj['contact_name'],
                    "email": form_data_obj['contact_email'],
                    "phone": form_data_obj['contact_phone'],
                },
            }
        }

        request_para = {
            method: 'POST',
            headers:{
                "Content-Type": 'application/json',
                "Authorization": 'Bearer ' + localStorage.getItem('jwt_token')
            },
            body: JSON.stringify(order_obj),
        }


        let response =  await fetch(window.location.origin + '/api/orders', request_para)
        let response_data = await response.json()
        document.querySelector("#confirm_submit_button").disabled = false
        if (response_data['error'] == true) {
            alert("交易失敗! 請重新下訂")
        }else{
            window.location.href = window.location.origin + '/thankyou?number=' + response_data['data']['number']
        }
        

    })

   

    
}


