# jobkorea

# directory 생성 및 이동
<pre>
mkdir ~/work
cd ~/work
</pre>

# google chrome 설치
<pre>
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo apt install google-chrome-stable_current_x86_64.rpm
</pre>

# chrome driver 다운로드
<pre>
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver ./
</pre>

# anaconda 설치
<pre>
wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
sudo bash Anaconda3-2023.09-0-Linux-x86_64.sh
</pre>  
<pre>
>>>설치위치는  /usr/share/python-3.11
설치후 PATH 추가
>>>vi ~/.bash_profile
>>>export PATH=/usr/share/python-3.11/bin:$PATH
</pre>

# source clone
<pre>
git clone https://github.com/talespin/jobkorea.git

cd jobkorea/src
sudo /usr/share/python-3.11/bin/pip install -r requirements.txt
cp chromedriver jobkorea/src/
</pre>

# nfs mount
<pre>
  sudo mount -t nfs xxxx.xxxx.xxxx.xxxx:/n3250909_kstat /mnt/work
</pre>
