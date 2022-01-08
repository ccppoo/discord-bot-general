# discord-bot

1. 이 레포지토리를 Clone을 한다
2. 필요에 맞게 `app.py`를 기준으로 봇을 작성한다
   1. 이 때 디렉토리를 만들어서 각자 용도에 알맞는 봇을 작성하면된다
   2. 이 앱의 실행시 디렉토리는 최상단, `app.py`가 있는 디렉토리 위치이므로 import를 할 때 최상단 디렉토리를 기준으로 작성한다.
      1. 예시) `app.py` , `my_commands/add.py`, `my_commands/say_hello.py` 가 있다고 하자.
      2. 이 때 `app.py`에서 import를 할 때 `from my_commands.add import ...` 이런식으로 해야한다.
3. 모두 작성하고나서 `requirements.txt`를 업데이트하자.
   1. 실행환경에 필요한 라이브러리(Python 내장 라이브러리 말고 pip으로 설치한 것들)을 적어줘야한다.
4. 빌드 환경을 만들 때 패키지를 설치하는 `pip install` 외에 다른 작업이 필요한 경우 `Docker` 파일을 수정하자.

----

Github Action에서 알아서 빌드하라고 하고 로컬에서 빌드하지 않아도 된다

도커란 그냥 뭐 설치하고, 뭐 하라고 지시내리는 설명서와 같기 때문이다.

직접 로컬에서 빌드를 하고, **내 컴퓨터에서** AWS ECR에 **직접** 배포(push) 할꺼면 아래의 과정을 따라한다.

직접 빌드를 하고자 하면 **분기점 1**, 그렇게 하기 싫으면 **분기점 2**로 넘어가자

## 중요!!

**분기점 1**을 하고 이어서 **분기점 2**를 해도 아무런 문제가 없다.

로컬에서 빌드를 하는 **분기점 1**은 로컬에서 미리 빌드가 되는지 테스트하는 것과 같다.

빌드가 되는지 안되는지 간에 일단 배포를 할 수 없으므로,

테스트가 필요하다면 직접 로컬에서 하고 난 뒤 push를 하거나

Github Action 스크립트를 수정해 빌드 실패시 업로드를 하지 않는 프로세스를 추가하자!!


## 분기점 1 : 이 과정을 최초로 실행하는 경우 + 내 컴퓨터에서 도커 빌드 안하는 경우

1. `Docker` 파일을 수정완료 했으면 `Docker Desktop`을 실행한 상태에서 빌드를 하자
    1. 로컬에서 빌드를 할 땐, `Dockerfile`에서 작성한 `env` 환경변수를 직접 커맨드 라인에 작성한 상태로 `docker build`를 작성해야한다.

    예시) `docker build --build-arg DISCORD_PUBLIC_KEY="본인의 키" -t aws-lambda-demo-ecr .`

    여기서 `--build-arg`를 사용하는 이유는 `Dockerfile`에 작성한 `env` 변수들을 어디서 참조할지 모르므로 빌드하는 커맨드를 작성할 때 필요한 변수가 무엇인지 알려주는 것이다.

    `-t` 옵션은 태그(tag)를 의미하는데, Docker이미지의 "이름"이다.

2. 빌드가 되었다면 AWS의 도커 레포지토리 "ECR"에 레포지토리를 만들고(AWS Console - 브라우저로 동작하는 거)
    `푸쉬 명령 보기`를 클릭해 푸쉬 커맨드 라인을 복사하자.

3. 그리고 푸쉬를 하기전에 로컬(당신 컴퓨터)에 AWS에 접근할 수 있는 사용자(당신 이메일 형식의 ID 말고, 사람이 아닌 프로그래밍으로 접근 할 수 있는 계정) configure를 설정해야한다.
    1. 만약 최초로 실행하는 경우 `aws configure`를 통해서 등록을 해야한다.
    IAM - 사용자(User)에 들어가
    AWSLambda_Full_Access, CloudWatchFullAccess, IAMFULLAccess, Elastic Container Registory full Access이 담긴
    인라인 정책을 만들어 추가하자

    그리고 발급받은
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    를 어디에 저장하자.

    이건 한 번만들고 나서 두 번다시 볼 수 없으므로 저장을 해야한다.
    Github repo secret에 저장해도 다시 볼 수 없다(update하거나 삭제하거나 둘 중하나일 뿐, 다시 볼 수 없음 ㅋㅋ;)

4. 이제 AWS 접근할 수 있는 configuration 까지 했으니 빌드된 이미지를 AWS의 ECR에 "push"하자.
    2에서 말한 커맨드 명령어를 복사해 실행하자, 아마 이렇게 생겼을 것이다
    `docker push <숫자>.dkr.ecr.<리전>.amazonaws.com/<ecr 레포지토리 이름>:latest`

5. 이전에 람다를 만들어 놓은 상태라면, 그 람다가 사용할 환경(image)를 사용할 수 있도록 업데이트를 해야한다.
   1. 우리가 지금까지 한건 도커 이미지 파일을 업로드한 것일 뿐, 람다와 아무것도 상관없었따!
   2. 4에서 푸쉬한 도커 이미지 레포지토리에 들어가 가장 최신(latest) 이미지의 URI를 복사하고 아래의 커맨드를 치자
   3. aws lambda update-function-code --function-name <여러분이 만든 람다 함수이름> --image-uri <방금전에 push한 이미지의 aws URI를 복붙>

6. 이렇게 람다가 사용할 새로운 환경+코드(도커 이미지 파일)를 업데이트 했다!

## 분기점 2 : 내 컴퓨터에서 도커 빌드를 안하고 Github Action한테 다 시키는 경우

**Github Action**은 `.github/workflows` 폴더에 있는 `*.yml` 파일에 정의되어 있는 것들을 실행시킨다.

일단 여기서는 workflows에 대한 세부적인 내용은 설명하지 않을 것이다.

`aws_lambda.yml` 파일을 보면 `{{ secrets.AWS_ACCESS_KEY_ID }}` 라는게 보일 것이다.

이 것은 Github 레포지토리 **settings**에 들어가서 아래에 **Secrets**에 적는 환경 변수, 비밀 환경 변수다.

*분기점 1*에서 본  `docker build --build-arg DISCORD_PUBLIC_KEY="본인의 키" -t aws-lambda-demo-ecr .` 이 것처럼

내 파일에 없지만, 필요한 변수들을 적는 곳이다

정리를 하자면  `{{ secrets.AWS_ACCESS_KEY_ID }}`는 `--build-arg AWS_ACCESS_KEY_ID="키"`와 같다고 볼 수 있다.

`Github Action`에는 Lambda에 배포하는 과정까지 있기 때문에 분기점 1에서 했던 커맨드 라인을 할 필요가 없다.

이것이 자동화 CI/CD의 힘이다!!

push를 할 떄마다 자동으로 하게끔 하려면 `workflows/aws_lambda.yml`에 `workflow_dispatch`를 수정하자.

## 마무리

이렇게 자동으로 배포를 하면 끝이다