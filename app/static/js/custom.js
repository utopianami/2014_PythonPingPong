window.addEventListener("load", function(e) {

    var idObj = {
        loginValidation: "login-form",
        signUpValidation: "signup-form",
        playerRegister: "player-register-btn",
        sendMatchInvitationToPushover: "send-invitation-pushover",
        sendMatchInvitationToRevenge: "send-invitation-revenge",
        gameResult: "game-result"
    };

    document.addEventListener("click", function(e) {
        var target = e.target;

        switch (target.id) {
            case idObj.playerRegister:
                window.location.href = "/players/signUp";
                break;
            case idObj.sendMatchInvitationToPushover:
            case idObj.sendMatchInvitationToRevenge:
                alert("아직 준비중입니다. 정식 릴리즈때 찾아뵙겠습니다.");
                break;
        }
    }, false);

    document.addEventListener("submit", function(e) {
        var target = e.target;

        switch (target.id) {
            case idObj.signUpValidation:
                e.preventDefault();
                checkSignUpValidation();
                break;
            case idObj.loginValidation:
                e.preventDefault();
                checkLoginValidation();
                break;

        }

        switch (target.className) {
            case classObj.sendMatchInvitation:
                alert("아직 준비중입니다. 정식 릴리즈때 찾아뵙겠습니다.");
                break;
        }
    }, false);

}, false);

function checkSignUpValidation() {

    var studentNo = document.getElementById("studentNo").value;
    var playerName = document.getElementById("playerName").value;
    var playerPwd = document.getElementById("playerPwd").value;
    var playerPwdRepeat = document.getElementById("playerPwdRepeat").value;

    if (playerPwd !== playerPwdRepeat) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }

    var signUpJsonData = {
        studentNo: studentNo,
        playerName: playerName,
        playerPassword: playerPwd
    };

    var formData = "studentNo=" + studentNo + "&playerName=" + playerName + "&playerPassword=" + playerPwd;

    var xhr = new XMLHttpRequest();
    var url = "/players/register";

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
          var resultString = xhr.responseText;

          switch (resultString) {
              case "INVALID_SIGNUP_DATA":
                document.querySelector("#signup-warning-text").style.display = "initial";
                break;
              case "SIGNUP_SUCCESS":
                window.location.href = "/";
                break;
          }
      }
    };

    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//    xhr.send(JSON.stringify(signUpJsonData));
    xhr.send(formData);
}

function changeOpponentResult() {

    var opponentResult = document.getElementById("opponent-result");

    if (document.querySelector(idObj.gameResult).value === "win") {
        opponentResult.innerHTML = "패배";
    } else {
        opponentResult.innerHTML = "승리";
    }
}

function checkLoginValidation() {
    var playerName = document.getElementById("loginPlayerName").value;
    var playerPwd = document.getElementById("loginPlayerPwd").value;

    if (!playerName || !playerPwd) {
        document.getElementById("loginFailText").style.display = "none";
        document.getElementById("loginFieldEmptyText").style.display = "initial";
        return;
    }

    var formData = "playerName=" + playerName + "&playerPassword=" + playerPwd;

    var xhr = new XMLHttpRequest();
    var url = "/players/login";

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var resultString = xhr.responseText;

            if (resultString === "LOGIN_FAIL") {
                document.getElementById("loginFailText").style.display = "initial";
                document.getElementById("loginFieldEmptyText").style.display = "none";

            } else {
                document.getElementById("login-form").style.display = "none";
                document.querySelector(".after_signin").style.display = "initial";
                document.getElementById("player-register-btn").style.display = "none";
                document.getElementById("href-personal-page").href = "/players/" + resultString;
            }
        }
    };

    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(formData);
}