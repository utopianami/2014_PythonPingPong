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