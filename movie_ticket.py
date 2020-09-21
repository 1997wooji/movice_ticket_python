#파이썬 클래스 쓰는법 공부하기 O
#파이썬 파일 입출력 공부하기 O
#파이썬에서 이미지 불러오는 모듈 공부하기 X
#코드 설명 및 어떻게 작동하는지 PPT 작성해서 제출 (d드라이브에 file 넣어달라고 꼭 말해야함!)

'''
import, 전역 변수들 선언 부분
실제 메인 코드는 맨 밑에 있다.
'''

import time
import msvcrt
import os

lastMovieId=15 

tomMovies = [] #내일 상영 영화들(07-10)
afTomMovies = [] #모레 상영 영화들(07-11)
reserveInfos = [] #영화 예매 정보를 모두 담고있는 배열

seatsInfo = {} #영화들 좌석 정보 key=movieId, value=Seats


'''
영화 클래스
'''
class Movie : 
    movieId = None #영화 고유 번호
    name = None #영화 이름
    date = None #영화 상영 날짜
    time = None #영화 시작 시간
    screen = None #영화 상영관 번호
    imageId = None #영화 이미지 번호

    def __init__(self, movieId, name, date, time, screen, imageId) : 
        self.movieId=movieId
        self.name=name
        self.date=date
        self.time=time
        self.screen=screen
        self.imageId=imageId

'''
예매 클래스 
'''
class Reservation : 
    movieId = None #어떤 영화인지
    reserveId = None #예매 번호
    reservePw = None #예매 비밀번호
    seats = None #예매 좌석

    def __init__(self, reserveId, movieId, reservePw, seats) : 
        self.movieId=movieId
        self.reserveId=reserveId
        self.reservePw=reservePw
        self.seats=seats


'''
좌석 클래스
'''
class Seats : 
    movieId = None
    num=0 #48좌석중 0개 채워짐
    matrix=[[0]*10 for i in range (5)] #5*10 2차원배열

    def __init__(self, movieId) :
        self.movieId=movieId

# 프로그램 초기화
'''
파일에서 영화, 좌석, 예매 정보를 읽어와 프로그램에 저장하는 역할을 하는 함수
'''
def initMovieInfo() :
    
    #영화 정보 update
    fp = open("d://movieinfo.txt")
        
    while 1 :

        line=fp.readline()
        if len(line)==0 : 
            break
    
        arr=line.split('/')

        if arr[2]=="2019-07-10" : # 내일 상영 영화들(07-10)
            newMovie = Movie(int(arr[0]), arr[1], arr[2], arr[3], int(arr[4]), int(arr[5]))
            tomMovies.append(newMovie)
        else : #모레 상영 영화들(07-11)
            newMovie = Movie(int(arr[0]), arr[1], arr[2], arr[3], int(arr[4]), int(arr[5]))
            afTomMovies.append(newMovie)
    
    fp.close()

    #좌석 정보 update
    fp = open("d://seatinfo.txt")
    while 1 :

        line=fp.readline()
        if len(line)==0 : 
            break

        movieId=int(line)
        seats=Seats(movieId)
        
        line=fp.readline()
        seats.num=int(line)

        matrix=[[0]*10 for i in range(5)]
        for i in range(5) : 
            line=fp.readline()
            arr=line.split(' ')
            for j in range(10) : 
                matrix[i][j]=int(arr[j])
        seats.matrix=matrix
        #아니 왜 seats.matrix[i][j]=int(arr[j])하면 안됨?? 이해가 안되네?!!
        seatsInfo[movieId]=seats

    fp.close()

    #예매 정보 update
    fp = open("d://reserveinfo.txt")

    while 1 :
    
        line=fp.readline()
        if len(line)==0 : 
            break
    
        arr=line.split('/')
        reservation=Reservation(arr[0],int(arr[1]),arr[2],arr[3])
        reserveInfos.append(reservation)
    fp.close()

    return 0


'''
로그인하는 함수, 관리자인지 예매자인지 확인하기 위함임
admin Id, Pw는 각각 admin, abcd
guest Id, Pw는 각각 guest, 1234이다.
return : 관리자일 경우 0, 예매자일 경우 1, 잘못된 정보가 들어온 경우 -1을 리턴함
'''
def login() : 
    guestId = "guest"
    guestPw = "1234"
    adminId = "admin"
    adminPw = "abcd"

    print("어서오세요, DongGu Cinema입니다. 저희 서비스를 이용하시려면 로그인이 필요합니다.\n")
    memberId = input("* 아이디를 입력하세요 : ")
    memberPw = input("* 비밀번호를 입력하세요 : ")

    if memberId==adminId and memberPw==adminPw :
        return 0
    elif memberId==guestId and memberPw==guestPw :
        return 1
    else : 
        return -1


'''
관리자용 메뉴를 보여주는 함수
'''
def adminMode() :
    
    while 1 : 
        os.system('cls')

        print("1. 영화 추가")
        print("2. 영화 삭제")
        print("3. 영화 전체 조회")
        print("4. 영화 예매 전체 조회")
        print("ESC를 누르면 밖으로 나갑니다.")

        key=ord(msvcrt.getch())

        if key == 27 : #ESC
            break
        elif key == 49 : #1
            addMovie()
        elif key == 50 : #2
            deleteMovie()
        elif key == 51 : #3
            totalMovies()
        elif key == 52 : #4
            totalReservations()

    return 0

# 관리자용 함수
'''
영화를 추가하는 함수
'''
def addMovie() : 
    os.system('cls')

    global lastMovieId #전역 변수 호출 방법
    name=input("영화 제목을 입력하세요 : ")
    date=input("영화 상영 날짜를 입력하세요 (2019-07-10, 2019-07-11 중 하나만 입력 가능) : ")
    time=input("영화 상영 시작 시간을 입력하세요 (hh:mm) : ")
    screen=int(input("상영관을 입력하세요 (숫자, ex : 1) : "))
    imageId=0 #나중에 image 하게될때 입력

    if date=="2019-07-10" :
        tomMovies.append(Movie(lastMovieId,name,date,time,screen,imageId))
    else : 
        afTomMovies.append(Movie(lastMovieId,name,date,time,screen,imageId))
    
    seatsInfo[lastMovieId]=Seats(lastMovieId)
    lastMovieId+=1

    print()
    print("영화 추가가 성공적으로 이루어졌습니다!")
    print("ESC를 누르면 밖으로 나갑니다.")

    while 1 :
        key=ord(msvcrt.getch())

        if key == 27 : #ESC
            break
    return 0

'''
영화를 삭제하는 함수
'''
def deleteMovie() : 
    os.system('cls')

    global lastMovieId 
    movieId=int(input("삭제할 영화 번호를 입력하세요 : "))
    movie=searchMovie(movieId)

    if movie != -1 :
        if movie.date=="2019-07-10" :
            tomMovies.remove(movie)
        else : 
            afTomMovies.remove(movie)
        del seatsInfo[movieId]
    else : #-1인 경우
        print("해당 영화를 찾을 수 없습니다. 3초 뒤 이전 화면으로 돌아갑니다.")
        time.sleep(3)
        return 0
    
    print()
    print("영화 삭제가 성공적으로 이루어졌습니다!")
    print("ESC를 누르면 밖으로 나갑니다.")

    while 1 :
        key=ord(msvcrt.getch())

        if key == 27 : #ESC
            break
    return 0

'''
모든 영화 정보를 볼 수 있는 함수
'''
def totalMovies() : 
    os.system('cls')
    print("2019-07-10 : ")
    print()
    for movie in tomMovies :
        printMovieInfo(movie)
    print()
    print()
    print("2019-07-11 : ")
    print()
    for movie in afTomMovies : 
        printMovieInfo(movie)
    print()
    print("ESC를 누르면 밖으로 나갑니다.")

    while 1 :
        key=ord(msvcrt.getch())

        if key == 27 : #ESC
            break

    return 0

'''
모든 예매 정보를 볼 수 있는 함수 (관리자용으로 보인다)
'''
def totalReservations() : 
    os.system('cls')
    print("** 예매 정보 **")
    print()
    print("%10s %10s %15s %10s" %("예매 번호", "영화 번호", "예매비밀번호", "좌석"))
    print("-----------------------------------------------------------------------------")
    for reserveInfo in reserveInfos : 
        print("%10s %10s %15s %10s" %(reserveInfo.reserveId,reserveInfo.movieId, reserveInfo.reservePw, reserveInfo.seats))
    
    print()
    print("ESC를 누르면 밖으로 나갑니다.")

    while 1 :
        key=ord(msvcrt.getch())

        if key == 27 : #ESC
            break
    return 0

# 예매자용 함수
'''
예매자용 메뉴를 보여주는 함수
'''
def guestMode() : 

    while 1 : 
        os.system('cls')

        print("1. 영화 예매")
        print("2. 예매 정보 조회")
        print("3. 예매 취소")
        print("ESC를 누르면 밖으로 나갑니다.")

        key=ord(msvcrt.getch())

        if key == 27 : #ESC
            break
        elif key == 49 : #1
            printCinemaInfo("2019-07-10")
        elif key == 50 : #2
            lookReservation()
        elif key == 51 : #3
            cancelReservation()

    return 0

'''
영화관 상영 영화 정보를 보여주는 함수
'''
def printCinemaInfo(date) :

    while 1 :
        os.system('cls')

        print("상영 날짜 : %s" %date)
        print("뒤로 가려면 ESC, 다음 날짜를 보려면 d, 이전 날짜를 보려면 왼쪽 화살표 a를 눌러주세요.")
        print()

        if date=="2019-07-10" :
            for movie in tomMovies : 
                printMovieInfo(movie)
        elif date=="2019-07-11" : 
            for movie in afTomMovies : 
                printMovieInfo(movie)

        print("영화 번호를 잘 기억해 주세요. 예매를 하시려면 1번키를 눌러주세요.")

        key=ord(msvcrt.getch())

        if key == 27 : #ESC
            break
        elif key == 100 : 
            date="2019-07-11"
        elif key == 97 : #왼쪽
            date="2019-07-10"
        elif key == 49 : #1
            reserveTicket()
            break
            
    return 0

'''
Movie 정보를 보여주는 함수
'''
def printMovieInfo(movie) :
    print("영화 번호 (%s) %s" %(movie.movieId, movie.name))
    print("상영관 : %s관" %movie.screen)
    print("상영 날짜 : %s" %movie.date)
    print("상영 시작 시간 : %s" %movie.time)
    print("예매된 좌석 : %s/48" %seatsInfo[movie.movieId].num)
    print()
    return 0

'''
좌석을 보여주는 함수.
'''
def printSeatsInfo(movieId) :
    matrix=seatsInfo[movieId].matrix
    print("■ - 예매 가능, ▨ - 예매 불가능")
    print("\t\t","screen")
    print("---------------------------------------------")
    print("%3s%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d" %(" ",1,2,3,4,5,6,7,8,9,10))

    for i in range(5) : 
        #A=65
        print("%3s" %chr(65+i),end="")
        for j in range(10) : 
            if matrix[i][j]==0 : 
                print("%3s" %"■",end="")
            elif matrix[i][j]==1 : 
                print("%3s" %"▨",end="")
            else : 
                print("%3s" %" ", end="")
        print()



'''
예매 하는 함수
'''
def reserveTicket() : 

    os.system('cls')

    movieId=int(input("영화 번호를 입력하세요 : "))
    print()
    print(" ** 좌석 정보 ** ")
    print()

    printSeatsInfo(movieId)

    print()
    num=int(input("예매할 인원수를 입력하세요 : "))
    line=input("인원수에 맞게 좌석을 선택해주십시오 A-3,B-4,C-10 이런식으로 입력해 주십시오. : ")
    arr=line.split(",")

    for i in range(num) : 
        semi=arr[i].split("-")
        if isReserved(movieId, semi[0], int(semi[1]))==False : 
            print("이미 예약된 좌석을 선택하셨습니다. 다시 시도해 주세요. 3초 뒤 이전 화면으로 돌아갑니다.")
            time.sleep(3)
            return 0
    
    for i in range(num) : 
        semi=arr[i].split("-")
        checkReserve(movieId,semi[0],int(semi[1]))

    # 예매 내역 저장
    pw=input("예매 비밀번호를 입력해 주세요. 삭제시 사용됩니다 : ")
    number=str(time.time())
    reserveNum=number.split(".")
    reserveInfos.append(Reservation(reserveNum[0],movieId,pw,line))
    print()
    print("예약에 성공하셨습니다!")
    print("예매번호는 %s 입니다! *^^*" %reserveNum[0])
    print()
    print("ESC를 누르면 이전 화면으로 돌아갑니다.")

    while 1 : 
        key=ord(msvcrt.getch())
        if key == 27 : #ESC
            return 0
    

'''
이미 그 좌석이 예매되었는지 확인하는 함수
'''
def isReserved(movieId,character,y) : 
    matrix=seatsInfo[movieId].matrix
    x=ord(character)-65 #A=65
    if matrix[x][y-1] == 0 : 
        return True
    else : 
        return False

'''
좌석에 표시하는 함수
'''
def checkReserve(movieId, character,y) : 
    x=ord(character)-65 #A=65
    seatsInfo[movieId].matrix[x][y-1]=1 #표시
    seatsInfo[movieId].num +=1 #인원수 하나 늘림
    return 0

'''
좌석표시를 없애는 함수
'''
def uncheckReserve(movieId, character, y) : 
    x=ord(character)-65
    seatsInfo[movieId].matrix[x][y-1]=0 #0표시
    seatsInfo[movieId].num -=1 #인원수 하나 줄임

'''
예매 정보 조회 함수
'''
def lookReservation() : 
    os.system('cls')
    print("** 예매 정보 조회 **")
    reserveId=input("예매 번호를 입력하세요 : ")
    print()

    for reserveInfo in reserveInfos : 
        if reserveInfo.reserveId==reserveId : 
            movie = searchMovie(reserveInfo.movieId)
            print(" ** 예매 조회 결과입니다. **")
            printMovieInfo(movie)
            print("예매 번호 : %s" %reserveInfo.reserveId)
            print("예매 좌석 : %s" %reserveInfo.seats)

            print("ESC를 누르면 이전 화면으로 돌아갑니다.")

            while 1 : 
                key=ord(msvcrt.getch())
                if key == 27 : #ESC
                    return 0
    
    print("죄송합니다. 고객님 예매 번호와 일치하는 예매 정보를 조회할 수 없습니다.")
    print("3초뒤 이전 화면으로 돌아갑니다.")
    time.sleep(3)
    return 0

'''
예매 취소 함수
'''
def cancelReservation() : 
    os.system('cls')
    print("** 예매 취소 **")
    reserveId=input("예매 번호를 입력하세요 : ")
    reservePw=input("예매 비밀번호를 입력하세요 : ")
    print()

    for reserveInfo in reserveInfos : 
        if reserveInfo.reserveId==reserveId and reserveInfo.reservePw==reservePw : 
            movie = searchMovie(reserveInfo.movieId)
            printMovieInfo(movie)
            print("예매 번호 : %s" %reserveInfo.reserveId)
            print("예매 비밀 번호 : %s" %reserveInfo.reservePw)
            print("예매 좌석 : %s" %reserveInfo.seats)

            print("해당 예매 취소 중...")
            time.sleep(1.5)
            arr=reserveInfo.seats.split(",")
            for a in arr : 
                semi=a.split("-")
                uncheckReserve(reserveInfo.movieId, semi[0], int(semi[1]))
            reserveInfos.remove(reserveInfo)
            print()
            print("예매 취소가 완료되었습니다!")
            print("ESC를 누르면 이전 화면으로 돌아갑니다.")

            while 1 : 
                key=ord(msvcrt.getch())
                if key == 27 : #ESC
                    return 0
    
    print("죄송합니다. 고객님 예매 번호와 일치하는 예매 정보를 조회할 수 없습니다.")
    print("3초뒤 이전 화면으로 돌아갑니다.")
    time.sleep(3)
    return 0

'''
영화 Id로 영화를 찾아주는 함수
'''
def searchMovie(movieId) : 
    for movie in tomMovies : 
        if movie.movieId==movieId : 
            return movie
    
    for movie in afTomMovies : 
        if movie.movieId==movieId : 
            return movie
    
    return -1

'''
영화관 예매 프로그램 :

admin(관리자) 모드와 guest(예매자) 모드가 있다.
로그인에 성공해야만 각각의 모드로 들어갈 수 있으며, 로그인에 실패시 프로그램이 꺼지게 된다.

관리자의 경우 id=admin, pw=abcd이며,
예매자의 경우 id=guest, pw=1234이다.
로그인에 실패하면 바로 프로그램이 종료된다.

로그인이 성공하면, 각각의 모드로 들어가게 되며
관리자는 영화를 추가, 삭제할 수 있고 현재 상영하고있는 영화를 모두 볼 수 있다.
예매자의 경우 영화를 예매할 수 있고 (여러명 가능), 예매 번호로 자신의 예매 정보룰 볼 수 있으며,
예매 번호와 당시 입력한 비밀번호로 예매를 취소할 수 있다.

모든 화면마다 '뒤로가기'가 있다.

file에서 읽어오긴 하지만 프로그램이 끝날때 file에 쓰지는 않는다..ㅠㅠ
'''

# 프로그램 초기화 (파일 읽어오기)
initMovieInfo()

loginInfo=login()

if loginInfo == 0 : 
    print("\n 관리자님! 환영합니다! 관리자 전용 페이지로 이동합니다.")
    time.sleep(1)
    adminMode() #관리자 모드로 이동
elif loginInfo == 1 : 
    print("\n 예매자님! 환영합니다! 예매자 전용 페이지로 이동합니다.")
    time.sleep(1)
    guestMode() #예매자 모드로 이동
else : 
    print("\n 죄송합니다. 잘못된 정보를 입력하셨습니다. 곧 프로그램을 종료합니다.")
    time.sleep(1)
    #프로그램 종료

print("\n 프로그램을 종료합니다. 방문해주셔서 감사합니다. *^^*")