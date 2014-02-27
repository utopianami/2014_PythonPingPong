'#'표시는 앞으로 해야될 일

0227

	- 서버 첫 화면 index page setting : main.html
	- 회원가입
		* singin.html -> signUp.html로 변경 (회원가입은 signUp, login == siginIn)
		* signUp.html : 사용자 이름 / password 에 name생성 (서버쪽 request)
		* url등록 : 서버주소/players/signUp
		* 사용자 이름 form이 email로 되어 있어서 삭제
		# main.html에 signUp버튼 생성, 버튼을 누르면 players.signUp이 실행되도록 등록
		# 회원가입할때 비밀번호 확인하는 박스 추가

	- 점수등록
		*url등록 : 서버주소/result
		*result_register.html코드에서 나와 상대 세트스코어 적는 박스 name설정 (name="player1set") / 서버에서 전달받기 위함
		*버튼의 type를 button에서 submit으로 변경
		#이름 옵션 부분
			*서버에서 result.views.result에서 쿼리를 통해 유저 정보를 전체 전달
			*서버에서 전달받은 리스트 html에서 보여주기 : jinja사용, for
			#상대방를 선택하고, 이를 제출하면 이름이 보내주게 form구성

	- #모음
		-회원가입
			# main.html에 signUp버튼 생성, 버튼을 누르면 players.signUp이 실행되도록 등록 (TS)
			# 회원가입할때 비밀번호 확인하는 박스 추가 (TS)
		-점수등록
			#상대방를 선택하고, 이를 제출하면 이름이 보내주게 form구성(TS)
			#점수 등록여부 확인(utopia)
		-main
			#서버에서 json보내기(utopianami)
		-design(TS)
			#모바일&컴퓨터에서 보여지는 화면 정하기
			#구성 고민
			#색깔정하기



0228

    - 할일(우선순위순)
        utopianami
        *점수등록 : 서버에서 선수이름 넘길 때 dict형태로 id도 함께 전달
        *점수등록 : 서버에서 점수가 정상적으로 등록되었는지 확인
        *점수등록 : 점수등록 방식 재정리, 싱글A 감정제도 없애기 등
        *점수등록 : 리스트에서 자신은 제외
        *점수등록 : 세션으로 '나' 처리하기
        *점수등록 : 날짜넣기
        *점수등록 : 선수 rank갱신 , 메인 로딩 로직을 활용
        *메인 : 랭킹 숫자 입력

        #점수등록 후 계급 갱신
        #rank에 대한 로직 고민
        #데이터베이스 고민
        #개인페이지 : 개인페이지로 전달할 내용 정리, dict파일 만들기

        TS
        #개인페이지 만들기
        #디자인 개선

        #예외상황 확인