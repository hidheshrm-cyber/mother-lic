document
.getElementById("loginForm")
.addEventListener("submit", function(e){

    e.preventDefault();

    let user =
    document.getElementById("username").value;

    let pass =
    document.getElementById("password").value;

    let mother =
    document.getElementById("mother");

    let son =
    document.getElementById("son");

    let msg =
    document.getElementById("message");

    if(
        user === "lic123"
        &&
        pass === "lic123"
    ){

        msg.innerHTML =
        "✅ Login Successful";

        msg.className =
        "success";

        mother.classList.add(
            "hug-left"
        );

        son.classList.add(
            "hug-right"
        );

        mother.innerHTML =
        "🤗";

        son.innerHTML =
        "🤗";

        setTimeout(function(){

            window.location =
            "/dashboard";

        },2000);

    }
    else{

        msg.innerHTML =
        "❌ Wrong Username or Password";

        msg.className =
        "error";

        mother.classList.add(
            "shake"
        );

        son.classList.add(
            "shake"
        );

        setTimeout(function(){

            mother.classList.remove(
                "shake"
            );

            son.classList.remove(
                "shake"
            );

        },1500);
    }
});