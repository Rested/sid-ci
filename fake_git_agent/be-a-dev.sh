echo "Waiting for git server to be online"
sleep 20

ssh-keyscan git-server >> gk
ssh-keygen -lf gk
cat gk >> /root/.ssh/known_hosts
cat /root/.ssh/known_hosts
eval $(ssh-agent -s)
ssh-add /root/.ssh/id_rsa
git config --global user.email "dev@example.com"
git config --global user.name "Dev McCode"

echo "Sleeping 10 seconds to ensure daemon is up and has done initial clone"
sleep 10

# make a random change to foo
git clone ssh://git@git-server:22/git-server/repos/foo-app.git
cd foo-app
echo "hi" > README.md
git add README.md
git commit -m 'foocus'
git push origin

# now bugfix bar
cd ..
git clone ssh://git@git-server:22/git-server/repos/bar-svc.git
cd bar-svc
touch thing
git add thing
git commit -m 'fix thing'
git push origin
cd ..

while true; do
    cd foo-app
    echo "hi" >> README.md
    git add README.md
    git commit -m 'greet more'
    git pull
    git push origin

    # now bugfix bar
    cd ../bar-svc
    head -n 1 /dev/urandom > thing
    git add thing
    git commit -m 'random thing'
    git pull
    git push origin
    cd ..
    echo "Dev having a sip of coffee"
    sleep 15
done
