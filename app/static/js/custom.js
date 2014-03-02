window.addEventListener("load", function(e) {

    var idObj = {
        signUpValidation: "signup-form",
        playerRegister: "player-register-btn"
    };

    var classObj = {
        sendMatchInvitation: "send-match-invitation"
    };

    document.addEventListener("click", function(e) {
        var target = e.target;

        switch (target.id) {
            case idObj.playerRegister:
                window.location.href = "/players/signUp";
                break;
        }
    }, false);

    document.addEventListener("submit", function(e) {
        var target = e.target;

        switch (target.id) {
            case idObj.signUpValidation:
                e.preventDefault();
                if(checkPwdValidation() === true) {
                    target.submit();
                }
                break;
        }

        switch (target.class) {
            case classObj.sendMatchInvitation:
                alert("아직 준비중입니다. 정식 릴리즈때 찾아뵙겠습니다.");
                break;
        }
    }, false);

}, false);

function checkPwdValidation() {

    var playerPwd = document.getElementById("playerPwd").value;
    var playerPwdRepeat = document.getElementById("playerPwdRepeat").value;

    if (playerPwd === playerPwdRepeat) {
        return true;
    } else {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }
}

