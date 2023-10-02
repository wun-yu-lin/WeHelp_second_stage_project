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




function booking_travel_submit(){
    if (document.querySelector("#confirm_submit_button").checkValidity() == false) {
        controll_sign_message(message = "輸入錯誤格式，請重新輸入")
        return
    }
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime, 如果不行就 show error
    if (tappayStatus.canGetPrime === false) {
        alert('信用卡資料認證錯誤')
        return
    }

    //get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error: ' + result.msg)
            return
        }
        let prime = result.card.prime
        console.log(prime)

        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })

   

    
}


