window.addEventListener("load", function(e) {

    var idObj = {
        loginValidation: "login-form",
        signUpValidation: "signup-form",
        playerRegister: "player-register-btn",
        sendMatchInvitationToPushover: "send-invitation-pushover",
        sendMatchInvitationToRevenge: "send-invitation-revenge",
        gameResult: "game-result",
        unregisteredResultOk: "unregistered-result-ok",
        unregisteredResultCancel: "unregistered-result-cancel",
        resultSave: "result-register-form"
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
            case idObj.unregisteredResultOk:
                manageResult(target.parentNode.parentNode.id, false);
                break;
            case idObj.unregisteredResultCancel:
                manageResult(target.parentNode.parentNode.id, true);
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
            case idObj.resultSave:
                e.preventDefault();
                if (resultCheck(target) === true) {
                    target.submit();
                }

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
                window.location.href = "/";
            }
        }
    };

    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(formData);
}

function manageResult(rowId, isCancel) {
    var xhr = new XMLHttpRequest();
    var url = "/result/verify";

    var resultId = rowId.split("-")[2];
    var formData = "result_id=" + resultId;

    if (isCancel === false) {
        formData += "&status=1";
    } else {
        formData += "&status=2";
    }

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var resultString = xhr.responseText;

            if (resultString === "IS_VERIFIED") {
                window.location.href = "/";
//                var unregisteredResultTable = document.getElementById("unregistered-result");
//                var numOfUnregisteredResult = unregisteredResultTable.getAttribute("data-row-num");
//                debugger;
//                if (numOfUnregisteredResult === 1) {
//                    unregisteredResultTable.style.display = "none";
//                    return;
//                }
//
//                unregisteredResultTable.setAttribute("data-row-num", numOfUnregisteredResult - 1);
//                var targetRow = document.getElementById(rowId);
//                targetRow.style.display = "none";
            } else {
                alert("오류가 발생했습니다. 다시 접속해주세요.")
            }

        }
    };

    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(formData);
}

function resultCheck(target) {
    if (document.getElementById("opponent-name").value === "") {
        alert("상대가 없습니다.");
        return false;
    }

    return true;
}