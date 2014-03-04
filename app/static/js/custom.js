window.addEventListener("load", function(e) {

    var idObj = {
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
                checkPwdValidation();
                break;
        }

        switch (target.className) {
            case classObj.sendMatchInvitation:
                alert("아직 준비중입니다. 정식 릴리즈때 찾아뵙겠습니다.");
                break;
        }
    }, false);

    document.addEventListener("change", function(e) {
        var target = e.target;

        switch (target.id) {
            case idObj.gameResult:
                changeOpponentResult(target);
                break;
        }

    }, false);

}, false);

function checkPwdValidation() {

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

function changeOpponentResult(target) {

    var opponentResult = document.getElementById("opponent-result");

    if (target.value === "win") {
        opponentResult.value = "패배";
    } else {
        opponentResult.value = "승리";
    }
}
