//Username
const usernameField=document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid-feedback');
const usernameSuccessOutput=document.querySelector('.usernameSuccessOutput');

//Email
const emailField=document.querySelector('#emailField');
const emailfeedbackArea=document.querySelector('.emailinvalid-feedback');
const emailSuccessOutput=document.querySelector('.emailSuccessOutput');

//Submit button
const submitBtn=document.querySelector(".submit-btn")


//Password
const showPasswordToggle=document.querySelector('.showPasswordToggle');
const passwordField=document.querySelector('#passwordField');
handleToggleInput=(e)=>{
    if(showPasswordToggle.textContent==='SHOW'){
        showPasswordToggle.textContent='HIDE';
        passwordField.setAttribute('type','text');
    }else{
        showPasswordToggle.textContent='SHOW';
        passwordField.setAttribute('type','password');


    }
}
showPasswordToggle.addEventListener('click',handleToggleInput)

//Email Validation
emailField.addEventListener('keyup',(e)=>{
    console.log('7777',7777);
    const emailVal=e.target.value;

    emailSuccessOutput.style.display='block';
    emailSuccessOutput.textContent=`Checking ${emailVal}`;

    emailField.classList.remove('is-invalid');
    emailfeedbackArea.style.display='none';
    
    
    if(emailVal.length>0){
    fetch('/authentication/validate-email',{
        body:JSON.stringify({email:emailVal}),
        method:"POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("data",data);
        emailSuccessOutput.style.display='none';

        if(data.email_error){
            //submitBtn.setAttribute("disabled","disabled");
            submitBtn.disabled=true;
            emailField.classList.add('is-invalid');
            emailfeedbackArea.style.display='block'
            emailfeedbackArea.innerHTML=`<p>${data.email_error}</p>`
        }else{
            submitBtn.removeAttribute("disabled");
          }
    });
}
    
});






//Username
usernameField.addEventListener('keyup',(e)=>{
    console.log('7777',7777);
    const usernameVal=e.target.value;
    usernameSuccessOutput.style.display='block';

    usernameSuccessOutput.textContent=`Checking ${usernameVal}`;

    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display='none';
    
    
    if(usernameVal.length>0){
    fetch('/authentication/validate-username',{
        body:JSON.stringify({username:usernameVal}),
        method:"POST",


    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("data",data);
        usernameSuccessOutput.style.display='none';
        if(data.username_error){
            submitBtn.disabled=true;
            usernameField.classList.add('is-invalid');
            feedbackArea.style.display='block'
            feedbackArea.innerHTML=`<p>${data.username_error}</p>`
        }
        else{
            submitBtn.removeAttribute("disabled");
          
        }
    });
}
    

});
