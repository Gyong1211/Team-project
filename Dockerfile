FROM        gyong1211/fc_tp_ubuntu
MAINTAINER gyong1211@gmail.com

#Timezone 변경
ENV         TZ 'Asia/Seoul'
RUN         echo $TZ > /etc/timezone && apt-get update && apt-get install -y tzdata && rm /etc/localtime && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata && apt-get clean

# 현재 경로의 모든 파일(프로젝트 파일)을 컨테이너의 /srv/app 폴더에 복사
COPY        . /srv/app
# 쉘에서 입력하는 cd /srv/app와 같은 명령어
WORKDIR     /srv/app
# requirements 설치
RUN         /root/.pyenv/versions/app/bin/pip install -r .requirements/deploy.txt
# front-end project clone
WORKDIR     /srv
RUN         git clone https://github.com/degose/Bond.git front

# build front-end project
#WORKDIR     /srv/front
#RUN         npm install
#RUN         npm run build


# supervisor file 복사
COPY        .config/supervisor/uwsgi.conf /etc/supervisor/conf.d/
COPY        .config/supervisor/nginx.conf /etc/supervisor/conf.d/
COPY        .config/supervisor/celery.conf /etc/supervisor/conf.d/

# nginx파일 복사
COPY        .config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY        .config/nginx/nginx-app.conf /etc/nginx/sites-available/nginx-app.conf
RUN         rm -rf /etc/nginx/sites-enabled/default
RUN         ln -sf /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/nginx-app.conf

# RUN         /root/.pyenv/versions/app/bin/python /srv/app/django_app/manage.py collectstatic --noinput --settings=config.settings.deploy

CMD         supervisord -n

EXPOSE 80 8000