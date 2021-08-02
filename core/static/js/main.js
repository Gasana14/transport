const tabAuth1 = document.getElementById('login_admin');
const tabAuth2 = document.getElementById('authenticate_client');
const tabAuth3 = document.getElementById('authenticate_driver');


const tabOneAuthButton = document.getElementById('adminTabButton')
const tabTwoAuthButton = document.getElementById('clientTabButton')
const tabThreeAuthButton = document.getElementById('driverTabButton')




tabAuth1.hidden = false
tabAuth2.hidden = true
tabAuth3.hidden = true

const activateTab1Auth =()=>{
    // console.log("Rwanda")
    tabAuth1.hidden = false
    tabOneAuthButton.classList.add('auth_nav_list_active')
    tabAuth2.hidden = true
    tabTwoAuthButton.classList.remove('auth_nav_list_active')
    tabAuth3.hidden = true
    tabThreeAuthButton.classList.remove('auth_nav_list_active')
}


const activateTab2Auth =()=>{
    tabAuth1.hidden = true
    tabOneAuthButton.classList.remove('auth_nav_list_active')
    tabAuth2.hidden = false
    tabTwoAuthButton.classList.add('auth_nav_list_active')
    tabAuth3.hidden = true
    tabThreeAuthButton.classList.remove('auth_nav_list_active')
}

const activateTab3Auth =()=>{
    tabAuth1.hidden = true
    tabOneAuthButton.classList.remove('auth_nav_list_active')
    tabAuth2.hidden = true
    tabTwoAuthButton.classList.remove('auth_nav_list_active')
    tabAuth3.hidden = false
    tabThreeAuthButton.classList.add('auth_nav_list_active')
}

tabOneAuthButton.addEventListener('click', activateTab1Auth);
tabTwoAuthButton.addEventListener('click', activateTab2Auth);
tabThreeAuthButton.addEventListener('click', activateTab3Auth);


// ----------------------------------------------------
// ----------------------------------------------------
// The register login stwisting 
// ----------------------------------------------------
// ----------------------------------------------------


const client_login_form = document.getElementById('customer_login_form')
const client_register_form = document.getElementById('customer_register_form') 
const client_register_button = document.getElementById('customer_register_button')
const client_login_button = document.getElementById('customer_login_button')

client_login_form.style.display = 'block'
client_register_form.style.display = 'none'


client_register_button.addEventListener('click',()=>{
    client_login_form.style.display = 'none'
    client_register_form.style.display = 'block'
})

client_login_button.addEventListener('click', ()=>{
    client_login_form.style.display = 'block'
    client_register_form.style.display = 'none'
})



const driver_register_button = document.getElementById('driver_register_button')
const driver_login_button = document.getElementById('driver_login_button')
const driver_login_form = document.getElementById('driver_login_form')
const driver_register_form = document.getElementById('driver_register_form')

driver_login_form.style.display = 'block'
driver_register_form.style.display = 'none'

driver_register_button.addEventListener('click', ()=>{
    driver_login_form.style.display = 'none'
    driver_register_form.style.display = 'block'
})

driver_login_button.addEventListener('click',()=>{
    driver_login_form.style.display = 'block'
    driver_register_form.style.display = 'none' 
})


// navigate profile modal

const profile_tab = document.getElementById('change_profile')
const logout_tab = document.getElementById('logout_form')
const profile_tab_button = document.getElementById('profile_button_nav')
const logout_tab_button = document.getElementById('logout_button_nav')

profile_tab.style.display = 'block'
logout_tab.style.display = 'none'

profile_tab_button.addEventListener('click', ()=>{
    profile_tab.style.display = 'block'
    logout_tab.style.display = 'none'
    profile_tab_button.classList.add('auth_nav_list_active')
    logout_tab_button.classList.remove('auth_nav_list_active')
})

logout_tab_button.addEventListener('click', ()=>{
    profile_tab.style.display = 'none'
    logout_tab.style.display = 'block'
    logout_tab_button.classList.add('auth_nav_list_active')
    profile_tab_button.classList.remove('auth_nav_list_active')
})






